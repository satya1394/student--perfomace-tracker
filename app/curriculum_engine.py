"""
Curriculum Resolution & Calculation Engine for StudIQ.
Provides strict cascading 6-field academic filtering, exact subject resolution, elective groups,
and Verified vs. Estimated vs. Incomplete SGPA/CGPA calculation rules.
"""

from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timezone
import pandas as pd
from sqlalchemy import text


def get_curriculum_id(college: str, degree: str, regulation: str, branch: str, specialization: str) -> str:
    """Generates canonical curriculum ID string."""
    col_code = "RAGHU" if "raghu" in college.lower() else "COLL"
    deg_code = degree.upper().replace(".", "")
    reg_code = regulation.upper().replace("-", "")
    br_code = branch.upper().replace(" ", "_")
    spec_clean = specialization.upper().replace("&", "AND").replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
    return f"{col_code}_{deg_code}_{reg_code}_{br_code}_{spec_clean}".strip("_")


class CurriculumEngine:
    """Core academic framework service for StudIQ."""

    @staticmethod
    def get_colleges(db_session) -> List[str]:
        """Returns all distinct colleges in the system."""
        from app.database import Curriculum
        results = db_session.query(Curriculum.college).distinct().all()
        colleges = [r[0] for r in results if r[0]]
        if "Raghu Engineering College" not in colleges:
            colleges.insert(0, "Raghu Engineering College")
        return colleges

    @staticmethod
    def get_degrees(db_session, college: str) -> List[str]:
        """Returns available degrees for the given college."""
        from app.database import Curriculum
        results = db_session.query(Curriculum.degree).filter(Curriculum.college == college).distinct().all()
        degrees = [r[0] for r in results if r[0]]
        return degrees or ["B.Tech"]

    @staticmethod
    def get_regulations(db_session, college: str, degree: str) -> List[str]:
        """Returns available regulations for college & degree."""
        from app.database import Curriculum
        results = db_session.query(Curriculum.regulation).filter(
            Curriculum.college == college,
            Curriculum.degree == degree
        ).distinct().all()
        regs = [r[0] for r in results if r[0]]
        return regs or ["AR23", "AR20"]

    @staticmethod
    def get_branches(db_session, college: str, degree: str, regulation: str) -> List[str]:
        """Returns available branches for college, degree & regulation."""
        from app.database import Curriculum
        results = db_session.query(Curriculum.branch).filter(
            Curriculum.college == college,
            Curriculum.degree == degree,
            Curriculum.regulation == regulation
        ).distinct().all()
        branches = [r[0] for r in results if r[0]]
        return branches

    @staticmethod
    def get_specializations(db_session, college: str, degree: str, regulation: str, branch: str) -> List[str]:
        """Returns available specializations for branch under specific regulation."""
        from app.database import Curriculum
        results = db_session.query(Curriculum.specialization).filter(
            Curriculum.college == college,
            Curriculum.degree == degree,
            Curriculum.regulation == regulation,
            Curriculum.branch == branch
        ).distinct().all()
        specs = [r[0] for r in results if r[0]]
        return specs

    @staticmethod
    def get_semesters(db_session, college: str, degree: str, regulation: str, branch: str, specialization: str) -> List[int]:
        """Returns available semesters (1 to 8) for exact curriculum."""
        from app.database import CurriculumSubject
        results = db_session.query(CurriculumSubject.semester).filter(
            CurriculumSubject.college == college,
            CurriculumSubject.degree == degree,
            CurriculumSubject.regulation == regulation,
            CurriculumSubject.branch == branch,
            CurriculumSubject.specialization == specialization
        ).distinct().order_by(CurriculumSubject.semester).all()
        sems = [r[0] for r in results if r[0]]
        return sems or list(range(1, 9))

    @staticmethod
    def get_subjects(db_session, college: str, degree: str, regulation: str, 
                     branch: str, specialization: str, semester: int) -> Dict[str, Any]:
        """
        Exact matching lookup across all six academic fields:
        College + Degree + Regulation + Branch + Specialization + Semester.
        """
        from app.database import CurriculumSubject
        
        subjects = db_session.query(CurriculumSubject).filter(
            CurriculumSubject.college == college,
            CurriculumSubject.degree == degree,
            CurriculumSubject.regulation == regulation,
            CurriculumSubject.branch == branch,
            CurriculumSubject.specialization == specialization,
            CurriculumSubject.semester == semester
        ).order_by(CurriculumSubject.subject_code).all()

        if not subjects:
            return {
                "found": False,
                "curriculum_id": get_curriculum_id(college, degree, regulation, branch, specialization),
                "compulsory_subjects": [],
                "elective_groups": {},
                "honors_options": [],
                "minors_options": [],
                "total_fixed_credits": 0.0,
                "is_verified": False,
                "message": f"No verified curriculum was found for {college} • {degree} • {regulation} • {branch} ({specialization}) • Semester {semester}."
            }

        compulsory = []
        elective_groups: Dict[str, List[CurriculumSubject]] = {}
        honors = []
        minors = []
        total_fixed_credits = 0.0

        for s in subjects:
            if s.is_compulsory and s.subject_type in ["COMPULSORY_THEORY", "COMPULSORY_LAB", "SKILL_COURSE", "PROJECT"]:
                compulsory.append(s)
                if s.official_credits:
                    total_fixed_credits += float(s.official_credits)
                elif s.credits:
                    total_fixed_credits += float(s.credits)
            elif s.is_elective or s.subject_type in ["PROFESSIONAL_ELECTIVE", "OPEN_ELECTIVE"]:
                grp = s.elective_group or (f"Professional Elective" if s.subject_type == "PROFESSIONAL_ELECTIVE" else "Open Elective")
                if grp not in elective_groups:
                    elective_groups[grp] = []
                elective_groups[grp].append(s)
            elif s.subject_type == "HONORS":
                honors.append(s)
            elif s.subject_type == "MINORS":
                minors.append(s)
            elif s.subject_type == "AUDIT_COURSE":
                compulsory.append(s)

        return {
            "found": True,
            "curriculum_id": subjects[0].curriculum_id if subjects else get_curriculum_id(college, degree, regulation, branch, specialization),
            "compulsory_subjects": compulsory,
            "elective_groups": elective_groups,
            "honors_options": honors,
            "minors_options": minors,
            "total_fixed_credits": round(total_fixed_credits, 2),
            "is_verified": all(s.verification_status == "official_verified" for s in compulsory),
            "message": "Curriculum loaded successfully."
        }

    @staticmethod
    def calculate_sgpa(subject_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates term SGPA and categorizes computation status:
        - VERIFIED_SGPA: All included credits are official.
        - ESTIMATED_SGPA: At least one included credit was entered by student.
        - INCOMPLETE_SGPA: At least one included subject has no credit value.
        """
        total_weighted_points = 0.0
        total_credits_used = 0.0
        official_credits_used = 0.0
        student_credits_used = 0.0
        
        included_subjects = []
        excluded_subjects = []
        missing_credit_subjects = []
        has_student_entered_credit = False

        for item in subject_entries:
            name = item.get("name") or item.get("title") or item.get("code") or "Unknown Subject"
            code = item.get("code", "")
            gp = item.get("grade_point")
            
            # Check if subject is an audit or zero-credit course
            stype = str(item.get("subject_type", "")).upper()
            if stype == "AUDIT_COURSE" or str(item.get("theory_or_lab", "")).lower() == "audit":
                excluded_subjects.append(f"{code} {name} (Audit Course - 0 Credits)")
                continue

            off_cr = item.get("official_credits")
            stu_cr = item.get("student_credits")
            cr = item.get("credits")

            credit_used = None
            source = "official"

            if off_cr is not None and str(off_cr).strip() != "" and float(off_cr) > 0:
                credit_used = float(off_cr)
                source = item.get("credit_source", "official_course_structure")
                official_credits_used += credit_used
            elif stu_cr is not None and str(stu_cr).strip() != "" and float(stu_cr) > 0:
                credit_used = float(stu_cr)
                source = item.get("credit_source", "student_reported_official")
                student_credits_used += credit_used
                has_student_entered_credit = True
            elif cr is not None and str(cr).strip() != "" and float(cr) > 0:
                credit_used = float(cr)
                src = item.get("credit_source", "official_course_structure")
                if src.startswith("student_") or item.get("verification_status") in ["student_confirmed", "unverified"]:
                    source = src
                    student_credits_used += credit_used
                    has_student_entered_credit = True
                else:
                    source = "official_course_structure"
                    official_credits_used += credit_used
            else:
                missing_credit_subjects.append(f"{code} {name}")
                continue

            if gp is None or str(gp).strip() == "":
                gp = 8.0
            else:
                try:
                    gp = float(gp)
                except (ValueError, TypeError):
                    gp = 8.0

            gp = max(0.0, min(10.0, round(gp, 2)))
            
            total_weighted_points += (gp * credit_used)
            total_credits_used += credit_used
            
            included_subjects.append({
                "code": code,
                "name": name,
                "credits": credit_used,
                "grade_point": gp,
                "credit_source": source,
                "is_official": (source in ["official_course_structure", "official_regulation", "official_subject_pdf", "official_notice"])
            })

        if missing_credit_subjects:
            return {
                "status": "INCOMPLETE_SGPA",
                "sgpa": None,
                "sgpa_display": "Incomplete",
                "status_title": "SGPA unavailable — enter credits for all selected subjects.",
                "total_credits_used": total_credits_used,
                "official_credits_used": official_credits_used,
                "student_credits_used": student_credits_used,
                "included_subjects": included_subjects,
                "excluded_subjects": excluded_subjects,
                "missing_credit_subjects": missing_credit_subjects,
                "has_student_credits": has_student_entered_credit
            }

        if total_credits_used == 0:
            return {
                "status": "INCOMPLETE_SGPA",
                "sgpa": None,
                "sgpa_display": "—",
                "status_title": "No subjects selected.",
                "total_credits_used": 0.0,
                "official_credits_used": 0.0,
                "student_credits_used": 0.0,
                "included_subjects": [],
                "excluded_subjects": excluded_subjects,
                "missing_credit_subjects": [],
                "has_student_credits": False
            }

        calculated_sgpa = round(total_weighted_points / total_credits_used, 2)

        if has_student_entered_credit:
            status = "ESTIMATED_SGPA"
            status_title = "Estimated SGPA — based partly on student-entered credits"
        else:
            status = "VERIFIED_SGPA"
            status_title = "SGPA — Verified curriculum credits"

        return {
            "status": status,
            "sgpa": calculated_sgpa,
            "sgpa_display": f"{calculated_sgpa:.2f} / 10.0",
            "status_title": status_title,
            "total_credits_used": round(total_credits_used, 2),
            "official_credits_used": round(official_credits_used, 2),
            "student_credits_used": round(student_credits_used, 2),
            "included_subjects": included_subjects,
            "excluded_subjects": excluded_subjects,
            "missing_credit_subjects": [],
            "has_student_credits": has_student_entered_credit
        }
