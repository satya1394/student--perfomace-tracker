"""
Authentication and Role-Based Access Control Module.
Integrates Flask-Login with SQLAlchemy User models and provides session security and academic context.
"""

from functools import wraps
from flask import redirect, url_for, flash, session, has_request_context
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import (
    get_db_session, User, Student, AuditLog, College, Regulation, 
    Branch, CurriculumSubject, Enrollment
)
from app.curriculum_engine import get_curriculum_id

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
                if user.student_id:
                    stu = db.query(Student).filter(Student.student_id == user.student_id).first()
                    if stu:
                        session['student_id'] = stu.student_id
                        session['college_id'] = stu.college_id
                        session['regulation_id'] = stu.regulation_id
                        session['branch_id'] = stu.branch_id
                        session['college_name'] = stu.college_name or "Raghu Engineering College"
                        session['degree'] = stu.degree or "B.Tech"
                        session['regulation_name'] = stu.regulation_name or "AR23"
                        session['branch_name'] = stu.branch_name or "CSE"
                        session['specialization'] = stu.specialization or "Core Computer Science"
                        session['active_semester'] = stu.current_semester or 3
                        session['student_name'] = stu.name
                        session['student_dept'] = stu.department
                        session['curriculum_id'] = stu.curriculum_id or get_curriculum_id(
                            stu.college_name or "Raghu Engineering College",
                            stu.degree or "B.Tech",
                            stu.regulation_name or "AR23",
                            stu.branch_name or "CSE",
                            stu.specialization or "Core Computer Science"
                        )
            
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
                          college_name="Raghu Engineering College", degree="B.Tech", regulation_name="AR23",
                          branch_name="CSE", specialization="Core Computer Science", college_id=None, regulation_id=None, branch_id=None):
    """
    Registers a new student user with strict validation and academic session binding:
    1. Validate required fields and password length (>=8 chars).
    2. Validate username contains roll number.
    3. Save exact 6 fields to Student table.
    4. Store academic identifiers into Flask session.
    """
    full_name = str(full_name).strip()
    roll_number = str(roll_number).strip().upper()
    username = str(username).strip()
    email = str(email).strip().lower()
    college_name = str(college_name).strip() or "Raghu Engineering College"
    degree = str(degree).strip() or "B.Tech"
    regulation_name = str(regulation_name).strip() or "AR23"
    branch_name = str(branch_name).strip() or "CSE"
    specialization = str(specialization).strip() or "Core Computer Science"
    
    try:
        semester = int(semester)
    except (ValueError, TypeError):
        semester = 3

    if not full_name or not roll_number or not username or not email or not password:
        return None, "All fields are required."

    if len(password) < 8:
        return None, "Password must be at least 8 characters long."

    if password != confirm_password:
        return None, "Passwords do not match."

    if roll_number.lower() not in username.lower():
        return None, f"Username must contain your Roll Number '{roll_number}' (e.g. {username}_{roll_number})."

    db = get_db_session()
    try:
        existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return None, "Username or email is already registered. Please sign in."

        curr_id = get_curriculum_id(college_name, degree, regulation_name, branch_name, specialization)

        existing_student = db.query(Student).filter(Student.student_id == roll_number).first()
        if not existing_student:
            student_obj = Student(
                student_id=roll_number,
                name=full_name,
                email=email,
                department=f"{branch_name} ({specialization})",
                college_id=college_id,
                regulation_id=regulation_id,
                branch_id=branch_id,
                curriculum_id=curr_id,
                college_name=college_name,
                degree=degree,
                regulation_name=regulation_name,
                branch_name=branch_name,
                specialization=specialization,
                current_semester=semester,
                enrollment_year=2024
            )
            db.add(student_obj)
            db.flush()
        else:
            student_obj = existing_student
            student_obj.name = full_name
            student_obj.email = email
            student_obj.curriculum_id = curr_id
            student_obj.college_name = college_name
            student_obj.degree = degree
            student_obj.regulation_name = regulation_name
            student_obj.branch_name = branch_name
            student_obj.specialization = specialization
            student_obj.current_semester = semester
            db.flush()

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
            session['student_id'] = student_obj.student_id
            session['college_name'] = student_obj.college_name
            session['degree'] = student_obj.degree
            session['regulation_name'] = student_obj.regulation_name
            session['branch_name'] = student_obj.branch_name
            session['specialization'] = student_obj.specialization
            session['active_semester'] = student_obj.current_semester
            session['student_name'] = student_obj.name
            session['student_dept'] = student_obj.department
            session['curriculum_id'] = student_obj.curriculum_id

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
    """Authenticates the demonstration student account (Rahul Kumar - AR23 CSE Sem 3)."""
    db = get_db_session()
    try:
        user = db.query(User).filter(User.username.in_(["demo_user", "rahulkumar", "student_demo"])).first()
        if not user:
            seed_default_users()
            user = db.query(User).filter(User.username.in_(["demo_user", "rahulkumar", "student_demo"])).first()
        
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
                    session['college_name'] = stu.college_name or "Raghu Engineering College"
                    session['degree'] = stu.degree or "B.Tech"
                    session['regulation_name'] = stu.regulation_name or "AR23"
                    session['branch_name'] = stu.branch_name or "CSE"
                    session['specialization'] = stu.specialization or "Core Computer Science"
                    session['active_semester'] = stu.current_semester or 3
                    session['student_name'] = stu.name
                    session['student_dept'] = stu.department
                    session['curriculum_id'] = stu.curriculum_id or "RAGHU_BTECH_AR23_CSE_CORE_COMPUTER_SCIENCE"
                    session['is_demo'] = True
            return True, auth_user
        return False, None
    finally:
        db.close()


def seed_default_users():
    """Initializes standard demonstration accounts and maps official AR23 curriculum data."""
    db = get_db_session()
    try:
        col = db.query(College).filter(College.name == "Raghu Engineering College").first()
        reg_ar23 = db.query(Regulation).filter(Regulation.code == "AR23").first()
        br_cse = db.query(Branch).filter(Branch.code == "CSE", Branch.specialization == "Core Computer Science").first()

        curr_id = "RAGHU_BTECH_AR23_CSE_CORE_COMPUTER_SCIENCE"
        
        # Seed Rahul Kumar (Official Verified Demo User)
        demo_student = db.query(Student).filter(Student.student_id == "STU2024001").first()
        if not demo_student:
            demo_student = Student(
                student_id="STU2024001",
                name="Rahul Kumar",
                email="rahul.cse@studiq.edu",
                department="Computer Science & Engineering",
                college_id=col.id if col else None,
                regulation_id=reg_ar23.id if reg_ar23 else None,
                branch_id=br_cse.id if br_cse else None,
                curriculum_id=curr_id,
                college_name="Raghu Engineering College",
                degree="B.Tech",
                regulation_name="AR23",
                branch_name="CSE",
                specialization="Core Computer Science",
                current_semester=3,
                enrollment_year=2023
            )
            db.add(demo_student)
            db.flush()

        # Seed users
        for uname, pwd in [("demo_user", "demo123"), ("rahulkumar", "Student@123"), ("student_demo", "Student@123")]:
            u = db.query(User).filter(User.username == uname).first()
            if not u:
                u = User(
                    username=uname,
                    email=f"{uname}@studiq.edu",
                    password_hash=generate_password_hash(pwd, method="pbkdf2:sha256"),
                    role="STUDENT",
                    student_id="STU2024001"
                )
                db.add(u)

        # Seed pre-loaded marks for Rahul Kumar in Semester 3 using official AR23 CSE subjects
        ar23_sem3_subs = db.query(CurriculumSubject).filter(
            CurriculumSubject.curriculum_id == curr_id,
            CurriculumSubject.semester == 3
        ).all()

        for s in ar23_sem3_subs:
            existing_enr = db.query(Enrollment).filter(
                Enrollment.student_id == "STU2024001",
                Enrollment.curriculum_subject_id == s.id
            ).first()
            if not existing_enr:
                enr = Enrollment(
                    student_id="STU2024001",
                    curriculum_subject_id=s.id,
                    course_id=s.subject_code,
                    marks_obtained=86.0,
                    grade="A+",
                    grade_letter="A+",
                    grade_point=9.0,
                    credits_used=s.official_credits or s.credits or 3.0,
                    attendance_percentage=88.0,
                    semester=3,
                    academic_year="2024-2025"
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
