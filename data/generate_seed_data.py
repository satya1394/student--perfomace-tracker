"""
Synthetic Seed Data Generation Script.
Generates 1000+ realistic student records across 4 departments, 8 semesters,
realistic normal grade distributions, attendance tracking, and edge cases.
Exports to PostgreSQL SQL script, CSVs, and seeds active database.
"""

import os
import sys
import random
from pathlib import Path
import numpy as np
import pandas as pd

# Add project root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from werkzeug.security import generate_password_hash

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

DATA_DIR = Path(__file__).resolve().parent
CSV_DIR = DATA_DIR / "sample_csv"
CSV_DIR.mkdir(parents=True, exist_ok=True)

DEPARTMENTS = ["Computer Science", "Electronics & Comm", "Mechanical Eng", "Civil Eng"]
DEPT_CODES = {"Computer Science": "CS", "Electronics & Comm": "EC", "Mechanical Eng": "ME", "Civil Eng": "CE"}

FIRST_NAMES = [
    "Aarav", "Aditi", "Rohan", "Priya", "Ananya", "Rahul", "Neha", "Vikram", "Sneha", "Karan",
    "Pooja", "Arjun", "Divya", "Siddharth", "Ishaan", "Riya", "Kavya", "Varun", "Meera", "Aditya",
    "Tanvi", "Nikhil", "Shreya", "Amit", "Bhavna", "Manish", "Deepika", "Harsh", "Gauri", "Suresh"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Patel", "Reddy", "Nair", "Iyer", "Rao", "Mehta", "Singh",
    "Kumar", "Das", "Joshi", "Bhat", "Deshmukh", "Choudhury", "Pillai", "Mishra", "Pandey", "Saxena"
]

COURSE_CATALOG = {
    "Computer Science": [
        ("CS101", "Introduction to Programming", 4, 1),
        ("CS102", "Discrete Mathematics", 4, 1),
        ("CS103", "Digital Logic Design", 3, 1),
        ("CS104", "Engineering Physics", 3, 1),
        ("CS105", "Communication Skills", 2, 1),
        ("CS201", "Data Structures & Algorithms", 4, 2),
        ("CS202", "Object Oriented Programming", 4, 2),
        ("CS203", "Computer Organization & Arch", 3, 2),
        ("CS204", "Probability & Statistics", 3, 2),
        ("CS205", "Environmental Science", 2, 2),
        ("CS301", "Database Management Systems", 4, 3),
        ("CS302", "Operating Systems", 4, 3),
        ("CS303", "Theory of Computation", 3, 3),
        ("CS304", "Software Engineering", 3, 3),
        ("CS305", "Web Technologies", 3, 3),
        ("CS401", "Computer Networks", 4, 4),
        ("CS402", "Design & Analysis of Algorithms", 4, 4),
        ("CS403", "Microprocessors & Interfacing", 3, 4),
        ("CS404", "Artificial Intelligence", 3, 4),
        ("CS405", "Cyber Security Fundamentals", 3, 4),
        ("CS501", "Machine Learning", 4, 5),
        ("CS502", "Compiler Design", 4, 5),
        ("CS503", "Cloud Computing", 3, 5),
        ("CS504", "Data Warehousing & Mining", 3, 5),
        ("CS505", "DevOps & Agile Practices", 3, 5),
        ("CS601", "Deep Learning & Neural Nets", 4, 6),
        ("CS602", "Distributed Systems", 4, 6),
        ("CS603", "Big Data Analytics", 3, 6),
        ("CS604", "Natural Language Processing", 3, 6),
        ("CS605", "Mobile App Development", 3, 6),
        ("CS701", "High Performance Computing", 4, 7),
        ("CS702", "Blockchain Technologies", 3, 7),
        ("CS703", "Computer Vision", 3, 7),
        ("CS704", "Major Project Phase I", 4, 7),
        ("CS801", "Internet of Things (IoT)", 3, 8),
        ("CS802", "Quantum Computing Intro", 3, 8),
        ("CS803", "Major Project Phase II", 8, 8),
    ],
    "Electronics & Comm": [
        ("EC101", "Basic Electrical Engineering", 4, 1),
        ("EC102", "Engineering Mathematics I", 4, 1),
        ("EC103", "Engineering Chemistry", 3, 1),
        ("EC104", "Engineering Graphics", 3, 1),
        ("EC105", "Basic Workshop Practice", 2, 1),
        ("EC201", "Electronic Devices & Circuits", 4, 2),
        ("EC202", "Network Theory", 4, 2),
        ("EC203", "Signals and Systems", 3, 2),
        ("EC204", "Engineering Mathematics II", 3, 2),
        ("EC301", "Analog Circuits", 4, 3),
        ("EC302", "Digital Electronics", 4, 3),
        ("EC303", "Electromagnetic Fields", 3, 3),
        ("EC401", "Analog Communication", 4, 4),
        ("EC402", "Microcontrollers & Embedded Sys", 4, 4),
        ("EC403", "Control Systems", 3, 4),
        ("EC501", "Digital Signal Processing", 4, 5),
        ("EC502", "Digital Communication", 4, 5),
        ("EC503", "VLSI Design", 3, 5),
        ("EC601", "Antenna & Wave Propagation", 4, 6),
        ("EC602", "Embedded IoT Systems", 4, 6),
        ("EC603", "Wireless Networks", 3, 6),
        ("EC701", "Optical Communication", 4, 7),
        ("EC702", "Radar & Satellite Comm", 3, 7),
        ("EC703", "Project Work I", 4, 7),
        ("EC801", "RF Circuit Design", 3, 8),
        ("EC802", "Nanoelectronics", 3, 8),
        ("EC803", "Major Project Phase II", 8, 8),
    ],
    "Mechanical Eng": [
        ("ME101", "Engineering Mechanics", 4, 1),
        ("ME102", "Mathematics for Engineers", 4, 1),
        ("ME103", "Applied Physics", 3, 1),
        ("ME104", "Workshop Technology", 3, 1),
        ("ME201", "Thermodynamics", 4, 2),
        ("ME202", "Material Science", 4, 2),
        ("ME203", "Strength of Materials", 3, 2),
        ("ME301", "Fluid Mechanics", 4, 3),
        ("ME302", "Manufacturing Processes", 4, 3),
        ("ME303", "Kinematics of Machinery", 3, 3),
        ("ME401", "Heat & Mass Transfer", 4, 4),
        ("ME402", "Dynamics of Machines", 4, 4),
        ("ME403", "Applied Thermal Eng", 3, 4),
        ("ME501", "Design of Machine Elements", 4, 5),
        ("ME502", "Turbo Machinery", 4, 5),
        ("ME503", "CAD/CAM Systems", 3, 5),
        ("ME601", "Finite Element Analysis", 4, 6),
        ("ME602", "Automobile Engineering", 4, 6),
        ("ME603", "Operations Research", 3, 6),
        ("ME701", "Refrigeration & Air Conditioning", 4, 7),
        ("ME702", "Robotics & Automation", 3, 7),
        ("ME703", "Capstone Design I", 4, 7),
        ("ME801", "Renewable Energy Systems", 3, 8),
        ("ME802", "Industrial Management", 3, 8),
        ("ME803", "Major Project Phase II", 8, 8),
    ],
    "Civil Eng": [
        ("CE101", "Building Materials & Construction", 4, 1),
        ("CE102", "Calculus & Linear Algebra", 4, 1),
        ("CE103", "Engineering Geology", 3, 1),
        ("CE104", "Surveying Fundamentals", 3, 1),
        ("CE201", "Structural Analysis I", 4, 2),
        ("CE202", "Fluid Mechanics for Civil", 4, 2),
        ("CE203", "Advanced Surveying", 3, 2),
        ("CE301", "Structural Analysis II", 4, 3),
        ("CE302", "Concrete Technology", 4, 3),
        ("CE303", "Soil Mechanics", 3, 3),
        ("CE401", "Design of RC Structures", 4, 4),
        ("CE402", "Hydrology & Water Resources", 4, 4),
        ("CE403", "Geotechnical Engineering", 3, 4),
        ("CE501", "Design of Steel Structures", 4, 5),
        ("CE502", "Transportation Engineering", 4, 5),
        ("CE503", "Environmental Engineering I", 3, 5),
        ("CE601", "Foundation Engineering", 4, 6),
        ("CE602", "Environmental Engineering II", 4, 6),
        ("CE603", "Construction Management", 3, 6),
        ("CE701", "Earthquake Resistant Design", 4, 7),
        ("CE702", "Remote Sensing & GIS", 3, 7),
        ("CE703", "Civil Design Project I", 4, 7),
        ("CE801", "Urban Planning & Smart Cities", 3, 8),
        ("CE802", "Bridge Engineering", 3, 8),
        ("CE803", "Major Capstone Project", 8, 8),
    ]
}


def get_grade_and_point(marks):
    if marks >= 90: return "O", 10.0
    elif marks >= 80: return "A+", 9.0
    elif marks >= 70: return "A", 8.0
    elif marks >= 60: return "B+", 7.0
    elif marks >= 50: return "B", 6.0
    elif marks >= 40: return "C", 5.0
    elif marks >= 35: return "P", 4.0
    else: return "F", 0.0


def generate_dataset(num_students=1050):
    print(f"Generating synthetic academic records for {num_students} students...")
    students = []
    courses = []
    enrollments = []

    # 1. Generate Course records
    course_id_map = {}
    for dept, crs_list in COURSE_CATALOG.items():
        for code, name, cr, sem in crs_list:
            cid = f"CRS_{code}"
            courses.append({
                "course_id": cid,
                "course_code": code,
                "course_name": name,
                "credits": cr,
                "semester": sem,
                "department": dept
            })
            course_id_map[code] = (cid, cr, sem, dept)

    # 2. Generate Student and Enrollment records
    dept_distribution = [0.40, 0.25, 0.20, 0.15]  # CS, EC, ME, CE
    student_count_per_dept = [int(num_students * frac) for frac in dept_distribution]
    student_count_per_dept[0] += num_students - sum(student_count_per_dept)  # balance remainder

    enr_counter = 1
    stu_idx = 1

    for dept_idx, dept in enumerate(DEPARTMENTS):
        dept_code = DEPT_CODES[dept]
        dept_n = student_count_per_dept[dept_idx]
        dept_courses = COURSE_CATALOG[dept]

        for i in range(dept_n):
            sid = f"STU2024{dept_code}{stu_idx:04d}"
            fname = random.choice(FIRST_NAMES)
            lname = random.choice(LAST_NAMES)
            name = f"{fname} {lname}"
            email = f"{fname.lower()}.{lname.lower()}{stu_idx}@university.edu"
            enr_year = random.choice([2021, 2022, 2023, 2024])

            students.append({
                "student_id": sid,
                "name": name,
                "email": email,
                "department": dept,
                "enrollment_year": enr_year
            })
            stu_idx += 1

            # Persona determination:
            # 1. Top Performer (10%): Mean=88, Std=6, Attendance=92-98%
            # 2. Regular Student (70%): Mean=75, Std=12, Attendance=75-90%
            # 3. At-Risk Student (15%): Mean=48, Std=14, Attendance=50-68%
            # 4. Inconsistent Student (5%): High variance across semesters
            rand_persona = random.random()
            if rand_persona < 0.10:
                base_mean = 88.0
                base_std = 6.0
                base_att_min, base_att_max = 88.0, 98.0
            elif rand_persona < 0.80:
                base_mean = 74.0
                base_std = 11.0
                base_att_min, base_att_max = 75.0, 92.0
            elif rand_persona < 0.95:
                base_mean = 46.0
                base_std = 13.0
                base_att_min, base_att_max = 52.0, 68.0
            else:
                base_mean = 62.0
                base_std = 18.0
                base_att_min, base_att_max = 60.0, 85.0

            # Generate 8 semesters of enrollments
            for code, cname, cr, sem in dept_courses:
                marks = float(np.clip(np.random.normal(base_mean, base_std), 15.0, 99.0))
                marks = round(marks, 1)
                grade, gp = get_grade_and_point(marks)
                att = float(np.clip(np.random.uniform(base_att_min, base_att_max), 40.0, 100.0))
                att = round(att, 1)

                cid = f"CRS_{code}"
                acad_year = f"{enr_year + (sem - 1) // 2}-{enr_year + (sem - 1) // 2 + 1}"

                enrollments.append({
                    "enrollment_id": enr_counter,
                    "student_id": sid,
                    "course_id": cid,
                    "marks_obtained": marks,
                    "grade": grade,
                    "grade_point": gp,
                    "attendance_percentage": att,
                    "semester": sem,
                    "academic_year": acad_year
                })
                enr_counter += 1

    # Save to CSV files
    df_students = pd.DataFrame(students)
    df_courses = pd.DataFrame(courses)
    df_enrollments = pd.DataFrame(enrollments)

    df_students.to_csv(CSV_DIR / "students.csv", index=False)
    df_courses.to_csv(CSV_DIR / "courses.csv", index=False)
    df_enrollments.to_csv(CSV_DIR / "enrollments.csv", index=False)

    print(f"Exported {len(df_students)} students, {len(df_courses)} courses, and {len(df_enrollments)} enrollments to CSV.")

    # Generate SQL file
    sql_path = DATA_DIR / "sample_data.sql"
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("-- Student Academic Performance Analytics Database Seed Script\n")
        f.write("-- Generated for PostgreSQL\n\n")

        f.write("-- 1. Insert Courses\n")
        for c in courses:
            escaped_name = c["course_name"].replace("'", "''")
            f.write(f"INSERT INTO courses (course_id, course_code, course_name, credits, semester, department) VALUES ('{c['course_id']}', '{c['course_code']}', '{escaped_name}', {c['credits']}, {c['semester']}, '{c['department']}');\n")

        f.write("\n-- 2. Insert Students\n")
        for s in students:
            escaped_name = s["name"].replace("'", "''")
            f.write(f"INSERT INTO students (student_id, name, email, department, enrollment_year, created_at) VALUES ('{s['student_id']}', '{escaped_name}', '{s['email']}', '{s['department']}', {s['enrollment_year']}, NOW());\n")

        f.write("\n-- 3. Insert Enrollments (Sample batch)\n")
        for e in enrollments[:1500]:  # batch in SQL
            f.write(f"INSERT INTO enrollments (student_id, course_id, marks_obtained, grade, grade_point, attendance_percentage, semester, academic_year) VALUES ('{e['student_id']}', '{e['course_id']}', {e['marks_obtained']}, '{e['grade']}', {e['grade_point']}, {e['attendance_percentage']}, {e['semester']}, '{e['academic_year']}');\n")

    print(f"Saved sample SQL script to: {sql_path}")
    return df_students, df_courses, df_enrollments


def seed_database_tables():
    """Seeds the active database engine with the generated dataset."""
    from app.database import get_db_session, init_db, Student, Course, Enrollment, User
    from app.auth import seed_default_users

    init_db()
    seed_default_users()

    db = get_db_session()
    try:
        if db.query(Student).count() > 0:
            print("Database already contains student records. Skipping seeding.")
            return

        df_students, df_courses, df_enrollments = generate_dataset(1050)

        # Batch insert Courses
        course_objs = [
            Course(
                course_id=r["course_id"],
                course_code=r["course_code"],
                course_name=r["course_name"],
                credits=r["credits"],
                semester=r["semester"],
                department=r["department"]
            )
            for _, r in df_courses.iterrows()
        ]
        db.bulk_save_objects(course_objs)
        db.commit()

        # Batch insert Students
        student_objs = [
            Student(
                student_id=r["student_id"],
                name=r["name"],
                email=r["email"],
                department=r["department"],
                enrollment_year=r["enrollment_year"]
            )
            for _, r in df_students.iterrows()
        ]
        db.bulk_save_objects(student_objs)
        db.commit()

        # Batch insert Enrollments in chunks
        chunk_size = 5000
        enr_objs = [
            Enrollment(
                student_id=r["student_id"],
                course_id=r["course_id"],
                marks_obtained=r["marks_obtained"],
                grade=r["grade"],
                grade_point=r["grade_point"],
                attendance_percentage=r["attendance_percentage"],
                semester=r["semester"],
                academic_year=r["academic_year"]
            )
            for _, r in df_enrollments.iterrows()
        ]

        for i in range(0, len(enr_objs), chunk_size):
            db.bulk_save_objects(enr_objs[i:i + chunk_size])
            db.commit()

        print(f"Successfully seeded database with {len(student_objs)} students and {len(enr_objs)} enrollment records!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database_tables()
