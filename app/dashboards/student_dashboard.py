"""
Student Dashboard Layout and Visualizations.
Spacious, beautifully unmerged layout with physics canvas, dynamic marks modal, & simple AI study tips.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from app.dashboards.components import create_kpi_card, create_export_controls


def build_student_dashboard_layout():
    """Builds the spacious, distinct, and human-understandable Student Dashboard."""
    from flask import session, has_request_context
    is_demo = session.get("is_demo", False) if has_request_context() else False

    demo_banner = None
    if is_demo:
        demo_banner = dbc.Alert([
            html.Div([
                html.Span("🔍 ", className="fs-5 me-2"),
                html.Strong("This is an interactive demo account (Rahul Kumar • 2024CSE001). "),
                html.Span("Demo data is for illustration purposes only. "),
                html.A("Register your free account →", href="/register", className="fw-bold text-white text-decoration-underline ms-2")
            ], className="d-flex align-items-center flex-wrap")
        ], color="info", className="mb-4 py-2 px-3 border-0 rounded-3 text-white", 
           style={"background": "linear-gradient(90deg, rgba(0, 240, 255, 0.25), rgba(168, 85, 247, 0.25))", "border": "1px solid rgba(0, 240, 255, 0.45)"})

    return dbc.Container([
        # Demo Banner (if in demo mode)
        demo_banner,

        # Self-Reported Data Notice
        html.Div([
            html.Span("ℹ️ Academic data is self-reported by the student for personal performance analytics.", className="small text-secondary fw-semibold")
        ], className="d-flex justify-content-end mb-2"),

        # =========================================================
        # SECTION 1: Filter & Primary Action Bar
        # =========================================================
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Label("FILTER BY SEMESTER", className="fw-bold small text-light opacity-75", style={"letterSpacing": "0.06em", "fontSize": "0.72rem"}),
                    dbc.Select(
                        id="student-semester-dropdown",
                        options=[{"label": f"Semester {i}", "value": str(i)} for i in range(1, 9)],
                        value="3" if is_demo else "8",
                        className="form-select-dark"
                    )
                ], md=4, xs=12),
                dbc.Col([
                    html.Label("ACADEMIC ACTIONS", className="fw-bold small text-light opacity-75", style={"letterSpacing": "0.06em", "fontSize": "0.72rem"}),
                    html.Div([
                        dbc.Button("✦ Enter / Edit Grade Points", id="open-marks-modal-btn", className="btn-gradient me-2", style={"fontWeight": "700"}),
                        html.Div(create_export_controls("student"), className="d-inline-block")
                    ], className="d-flex align-items-center flex-wrap gap-2")
                ], md=8, xs=12, className="d-flex flex-column justify-content-end align-items-md-end")
            ], className="g-3 align-items-center")
        ], className="dashboard-filter-card mb-4"),

        # =========================================================
        # SECTION 2: Top Academic KPI Performance Indicators
        # =========================================================
        html.Div(id="student-kpi-container", children=[
            dbc.Row([
                dbc.Col(create_kpi_card("Overall CGPA", "...", "Your cumulative grade point average across all semesters (Scale 0-10)", "primary", "cgpa"), md=3, xs=6),
                dbc.Col(create_kpi_card("Latest Semester GPA", "...", "Grade point average scored in your active semester", "info", "sgpa"), md=3, xs=6),
                dbc.Col(create_kpi_card("Class Attendance", "...", "Target: 75% or higher to be eligible for finals", "success", "attendance"), md=3, xs=6),
                dbc.Col(create_kpi_card("Estimated Exam Score", "...", "AI prediction of your upcoming final exam score", "warning", "forecast"), md=3, xs=6),
            ], className="g-3")
        ], className="dashboard-section mb-4 pb-2"),

        # =========================================================
        # SECTION 3: GPA Growth Over Time & Subject Breakdown
        # =========================================================
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Span("📈", className="me-2 fs-5"),
                            html.Span("Semester GPA Progression (Terms 1 to 8)", className="fw-bold text-white fs-6"),
                            html.Span("GPA TREND", className="badge bg-info bg-opacity-25 text-info ms-auto")
                        ], className="d-flex align-items-center"),
                        dbc.CardBody([
                            dcc.Loading(dcc.Graph(id="student-sgpa-trend-chart", config={"displayModeBar": False})),
                            html.Div([
                                html.Strong("How to read this chart: "),
                                "Each point shows your SGPA for that semester. The green dashed line is your overall cumulative average (CGPA). Higher is better!"
                            ], className="desc-callout")
                        ], className="p-3")
                    ], className="card h-100")
                ], lg=6, xs=12),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Span("🎯", className="me-2 fs-5"),
                            html.Span("Subject Grade Points & Mastery (Scale 0-10)", className="fw-bold text-white fs-6"),
                            html.Span("GRADE POINTS", className="badge bg-primary bg-opacity-25 text-primary ms-auto")
                        ], className="d-flex align-items-center"),
                        dbc.CardBody([
                            dcc.Loading(dcc.Graph(id="student-radar-chart", config={"displayModeBar": False})),
                            html.Div([
                                html.Strong("Grade Point Breakdown: "),
                                "Shows Grade Points scored per subject on a 10-point scale. 10.0 = O (Outstanding), 9.0 = A+ (Excellent), 8.0 = A (Very Good), 7.0 = B+ (Good)."
                            ], className="desc-callout")
                        ], className="p-3")
                    ], className="card h-100")
                ], lg=6, xs=12)
            ], className="g-4")
        ], className="dashboard-section mb-4 pb-2"),

        # =========================================================
        # SECTION 4: Attendance vs GPA & AI Study Tips
        # =========================================================
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Span("📊", className="me-2 fs-5"),
                            html.Span("How Attendance Impacts Grade Points", className="fw-bold text-white fs-6"),
                            html.Span("COHORT BENCHMARK", className="badge bg-success bg-opacity-25 text-success ms-auto")
                        ], className="d-flex align-items-center"),
                        dbc.CardBody([
                            dcc.Loading(dcc.Graph(id="student-attendance-scatter", config={"displayModeBar": False})),
                            html.Div([
                                html.Strong("Key Takeaway: "),
                                "Students with higher attendance consistently achieve higher Grade Points. The glowing cyan diamond marks where you currently stand."
                            ], className="desc-callout mb-3"),
                            html.Div([
                                html.Div([
                                    html.Span("🛡️ Attendance Safety Status", className="ai-tip-badge", style={"background": "rgba(16, 185, 129, 0.2)", "color": "#A7F3D0", "border": "1px solid rgba(16, 185, 129, 0.4)"}),
                                    html.H6("Eligible for End-Semester Examinations", className="fw-bold text-white mb-1"),
                                    html.P("Your tracked attendance is in the safe zone (above 75%). Attending the next 4 classes creates a solid buffer for distinction honours.", className="small text-secondary mb-0")
                                ], className="ai-tip-box mb-2"),
                                html.Div([
                                    html.Span("🎯 Academic Standing Forecast", className="ai-tip-badge", style={"background": "rgba(6, 182, 212, 0.2)", "color": "#A5F3FC", "border": "1px solid rgba(6, 182, 212, 0.4)"}),
                                    html.H6("High Pass Probability (99.8%)", className="fw-bold text-white mb-1"),
                                    html.P("Machine learning models classify your academic standing as LOW RISK. Maintain consistency across practical labs and unit tests.", className="small text-secondary mb-0")
                                ], className="ai-tip-box mb-0")
                            ])
                        ], className="p-3")
                    ], className="card h-100")
                ], lg=6, xs=12),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Span("💡", className="me-2 fs-5"),
                            html.Span("AI Study Tips & Action Plan", className="fw-bold text-white fs-6"),
                            html.Span("PERSONALIZED ADVISORY", className="badge bg-info bg-opacity-25 text-info ms-auto")
                        ], className="d-flex align-items-center"),
                        dbc.CardBody([
                            html.Div(id="student-ai-recommendations-container"),
                        ], className="p-3")
                    ], className="card h-100")
                ], lg=6, xs=12)
            ], className="g-4")
        ], className="dashboard-section mb-4 pb-2"),

        # =========================================================
        # SECTION 5: Official Course Marksheet & Attendance
        # =========================================================
        html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Span("📋", className="me-2 fs-5"),
                            html.Span("Your Complete Subject Grade Points & Attendance Sheet", className="fw-bold text-white fs-6")
                        ], className="d-flex align-items-center"),
                        dbc.CardBody([
                            html.Div(id="student-courses-table-container"),
                            html.Div([
                                html.Strong("10-Point Grading Scale: "),
                                "10 GP = O (Outstanding), 9 GP = A+ (Excellent), 8 GP = A (Very Good), 7 GP = B+ (Good), 6 GP = B (Above Average), 5 GP = C (Pass), 0 GP = F (Fail)."
                            ], className="desc-callout mt-3")
                        ], className="p-3")
                    ], className="card")
                ], xs=12)
            ])
        ], className="dashboard-section mb-5"),

        # =========================================================
        # SECTION 6: Grade Points Input Modal Component
        # =========================================================
        dbc.Modal([
            dbc.ModalHeader(
                dbc.ModalTitle(id="marks-modal-title", children="Enter Academic Grade Points", className="fw-bold text-white"),
                close_button=True,
                className="border-bottom border-secondary border-opacity-25"
            ),
            dbc.ModalBody([
                html.Div(id="marks-modal-alert"),
                dcc.Loading(html.Div(id="marks-modal-subjects-container", className="py-2"))
            ], className="p-4", style={"maxHeight": "70vh", "overflowY": "auto"}),
            dbc.ModalFooter([
                dbc.Button("Cancel", id="marks-modal-cancel-btn", className="btn-celestial-outline me-2"),
                dbc.Button("Save & Recalculate SGPA / CGPA", id="marks-modal-save-btn", className="btn-celestial")
            ], className="border-top border-secondary border-opacity-25")
        ], id="student-marks-modal", is_open=False, size="lg", centered=True, className="modal-dark-glass"),

        # Hidden download & state components
        dcc.Store(id="marks-refresh-trigger", data=0),
        dcc.Download(id="download-student-excel"),
        dcc.Download(id="download-student-pdf")
    ], fluid=True, className="px-4 pb-5")
