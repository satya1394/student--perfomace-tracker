import unittest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.database import (
    get_db_session, init_db, Curriculum, CurriculumSubject, 
    ElectiveOption, StudentSubjectSelection, StudentSemesterResult, Student, User
)
from app.curriculum_engine import CurriculumEngine, get_curriculum_id


class TestCurriculumAccuracy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.db = get_db_session()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_ar20_and_ar23_strict_separation(self):
        ar23_data = CurriculumEngine.get_subjects(
            self.db, "Raghu Engineering College", "B.Tech", "AR23", "CSE", "Core Computer Science", 3
        )
        ar20_data = CurriculumEngine.get_subjects(
            self.db, "Raghu Engineering College", "B.Tech", "AR20", "CSE", "Core Computer Science", 3
        )
        self.assertTrue(ar23_data["found"])
        self.assertTrue(ar20_data["found"])
        self.assertNotEqual(ar23_data["curriculum_id"], ar20_data["curriculum_id"])
        
        ar23_codes = [s.subject_code for s in ar23_data["compulsory_subjects"]]
        ar20_codes = [s.subject_code for s in ar20_data["compulsory_subjects"]]
        self.assertTrue(all(c.startswith("23") or c.startswith("20ES") for c in ar23_codes))
        self.assertTrue(all(c.startswith("20") for c in ar20_codes))
        self.assertIn("2305102", ar23_codes)
        self.assertIn("20CS3001", ar20_codes)

    def test_regulation_credit_structure_differences(self):
        ar20_sem8 = CurriculumEngine.get_subjects(
            self.db, "Raghu Engineering College", "B.Tech", "AR20", "CSE", "Core Computer Science", 8
        )
        ar23_sem8 = CurriculumEngine.get_subjects(
            self.db, "Raghu Engineering College", "B.Tech", "AR23", "CSE", "Core Computer Science", 8
        )
        self.assertTrue(ar20_sem8["found"])
        self.assertTrue(ar23_sem8["found"])
        ar20_cr = sum(s.credits for s in ar20_sem8["compulsory_subjects"])
        ar23_cr = sum(s.credits for s in ar23_sem8["compulsory_subjects"])
        self.assertEqual(ar20_cr, 12.0)
        self.assertEqual(ar23_cr, 12.0)

    def test_cse_aiml_vs_cse_datascience_isolation(self):
        aiml_data = CurriculumEngine.get_subjects(
            self.db, "Raghu Engineering College", "B.Tech", "AR23", "CSE", "AI & ML", 4
        )
        ds_data = CurriculumEngine.get_subjects(
            self.db, "Raghu Engineering College", "B.Tech", "AR23", "CSE", "Data Science", 4
        )
        self.assertTrue(aiml_data["found"])
        self.assertTrue(ds_data["found"])
        self.assertNotEqual(aiml_data["curriculum_id"], ds_data["curriculum_id"])
        aiml_codes = [s.subject_code for s in aiml_data["compulsory_subjects"]]
        self.assertIn("2342102", aiml_codes)

    def test_all_branches_isolation(self):
        branches = ["CSE", "ECE", "EEE", "MECH", "CIVIL"]
        curr_ids = set()
        for b in branches:
            specs = CurriculumEngine.get_specializations(self.db, "Raghu Engineering College", "B.Tech", "AR23", b)
            data = CurriculumEngine.get_subjects(self.db, "Raghu Engineering College", "B.Tech", "AR23", b, specs[0], 1)
            self.assertTrue(data["found"])
            curr_ids.add(data["curriculum_id"])
        self.assertEqual(len(curr_ids), len(branches))

    def test_professional_elective_grouping_and_selection(self):
        curr_data = CurriculumEngine.get_subjects(
            self.db, "Raghu Engineering College", "B.Tech", "AR23", "CSE", "Core Computer Science", 5
        )
        self.assertTrue("Professional Elective I" in curr_data["elective_groups"])
        options = curr_data["elective_groups"]["Professional Elective I"]
        self.assertGreaterEqual(len(options), 3)

        subj_entry_1 = [
            {"code": "2305107", "name": "Compiler Design", "credits": 3.0, "grade_point": 9.0, "subject_type": "COMPULSORY_THEORY", "credit_source": "official_course_structure"},
            {"code": "2305301", "name": "Software Engineering", "credits": 3.0, "grade_point": 10.0, "subject_type": "PROFESSIONAL_ELECTIVE", "credit_source": "official_course_structure"}
        ]
        calc_1 = CurriculumEngine.calculate_sgpa(subj_entry_1)
        self.assertEqual(calc_1["status"], "VERIFIED_SGPA")
        self.assertEqual(calc_1["sgpa"], 9.5)
        self.assertEqual(calc_1["total_credits_used"], 6.0)

    def test_independent_student_elective_choices(self):
        curr_id = "RAGHU_BTECH_AR23_CSE_CORE_COMPUTER_SCIENCE"
        sel_a = StudentSubjectSelection(
            student_id="STU_A", curriculum_id=curr_id, semester=5, category="PROFESSIONAL_ELECTIVE",
            group_name="Professional Elective I", subject_code="2305301", subject_name="Software Engineering",
            credits_used=3.0, grade_point=9.0
        )
        sel_b = StudentSubjectSelection(
            student_id="STU_B", curriculum_id=curr_id, semester=5, category="PROFESSIONAL_ELECTIVE",
            group_name="Professional Elective I", subject_code="2305303", subject_name="Artificial Intelligence",
            credits_used=3.0, grade_point=10.0
        )
        self.db.add(sel_a)
        self.db.add(sel_b)
        self.db.commit()

        q_a = self.db.query(StudentSubjectSelection).filter(StudentSubjectSelection.student_id == "STU_A").first()
        q_b = self.db.query(StudentSubjectSelection).filter(StudentSubjectSelection.student_id == "STU_B").first()
        self.assertEqual(q_a.subject_code, "2305301")
        self.assertEqual(q_b.subject_code, "2305303")

        self.db.query(StudentSubjectSelection).filter(StudentSubjectSelection.student_id.in_(["STU_A", "STU_B"])).delete()
        self.db.commit()

    def test_verified_sgpa_calculation(self):
        subjects = [
            {"code": "23BS101", "name": "Linear Algebra", "official_credits": 3.0, "grade_point": 9.0, "credit_source": "official_course_structure"},
            {"code": "23BS104", "name": "Applied Chemistry", "official_credits": 3.0, "grade_point": 8.0, "credit_source": "official_course_structure"},
            {"code": "23ES203", "name": "C Lab", "official_credits": 1.5, "grade_point": 10.0, "credit_source": "official_course_structure"}
        ]
        calc = CurriculumEngine.calculate_sgpa(subjects)
        self.assertEqual(calc["status"], "VERIFIED_SGPA")
        self.assertEqual(calc["sgpa"], 8.8)
        self.assertEqual(calc["status_title"], "SGPA — Verified curriculum credits")

    def test_estimated_sgpa_with_student_entered_credit(self):
        subjects = [
            {"code": "23BS101", "name": "Linear Algebra", "official_credits": 3.0, "grade_point": 9.0, "credit_source": "official_course_structure"},
            {"code": "23CUST01", "name": "Custom Elective", "student_credits": 3.0, "grade_point": 9.0, "credit_source": "student_reported_official"}
        ]
        calc = CurriculumEngine.calculate_sgpa(subjects)
        self.assertEqual(calc["status"], "ESTIMATED_SGPA")
        self.assertIn("Estimated SGPA", calc["status_title"])
        self.assertEqual(calc["student_credits_used"], 3.0)
        self.assertEqual(calc["official_credits_used"], 3.0)

    def test_incomplete_sgpa_with_missing_credit(self):
        subjects = [
            {"code": "23BS101", "name": "Linear Algebra", "official_credits": 3.0, "grade_point": 9.0},
            {"code": "23MISS01", "name": "Unknown Subject", "official_credits": None, "student_credits": None, "credits": None, "grade_point": 8.0}
        ]
        calc = CurriculumEngine.calculate_sgpa(subjects)
        self.assertEqual(calc["status"], "INCOMPLETE_SGPA")
        self.assertIsNone(calc["sgpa"])
        self.assertEqual(len(calc["missing_credit_subjects"]), 1)
        self.assertIn("23MISS01", calc["missing_credit_subjects"][0])

    def test_audit_courses_excluded_from_sgpa(self):
        subjects = [
            {"code": "2305104", "name": "Theory of Computation", "official_credits": 3.0, "grade_point": 9.0, "subject_type": "COMPULSORY_THEORY"},
            {"code": "23MC601", "name": "Environmental Science", "official_credits": 0.0, "grade_point": 10.0, "subject_type": "AUDIT_COURSE"}
        ]
        calc = CurriculumEngine.calculate_sgpa(subjects)
        self.assertEqual(calc["sgpa"], 9.0)
        self.assertEqual(calc["total_credits_used"], 3.0)
        self.assertEqual(len(calc["excluded_subjects"]), 1)

    def test_manual_mode_custom_curriculum(self):
        custom_subjects = [
            {"code": "MANUAL_01", "name": "Custom Robotics", "credits": 4.0, "grade_point": 9.0, "credit_source": "student_estimate", "verification_status": "unverified"},
            {"code": "MANUAL_02", "name": "Custom Control Theory", "credits": 3.0, "grade_point": 8.0, "credit_source": "student_estimate", "verification_status": "unverified"}
        ]
        calc = CurriculumEngine.calculate_sgpa(custom_subjects)
        self.assertEqual(calc["status"], "ESTIMATED_SGPA")
        self.assertEqual(calc["sgpa"], 8.57)
        self.assertEqual(calc["student_credits_used"], 7.0)
        self.assertEqual(calc["official_credits_used"], 0.0)


if __name__ == "__main__":
    unittest.main()
