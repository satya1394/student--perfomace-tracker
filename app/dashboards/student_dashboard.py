"""
Student Dashboard Layout and Visualizations for StudIQ.
Provides Cascading 6-Field Academic Selection, Curriculum Confirmation Card,
Simple Line & Bar Charts (SGPA Progression, Subject Performance Bar Chart, Attendance Bar Chart with 75% line),
and Verified/Estimated/Incomplete SGPA calculation status.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from app.dashboards.components import create_kpi_card, create_export_controls


def build_student_dashboard_layout():
    """Builds the clean, simple, and human-understandable Student Dashboard."""
    from flask import session, has_request_context
    
    is_demo = session.get("is_demo", False) if has_request_context() else False
    def_college = session.get("college_name", "Raghu Engineering College") if has_request_context() else "Raghu Engineering College"
    def_degree = session.get("degree", "B.Tech") if has_request_context() else "B.Tech"
    def_reg = session.get("regulation_name", "AR23") if has_request_context() else "AR23"
    def_branch = session.get("branch_name", "CSE") if has_request_context() else "CSE"
    def_spec = session.get("specialization", "Core Computer Science") if has_request_context() else "Core Computer Science"
    def_sem = str(session.get("active_semester", 3)) if has_request_context() else "3"

    demo_banner = None
    if is_demo:
        demo_banner = dbc.Alert([
            html.Div([
                html.Span("🔍 ", className="fs-5 me-2"),
                html.Strong("Interactive Demo Mode: "),
                html.Span("Currently logged in as Rahul Kumar (STU2024001 • Raghu Engineering College • AR23 Core CSE Sem 3). "),
                html.A("Register your personal student account →", href="/register", className="fw-bold text-white text-decoration-underline ms-2")
            ], className="d-flex align-items-center flex-wrap")
        ], color="info", className="mb-4 py-2 px-3 border-0 rounded-3 text-white", 
           style={"background": "linear-gradient(90deg, rgba(0, 240, 255, 0.25), rgba(168, 85, 247, 0.25))", "border": "1px solid rgba(0, 240, 255, 0.45)"})

    return dbc.Container([
        # Demo Banner
        demo_banner,

        # Self-Reported Notice
        html.Div([
            html.Span("ℹ️ Academic marks & elective selections are student self-reported for official curriculum tracking.", className="small text-secondary fw-semibold")
        ], className="d-flex justify-content-end mb-2"),

        # =========================================================
        # SECTION 1: Cascading 6-Tier Academic Selection Bar
        # =========================================================
        html.Div([
            html.Div([
                html.Span("🎓", className="me-2 fs-5"),
                html.Span("Exact Academic Curriculum Identification", className="fw-bold text-white fs-6"),
                html.Span("CASCADING SELECTION", className="badge bg-primary bg-opacity-25 text-primary ms-auto")
            ], className="d-flex align-items-center mb-3 pb-2 border-bottom border-secondary border-opacity-25"),

            dbc.Row([
                # 1. College
                dbc.Col([
                    html.Label("1. COLLEGE / INSTITUTION", className="fw-bold small text-light opacity-75", style={"fontSize": "0.72rem"}),
                    dbc.Select(
                        id="curriculum-college-select",
                        options=[
                            {"label": "Raghu Engineering College (Autonomous)", "value": "Raghu Engineering College"},
                            {"label": "+ Custom / Other College (Manual Mode)", "value": "Custom College"}
                        ],
                        value=def_college,
                        className="form-select-dark"
                    )
                ], lg=3, md=6, xs=12),

                # 2. Degree
                dbc.Col([
                    html.Label("2. DEGREE", className="fw-bold small text-light opacity-75", style={"fontSize": "0.72rem"}),
                    dbc.Select(
                        id="curriculum-degree-select",
                        options=[{"label": "B.Tech", "value": "B.Tech"}],
                        value=def_degree,
                        className="form-select-dark"
                    )
                ], lg=2, md=6, xs=12),

                # 3. Regulation
                dbc.Col([
                    html.Label("3. REGULATION", className="fw-bold small text-light opacity-75", style={"fontSize": "0.72rem"}),
                    dbc.Select(
                        id="curriculum-regulation-select",
                        options=[
                            {"label": "AR23 (Autonomous 2023)", "value": "AR23"},
                            {"label": "AR20 (Autonomous 2020)", "value": "AR20"}
                        ],
                        value=def_reg,
                        className="form-select-dark"
                    )
                ], lg=2, md=6, xs=12),

                # 4. Branch
                dbc.Col([
                    html.Label("4. BRANCH", className="fw-bold small text-light opacity-75", style={"fontSize": "0.72rem"}),
                    dbc.Select(
                        id="curriculum-branch-select",
                        options=[
                            {"label": "CSE (Computer Science)", "value": "CSE"},
                            {"label": "ECE (Electronics & Comm)", "value": "ECE"},
                            {"label": "EEE (Electrical & Electronics)", "value": "EEE"},
                            {"label": "MECH (Mechanical Engg)", "value": "MECH"},
                            {"label": "CIVIL (Civil Engg)", "value": "CIVIL"}
                        ],
                        value=def_branch,
                        className="form-select-dark"
                    )
                ], lg=2, md=6, xs=12),

                # 5. Specialization
                dbc.Col([
                    html.Label("5. SPECIALIZATION", className="fw-bold small text-light opacity-75", style={"fontSize": "0.72rem"}),
                    dbc.Select(
                        id="curriculum-spec-select",
                        options=[
                            {"label": "Core Computer Science", "value": "Core Computer Science"},
                            {"label": "AI & ML", "value": "AI & ML"},
                            {"label": "Data Science", "value": "Data Science"},
                            {"label": "Cyber Security", "value": "Cyber Security"},
                            {"label": "IoT & Blockchain", "value": "IoT & Blockchain"}
                        ],
                        value=def_spec,
                        className="form-select-dark"
                    )
                ], lg=3, md=12, xs=12),
            ], className="g-3 mb-3"),

            dbc.Row([
                # 6. Semester
                dbc.Col([
                    html.Label("6. ACTIVE SEMESTER", className="fw-bold small text-light opacity-75", style={"fontSize": "0.72rem"}),
                    dbc.Select(
                        id="student-semester-dropdown",
                        options=[{"label": f"Semester {i}", "value": str(i)} for i in range(1, 9)],
                        value=def_sem,
                        className="form-select-dark"
                    )
                ], lg=3, md=4, xs=12),

                # Action Buttons
                dbc.Col([
                    html.Label("ELECTIVES & MARKS ACTIONS", className="fw-bold small text-light opacity-75", style={"fontSize": "0.72rem"}),
                    html.Div([
                        dbc.Button("✦ Enter / Edit Marks & Grades", id="open-marks-modal-btn", className="btn-gradient", style={"fontWeight": "700"}),
                        dbc.Button("+ Professional Elective", id="open-elective-modal-btn", className="btn-celestial-outline", size="sm"),
                        dbc.Button("+ Open Elective", id="open-open-elective-modal-btn", className="btn-celestial-outline", size="sm"),
                        dbc.Button("+ Honors / Minors", id="open-honors-modal-btn", className="btn-celestial-outline", size="sm"),
                        html.Div(create_export_controls("student"), className="d-inline-block")
                    ], className="d-flex align-items-center flex-wrap gap-2")
                ], lg=9, md=8, xs=12, className="d-flex flex-column justify-content-end")
            ], className="g-3 align-items-center")
        ], className="dashboard-filter-card mb-4"),

        # =========================================================
        # SECTION 2: Curriculum Confirmation Banner & Calculation Status
        # =========================================================
        html.Div(id="curriculum-confirmation-banner", className="mb-4"),

        # =========================================================
        # SECTION 3: Top Academic KPI Performance Indicators
        # =========================================================
        html.Div(id="student-kpi-container", children=[
            dbc.Row([
                dbc.Col(create_kpi_card("Overall CGPA", "...", "Cumulative grade points across completed semesters (Scale 0-10)", "primary", "cgpa"), md=3, xs=6),
                dbc.Col(create_kpi_card("Active Term SGPA", "...", "Grade point average for this exact curriculum semester", "info", "sgpa"), md=3, xs=6),
                dbc.Col(create_kpi_card("Class Attendance", "...", "Target: >= 75% for examination hall ticket eligibility", "success", "attendance"), md=3, xs=6),
                dbc.Col(create_kpi_card("Total Credits Tracked", "...", "Sum of verified official and student-entered credits", "warning", "forecast"), md=3, xs=6),
            ], className="g-3")
        ], className="dashboard-section mb-4 pb-2"),

        # =========================================================
        # SECTION 4: Simple Visualizations (Line Chart & Bar Charts)
        # =========================================================
        html.Div([
            dbc.Row([
                # 1. Simple Line Chart: SGPA Progression
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Span("📈", className="me-2 fs-5"),
                            html.Span("SGPA & CGPA Progression", className="fw-bold text-white fs-6"),
                            html.Span("SEMESTER TREND", className="badge bg-info bg-opacity-25 text-info ms-auto")
                        ], className="d-flex align-items-center"),
                        dbc.CardBody([
                            dcc.Loading(dcc.Graph(id="student-sgpa-trend-chart", config={"displayModeBar": False})),
                            html.Div([
                                html.Strong("Progression Trend: "),
                                "Cyan line shows term SGPA across semesters; green dashed line indicates overall CGPA average."
                            ], className="desc-callout")
                        ], className="p-3")
                    ], className="card h-100")
                ], lg=6, xs=12),

                # 2. Simple Bar Chart: Subject Grade Points
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Span("📊", className="me-2 fs-5"),
                            html.Span("Subject Grade Points Breakdown", className="fw-bold text-white fs-6"),
                            html.Span("SUBJECT PERFORMANCE", className="badge bg-primary bg-opacity-25 text-primary ms-auto")
                        ], className="d-flex align-items-center"),
                        dbc.CardBody([
                            dcc.Loading(dcc.Graph(id="student-radar-chart", config={"displayModeBar": False})),
                            html.Div([
                                html.Strong("10-Point Scale: "),
                                "10 = O (Outstanding), 9 = A+ (Excellent), 8 = A (Very Good), 7 = B+ (Good), 6 = B (Above Avg), 5 = C (Pass), 0 = F (Fail)."
                            ], className="desc-callout")
                        ], className="p-3")
                    ], className="card h-100")
                ], lg=6, xs=12)
            ], className="g-4 mb-4"),

            dbc.Row([
                # 3. Simple Bar Chart: Attendance Breakdown with 75% Threshold Line
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Span("📋", className="me-2 fs-5"),
                            html.Span("Subject Attendance & 75% Threshold", className="fw-bold text-white fs-6"),
                            html.Span("ATTENDANCE", className="badge bg-success bg-opacity-25 text-success ms-auto")
                        ], className="d-flex align-items-center"),
                        dbc.CardBody([
                            dcc.Loading(dcc.Graph(id="student-attendance-scatter", config={"displayModeBar": False})),
                            html.Div([
                                html.Strong("Attendance Policy: "),
                                "Green bars show your attendance % per course. The amber dashed line marks the 75% university examination minimum."
                            ], className="desc-callout mb-0")
                        ], className="p-3")
                    ], className="card h-100")
                ], lg=6, xs=12),

                # 4. Action Plan / Advisory
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Span("💡", className="me-2 fs-5"),
                            html.Span("Curriculum Mastery & Action Plan", className="fw-bold text-white fs-6"),
                            html.Span("AI ADVISORY", className="badge bg-info bg-opacity-25 text-info ms-auto")
                        ], className="d-flex align-items-center"),
                        dbc.CardBody([
                            html.Div(id="student-ai-recommendations-container"),
                        ], className="p-3")
                    ], className="card h-100")
                ], lg=6, xs=12)
            ], className="g-4")
        ], className="dashboard-section mb-4 pb-2"),

        # =========================================================
        # SECTION 5: Official Marksheet & Subject Roster Table
        # =========================================================
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Span("📋", className="me-2 fs-5"),
                            html.Span("Semester Subject Performance & Verified Marksheet", className="fw-bold text-white fs-6")
                        ], className="d-flex align-items-center"),
                        dbc.CardBody([
                            html.Div(id="student-courses-table-container"),
                        ], className="p-3")
                    ], className="card")
                ], xs=12)
            ])
        ], className="dashboard-section mb-5"),

        # =========================================================
        # SECTION 6: Grade Points Entry Modal
        # =========================================================
        dbc.Modal([
            dbc.ModalHeader(
                dbc.ModalTitle(id="marks-modal-title", children="Enter / Edit Academic Grade Points", className="fw-bold text-white"),
                close_button=True,
                className="border-bottom border-secondary border-opacity-25"
            ),
            dbc.ModalBody([
                html.Div(id="marks-modal-alert"),
                dcc.Loading(html.Div(id="marks-modal-subjects-container", className="py-2")),
            ], className="p-4", style={"maxHeight": "70vh", "overflowY": "auto"}),
            dbc.ModalFooter([
                dbc.Button("Cancel", id="marks-modal-cancel-btn", className="btn-celestial-outline me-2"),
                dbc.Button("Save & Recalculate SGPA / CGPA", id="marks-modal-save-btn", className="btn-gradient")
            ], className="border-top border-secondary border-opacity-25")
        ], id="student-marks-modal", is_open=False, size="lg", centered=True, className="modal-dark-glass"),

        # =========================================================
        # SECTION 7: Electives, Honors & Minors Selection Modal
        # =========================================================
        dbc.Modal([
            dbc.ModalHeader(
                dbc.ModalTitle(id="elective-modal-title", children="Select Curriculum Elective / Honor Track", className="fw-bold text-white"),
                close_button=True,
                className="border-bottom border-secondary border-opacity-25"
            ),
            dbc.ModalBody([
                html.Div(id="elective-modal-alert"),
                dcc.Loading(html.Div(id="elective-modal-options-container", className="py-2")),
            ], className="p-4", style={"maxHeight": "70vh", "overflowY": "auto"}),
            dbc.ModalFooter([
                dbc.Button("Cancel", id="elective-modal-cancel-btn", className="btn-celestial-outline me-2"),
                dbc.Button("Confirm & Add to Marksheet", id="elective-modal-save-btn", className="btn-gradient")
            ], className="border-top border-secondary border-opacity-25")
        ], id="student-elective-modal", is_open=False, size="lg", centered=True, className="modal-dark-glass"),

        # Hidden download & state triggers
        dcc.Store(id="marks-refresh-trigger", data=0),
        dcc.Store(id="current-elective-modal-category", data="PROFESSIONAL_ELECTIVE"),
        dcc.Download(id="download-student-excel"),
        dcc.Download(id="download-student-pdf")
    ], fluid=True, className="px-4 pb-5")
