# User Manual & Feature Walkthrough

This manual explains how to interact with the three personas available on the **EduPulse Academic Performance Analytics Platform**.

---

## 1. Student Dashboard (`/student`)

The Student Dashboard gives learners a comprehensive overview of their academic journey.

### Key Visualizations & Features
- **Dynamic KPI Tiles**: Displays real-time Cumulative CGPA, Latest SGPA, Attendance %, and ML-predicted final score.
- **SGPA Progression Curve**: Interactive line chart showing semester-by-semester SGPA changes against the overall CGPA benchmark line.
- **Competency Radar**: Visualizes marks distribution across enrolled subjects in a spider/radar geometry.
- **Attendance vs. Marks Correlation**: Shows where the student's attendance & marks sit relative to the department cohort.
- **AI-Powered Study Roadmap**: Generates personalized topic priorities and remedial suggestions based on SHAP feature attributions.
- **One-Click Export**: Download official grade sheets in styled Excel (`.xlsx`) or PDF.

---

## 2. Faculty Dashboard (`/faculty`)

The Faculty Dashboard provides educators with early warning systems and cohort management tools.

### Key Visualizations & Features
- **Class-wide Health KPIs**: Batch average CGPA, pass rates, at-risk student headcount, and class attendance averages.
- **Department & Semester Heatmap**: Heatmap displaying average marks across curriculum departments and semesters.
- **Grade Distribution Histogram**: Interactive multi-color histogram categorizing grades (O, A+, A, B+, B, C, P, F).
- **Early Warning At-Risk Table**: Flags students with $< 65\%$ attendance or $< 45\%$ marks 4-6 weeks before exams.
- **Automated Email Alerts**: 1-click trigger to dispatch academic deficiency notices.

---

## 3. Administrator Dashboard (`/admin`)

The Admin Dashboard provides institutional governance, accreditation tracking, and compliance metrics.

### Key Visualizations & Features
- **Institutional Governance KPIs**: Total student headcount, institute-wide average CGPA, retention rates, and accreditation compliance index.
- **Department Benchmarking**: Comparative bar charts of average performance across Engineering departments.
- **Cohort Retention Trends**: Longitudinal analysis of retention across academic years.
- **Compliance Audit Trail**: Real-time log table monitoring user authentication events, grade alterations, and prediction events.
