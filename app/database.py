"""
SQLAlchemy Database Models and Connection Management.
Implements models for Colleges, Regulations, Branches, Subjects, Users, Students, Courses, Enrollments, Predictions, and Audit Logs.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, 
    DateTime, ForeignKey, Text, JSON, text
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session
from app.config import Config

Base = declarative_base()
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, **Config.SQLALCHEMY_ENGINE_OPTIONS)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def utc_now():
    return datetime.now(timezone.utc)


# =========================================================================
# 1. Institutional Academic Framework Models
# =========================================================================

class College(Base):
    """Higher education institutions / universities."""
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(32), unique=True, nullable=False)
    name = Column(String(150), unique=True, nullable=False)
    location = Column(String(100), nullable=True)

    # Relationships
    regulations = relationship("Regulation", back_populates="college", cascade="all, delete-orphan")
    students = relationship("Student", back_populates="college")

    def __repr__(self):
        return f"<College {self.code}: {self.name}>"


class Regulation(Base):
    """Academic curriculum regulations (e.g. R23, R20, R19, R21, R22)."""
    __tablename__ = "regulations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"), nullable=True)
    code = Column(String(20), nullable=False)  # e.g. "R23", "R20"
    name = Column(String(150), nullable=False)  # e.g. "R23 - JNTU 2023 Syllabus"

    # Relationships
    college = relationship("College", back_populates="regulations")
    branches = relationship("Branch", back_populates="regulation", cascade="all, delete-orphan")
    subjects = relationship("Subject", back_populates="regulation")

    def __repr__(self):
        return f"<Regulation {self.code}: {self.name}>"


class Branch(Base):
    """Academic branches and specialized domains."""
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"), nullable=True)
    regulation_id = Column(Integer, ForeignKey("regulations.id", ondelete="CASCADE"), nullable=True)
    code = Column(String(32), nullable=False)  # e.g. "CSE", "CSD", "CSM"
    name = Column(String(100), nullable=False)  # e.g. "Computer Science & Engineering"
    specialization = Column(String(100), nullable=False)  # e.g. "Data Science", "AI & ML"

    # Relationships
    regulation = relationship("Regulation", back_populates="branches")
    subjects = relationship("Subject", back_populates="branch", cascade="all, delete-orphan")
    students = relationship("Student", back_populates="branch")

    def display_label(self):
        return f"{self.code} - {self.name} ({self.specialization})"

    def __repr__(self):
        return f"<Branch {self.code} ({self.specialization})>"


class Subject(Base):
    """Canonical curriculum subjects with credit points and term allocations."""
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="CASCADE"), nullable=True)
    regulation_id = Column(Integer, ForeignKey("regulations.id", ondelete="CASCADE"), nullable=True)
    code = Column(String(32), nullable=False)
    title = Column(String(150), nullable=False)
    credits = Column(Float, nullable=False, default=4.0)
    semester = Column(Integer, nullable=False, default=1)

    # Relationships
    branch = relationship("Branch", back_populates="subjects")
    regulation = relationship("Regulation", back_populates="subjects")
    enrollments = relationship("Enrollment", back_populates="subject_ref")

    def __repr__(self):
        return f"<Subject {self.code}: {self.title} ({self.credits} cr, Sem {self.semester})>"


# =========================================================================
# 2. User Authentication and Student Profile Models
# =========================================================================

class User(Base):
    """User accounts table for Flask-Login authentication and role control."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), nullable=False, default="STUDENT")  # STUDENT, FACULTY, ADMIN
    student_id = Column(String(32), ForeignKey("students.student_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=utc_now)

    # Relationships
    student = relationship("Student", back_populates="user_account")
    audit_logs = relationship("AuditLog", back_populates="user")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class Student(Base):
    """Student profiles table containing institutional demographics and branch mappings."""
    __tablename__ = "students"

    student_id = Column(String(32), primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    department = Column(String(64), nullable=False, index=True)
    
    # Institutional Foreign Keys
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="SET NULL"), nullable=True)
    regulation_id = Column(Integer, ForeignKey("regulations.id", ondelete="SET NULL"), nullable=True)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="SET NULL"), nullable=True)

    # Human-readable meta mappings
    college_name = Column(String(150), default="Apex Institute of Engineering & Technology", nullable=True)
    specialization = Column(String(100), default="CSE (Data Science)", nullable=True)
    current_semester = Column(Integer, default=8, nullable=True)
    enrollment_year = Column(Integer, nullable=False, default=2024)
    created_at = Column(DateTime, default=utc_now)

    # Relationships
    user_account = relationship("User", back_populates="student", uselist=False)
    college = relationship("College", back_populates="students")
    branch = relationship("Branch", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student {self.student_id} - {self.name} ({self.specialization})>"


class Course(Base):
    """Curriculum courses table with credit weights and semester allocations."""
    __tablename__ = "courses"

    course_id = Column(String(32), primary_key=True, index=True)
    course_code = Column(String(20), unique=True, nullable=False)
    course_name = Column(String(150), nullable=False)
    credits = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False, index=True)
    department = Column(String(64), nullable=False, index=True)

    # Relationships
    enrollments = relationship("Enrollment", back_populates="course")

    def __repr__(self):
        return f"<Course {self.course_code}: {self.course_name} ({self.credits} cr)>"


class Enrollment(Base):
    """Student course registrations with grade records and attendance tracking."""
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(32), ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(String(32), ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True, index=True)
    
    marks_obtained = Column(Float, nullable=False)
    grade = Column(String(5), nullable=False)
    grade_letter = Column(String(5), nullable=True)
    grade_point = Column(Float, nullable=False)
    attendance_percentage = Column(Float, nullable=False)
    semester = Column(Integer, nullable=False, index=True)
    academic_year = Column(String(20), nullable=False, default="2024-2025")

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    subject_ref = relationship("Subject", back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment {self.student_id} in {self.course_id or self.subject_id}: {self.grade} ({self.marks_obtained}m)>"


class Prediction(Base):
    """Machine learning model outputs and student risk evaluations."""
    __tablename__ = "predictions"

    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(32), ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    predicted_score = Column(Float, nullable=False)
    pass_probability = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False, index=True)  # LOW, MEDIUM, HIGH
    confidence_score = Column(Float, nullable=False)
    shap_values = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    # Relationships
    student = relationship("Student", back_populates="predictions")

    def __repr__(self):
        return f"<Prediction {self.student_id}: Risk={self.risk_level}, Score={self.predicted_score:.1f}>"


class GradeRule(Base):
    """Academic grade boundary rules by regulation framework (e.g. R23, R20)."""
    __tablename__ = "grade_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    regulation_id = Column(Integer, ForeignKey("regulations.id", ondelete="CASCADE"), nullable=True)
    grade_letter = Column(String(5), nullable=False)
    grade_point = Column(Float, nullable=False)
    min_marks = Column(Float, nullable=False)
    max_marks = Column(Float, nullable=False)

    # Relationships
    regulation = relationship("Regulation")

    def __repr__(self):
        return f"<GradeRule Reg {self.regulation_id}: {self.grade_letter} ({self.grade_point} GP)>"


class AuditLog(Base):
    """System-wide audit trail for compliance, role actions, and data changes."""
    __tablename__ = "audit_logs"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(64), nullable=False)
    target_entity = Column(String(64), nullable=False)
    entity_id = Column(String(64), nullable=True)
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=utc_now, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog {self.action} on {self.target_entity}:{self.entity_id} at {self.timestamp}>"


# =========================================================================
# 3. Seeding & Schema Migration Utilities
# =========================================================================

def seed_academic_framework():
    """Seeds institutional colleges, regulations, branches, grade rules, and semester subjects."""
    db = get_db_session()
    try:
        # 1. Colleges
        colleges_data = [
            ("REC", "Raghu Engineering College", "Visakhapatnam"),
            ("APEX", "Apex Institute of Engineering & Technology", "Jaipur"),
            ("IITB", "Indian Institute of Technology (IIT)", "Mumbai"),
            ("NITT", "National Institute of Technology (NIT)", "Trichy"),
            ("DTU", "Delhi Technological University (DTU)", "New Delhi"),
            ("BITS", "Birla Institute of Technology and Science (BITS)", "Pilani"),
            ("VIT", "Vellore Institute of Technology (VIT)", "Vellore"),
        ]
        colleges = {}
        for code, name, loc in colleges_data:
            c = db.query(College).filter(College.code == code).first()
            if not c:
                c = College(code=code, name=name, location=loc)
                db.add(c)
                db.flush()
            colleges[code] = c

        # 2. Regulations
        regulations_data = [
            ("R23", "R23 - JNTU 2023 Syllabus"),
            ("R20", "R20 - CBCS Autonomous 2020"),
            ("R19", "R19 - Outcome Based Curriculum"),
            ("R21", "R21 - AICTE Model Curriculum"),
            ("R22", "R22 - Industry 4.0 Standard"),
        ]
        regulations = {}
        for reg_code, reg_name in regulations_data:
            r = db.query(Regulation).filter(Regulation.code == reg_code).first()
            if not r:
                r = Regulation(code=reg_code, name=reg_name, college_id=colleges["REC"].id)
                db.add(r)
                db.flush()
            regulations[reg_code] = r

        # 3. Grade Rules for R23 & Standard Regulations
        r23_reg = regulations.get("R23")
        if r23_reg:
            r23_rules = [
                ("S", 10.0, 90.0, 100.0),
                ("A", 9.0, 80.0, 89.99),
                ("B", 8.0, 70.0, 79.99),
                ("C", 7.0, 60.0, 69.99),
                ("D", 6.0, 50.0, 59.99),
                ("E", 5.0, 40.0, 49.99),
                ("F", 0.0, 0.0, 39.99),
            ]
            for g_let, gp, min_m, max_m in r23_rules:
                existing_gr = db.query(GradeRule).filter(
                    GradeRule.regulation_id == r23_reg.id,
                    GradeRule.grade_letter == g_let
                ).first()
                if not existing_gr:
                    gr = GradeRule(
                        regulation_id=r23_reg.id,
                        grade_letter=g_let,
                        grade_point=gp,
                        min_marks=min_m,
                        max_marks=max_m
                    )
                    db.add(gr)

        # 4. Branches
        branches_data = [
            ("CSE", "Computer Science & Engineering", "Core Computer Science", "R23", "REC"),
            ("CSD", "Computer Science & Engineering", "Data Science", "R23", "REC"),
            ("CSM", "Computer Science & Engineering", "AI & ML", "R23", "REC"),
            ("CSC", "Computer Science & Engineering", "Cyber Security", "R23", "REC"),
            ("CSI", "Computer Science & Engineering", "IoT & Embedded Systems", "R23", "REC"),
            ("ECE", "Electronics & Communication Engineering", "VLSI & Embedded", "R23", "REC"),
            ("IT", "Information Technology", "Cloud & Web Computing", "R23", "REC"),
            # Apex branches
            ("CSE_APEX", "Computer Science & Engineering", "Core Computer Science", "R20", "APEX"),
            ("CSD_APEX", "Computer Science & Engineering", "Data Science", "R20", "APEX"),
        ]
        branches = {}
        for b_code, b_name, b_spec, reg_key, col_key in branches_data:
            b = db.query(Branch).filter(Branch.code == b_code, Branch.specialization == b_spec).first()
            if not b:
                b = Branch(
                    code=b_code,
                    name=b_name,
                    specialization=b_spec,
                    college_id=colleges[col_key].id if col_key in colleges else colleges["REC"].id,
                    regulation_id=regulations[reg_key].id
                )
                db.add(b)
                db.flush()
            branches[f"{b_code}_{b_spec}"] = b

        # 5. Canonical Semester Subjects (Sem 1 to 8) for Branches
        semester_subjects = {
            1: [
                ("101", "Engineering Mathematics I", 4.0),
                ("102", "Applied Physics & Optics", 4.0),
                ("103", "Programming Fundamentals in C", 4.0),
            ],
            2: [
                ("201", "Data Structures", 4.0),
                ("202", "Database Management Systems", 3.0),
                ("203", "Digital Logic Design", 4.0),
                ("204", "Object Oriented Programming", 4.0),
                ("205", "Discrete Mathematics", 3.0),
                ("206", "Data Structures Lab", 1.5),
                ("207", "DBMS Lab", 1.5),
            ],
            3: [
                ("301", "Data Structures", 4.0),
                ("302", "Database Management", 3.0),
                ("303", "Digital Logic Design", 4.0),
                ("304", "Object Oriented Programming", 4.0),
                ("305", "Discrete Mathematics", 3.0),
                ("306", "Data Structures Lab", 1.5),
                ("307", "DBMS Lab", 1.5),
            ],
            4: [
                ("401", "Design & Analysis of Algorithms", 4.0),
                ("402", "Database Management Systems", 4.0),
                ("403", "Operating Systems & Kernel Design", 4.0),
            ],
            5: [
                ("501", "Theory of Computation & Automata", 4.0),
                ("502", "Computer Networks & Protocols", 4.0),
                ("503", "Software Engineering & Agile DevOps", 4.0),
            ],
            6: [
                ("601", "Compiler Design & Optimization", 4.0),
                ("602", "Machine Learning Systems & Modeling", 4.0),
                ("603", "Web & Cloud Native Technologies", 4.0),
            ],
            7: [
                ("701", "Distributed Systems & Cloud Clusters", 4.0),
                ("702", "Cybersecurity & Cryptographic Protocols", 4.0),
                ("703", "Deep Learning & Neural Architectures", 3.0),
            ],
            8: [
                ("801", "Capstone Major Project & Viva", 6.0),
                ("802", "Structural Dynamics & System Synthesis", 4.0),
                ("803", "Industrial Seminar & Professional Ethics", 2.0),
            ]
        }

        # Seed subjects for each branch
        for b_key, b_obj in branches.items():
            prefix = b_obj.code.replace("_APEX", "")
            for sem, subjs in semester_subjects.items():
                for sub_code_num, sub_title, creds in subjs:
                    full_code = f"{prefix}{sub_code_num}"
                    existing_sub = db.query(Subject).filter(
                        Subject.branch_id == b_obj.id,
                        Subject.code == full_code
                    ).first()
                    if not existing_sub:
                        s = Subject(
                            branch_id=b_obj.id,
                            regulation_id=b_obj.regulation_id,
                            code=full_code,
                            title=sub_title,
                            credits=creds,
                            semester=sem
                        )
                        db.add(s)

        # Seed corresponding Course records
        for sem, subjs in semester_subjects.items():
            for sub_code_num, sub_title, creds in subjs:
                for dept_pfx in ["CS", "EC", "ME", "CE"]:
                    cid = f"CRS_{dept_pfx}{sub_code_num}"
                    ccode = f"{dept_pfx}{sub_code_num}"
                    c = db.query(Course).filter(Course.course_id == cid).first()
                    if not c:
                        c = Course(
                            course_id=cid,
                            course_code=ccode,
                            course_name=sub_title,
                            credits=int(creds),
                            semester=sem,
                            department="Computer Science" if dept_pfx == "CS" else "Electronics"
                        )
                        db.add(c)

        db.commit()
    finally:
        db.close()


def init_db():
    """Create all database tables and safely migrate added columns."""
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        for col, col_type in [
            ("college_id", "INTEGER"),
            ("regulation_id", "INTEGER"),
            ("branch_id", "INTEGER"),
            ("college_name", "VARCHAR(150) DEFAULT 'Raghu Engineering College'"),
            ("specialization", "VARCHAR(100) DEFAULT 'CSE (Data Science)'"),
            ("current_semester", "INTEGER DEFAULT 3")
        ]:
            try:
                conn.execute(text(f"ALTER TABLE students ADD COLUMN {col} {col_type}"))
                conn.commit()
            except Exception:
                pass

        for col, col_type in [
            ("subject_id", "INTEGER"),
            ("grade_letter", "VARCHAR(5)")
        ]:
            try:
                conn.execute(text(f"ALTER TABLE enrollments ADD COLUMN {col} {col_type}"))
                conn.commit()
            except Exception:
                pass

    # Populate canonical institutional dataset
    seed_academic_framework()


def get_db_session():
    """Context-safe DB session provider."""
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.close()
        raise
