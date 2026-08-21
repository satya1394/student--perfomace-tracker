"""
Curriculum CSV & JSON Importer and Validator.
Parses, validates, and loads canonical curricula into the SQLite database.
Generates comprehensive validation reports as specified in Section 14.
"""

import csv
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from typing import Dict, List, Any
from datetime import datetime, timezone

from app.database import (
    get_db_session, init_db, Curriculum, CurriculumSubject, 
    ElectiveOption, GradeRule, College, Regulation, Branch
)
from app.curriculum_engine import get_curriculum_id


def load_and_validate_curricula(csv_path: str = None) -> Dict[str, Any]:
    """
    Parses and validates official curricula CSV file, loads records into DB,
    and returns a detailed validation report.
    """
    if csv_path is None:
        csv_path = Path(__file__).resolve().parent.parent / "data" / "official_curricula.csv"
    
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"Curriculum CSV not found at {csv_file}")

    db = get_db_session()
    
    report = {
        "total_rows_processed": 0,
        "valid_subjects_imported": 0,
        "curricula_count": 0,
        "curricula_list": [],
        "subject_counts_per_curriculum": {},
        "credits_per_semester": {},
        "verified_records": 0,
        "pending_credit_subjects": 0,
        "records_needing_review": 0,
        "duplicate_codes_detected": [],
        "placeholder_codes_detected": [],
        "ambiguous_records": [],
        "elective_groups_count": 0
    }

    try:
        # Clear previous curriculum records for a clean load
        db.query(ElectiveOption).delete()
        db.query(CurriculumSubject).delete()
        db.query(Curriculum).delete()
        db.commit()

        curricula_map = {}
        seen_codes_per_sem = {}

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                report["total_rows_processed"] += 1
                
                college = (row.get("College") or "").strip()
                degree = (row.get("Degree") or "").strip()
                reg = (row.get("Regulation") or "").strip()
                branch = (row.get("Branch") or "").strip()
                spec = (row.get("Specialization") or "").strip()
                sem_str = (row.get("Semester") or "").strip()
                sub_code = (row.get("Subject Code") or "").strip()
                sub_name = (row.get("Subject Name") or "").strip()
                stype = (row.get("Subject Type") or "COMPULSORY_THEORY").strip()
                cr_str = (row.get("Credits") or "").strip()
                t_or_l = (row.get("Theory/Lab") or "Theory").strip()
                is_comp = (row.get("Is Compulsory") or "True").strip().lower() == "true"
                is_elec = (row.get("Is Elective") or "False").strip().lower() == "true"
                elec_grp = (row.get("Elective Group") or "").strip()
                cr_src = (row.get("Credit Source") or "official_course_structure").strip()
                cr_status = (row.get("Credit Status") or "confirmed").strip()
                ver_status = (row.get("Verification Status") or "official_verified").strip()
                src_url = (row.get("Source URL") or "").strip()
                src_doc = (row.get("Source Document") or "").strip()
                notes = (row.get("Notes") or "").strip()

                # Basic validation
                if not college or not degree or not reg or not branch or not spec or not sem_str:
                    report["ambiguous_records"].append(f"Row {report['total_rows_processed']}: Missing academic parameters.")
                    continue
                if not sub_code or not sub_name:
                    report["ambiguous_records"].append(f"Row {report['total_rows_processed']}: Missing code or name.")
                    continue

                try:
                    sem = int(sem_str)
                except ValueError:
                    report["ambiguous_records"].append(f"Row {report['total_rows_processed']}: Invalid semester '{sem_str}'.")
                    continue

                credits_val = None
                if cr_str != "":
                    try:
                        credits_val = float(cr_str)
                    except ValueError:
                        credits_val = None
                        cr_status = "pending"
                        ver_status = "needs_review"

                if credits_val is None:
                    cr_status = "pending"
                    report["pending_credit_subjects"] += 1

                # Check for placeholder codes (e.g. 20XX54XX)
                if "XX" in sub_code.upper() or "PLACEHOLDER" in sub_code.upper():
                    report["placeholder_codes_detected"].append(f"{sub_code} ({sub_name})")
                    ver_status = "needs_review"

                # Check duplicate subject codes within one curriculum & semester
                curr_id = get_curriculum_id(college, degree, reg, branch, spec)
                key = (curr_id, sem, sub_code)
                if key in seen_codes_per_sem:
                    report["duplicate_codes_detected"].append(f"{curr_id} Sem {sem}: Duplicate {sub_code}")
                seen_codes_per_sem[key] = True

                # Ensure Curriculum parent record exists
                if curr_id not in curricula_map:
                    c_obj = Curriculum(
                        curriculum_id=curr_id,
                        college=college,
                        degree=degree,
                        regulation=reg,
                        branch=branch,
                        specialization=spec,
                        curriculum_version="1.0",
                        effective_from="2023" if "23" in reg else "2020",
                        source_document=src_doc or f"{college} {reg} Course Structure",
                        last_verified_at=datetime.now(timezone.utc)
                    )
                    db.add(c_obj)
                    db.flush()
                    curricula_map[curr_id] = c_obj
                    report["curricula_list"].append(curr_id)

                # Create CurriculumSubject record
                csub = CurriculumSubject(
                    curriculum_id=curr_id,
                    college=college,
                    degree=degree,
                    regulation=reg,
                    branch=branch,
                    specialization=spec,
                    semester=sem,
                    subject_code=sub_code,
                    subject_name=sub_name,
                    subject_type=stype,
                    credits=credits_val,
                    official_credits=credits_val,
                    student_credits=None,
                    credits_used=credits_val,
                    is_compulsory=is_comp,
                    is_elective=is_elec,
                    elective_group=elec_grp if elec_grp else None,
                    theory_or_lab=t_or_l,
                    max_marks=100.0,
                    pass_marks=40.0,
                    credit_source=cr_src,
                    credit_status=cr_status,
                    verification_status=ver_status,
                    source_url=src_url,
                    source_document=src_doc,
                    curriculum_version="1.0",
                    effective_from="2023" if "23" in reg else "2020",
                    notes=notes
                )
                db.add(csub)

                # If elective / honors / minors, add to ElectiveOption
                if is_elec or stype in ["PROFESSIONAL_ELECTIVE", "OPEN_ELECTIVE", "HONORS", "MINORS"]:
                    e_opt = ElectiveOption(
                        curriculum_id=curr_id,
                        semester=sem,
                        category=stype,
                        group_name=elec_grp or (f"Professional Elective" if stype == "PROFESSIONAL_ELECTIVE" else "Open Elective"),
                        subject_code=sub_code,
                        subject_name=sub_name,
                        credits=credits_val,
                        credit_status=cr_status,
                        verification_status=ver_status,
                        source_url=src_url
                    )
                    db.add(e_opt)
                    report["elective_groups_count"] += 1

                report["valid_subjects_imported"] += 1
                if ver_status == "official_verified":
                    report["verified_records"] += 1
                elif ver_status == "needs_review":
                    report["records_needing_review"] += 1

                # Track counts
                report["subject_counts_per_curriculum"][curr_id] = report["subject_counts_per_curriculum"].get(curr_id, 0) + 1
                sem_key = f"{curr_id}_Sem_{sem}"
                if credits_val:
                    report["credits_per_semester"][sem_key] = report["credits_per_semester"].get(sem_key, 0.0) + credits_val

        db.commit()
        report["curricula_count"] = len(curricula_map)
        return report
    finally:
        db.close()


def print_validation_report(report: Dict[str, Any]):
    """Outputs human-readable validation summary."""
    print("==========================================================")
    print("           STUDIQ CURRICULUM VALIDATION REPORT            ")
    print("==========================================================")
    print(f"Total Rows Processed: {report['total_rows_processed']}")
    print(f"Valid Subjects Imported: {report['valid_subjects_imported']}")
    print(f"Curricula Registered: {report['curricula_count']}")
    print(f"Official Verified Records: {report['verified_records']}")
    print(f"Pending Credit Records: {report['pending_credit_subjects']}")
    print(f"Records Needing Review: {report['records_needing_review']}")
    print(f"Elective Options Classified: {report['elective_groups_count']}")
    print(f"Duplicate Codes Detected: {len(report['duplicate_codes_detected'])}")
    print(f"Placeholder Codes Detected: {len(report['placeholder_codes_detected'])}")
    print("----------------------------------------------------------")
    print("Registered Curricula:")
    for cid in report["curricula_list"]:
        print(f"  • {cid}: {report['subject_counts_per_curriculum'].get(cid, 0)} subjects")
    print("==========================================================")


if __name__ == "__main__":
    init_db()
    rep = load_and_validate_curricula()
    print_validation_report(rep)
