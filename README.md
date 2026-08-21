# ⚡ StudIQ: Student Academic Performance & Curriculum Tracking Platform

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11+-111827?style=flat-square&logo=python&logoColor=3776AB)](https://www.python.org/)

[![Plotly Dash](https://img.shields.io/badge/Plotly%20Dash-2.18+-111827?style=flat-square&logo=plotly&logoColor=00C2FF)](https://dash.plotly.com/)

[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20SQLAlchemy-111827?style=flat-square&logo=sqlite&logoColor=8B5CF6)](https://www.sqlalchemy.org/)

[![License](https://img.shields.io/badge/License-MIT-111827?style=flat-square&logo=opensourceinitiative&logoColor=FACC15)](https://opensource.org/licenses/MIT)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20StudIQ-111827?style=flat-square&logo=googlechrome&logoColor=22C55E)](https://student-perfomace-tracker.onrender.com/)

**StudIQ** is a modern, student-centric academic performance tracker and exact curriculum management platform. Designed exclusively as a **Student Self-Service Platform**, StudIQ eliminates generic estimation by resolving subjects through an exact 6-parameter academic path, enforcing regulation boundaries, managing elective and honors pools, calculating verified SGPA/CGPA with audit course exclusions, and delivering intuitive, presentation-ready visual analytics.

---

## 🌟 Key Platform Capabilities

### 1. Exact 6-Tier Cascading Academic Resolution
StudIQ does not guess subjects from branch names alone. Academic curricula are identified through a deterministic 6-tier hierarchy:
$$\text{College} \longrightarrow \text{Degree} \longrightarrow \text{Regulation} \longrightarrow \text{Branch} \longrightarrow \text{Specialization} \longrightarrow \text{Semester}$$

- **Strict Regulation Separation**: Never merges or confuses **AR23** and **AR20** structures.
- **Branch & Department Isolation**: Full distinction between CSE Core, CSE AI & ML, CSE Data Science, CSE Cyber Security, CSE IoT & Blockchain, ECE (VLSI & Embedded Systems), EEE (Power Systems & Automation), MECH (Design & Manufacturing), and CIVIL (Structural Engineering).
- **Official Master Dataset**: Pre-compiled with **1,123 verified course records** across Semesters 1 to 8 from **Raghu Engineering College (Autonomous)**.

---

### 2. Verified vs. Estimated vs. Incomplete SGPA Engine
Calculates semester grade point average with strict credit accounting:
$$\text{SGPA} = \frac{\sum (\text{Grade Point}_i \times \text{Credits Used}_i)}{\sum \text{Credits Used}_i}$$

- **Zero-Credit Audit Exclusion**: Non-credit and audit mandatory courses (e.g. *23MC601 Environmental Science*, Induction Programs) are automatically excluded from the SGPA divisor.
- **Auditability & Status Tagging**:
  - `VERIFIED_SGPA`: All credits are confirmed against the official university course structure.
  - `ESTIMATED_SGPA`: Flagged whenever custom/student-entered credits or manual mode are used.
  - `INCOMPLETE_SGPA`: Missing credits are highlighted without crashing calculations.

---

### 3. Dynamic Elective, Open Elective & Honors Management
- **Compact Elective Selector (`[✚ Add / Change Elective]`)**: Allows students to select, switch, or remove courses from official elective pools (e.g. *Professional Elective I* in Sem 5; *Professional Elective II & Open Elective I* in Sem 6).
- **Single-Course Selection Rule**: Enforces choosing at most 1 course per elective group, preventing accidental double-counting.
- **Dynamic Credit Sync**: Unselected electives do not appear in the active subject list and do not affect base credits; selecting an elective dynamically updates total tracked credits and SGPA.

---

### 4. Simple, Dark-Themed Visual Analytics

| Chart | Visualization Type | Key Details |
| :--- | :--- | :--- |
| **📈 SGPA & CGPA Progression** | Simple Line Chart | Solid **Cyan** line (`#00F0FF`) for term SGPA progression across completed semesters; dashed **Green** line (`#10B981`) for overall cumulative CGPA baseline. |
| **📊 Subject Performance** | Simple Bar Chart | Clean **Purple** bars (`#8B5CF6`) showing individual Grade Points (0.0–10.0 scale) per course code with readable tooltips. |
| **📋 Attendance Breakdown** | Simple Bar Chart | Clean **Green** bars (`#10B981`) with an **Amber dashed 75% reference line** (`#F59E0B`) marking university examination eligibility. |
| **💡 Curriculum Action Plan** | AI Advisory Panel | Real-time strengths and focus-area recommendations generated directly from active subject scores. |

> [!NOTE]
> All charts display standardized, user-friendly empty-state messages (e.g., *"Add semester grades to see your progress."*) whenever a semester has not yet had marks entered.

---

### 5. Marksheet Table & Export Engine
- **Active Subject Marksheet**: Displays Course Code, Subject Name, Type (Compulsory Theory, Lab, Skill Course, Elective), Credits, Verification Source, Marks, Grade Letter, Grade Point, and Attendance %.
- **Excel Export**: Generates styled `.xlsx` marksheets via `openpyxl` with a single click.

---

## 🏛️ Project Architecture & Directory Structure

```
student_performance_tracker/
├── app/
│   ├── __init__.py                  # Package initializer
│   ├── config.py                    # Environment and secret configuration
│   ├── main.py                      # Flask + Dash application entry point
│   ├── auth.py                      # Student authentication, session binding & demo seed
│   ├── database.py                  # SQLAlchemy ORM models (Curriculum, Subjects, Enrollments)
│   ├── curriculum_engine.py         # 6-tier academic resolution & SGPA calculation engine
│   ├── curriculum_loader.py         # CSV curriculum parser, validator & reporter
│   ├── callbacks.py                 # Dash reactive callbacks (Cascading filters, modals, charts)
│   ├── utils.py                     # Grade scales, math utilities & Excel exporter
│   └── dashboards/
│       ├── __init__.py
│       ├── components.py            # Bioluminescent KPI cards, dock navbar & export controls
│       └── student_dashboard.py     # Student self-service dashboard layout
├── data/
│   ├── official_curricula.csv       # 1,123 verified official course structure records
│   ├── sample_data.sql              # Standard SQL seed script
│   └── generate_seed_data.py        # Seed script generator
├── tests/
│   ├── test_curriculum_accuracy.py  # 11 unit tests for curriculum isolation & SGPA math
│   └── test_platform.py             # General platform validation tests
├── assets/                          # CSS stylesheets, themes, and animations
├── requirements.txt                 # Pinned project dependencies
└── README.md                        # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.10+** or **Python 3.11+**
- Recommended: A dedicated virtual environment (`venv` or `conda`)

### 2. Installation & Setup
```bash
# Clone the repository
git clone https://github.com/your-org/student-performance-tracker.git
cd student-performance-tracker

# Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Automated Tests
Verify curriculum accuracy, AR20/AR23 isolation, and SGPA calculation rules:
```bash
python -m unittest tests/test_curriculum_accuracy.py -v
```

### 4. Launch the Platform
```bash
python app/main.py
```
Open your browser and navigate to **`http://127.0.0.1:8050`**.

---

## 🔐 Default Demo Student Account

For instant testing, click **"Explore Interactive Demo"** on the hero landing page or sign in using:

| Parameter | Demo Value |
| :--- | :--- |
| **Username** | `rahulkumar` (or `demo_user`) |
| **Password** | `Student@123` |
| **Preloaded Curriculum** | Raghu Engineering College • B.Tech • AR23 • CSE (Core) • Semester 3 |
| **Direct URL** | `http://127.0.0.1:8050/demo-login` |

---

## 📋 Grade Point Mapping Reference

| Marks Range | Grade Letter | Grade Point | Performance Classification |
| :---: | :---: | :---: | :--- |
| **$\ge 90\%$** | **O** | **10.0** | Outstanding |
| **$80 - 89\%$** | **A+** | **9.0** | Excellent |
| **$70 - 79\%$** | **A** | **8.0** | Very Good |
| **$60 - 69\%$** | **B+** | **7.0** | Good |
| **$50 - 59\%$** | **B** | **6.0** | Above Average |
| **$40 - 49\%$** | **C** | **5.0** | Pass |
| **$< 40\%$** | **F** | **0.0** | Fail |

---

## 🛡️ Academic Integrity & Privacy
- **Student-Only Scope**: No faculty or administrator roles, access switches, or portals exist in this system.
- **Session Isolation**: Student marks and elective selections are strictly scoped to the logged-in student session and stored securely in SQLite with SQLAlchemy ORM.
- **Audit Logging**: Sensitive actions (logins, marks updates) are recorded in internal audit logs.

---

## 📄 License
This project is licensed under the **MIT License** — see the LICENSE file for details.
