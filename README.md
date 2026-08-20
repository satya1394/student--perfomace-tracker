# 🎓 EduPulse: Student Academic Performance Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Plotly Dash](https://img.shields.io/badge/Plotly%20Dash-3.0-0083B0.svg)](https://dash.plotly.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-2088FF.svg)](https://xgboost.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-grade, AI-powered full-stack academic performance analytics platform. Features automated **SGPA/CGPA calculations**, **machine learning performance forecasting** (Random Forest, Logistic Regression, XGBoost), **SHAP explainability**, and **interactive Plotly Dashboards** for Students, Faculty, and Administrators.

---

## 🌟 Key Platform Features

### 1. Multi-Persona Interactive Dashboards
- **Student View (`/student`)**:
  - Longitudinal SGPA progression curve with CGPA benchmark baseline.
  - Multi-axis subject competency radar chart.
  - Attendance vs. marks correlation scatter with student locator.
  - Dynamic AI-generated study roadmap with prioritized remedial actions.
- **Faculty View (`/faculty`)**:
  - Class-wide department and semester average marks heatmap.
  - Multi-tiered grade distribution histograms and box plots.
  - Early-warning alert table identifying high-risk students 4-6 weeks prior to exams.
  - One-click automated email alert dispatcher.
- **Administrator View (`/admin`)**:
  - Macro-level institutional KPIs (total enrollments, overall mean CGPA, retention rates).
  - Department comparative performance benchmarking.
  - Longitudinal cohort retention analysis.
  - System security and academic audit trail.

### 2. Accurate Academic Formulas
- **Grade Point System (10-Point Scale)**: $\ge 90\% \rightarrow 10.0$ (O), $80-89\% \rightarrow 9.0$ (A+), $70-79\% \rightarrow 8.0$ (A), $60-69\% \rightarrow 7.0$ (B+), $50-59\% \rightarrow 6.0$ (B), $40-49\% \rightarrow 5.0$ (C), $35-39\% \rightarrow 4.0$ (P), $<35\% \rightarrow 0.0$ (F).
- **SGPA Formula**:
  $$\text{SGPA} = \frac{\sum (\text{Grade Point}_i \times \text{Credits}_i)}{\sum \text{Credits}_i}$$
- **CGPA Formula**:
  $$\text{CGPA} = \frac{\sum (\text{Grade Point}_j \times \text{Credits}_j)}{\sum \text{Credits}_j}$$

### 3. Production Machine Learning & Interpretability
- **Random Forest Regressor**: Predicts continuous final exam scores ($R^2 > 0.85$, $RMSE < 6.0$).
- **Logistic Regression Classifier**: Predicts binary pass/fail probability ($> 88\%$ accuracy).
- **XGBoost Classifier**: Multi-class dropout/academic probation risk classifier (`LOW`, `MEDIUM`, `HIGH`).
- **SHAP Feature Attribution**: Explains individual score impacts (e.g. attendance rate, internal marks, credit burden).

### 4. Enterprise Reporting & Security
- **Export Engine**: Generates styled Excel workbooks (`.xlsx`) via `openpyxl` and formal PDF transcripts via `WeasyPrint`.
- **Security**: Flask-Login role-based access control, PBKDF2 password hashing, SQL injection prevention via SQLAlchemy ORM, and compliance audit logs.

---

## 🏛️ Architecture & File Structure

```
student_performance_tracker/
├── app/
│   ├── __init__.py                  # Package initializer
│   ├── config.py                    # Environment & configuration settings
│   ├── main.py                      # Dash app entry point (server = Flask(__name__))
│   ├── auth.py                      # Flask-Login auth manager & RBAC decorators
│   ├── database.py                  # SQLAlchemy ORM models (User, Student, Course, etc.)
│   ├── callbacks.py                 # Multi-page routing, filtering & chart callbacks
│   ├── utils.py                     # SGPA/CGPA math, Excel/PDF generators, alerts
│   ├── ml_models/
│   │   ├── __init__.py
│   │   ├── train_models.py          # ML training pipeline with 5-fold cross-validation
│   │   ├── predict.py               # Inference engine, SHAP attribution, study roadmaps
│   │   └── models/                  # Exported .pkl model artifacts
│   └── dashboards/
│       ├── __init__.py
│       ├── components.py            # Reusable UI cards, KPI indicators, navbar, badges
│       ├── student_dashboard.py     # Student view layout
│       ├── faculty_dashboard.py     # Faculty view layout
│       └── admin_dashboard.py       # Admin view layout
├── data/
│   ├── sample_data.sql              # SQL seed script with 1000+ students & 8 semesters
│   ├── generate_seed_data.py        # Synthetic data generation engine
│   └── sample_csv/                  # CSV datasets for bulk imports
├── docker/
│   ├── Dockerfile                   # Python 3.11 + Pango/Cairo + PostgreSQL dependencies
│   └── docker-compose.yml           # PostgreSQL 16 + Web App multi-service compose
├── tests/
│   └── test_platform.py             # Automated test suite
├── docs/
│   ├── installation.md              # Installation guide
│   ├── user_manual.md               # User manual for all 3 personas
│   └── api_reference.md             # API & ORM reference
├── requirements.txt                 # Pinned dependencies
├── .env.example                     # Environment template
└── README.md                        # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Local Run
```bash
# Clone & Navigate
git clone https://github.com/your-org/student-performance-tracker.git
cd student-performance-tracker

# Setup Environment
python -m venv venv
source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

# Seed Database & Train Models
python data/generate_seed_data.py
python app/ml_models/train_models.py

# Run Tests
python -m unittest tests/test_platform.py -v

# Launch Platform
python app/main.py
```
Visit `http://127.0.0.1:8050` in your web browser.

### 2. Docker Compose (1-Command Production Setup)
```bash
cd docker
docker-compose up --build -d
```

---

## 🔐 Default Demo Accounts

| Role | Username | Password | Direct Path |
|---|---|---|---|
| 👩‍🎓 **Student** | `student_demo` | `Student@123` | `/student` |
| 👨‍🏫 **Faculty** | `faculty_demo` | `Faculty@123` | `/faculty` |
| 🏛️ **Admin** | `admin_demo` | `Admin@123` | `/admin` |

---

## 🧪 Testing & Verification

Run the comprehensive test suite:
```bash
python -m unittest tests/test_platform.py -v
```
All unit tests verify:
- ✅ Accurate 10-point grade mappings & SGPA/CGPA formulas
- ✅ Role-based authentication & password verification
- ✅ ML training metrics ($>85\%$ accuracy on 5-fold cross-validation)
- ✅ Inference & personalized study roadmap generation
- ✅ Excel (`openpyxl`) and PDF report output streams
