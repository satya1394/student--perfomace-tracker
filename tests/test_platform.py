"""
Platform Verification and Test Suite.
Tests Database schema & ORM, SGPA/CGPA calculations, ML accuracy, and reporting pipelines.
"""

import sys
import unittest
from pathlib import Path
import pandas as pd

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.config import Config
from app.database import init_db, get_db_session, Student, Course, Enrollment, User
from app.auth import seed_default_users, authenticate_user
from app.utils import calculate_grade_and_points, calculate_sgpa, calculate_cgpa, generate_excel_report, generate_pdf_report
from app.ml_models.train_models import generate_synthetic_training_data, train_and_export_models
from app.ml_models.predict import predict_student_performance, generate_study_roadmap


class TestAcademicPlatform(unittest.TestCase):
    """Automated integration and unit test suite."""

    @classmethod
    def setUpClass(cls):
        """Initializes database schema and default accounts for testing."""
        init_db()
        seed_default_users()

    def test_01_grade_and_points_mapping(self):
        """Verifies accurate mapping of marks to letter grades and 10-point scale."""
        self.assertEqual(calculate_grade_and_points(95.0), ("O", 10.0))
        self.assertEqual(calculate_grade_and_points(85.0), ("A+", 9.0))
        self.assertEqual(calculate_grade_and_points(75.0), ("A", 8.0))
        self.assertEqual(calculate_grade_and_points(65.0), ("B+", 7.0))
        self.assertEqual(calculate_grade_and_points(55.0), ("B", 6.0))
        self.assertEqual(calculate_grade_and_points(45.0), ("C", 5.0))
        self.assertEqual(calculate_grade_and_points(37.0), ("P", 4.0))
        self.assertEqual(calculate_grade_and_points(25.0), ("F", 0.0))

    def test_02_sgpa_and_cgpa_calculations(self):
        """Verifies SGPA and CGPA formula math against known ground-truth calculations."""
        # Semester 1:
        # Course 1: Grade A (8.0), Credits 4 -> 32
        # Course 2: Grade O (10.0), Credits 4 -> 40
        # Course 3: Grade B (6.0), Credits 3 -> 18
        # Total Weighted: 90 / 11 Credits = 8.1818 -> 8.18
        sem1_courses = [
            {"grade_point": 8.0, "credits": 4},
            {"grade_point": 10.0, "credits": 4},
            {"grade_point": 6.0, "credits": 3}
        ]
        sgpa1 = calculate_sgpa(sem1_courses)
        self.assertAlmostEqual(sgpa1, 8.18, places=2)

        # Semester 2:
        # Course 4: Grade A+ (9.0), Credits 4 -> 36
        # Course 5: Grade A (8.0), Credits 4 -> 32
        # Total Weighted: 68 / 8 Credits = 8.50
        sem2_courses = [
            {"grade_point": 9.0, "credits": 4},
            {"grade_point": 8.0, "credits": 4}
        ]
        sgpa2 = calculate_sgpa(sem2_courses)
        self.assertAlmostEqual(sgpa2, 8.50, places=2)

        # CGPA across Sem 1 & 2: (90 + 68) / (11 + 8) = 158 / 19 = 8.3157 -> 8.32
        all_courses = sem1_courses + sem2_courses
        cgpa = calculate_cgpa(all_courses)
        self.assertAlmostEqual(cgpa, 8.32, places=2)

    def test_03_authentication_and_roles(self):
        """Verifies Flask-Login authentication and role assignment."""
        success, user = authenticate_user("student_demo", "Student@123")
        self.assertTrue(success)
        self.assertEqual(user.role, "STUDENT")

        success, faculty = authenticate_user("faculty_demo", "Faculty@123")
        self.assertTrue(success)
        self.assertEqual(faculty.role, "FACULTY")

        success, admin = authenticate_user("admin_demo", "Admin@123")
        self.assertTrue(success)
        self.assertEqual(admin.role, "ADMIN")

        fail_success, _ = authenticate_user("admin_demo", "WrongPassword")
        self.assertFalse(fail_success)

    def test_04_ml_model_training_and_accuracy(self):
        """Verifies ML models train and achieve >85% target metrics."""
        metrics = train_and_export_models()
        self.assertGreater(metrics["clf_accuracy"], 0.85, "Pass/Fail accuracy must exceed 85%")
        self.assertGreater(metrics["risk_accuracy"], 0.85, "Risk classifier accuracy must exceed 85%")
        self.assertGreater(metrics["cv_mean"], 0.85, "Cross-validation score must exceed 85%")

    def test_05_ml_prediction_and_roadmap(self):
        """Verifies ML inference outputs, risk classification, and roadmap generation."""
        sample_metrics = {
            "past_cgpa": 8.5,
            "attendance_rate": 92.0,
            "internal_assessment": 26.0,
            "assignments_completed": 9,
            "study_hours_per_week": 24.0,
            "credit_load": 20
        }
        res = predict_student_performance(sample_metrics)
        self.assertIn("predicted_score", res)
        self.assertIn("risk_level", res)
        self.assertIn("pass_probability", res)
        self.assertIn("shap_contributions", res)
        self.assertGreaterEqual(res["predicted_score"], 0.0)
        self.assertLessEqual(res["predicted_score"], 100.0)

        roadmap = generate_study_roadmap(sample_metrics, res)
        self.assertIn("steps", roadmap)
        self.assertGreater(len(roadmap["steps"]), 0)

    def test_06_excel_and_pdf_reporting(self):
        """Verifies openpyxl Excel and PDF report byte generation."""
        df_sample = pd.DataFrame([
            {"semester": 1, "course_code": "CS101", "course_name": "Programming", "credits": 4, "marks_obtained": 88.0, "grade": "A+", "attendance_percentage": 94.0},
            {"semester": 1, "course_code": "CS102", "course_name": "Discrete Math", "credits": 4, "marks_obtained": 76.0, "grade": "A", "attendance_percentage": 90.0},
        ])
        stu_meta = {"student_id": "STU2024CS0001", "name": "Aarav Sharma", "department": "Computer Science"}
        kpi_meta = {"cgpa": 8.50, "attendance": 92.0, "risk_level": "LOW"}

        excel_bytes = generate_excel_report(stu_meta, kpi_meta, df_sample)
        self.assertGreater(len(excel_bytes), 1000)

        pdf_bytes = generate_pdf_report(stu_meta, kpi_meta, df_sample)
        self.assertGreater(len(pdf_bytes), 100)

    def test_07_student_registration_and_constraints(self):
        """Verifies new user registration with 8-character password constraint and roll number username validation."""
        import uuid
        from app.auth import register_student_user

        uid = uuid.uuid4().hex[:6].upper()
        test_roll = f"2024CS{uid}"
        test_user = f"scholar_{test_roll}"

        # 1. Reject password under 8 characters
        _, err_short = register_student_user("Test Short", test_roll, test_user, f"short_{uid}@test.com", "Computer Science", 1, "Short1", "Short1")
        self.assertIn("at least 8 characters", err_short)

        # 2. Reject username missing roll number
        _, err_roll = register_student_user("Test Roll", test_roll, "random_username", f"roll_{uid}@test.com", "Computer Science", 1, "Password@123", "Password@123")
        self.assertIn("must contain your Roll Number", err_roll)

        # 3. Successful registration when all constraints are satisfied
        user, err_ok = register_student_user(
            full_name="Priya Patel",
            roll_number=test_roll,
            username=test_user,
            email=f"priya_{uid}@test.com",
            department="Computer Science",
            semester=2,
            password="PriyaPass@123",
            confirm_password="PriyaPass@123",
            college_id=1,
            regulation_id=1,
            branch_id=2
        )
        self.assertIsNone(err_ok)
        self.assertIsNotNone(user)
        self.assertEqual(user.role, "STUDENT")
        self.assertEqual(user.student_id, test_roll)

    def test_08_academic_framework_seeding(self):
        """Verifies Colleges, Regulations, Branches, and Subjects are properly populated in database."""
        from app.database import get_db_session, College, Regulation, Branch, Subject
        db = get_db_session()
        try:
            colleges = db.query(College).all()
            regulations = db.query(Regulation).all()
            branches = db.query(Branch).all()
            subjects = db.query(Subject).all()

            self.assertGreaterEqual(len(colleges), 5)
            self.assertGreaterEqual(len(regulations), 5)
            self.assertGreaterEqual(len(branches), 5)
            self.assertGreaterEqual(len(subjects), 50)
        finally:
            db.close()

    def test_09_marks_entry_and_recalculation(self):
        """Verifies marks insertion, grade calculation, and SGPA calculation for student."""
        from app.database import get_db_session, Student, Subject, Enrollment
        from app.utils import calculate_grade, calculate_sgpa_for_student
        import uuid

        db = get_db_session()
        try:
            uid = uuid.uuid4().hex[:6].upper()
            roll = f"TEST{uid}"
            
            # Create test student
            stu = Student(
                student_id=roll,
                name="Test Student",
                email=f"test_{uid}@test.com",
                department="Computer Science",
                college_id=1,
                regulation_id=1,
                branch_id=2,
                current_semester=1
            )
            db.add(stu)
            db.commit()

            # Add test marks for Semester 1 subjects
            subjects = db.query(Subject).filter(Subject.branch_id == 2, Subject.semester == 1).all()
            self.assertTrue(len(subjects) > 0)

            for s in subjects:
                g_let, g_pt = calculate_grade(85.0)
                enr = Enrollment(
                    student_id=roll,
                    subject_id=s.id,
                    course_id=s.code,
                    marks_obtained=85.0,
                    grade=g_let,
                    grade_letter=g_let,
                    grade_point=g_pt,
                    attendance_percentage=90.0,
                    semester=1,
                    academic_year="2024-2025"
                )
                db.add(enr)
            db.commit()

            # Calculate SGPA
            sgpa = calculate_sgpa_for_student(roll, 1)
            self.assertEqual(sgpa, 9.0) # 85 marks = A+ (9.0 grade point)
        finally:
            db.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)

