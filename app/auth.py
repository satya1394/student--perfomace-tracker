"""
Authentication and Role-Based Access Control Module.
Integrates Flask-Login with SQLAlchemy User models and provides session security and academic context.
"""

from functools import wraps
from flask import redirect, url_for, flash, session, has_request_context
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db_session, User, Student, AuditLog, College, Regulation, Branch

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.login_message = "Please authenticate to access the academic performance platform."
login_manager.login_message_category = "warning"


class AuthenticatedUser(UserMixin):
    """Wrapper class conforming to Flask-Login expectations."""
    def __init__(self, user_id, username, email, role, student_id=None):
        self.id = user_id
        self.username = username
        self.email = email
        self.role = role
        self.student_id = student_id

    @property
    def is_admin(self):
        return self.role == "ADMIN"

    @property
    def is_faculty(self):
        return self.role in ("FACULTY", "ADMIN")

    @property
    def is_student(self):
        return self.role == "STUDENT"


@login_manager.user_loader
def load_user(user_id):
    """Loads authenticated user by ID."""
    db = get_db_session()
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user:
            return AuthenticatedUser(
                user_id=user.id,
                username=user.username,
                email=user.email,
                role=user.role,
                student_id=user.student_id
            )
        return None
    finally:
        db.close()


def authenticate_user(username, password):
    """Validates user credentials against database password hash and binds academic session."""
    db = get_db_session()
    try:
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()

        if user and check_password_hash(user.password_hash, password):
            auth_user = AuthenticatedUser(
                user_id=user.id,
                username=user.username,
                email=user.email,
                role=user.role,
                student_id=user.student_id
            )
            if has_request_context():
                login_user(auth_user)
                # Bind student academic context to session
                if user.student_id:
                    stu = db.query(Student).filter(Student.student_id == user.student_id).first()
                    if stu:
                        session['student_id'] = stu.student_id
                        session['college_id'] = stu.college_id
                        session['regulation_id'] = stu.regulation_id
                        session['branch_id'] = stu.branch_id
                        session['active_semester'] = stu.current_semester or 8
                        session['student_name'] = stu.name
                        session['student_dept'] = stu.department
                        session['specialization'] = stu.specialization
            
            # Record audit log
            log = AuditLog(
                user_id=user.id,
                action="LOGIN_SUCCESS",
                target_entity="User",
                entity_id=str(user.id),
                details={"ip": "127.0.0.1", "role": user.role}
            )
            db.add(log)
            db.commit()
            return True, auth_user
        return False, "Invalid username or password."
    finally:
        db.close()


def register_student_user(full_name, roll_number, username, email, department, semester, password, confirm_password,
                          college_id=None, regulation_id=None, branch_id=None, college_name=None, specialization=None):
    """
    Registers a new student user with strict validation and academic session binding:
    1. Validate required fields and password length (>=8 chars).
    2. Validate username contains roll number.
    3. Save college_id, regulation_id, branch_id to Student table.
    4. Store academic identifiers into Flask session.
    """
    full_name = str(full_name).strip()
    roll_number = str(roll_number).strip().upper()
    username = str(username).strip()
    email = str(email).strip().lower()
    
    try:
        semester = int(semester)
    except (ValueError, TypeError):
        semester = 1

    if not full_name or not roll_number or not username or not email or not password:
        return None, "All fields are required."

    if len(password) < 8:
        return None, "Password must be at least 8 characters long."

    if password != confirm_password:
        return None, "Passwords do not match."

    # Validate that username contains their roll number
    if roll_number.lower() not in username.lower():
        return None, f"Username must contain your Roll Number '{roll_number}' (e.g. {username}_{roll_number})."

    db = get_db_session()
    try:
        # Check if username or email already exists
        existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return None, "Username or email is already registered. Please sign in."

        # Resolve College, Regulation, and Branch
        college_obj = None
        if college_id:
            try:
                college_obj = db.query(College).filter(College.id == int(college_id)).first()
            except Exception:
                pass
        if not college_obj and college_name:
            college_obj = db.query(College).filter(College.name.like(f"%{college_name}%")).first()
        if not college_obj:
            college_obj = db.query(College).first()

        regulation_obj = None
        if regulation_id:
            try:
                regulation_obj = db.query(Regulation).filter(Regulation.id == int(regulation_id)).first()
            except Exception:
                pass
        if not regulation_obj:
            regulation_obj = db.query(Regulation).first()

        branch_obj = None
        if branch_id:
            try:
                branch_obj = db.query(Branch).filter(Branch.id == int(branch_id)).first()
            except Exception:
                pass
        if not branch_obj and specialization:
            branch_obj = db.query(Branch).filter(Branch.specialization.like(f"%{specialization}%")).first()
        if not branch_obj:
            branch_obj = db.query(Branch).first()

        resolved_college_id = college_obj.id if college_obj else None
        resolved_college_name = college_obj.name if college_obj else (college_name or "Apex Institute of Engineering & Technology")
        resolved_regulation_id = regulation_obj.id if regulation_obj else None
        resolved_branch_id = branch_obj.id if branch_obj else None
        resolved_specialization = branch_obj.specialization if branch_obj else (specialization or "CSE (Data Science)")
        resolved_dept = branch_obj.name if branch_obj else (department or "Computer Science")

        # Create or fetch Student profile
        existing_student = db.query(Student).filter(Student.student_id == roll_number).first()
        if not existing_student:
            student_obj = Student(
                student_id=roll_number,
                name=full_name,
                email=email,
                department=resolved_dept,
                college_id=resolved_college_id,
                regulation_id=resolved_regulation_id,
                branch_id=resolved_branch_id,
                college_name=resolved_college_name,
                specialization=resolved_specialization,
                current_semester=semester,
                enrollment_year=2024
            )
            db.add(student_obj)
            db.flush()
        else:
            student_obj = existing_student
            student_obj.name = full_name
            student_obj.email = email
            student_obj.college_id = resolved_college_id
            student_obj.regulation_id = resolved_regulation_id
            student_obj.branch_id = resolved_branch_id
            student_obj.college_name = resolved_college_name
            student_obj.specialization = resolved_specialization
            student_obj.current_semester = semester
            db.flush()

        # Create User Auth entity
        pwd_hash = generate_password_hash(password, method="pbkdf2:sha256")
        user = User(
            username=username,
            email=email,
            password_hash=pwd_hash,
            role="STUDENT",
            student_id=roll_number
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        auth_user = AuthenticatedUser(
            user_id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            student_id=user.student_id
        )
        if has_request_context():
            login_user(auth_user)
            # Store in Flask session
            session['student_id'] = student_obj.student_id
            session['college_id'] = student_obj.college_id
            session['regulation_id'] = student_obj.regulation_id
            session['branch_id'] = student_obj.branch_id
            session['active_semester'] = student_obj.current_semester
            session['student_name'] = student_obj.name
            session['student_dept'] = student_obj.department
            session['specialization'] = student_obj.specialization

        return user, None
    except Exception as e:
        db.rollback()
        return None, f"Registration failed: {str(e)}"
    finally:
        db.close()


def create_user(username, email, password, role="STUDENT", student_id=None):
    """Registers a new user with hashed credentials."""
    db = get_db_session()
    try:
        existing = db.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing:
            return None, "Username or email already exists."

        pwd_hash = generate_password_hash(password, method="pbkdf2:sha256")
        user = User(
            username=username,
            email=email,
            password_hash=pwd_hash,
            role=role,
            student_id=student_id
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user, None
    finally:
        db.close()


def login_demo_user():
    """Authenticates the demonstration student account and initializes demo session flags."""
    db = get_db_session()
    try:
        user = db.query(User).filter(User.username == "demo_user").first()
        if not user:
            seed_default_users()
            user = db.query(User).filter(User.username == "demo_user").first()
        
        if user:
            auth_user = AuthenticatedUser(
                user_id=user.id,
                username=user.username,
                email=user.email,
                role=user.role,
                student_id=user.student_id
            )
            if has_request_context():
                login_user(auth_user)
                stu = db.query(Student).filter(Student.student_id == user.student_id).first()
                if stu:
                    session['student_id'] = stu.student_id
                    session['college_id'] = stu.college_id
                    session['regulation_id'] = stu.regulation_id
                    session['branch_id'] = stu.branch_id
                    session['active_semester'] = stu.current_semester or 3
                    session['student_name'] = stu.name
                    session['student_dept'] = stu.department
                    session['specialization'] = stu.specialization
                    session['is_demo'] = True
            return True, auth_user
        return False, None
    finally:
        db.close()


def seed_default_users():
    """Initializes standard demonstration accounts and maps institutional relationships."""
    from app.database import Enrollment, Subject
    db = get_db_session()
    try:
        # Resolve default academic entities
        raghu_col = db.query(College).filter(College.code == "REC").first() or db.query(College).first()
        r23_reg = db.query(Regulation).filter(Regulation.code == "R23").first() or db.query(Regulation).first()
        csd_branch = db.query(Branch).filter(Branch.code == "CSD").first() or db.query(Branch).first()

        # Seed Rahul Kumar (Official Demo User)
        demo_student = db.query(Student).filter(Student.student_id == "2024CSE001").first()
        if not demo_student:
            demo_student = Student(
                student_id="2024CSE001",
                name="Rahul Kumar",
                email="demo_user@studiq.edu",
                department="Computer Science & Engineering",
                college_id=raghu_col.id if raghu_col else 1,
                regulation_id=r23_reg.id if r23_reg else 1,
                branch_id=csd_branch.id if csd_branch else 1,
                college_name="Raghu Engineering College",
                specialization="CSE (Data Science)",
                current_semester=3,
                enrollment_year=2024
            )
            db.add(demo_student)
            db.flush()
        else:
            demo_student.name = "Rahul Kumar"
            demo_student.college_name = "Raghu Engineering College"
            demo_student.specialization = "CSE (Data Science)"
            demo_student.current_semester = 3
            if raghu_col:
                demo_student.college_id = raghu_col.id
            if r23_reg:
                demo_student.regulation_id = r23_reg.id
            if csd_branch:
                demo_student.branch_id = csd_branch.id

        # Seed demo user login account
        demo_u = db.query(User).filter(User.username == "demo_user").first()
        if not demo_u:
            pwd_hash = generate_password_hash("demo123", method="pbkdf2:sha256")
            demo_u = User(
                username="demo_user",
                email="demo_user@studiq.edu",
                password_hash=pwd_hash,
                role="STUDENT",
                student_id="2024CSE001"
            )
            db.add(demo_u)
        else:
            demo_u.student_id = "2024CSE001"

        # Also preserve legacy student_demo account
        leg_u = db.query(User).filter(User.username == "student_demo").first()
        if not leg_u:
            pwd_hash = generate_password_hash("Student@123", method="pbkdf2:sha256")
            leg_u = User(
                username="student_demo",
                email="student@university.edu",
                password_hash=pwd_hash,
                role="STUDENT",
                student_id="2024CSE001"
            )
            db.add(leg_u)

        # Seed pre-loaded marks for Rahul Kumar (Semester 3)
        sem3_marks_data = [
            ("CS301", "Data Structures", 4.0, 85.0, "A", 9.0, 78.0),
            ("CS302", "Database Management", 3.0, 78.0, "B", 8.0, 75.0),
            ("CS303", "Digital Logic Design", 4.0, 92.0, "S", 10.0, 82.0),
            ("CS304", "Object Oriented Programming", 4.0, 88.0, "A", 9.0, 80.0),
            ("CS305", "Discrete Mathematics", 3.0, 76.0, "B", 8.0, 76.0),
            ("CS306", "Data Structures Lab", 1.5, 90.0, "A", 9.0, 85.0),
            ("CS307", "DBMS Lab", 1.5, 82.0, "A", 9.0, 79.0),
        ]
        for ccode, ctitle, cred, mrk, grd, gp, att in sem3_marks_data:
            subj = db.query(Subject).filter(
                Subject.branch_id == csd_branch.id,
                Subject.code == f"CSD{ccode.replace('CS', '')}"
            ).first() or db.query(Subject).filter(Subject.code.like(f"%{ccode.replace('CS', '')}")).first()
            
            sub_id = subj.id if subj else None
            existing_enr = db.query(Enrollment).filter(
                Enrollment.student_id == "2024CSE001",
                Enrollment.semester == 3,
                (Enrollment.course_id == ccode) | (Enrollment.subject_id == sub_id)
            ).first()
            if not existing_enr:
                enr = Enrollment(
                    student_id="2024CSE001",
                    course_id=ccode,
                    subject_id=sub_id,
                    marks_obtained=mrk,
                    grade=grd,
                    grade_letter=grd,
                    grade_point=gp,
                    attendance_percentage=att,
                    semester=3,
                    academic_year="2024-2025"
                )
                db.add(enr)

        # Seed Semester 1 and Semester 2 records for Rahul Kumar to provide realistic multi-semester progression
        sem1_data = [
            ("CS101", "Engineering Mathematics I", 4.0, 80.0, "A", 9.0, 78.0),
            ("CS102", "Applied Physics & Optics", 4.0, 75.0, "B", 8.0, 80.0),
            ("CS103", "Programming Fundamentals", 4.0, 82.0, "A", 9.0, 80.0),
        ]
        for ccode, ctitle, cred, mrk, grd, gp, att in sem1_data:
            existing_enr = db.query(Enrollment).filter(
                Enrollment.student_id == "2024CSE001",
                Enrollment.semester == 1,
                Enrollment.course_id == ccode
            ).first()
            if not existing_enr:
                enr = Enrollment(
                    student_id="2024CSE001",
                    course_id=ccode,
                    marks_obtained=mrk,
                    grade=grd,
                    grade_letter=grd,
                    grade_point=gp,
                    attendance_percentage=att,
                    semester=1,
                    academic_year="2023-2024"
                )
                db.add(enr)

        sem2_data = [
            ("CS201", "Data Structures", 4.0, 78.0, "B", 8.0, 76.0),
            ("CS202", "Database Management Systems", 3.0, 80.0, "A", 9.0, 78.0),
            ("CS203", "Digital Logic Design", 4.0, 74.0, "B", 8.0, 75.0),
        ]
        for ccode, ctitle, cred, mrk, grd, gp, att in sem2_data:
            existing_enr = db.query(Enrollment).filter(
                Enrollment.student_id == "2024CSE001",
                Enrollment.semester == 2,
                Enrollment.course_id == ccode
            ).first()
            if not existing_enr:
                enr = Enrollment(
                    student_id="2024CSE001",
                    course_id=ccode,
                    marks_obtained=mrk,
                    grade=grd,
                    grade_letter=grd,
                    grade_point=gp,
                    attendance_percentage=att,
                    semester=2,
                    academic_year="2023-2024"
                )
                db.add(enr)

        db.commit()
    finally:
        db.close()


def role_required(*allowed_roles):
    """Decorator to enforce role-based access control on routes."""
    def decorator(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("login_route"))
            if current_user.role not in allowed_roles:
                flash("Access denied: You do not have permission for this resource.", "danger")
                return redirect(url_for("unauthorized_route"))
            return fn(*args, **kwargs)
        return decorated_view
    return decorator
