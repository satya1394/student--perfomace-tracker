<div align="center">

# ⚡ StudIQ
### Operational Student Intelligence & Exact Curriculum Analytics Platform

[![Live Production](https://img.shields.io/badge/Production%20Live-student--perfomace--tracker.onrender.com-00F0FF?style=flat-square&logo=render&logoColor=000000)](https://student-perfomace-tracker.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Plotly Dash](https://img.shields.io/badge/Plotly%20Dash-3.0+-00C2FF?style=flat-square&logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-Production%20WSGI-499848?style=flat-square&logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20SQLAlchemy-8B5CF6?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-FACC15?style=flat-square&logo=opensourceinitiative&logoColor=black)](https://opensource.org/licenses/MIT)

**StudIQ** is a production-grade academic intelligence cockpit and deterministic curriculum resolution engine for autonomous engineering institutions.

[🚀 Explore Live Demo](https://student-perfomace-tracker.onrender.com/) • [📊 Launch Interactive Cockpit](/demo) • [📑 Report Issue](https://github.com/your-org/student-performance-tracker/issues)

</div>

---

## ⚡ Institutional Scale at a Glance

| Metric | Scope & Coverage |
| :--- | :--- |
| **🏛️ Affiliated Institution** | **Raghu Engineering College (Autonomous)** |
| **📚 Canonical Subjects** | **1,123 verified courses** across Semesters 1–8 |
| **📜 Regulations** | **AR23** & **AR20** (strictly isolated) |
| **🎯 Branch Specializations** | **21 tracks** across **CSE**, **ECE**, **EEE**, **MECH**, and **CIVIL** |
| **🎛️ Elective Pools** | **205 options** (Professional Electives, Open Electives, Honors, Minors) |

---

## 🌟 Core Highlights

- **🎯 6-Tier Cascading Resolution**: Deterministically resolves subjects via $\text{College} \to \text{Degree} \to \text{Regulation} \to \text{Branch} \to \text{Specialization} \to \text{Semester}$.
- **📊 Verified SGPA Engine**: Strict credit-weighted accounting with automatic exclusion of zero-credit audit courses (e.g. *Environmental Science*).
- **🎛️ Dynamic Elective Picker**: Single-course selection constraint per elective group with instant credit sync.
- **✨ Bioluminescent UI**: Dark-mode glassmorphic interface with glowing cyan/teal gradients and responsive chart layouts.
- **☁️ Zero-Config Cold Start**: Ephemeral-resilient bootstrapping automatically populates schema, branches, and 1,123 subjects on startup.

---

## 🌐 Application Route Map

| Path | View | Highlights |
| :--- | :--- | :--- |
| **`/`** & **`/app/`** | Public Hero Landing | Instant SaaS introduction, zero auth interception. |
| **`/demo`** | Interactive Demo Cockpit | Instant access as *Rahul Kumar* (AR23 CSE Sem 3) with preloaded marks. |
| **`/login`** / **`/register`** | Vesper Auth Portal | Pure-black video background authentication. |
| **`/app/overview`** | Student Overview | SGPA, CGPA, credit trackers, and performance metrics. |
| **`/app/analytics`** | Visual Analytics | SGPA progression line chart & subject score breakdowns. |
| **`/app/marks-subjects`** | Marksheet & Electives | Official transcript table, marks modal, and elective chooser. |
| **`/app/attendance`** | Attendance Monitor | Statutory 75% exam compliance tracker with glowing bar charts. |
| **`/app/academic-profile`** | Student Profile | 6-card verified academic credentials grid. |
| **`/app/settings`** | Account Settings | Clean flex-column session & sign-out controls. |

---

## 🛠️ Tech Stack

- **Backend & WSGI**: Python 3.10+, Flask 3.0+, Gunicorn 21.2+, Flask-Login (PBKDF2/SHA-256)
- **Frontend SPA**: Plotly Dash 3.0+, Dash Bootstrap Components, Tailwind CSS, Pure Black Vesper Dark Theme
- **Data & ORM**: SQLAlchemy 2.0+, SQLite 3, Pandas 2.2+, OpenPyXL (Excel Export)
- **ML / Predictive**: Scikit-Learn, XGBoost, SHAP explainability

---

## 🚀 Quickstart & Local Setup

```bash
# 1. Clone & enter repository
git clone https://github.com/your-username/student-performance-tracker.git
cd student-performance-tracker

# 2. Set up virtual environment & install dependencies
python -m venv venv
# Windows: .\venv\Scripts\activate | macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

# 3. Run automated tests (Optional)
python -m unittest tests/test_curriculum_accuracy.py -v

# 4. Launch local server
python app/main.py
# Server runs at http://127.0.0.1:8050
```

---

## ☁️ Zero-Config Cloud Deployment (Render)

StudIQ is pre-configured for instant deployment on **Render**, **Railway**, or containerized hosts:

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app.main:server --bind 0.0.0.0:$PORT`
- **Auto-Bootstrap**: On worker launch, `bootstrap_application()` runs `init_db()`, seeds all 21 branches, loads all 1,123 canonical subjects from `data/official_curricula.csv`, and provisions demo accounts—with zero manual database steps required.

---

## 📋 Grade Point Mapping Reference

| Marks Range | Grade | Point | Classification |
| :---: | :---: | :---: | :--- |
| **$\ge 90\%$** | **O** | **10.0** | Outstanding |
| **$80 - 89\%$** | **A+** | **9.0** | Excellent |
| **$70 - 79\%$** | **A** | **8.0** | Very Good |
| **$60 - 69\%$** | **B+** | **7.0** | Good |
| **$50 - 59\%$** | **B** | **6.0** | Above Average |
| **$40 - 49\%$** | **C** | **5.0** | Pass |
| **$< 40\%$** | **F** | **0.0** | Fail |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
