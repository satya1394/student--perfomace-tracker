"""
SQLAlchemy Database Models and Connection Management.
Implements models for Curricula, CurriculumSubjects, ElectiveOptions, StudentSubjectSelections,
StudentSemesterResults, Colleges, Regulations, Branches, Subjects, Users, Students, Courses, Enrollments, Predictions, and Audit Logs.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean,
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
# 1. Canonical Curriculum Framework Models (Section 5 & 6)
# =========================================================================

class Curriculum(Base):
    """Canonical curriculum identity representing College + Degree + Regulation + Branch + Specialization."""
    __tablename__ = "curricula"

    curriculum_id = Column(String(100), primary_key=True, index=True)
    college = Column(String(150), nullable=False, index=True)
    degree = Column(String(32), nullable=False, default="B.Tech")
    regulation = Column(String(32), nullable=False, index=True)  # AR20, AR23
    branch = Column(String(64), nullable=False, index=True)      # CSE, ECE, EEE, MECH, CIVIL
    specialization = Column(String(100), nullable=False, index=True)
    curriculum_version = Column(String(20), default="1.0")
    effective_from = Column(String(20), default="2023")
    effective_until = Column(String(20), nullable=True)
    source_document = Column(String(200), nullable=True)
    last_verified_at = Column(DateTime, default=utc_now)
    created_at = Column(DateTime, default=utc_now)

    # Relationships
    subjects = relationship("CurriculumSubject", back_populates="curriculum", cascade="all, delete-orphan")
    elective_options = relationship("ElectiveOption", back_populates="curriculum", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Curriculum {self.curriculum_id}>"


class CurriculumSubject(Base):
    """Detailed canonical subject record with exact classification, credits, and verification metadata."""
    __tablename__ = "curriculum_subjects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    curriculum_id = Column(String(100), ForeignKey("curricula.curriculum_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 6-Field Explicit Composite Keys
    college = Column(String(150), nullable=False, index=True)
    degree = Column(String(32), nullable=False, default="B.Tech")
    regulation = Column(String(32), nullable=False, index=True)
    branch = Column(String(64), nullable=False, index=True)
    specialization = Column(String(100), nullable=False, index=True)
    semester = Column(Integer, nullable=False, index=True)

    # Subject details
    subject_code = Column(String(32), nullable=False, index=True)
    subject_name = Column(String(180), nullable=False)
    subject_type = Column(String(40), nullable=False, default="COMPULSORY_THEORY")  # COMPULSORY_THEORY, COMPULSORY_LAB, PROFESSIONAL_ELECTIVE, OPEN_ELECTIVE, HONORS, MINORS, SKILL_COURSE, AUDIT_COURSE, PROJECT, INTERNSHIP
    
    credits = Column(Float, nullable=True)
    official_credits = Column(Float, nullable=True)
    student_credits = Column(Float, nullable=True)
    credits_used = Column(Float, nullable=True)

    is_compulsory = Column(Boolean, default=True)
    is_elective = Column(Boolean, default=False)
    elective_group = Column(String(80), nullable=True)  # e.g. "Professional Elective I", "Open Elective II"
    theory_or_lab = Column(String(20), default="Theory")  # Theory, Lab, Skill, Project, Audit
    max_marks = Column(Float, default=100.0)
    pass_marks = Column(Float, default=40.0)

    # Verification and Status Values (Section 5)
    credit_source = Column(String(40), default="official_course_structure")  # official_course_structure, official_regulation, official_subject_pdf, official_notice, student_reported_official, student_estimate
    credit_status = Column(String(30), default="confirmed")                  # confirmed, pending, not_applicable
    verification_status = Column(String(30), default="official_verified")     # official_verified, student_confirmed, unverified, needs_review, unavailable
    
    source_url = Column(String(255), nullable=True)
    source_document = Column(String(200), nullable=True)
    curriculum_version = Column(String(20), default="1.0")
    effective_from = Column(String(20), default="2023")
    effective_until = Column(String(20), nullable=True)
    last_verified_at = Column(DateTime, default=utc_now)
    notes = Column(Text, nullable=True)

    # Relationship
    curriculum = relationship("Curriculum", back_populates="subjects")

    def __repr__(self):
        return f"<CurriculumSubject {self.subject_code}: {self.subject_name} ({self.credits} cr, Sem {self.semester})>"


class ElectiveOption(Base):
    """Categorized elective, honor, and minor pools selectable per semester."""
    __tablename__ = "elective_options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    curriculum_id = Column(String(100), ForeignKey("curricula.curriculum_id", ondelete="CASCADE"), nullable=False, index=True)
    semester = Column(Integer, nullable=False, index=True)
    category = Column(String(40), nullable=False)  # PROFESSIONAL_ELECTIVE, OPEN_ELECTIVE, HONORS, MINORS
    group_name = Column(String(80), nullable=False)  # e.g. "Professional Elective I"
    subject_code = Column(String(32), nullable=False)
    subject_name = Column(String(180), nullable=False)
    credits = Column(Float, nullable=True)
    credit_status = Column(String(30), default="confirmed")
    verification_status = Column(String(30), default="official_verified")
    source_url = Column(String(255), nullable=True)

    # Relationship
    curriculum = relationship("Curriculum", back_populates="elective_options")

    def __repr__(self):
        return f"<ElectiveOption {self.group_name} -> {self.subject_code}: {self.subject_name}>"


class StudentSubjectSelection(Base):
    """Individual student custom selections for electives, honors, and minors."""
    __tablename__ = "student_subject_selections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(32), ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    curriculum_id = Column(String(100), nullable=False, index=True)
    semester = Column(Integer, nullable=False, index=True)
    category = Column(String(40), nullable=False)
    group_name = Column(String(80), nullable=False)
    subject_code = Column(String(32), nullable=False)
    subject_name = Column(String(180), nullable=False)
    official_credits = Column(Float, nullable=True)
    student_credits = Column(Float, nullable=True)
    credits_used = Column(Float, nullable=True)
    credit_source = Column(String(40), default="official_course_structure")
    credit_status = Column(String(30), default="confirmed")
    marks = Column(Float, nullable=True)
    grade = Column(String(5), nullable=True)
    grade_point = Column(Float, nullable=True)
    created_at = Column(DateTime, default=utc_now)


class StudentSemesterResult(Base):
    """Preserved semester calculation snapshot with auditability and calculation status."""
    __tablename__ = "student_semester_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(32), ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    curriculum_id = Column(String(100), nullable=False, index=True)
    curriculum_version = Column(String(20), default="1.0")
    regulation = Column(String(32), nullable=False)
    branch = Column(String(64), nullable=False)
    specialization = Column(String(100), nullable=False)
    semester = Column(Integer, nullable=False, index=True)
    sgpa = Column(Float, nullable=True)
    calculation_status = Column(String(30), nullable=False, default="VERIFIED_SGPA")  # VERIFIED_SGPA, ESTIMATED_SGPA, INCOMPLETE_SGPA
    total_credits_used = Column(Float, default=0.0)
    official_credits_used = Column(Float, default=0.0)
    student_credits_used = Column(Float, default=0.0)
    subjects_used_json = Column(JSON, nullable=True)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)


# =========================================================================
# 2. Legacy Institutional & Profile Models
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
    """Academic curriculum regulations (e.g. AR23, AR20, R20)."""
    __tablename__ = "regulations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"), nullable=True)
    code = Column(String(20), nullable=False)  # e.g. "AR23", "AR20"
    name = Column(String(150), nullable=False)

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
    code = Column(String(32), nullable=False)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)

    # Relationships
    regulation = relationship("Regulation", back_populates="branches")
    subjects = relationship("Subject", back_populates="branch", cascade="all, delete-orphan")
    students = relationship("Student", back_populates="branch")

    def display_label(self):
        return f"{self.code} - {self.name} ({self.specialization})"

    def __repr__(self):
        return f"<Branch {self.code} ({self.specialization})>"


class Subject(Base):
    """Canonical curriculum subjects table."""
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


class User(Base):
    """User accounts table."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), nullable=False, default="STUDENT")
    student_id = Column(String(32), ForeignKey("students.student_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=utc_now)

    student = relationship("Student", back_populates="user_account")
    audit_logs = relationship("AuditLog", back_populates="user")


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
    curriculum_id = Column(String(100), nullable=True)

    # Academic metadata
    college_name = Column(String(150), default="Raghu Engineering College", nullable=True)
    degree = Column(String(32), default="B.Tech", nullable=True)
    regulation_name = Column(String(32), default="AR23", nullable=True)
    branch_name = Column(String(64), default="CSE", nullable=True)
    specialization = Column(String(100), default="Core Computer Science", nullable=True)
    current_semester = Column(Integer, default=3, nullable=True)
    enrollment_year = Column(Integer, nullable=False, default=2024)
    created_at = Column(DateTime, default=utc_now)

    user_account = relationship("User", back_populates="student", uselist=False)
    college = relationship("College", back_populates="students")
    branch = relationship("Branch", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="student", cascade="all, delete-orphan")


class Course(Base):
    """Courses catalog."""
    __tablename__ = "courses"

    course_id = Column(String(32), primary_key=True, index=True)
    course_code = Column(String(20), unique=True, nullable=False)
    course_name = Column(String(150), nullable=False)
    credits = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False, index=True)
    department = Column(String(64), nullable=False, index=True)

    enrollments = relationship("Enrollment", back_populates="course")


class Enrollment(Base):
    """Student course registrations with grade records and attendance tracking."""
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(32), ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(String(32), ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True, index=True)
    curriculum_subject_id = Column(Integer, ForeignKey("curriculum_subjects.id", ondelete="SET NULL"), nullable=True)
    
    marks_obtained = Column(Float, nullable=False)
    grade = Column(String(5), nullable=False)
    grade_letter = Column(String(5), nullable=True)
    grade_point = Column(Float, nullable=False)
    credits_used = Column(Float, default=3.0)
    attendance_percentage = Column(Float, nullable=False)
    semester = Column(Integer, nullable=False, index=True)
    academic_year = Column(String(20), nullable=False, default="2024-2025")

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    subject_ref = relationship("Subject", back_populates="enrollments")


class Prediction(Base):
    """Machine learning model outputs and student risk evaluations."""
    __tablename__ = "predictions"

    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(32), ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False, index=True)
    predicted_score = Column(Float, nullable=False)
    pass_probability = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False, index=True)
    confidence_score = Column(Float, nullable=False)
    shap_values = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    student = relationship("Student", back_populates="predictions")


class GradeRule(Base):
    """Academic grade boundary rules by regulation framework (e.g. AR23, AR20)."""
    __tablename__ = "grade_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    regulation_code = Column(String(20), nullable=False, default="AR23")
    regulation_id = Column(Integer, ForeignKey("regulations.id", ondelete="CASCADE"), nullable=True)
    grade_letter = Column(String(5), nullable=False)
    grade_point = Column(Float, nullable=False)
    min_marks = Column(Float, nullable=False)
    max_marks = Column(Float, nullable=False)


class AuditLog(Base):
    """System-wide audit trail."""
    __tablename__ = "audit_logs"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(64), nullable=False)
    target_entity = Column(String(64), nullable=False)
    entity_id = Column(String(64), nullable=True)
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=utc_now, index=True)

    user = relationship("User", back_populates="audit_logs")


def init_db():
    """Create all database tables and seed grade rules and institutional metadata."""
    Base.metadata.create_all(bind=engine)
    
    # Populate standard Grade Rules for AR23 & AR20 if not present
    db = SessionLocal()
    try:
        if db.query(GradeRule).count() == 0:
            for reg in ["AR23", "AR20", "R23", "R20"]:
                rules = [
                    ("O", 10.0, 90.0, 100.0),
                    ("A+", 9.0, 80.0, 89.99),
                    ("A", 8.0, 70.0, 79.99),
                    ("B+", 7.0, 60.0, 69.99),
                    ("B", 6.0, 50.0, 59.99),
                    ("C", 5.0, 40.0, 49.99),
                    ("F", 0.0, 0.0, 39.99),
                ]
                for g_let, gp, min_m, max_m in rules:
                    db.add(GradeRule(
                        regulation_code=reg,
                        grade_letter=g_let,
                        grade_point=gp,
                        min_marks=min_m,
                        max_marks=max_m
                    ))
            db.commit()
    finally:
        db.close()


def get_db_session():
    """Context-safe DB session provider."""
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.close()
        raise
