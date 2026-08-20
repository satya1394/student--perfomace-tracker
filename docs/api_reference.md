# API & Database Reference

## 1. Database Schema & ORM Classes

### `User` Table (`app/database.py`)
- `id` (Integer, Primary Key)
- `username` (String(64), Unique, Indexed)
- `email` (String(120), Unique, Indexed)
- `password_hash` (String(256), Werkzeug Hash)
- `role` (String(20): `STUDENT`, `FACULTY`, `ADMIN`)
- `student_id` (String(32), Foreign Key -> `students.student_id`)
- `created_at` (DateTime)

### `Student` Table (`app/database.py`)
- `student_id` (String(32), Primary Key)
- `name` (String(120))
- `email` (String(120), Unique)
- `department` (String(64), Indexed)
- `enrollment_year` (Integer)
- `created_at` (DateTime)

### `Course` Table (`app/database.py`)
- `course_id` (String(32), Primary Key)
- `course_code` (String(20), Unique)
- `course_name` (String(150))
- `credits` (Integer)
- `semester` (Integer)
- `department` (String(64))

### `Enrollment` Table (`app/database.py`)
- `enrollment_id` (Integer, Primary Key)
- `student_id` (String(32), Foreign Key -> `students.student_id`)
- `course_id` (String(32), Foreign Key -> `courses.course_id`)
- `marks_obtained` (Float, 0.0 - 100.0)
- `grade` (String(5): O, A+, A, B+, B, C, P, F)
- `grade_point` (Float, 0.0 - 10.0)
- `attendance_percentage` (Float, 0.0 - 100.0)
- `semester` (Integer)
- `academic_year` (String(20))

---

## 2. Core Python Functions

### `calculate_sgpa(enrollment_records: list[dict]) -> float`
Computes Semester Grade Point Average.
```python
from app.utils import calculate_sgpa
records = [{"grade_point": 9.0, "credits": 4}, {"grade_point": 8.0, "credits": 3}]
sgpa = calculate_sgpa(records) # 8.57
```

### `calculate_cgpa(all_semesters_enrollments: list[dict]) -> float`
Computes Cumulative Grade Point Average across all semesters.

### `predict_student_performance(metrics: dict) -> dict`
Generates regression score forecast, pass probability, risk classification, and SHAP feature attributions.
```python
from app.ml_models.predict import predict_student_performance
result = predict_student_performance({
    "past_cgpa": 8.2,
    "attendance_rate": 88.0,
    "internal_assessment": 24.0,
    "assignments_completed": 9,
    "study_hours_per_week": 20.0,
    "credit_load": 22.0
})
```
