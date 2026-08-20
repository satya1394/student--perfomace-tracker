# 🎓 StudIQ

## 📊 Student Academic Performance Analytics Platform

<p align="center">
  <strong>Understand your academic performance. Plan your next best move.</strong>
</p>

<p align="center">
  A modern student self-service platform for tracking marks, attendance, SGPA, CGPA, and academic progress.
</p>

***

## 🛠️ Tech Stack











### Core Technologies

- 🐍 **Python** — Main programming language.
- ⚡ **Plotly Dash** — Interactive web dashboard.
- 🌶️ **Flask** — Backend server and routing.
- 🗄️ **SQLAlchemy and SQLite** — Database management and ORM.
- 🧠 **Scikit-learn, XGBoost, and SHAP** — Machine learning and explainable insights.
- 📊 **Plotly** — Interactive academic charts and visualizations.
- 🔐 **Flask-Login** — Student authentication and sessions.

***

## 🌟 About StudIQ

StudIQ is a modern student self-service academic analytics platform that transforms marks, credits, attendance, and academic history into clear, actionable insights.

Instead of relying on scattered spreadsheets or manual calculations, students can use StudIQ to understand their academic progress, calculate SGPA and CGPA, identify weaker subjects, and plan their next steps through an interactive dashboard.

> 💡 Built for students who want to track their progress, understand their performance, and stay ahead of their academic goals.

***

## ✨ Platform Features

### 🎨 Modern Landing Page

StudIQ includes a professional SaaS-inspired landing page featuring:

- 🌈 Modern glowing brand identity.
- 🧭 Clear navigation.
- 💎 Feature highlights.
- 🎮 Demo access.
- 🔐 Login and registration buttons.
- 🪄 A simple explanation of how the platform works.

### 🧪 Interactive Demo Mode

Visitors can explore StudIQ without creating an account.

Demo Mode automatically opens a sample student dashboard using pre-loaded academic data for Rahul Kumar.

It includes:

- 👨‍🎓 Sample student profile.
- 📚 Pre-loaded semester subjects.
- 📝 Example marks and attendance.
- 🧮 SGPA and CGPA results.
- 📊 Interactive charts.
- 🔍 Demo-account notice.
- 🔒 Read-only behavior for sample data.

### 📝 Student Registration

Students can create an account using their academic details:

1. 🏫 Select a college.
2. 📘 Select the applicable regulation.
3. 🎓 Select a branch.
4. 📅 Select a semester.
5. 🔑 Create login credentials.

The selected academic information is used to identify the correct subjects dynamically.

### 📋 Student Dashboard

The dashboard provides an organized view of a student’s academic journey, including:

- 📌 Current SGPA.
- 📈 Overall CGPA.
- 📚 Semester performance.
- 📝 Subject-wise marks.
- 🏆 Grade points.
- 🎯 Credit details.
- ✅ Attendance information.
- 📊 Performance charts.
- 🧠 Academic improvement suggestions.
- 🌱 Empty states for students who have not entered marks yet.

***

## 📐 Academic Calculations

StudIQ supports regulation-based academic calculations instead of applying one universal grading system.

### 🧮 SGPA

SGPA is calculated using credit-weighted grade points:

```text
SGPA = Σ(Grade Point × Credits) / Σ(Credits)
```

### 📊 CGPA

CGPA is calculated using credit-weighted performance across completed semesters:

```text
CGPA = Σ(Grade Point × Credits) / Σ(Credits)
```

### ⚙️ Regulation-Based Grade Rules

Grade mappings can vary between academic regulations. StudIQ stores these rules in the database so calculations can be adapted to the selected regulation.

Example grade rules may include:

| Grade | Grade Point |
|---|---:|
| S / O | 10 |
| A+ | 9 |
| A | 8 or 9 |
| B+ | 7 |
| B | 6 or 8 |
| C | 5 or 7 |
| F | 0 |

The exact mapping depends on the selected college regulation.

***

## 🤖 Intelligent Academic Insights

StudIQ is designed to support data-driven academic guidance.

Depending on the available data and configured models, the platform can support:

- 🔮 Exam score forecasting.
- ✅ Pass/fail prediction.
- 📚 Subject performance analysis.
- 📉 Attendance and marks comparison.
- 🔍 Feature-based academic explanations.
- 🗺️ Personalized study recommendations.

These insights are informational and are not a replacement for official academic evaluation or guidance from qualified academic staff.

***

## 📈 Interactive Visualizations

The dashboard uses interactive visualizations to make academic data easier to understand.

Visual insights may include:

- 📈 SGPA progression across semesters.
- 📚 Subject performance comparisons.
- 🔗 Marks and attendance relationships.
- 📊 Subject competency summaries.
- 📌 Academic trend indicators.

Interactive charts allow students to explore their own data instead of viewing only static tables.

***

## 🎓 Student-Only Platform

StudIQ currently operates as a student self-service application.

The current platform focuses exclusively on:

- 📝 Student registration.
- 🔐 Student login.
- 📚 Student academic data.
- 📊 Student dashboards.
- 🧠 Student performance analytics.

> 🚫 The current version does not include public Faculty or Administrator dashboards.

***

## 🧭 Application Routes

| Route | Purpose |
|---|---|
| `/` | 🏠 StudIQ landing page |
| `/demo` | 🧪 Interactive demo mode |
| `/login` | 🔐 Student login |
| `/register` | 📝 Student registration |
| `/dashboard` | 📊 Student academic dashboard |
| `/student` | 🎓 Alternative student dashboard route |

***

## 🏗️ Project Structure

```text
student_performance_tracker/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── callbacks.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── utils.py
│   ├── dashboards/
│   │   ├── __init__.py
│   │   ├── components.py
│   │   ├── hero_page.py
│   │   └── student_dashboard.py
│   └── ml_models/
│       ├── __init__.py
│       ├── predict.py
│       ├── train_models.py
│       └── models/
├── assets/
├── data/
│   ├── generate_seed_data.py
│   ├── sample_data.sql
│   └── sample_csv/
├── docs/
├── tests/
│   └── test_platform.py
├── docker/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

***

## 🚀 Quick Start

### 1️⃣ Clone the Repository

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git clone https://github.com/YOUR_USERNAME/student-performance-tracker.git
cd student-performance-tracker
```

### 2️⃣ Create a Virtual Environment

#### 🪟 Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### 🐧 macOS or Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a local `.env` file using `.env.example` as a reference.

> 🔒 Never commit passwords, API keys, secret keys, or other sensitive information to GitHub.

### 5️⃣ Initialize Sample Data

```bash
python data/generate_seed_data.py
```

### 6️⃣ Train Models, If Required

```bash
python app/ml_models/train_models.py
```

### 7️⃣ Start StudIQ

#### 🪟 Windows

```bash
python app\main.py
```

#### 🐧 macOS or Linux

```bash
python app/main.py
```

Open the application at:

```text
http://127.0.0.1:8050
```

***

## 🎮 Demo Account

Use the following account to explore the application:

```text
Username: demo_user
Password: demo123
Student: Rahul Kumar
College: Raghu Engineering College
Branch: CSE Data Science
Regulation: R23
Semester: 3
```

You can also access Demo Mode directly at:

```text
http://127.0.0.1:8050/demo
```

Demo data is provided for exploration and may be read-only.

***

## 🧪 Testing

Run the automated tests with:

```bash
python -m unittest tests/test_platform.py -v
```

Or:

```bash
pytest
```

The test suite may cover:

- ✅ Student registration.
- ✅ Login and password verification.
- ✅ Demo-mode authentication.
- ✅ Dynamic subject selection.
- ✅ Regulation-specific grade rules.
- ✅ SGPA and CGPA calculations.
- ✅ Academic data processing.
- ✅ Model prediction functions.
- ✅ Report generation.

***

## 🔒 Data and Security Notes

- 📝 Student academic information is self-reported.
- 🧪 Demo information is sample data.
- ⚠️ Predictions are informational and should not replace official academic decisions.
- 🗄️ Local databases may contain sensitive information.
- 🔑 Keep `.env` files outside version control.
- 🚫 Do not upload real student records to a public repository.
- 📦 Model-based predictions require trained model files and sufficient input data.

***

## 🗺️ Future Direction

StudIQ is an ongoing project. Future improvements may include:

- 🏫 More college and regulation templates.
- 📱 Improved mobile responsiveness.
- 🔮 Advanced academic forecasting.
- 🗺️ More detailed study roadmaps.
- 📄 Additional report formats.
- ☁️ Cloud deployment.
- ✅ Stronger data validation.
- 🧪 Expanded automated test coverage.

***

## 📌 Project Status

StudIQ is currently under active development.

The goal is to provide students with a simple, attractive, and intelligent way to understand their academic performance.

***

## 📄 License

This project is currently intended for educational and development purposes.

> 💙 Built for students, by students.

© 2026 StudIQ

