"""
StudIQ - Shared Authenticated Dashboard Shell (Frosted Liquid Glass Cockpit)
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from flask import session, has_request_context
from flask_login import current_user

from app.dashboards.pages.overview_page import build_overview_page
from app.dashboards.pages.analytics_page import build_analytics_page
from app.dashboards.pages.marks_subjects_page import build_marks_subjects_page
from app.dashboards.pages.attendance_page import build_attendance_page
from app.dashboards.pages.academic_profile_page import build_academic_profile_page
from app.dashboards.pages.settings_page import build_settings_page


def create_framer_navbar_with_active(active_path: str = "/overview"):
    """Generates the Framer Superellipse Liquid Glass Navbar."""
    is_demo = session.get("is_demo", False) if has_request_context() else False
    norm_path = active_path if active_path.startswith("/app") else f"/app{active_path}"

    tabs = [
        {"label": "Overview", "href": "/app/overview"},
        {"label": "Analytics", "href": "/app/analytics"},
        {"label": "Marks & Subjects", "href": "/app/marks-subjects"},
        {"label": "Attendance", "href": "/app/attendance"},
        {"label": "Academic Profile", "href": "/app/academic-profile"},
        {"label": "Settings", "href": "/app/settings"},
    ]

    tab_elements = []
    for tab in tabs:
        is_active = (norm_path == tab["href"]) or (tab["href"] == "/app/overview" and norm_path in ("/app", "/app/", "/student", "/dashboard"))
        tab_class = "framer-nav-link active" if is_active else "framer-nav-link"
        tab_elements.append(
            dcc.Link(tab["label"], href=tab["href"], className=tab_class)
        )

    return html.Div([
        html.Div([
            html.Div([
                # Left: Brand with Diamond Facet Gem
                html.A([
                    html.Div([
                        html.Div([
                            html.Div(className="framer-gem-facet")
                        ], className="framer-gem-body")
                    ], className="framer-gem-wrapper"),
                    html.Span([
                        html.Span("StudIQ", className="framer-brand-text"),
                        html.Span(".ai", className="framer-brand-suffix")
                    ])
                ], href="/", className="framer-nav-brand"),

                # Center: Navigation Links
                html.Div(tab_elements, className="framer-nav-links"),

                # Right: Liquid Glass CTA Button
                html.A(
                    "Exit Demo" if is_demo else "Sign Out",
                    href="/logout",
                    className="framer-glass-cta"
                )
            ], className="framer-liquid-glass-inner")
        ], className="framer-liquid-glass-nav")
    ], className="framer-navbar-outer-wrapper")


def create_stage_route_header(title_markup, subtitle: str, badge_text: str = "PAGE VIEW"):
    """Renders a clean page header with Instrument Serif italic accents."""
    return html.Div([
        html.Div([
            html.Div([
                html.H3(title_markup, className="cockpit-page-title mb-1"),
                html.P(subtitle, className="text-secondary small mb-0")
            ]),
            html.Span(badge_text, className="badge bg-secondary bg-opacity-50 text-white py-2 px-3 fw-semibold small mono-font")
        ], className="d-flex align-items-center justify-content-between flex-wrap py-2")
    ], className="cockpit-page-header")


def build_dashboard_shell(active_path: str = "/overview"):
    """
    Builds the clean, unified frosted liquid-glass dashboard shell.
    Automatically binds and persists branch, specialization, and regulation across all navigation tabs.
    """
    from app.database import get_db_session, Student
    from app.curriculum_engine import CurriculumEngine

    def_college = session.get("college_name") if has_request_context() else None
    def_degree = session.get("degree") if has_request_context() else None
    def_reg = session.get("regulation_name") if has_request_context() else None
    def_branch = session.get("branch_name") if has_request_context() else None
    def_spec = session.get("specialization") if has_request_context() else None
    def_sem = session.get("active_semester") if has_request_context() else None

    # Fallback to querying Student DB record if missing from session
    if (not def_branch or not def_spec or not def_reg) and current_user and current_user.is_authenticated:
        db = get_db_session()
        try:
            sid = current_user.student_id or current_user.username.upper()
            stu = db.query(Student).filter(Student.student_id == sid).first()
            if not stu and current_user.email:
                stu = db.query(Student).filter(Student.email == current_user.email).first()
            if stu:
                def_college = def_college or stu.college_name or "Raghu Engineering College"
                def_degree = def_degree or stu.degree or "B.Tech"
                def_reg = def_reg or stu.regulation_name or "AR23"
                def_branch = def_branch or stu.branch_name or "CSE"
                def_spec = def_spec or stu.specialization or "Core Computer Science"
                def_sem = def_sem or stu.current_semester or 3
                if has_request_context():
                    session["college_name"] = def_college
                    session["degree"] = def_degree
                    session["regulation_name"] = def_reg
                    session["branch_name"] = def_branch
                    session["specialization"] = def_spec
                    session["active_semester"] = def_sem
                    session["student_id"] = stu.student_id
                    session["student_name"] = stu.name
                    session["student_dept"] = stu.department
                    session["curriculum_id"] = stu.curriculum_id
        finally:
            db.close()

    def_college = def_college or "Raghu Engineering College"
    def_degree = def_degree or "B.Tech"
    def_reg = def_reg or "AR23"
    def_branch = def_branch or "CSE"
    def_spec = def_spec or ("VLSI & Embedded Systems" if def_branch == "ECE" else ("Power Systems & Automation" if def_branch == "EEE" else ("Design & Manufacturing" if def_branch == "MECH" else ("Structural Engineering" if def_branch == "CIVIL" else "Core Computer Science"))))
    def_sem = str(def_sem or 3)

    # Dynamic specialization options for active branch
    db = get_db_session()
    try:
        spec_list = CurriculumEngine.get_specializations(db, def_college, def_degree, def_reg, def_branch)
    finally:
        db.close()

    if not spec_list:
        if def_branch == "CSE":
            spec_list = ["Core Computer Science", "AI & ML", "Data Science", "Cyber Security", "IoT & Blockchain"]
        elif def_branch == "ECE":
            spec_list = ["VLSI & Embedded Systems"]
        elif def_branch == "EEE":
            spec_list = ["Power Systems & Automation"] if def_reg == "AR23" else ["Power Systems"]
        elif def_branch == "MECH":
            spec_list = ["Design & Manufacturing"] if def_reg == "AR23" else ["Thermal & Design"]
        elif def_branch == "CIVIL":
            spec_list = ["Structural Engineering"]
        else:
            spec_list = [def_spec] if def_spec else ["Core Computer Science"]

    if def_spec not in spec_list:
        spec_list.insert(0, def_spec)
    spec_options = [{"label": s, "value": s} for s in spec_list]

    norm_path = active_path.replace("/app", "") if active_path.startswith("/app") else active_path
    if norm_path in ("", "/"):
        norm_path = "/overview"

    # Route Header & Subpage Content Selection
    route_header = None
    subpage_content = None

    if norm_path == "/overview":
        route_header = create_stage_route_header(
            [html.Span("Academic "), html.Em("Performance"), html.Span(" Overview")],
            "Executive summary of cumulative CGPA, active term SGPA, attendance, and semester progression.",
            "OVERVIEW"
        )
        subpage_content = build_overview_page()
    elif norm_path == "/analytics":
        route_header = create_stage_route_header(
            [html.Span("Performance Analytics & "), html.Em("Study Roadmap")],
            "Detailed subject grade points mastery breakdown, competency analytics, and study recommendations.",
            "ANALYTICS"
        )
        subpage_content = build_analytics_page()
    elif norm_path in ("/marks-subjects", "/marks", "/subjects"):
        route_header = create_stage_route_header(
            [html.Span("Marks & Subjects "), html.Em("Marksheet")],
            "Official semester subject roster, grade point entry, elective course selections, and verified transcript.",
            "MARKS & SUBJECTS"
        )
        subpage_content = build_marks_subjects_page()
    elif norm_path == "/attendance":
        route_header = create_stage_route_header(
            [html.Span("Attendance & "), html.Em("Exam Eligibility")],
            "Subject-wise attendance tracking, 75% university eligibility compliance, and hall ticket alerts.",
            "ATTENDANCE"
        )
        subpage_content = build_attendance_page()
    elif norm_path in ("/academic-profile", "/profile"):
        route_header = create_stage_route_header(
            [html.Span("Student "), html.Em("Academic Profile")],
            "Student enrollment credentials, institutional affiliation, branch specialization, and regulation governance.",
            "ACADEMIC PROFILE"
        )
        subpage_content = build_academic_profile_page()
    elif norm_path == "/settings":
        route_header = create_stage_route_header(
            [html.Span("Student "), html.Em("Preferences & Settings")],
            "Academic curriculum defaults, account session security, and transcript export controls.",
            "SETTINGS"
        )
        subpage_content = build_settings_page()

    return dbc.Container([
        # Exact Preview Card Container with Strict CSS Grid
        html.Div([
            html.Div([
                html.Span([
                    html.Span("⚡", style={"fontSize": "0.9rem"}),
                    html.Span("Curriculum & Academic Structure")
                ], className="preview-card-heading"),
                html.Span([
                    html.Span("●", style={"color": "#34D399", "fontSize": "0.8rem"}),
                    html.Span(f"{def_reg} {def_branch} ({def_spec})")
                ], className="preview-card-status-pill mono-font")
            ], className="preview-card-top-header"),

            html.Div([
                # 1. Institution
                html.Div([
                    html.Label("🏛️ Institution", className="preview-field-label"),
                    dbc.Select(
                        id="curriculum-college-select",
                        options=[
                            {"label": "Raghu Engineering College (Autonomous)", "value": "Raghu Engineering College"},
                            {"label": "+ Custom / Other College", "value": "Custom College"}
                        ],
                        value=def_college,
                        className="preview-form-select"
                    )
                ], className="preview-field-wrapper"),

                # 2. Degree
                html.Div([
                    html.Label("🎓 Degree Program", className="preview-field-label"),
                    dbc.Select(
                        id="curriculum-degree-select",
                        options=[{"label": "B.Tech", "value": "B.Tech"}],
                        value=def_degree,
                        className="preview-form-select"
                    )
                ], className="preview-field-wrapper"),

                # 3. Regulation
                html.Div([
                    html.Label("📜 Regulation Schema", className="preview-field-label"),
                    dbc.Select(
                        id="curriculum-regulation-select",
                        options=[
                            {"label": "AR23 (Latest Autonomous)", "value": "AR23"},
                            {"label": "AR20 (Previous Schema)", "value": "AR20"}
                        ],
                        value=def_reg,
                        className="preview-form-select"
                    )
                ], className="preview-field-wrapper"),

                # 4. Branch
                html.Div([
                    html.Label("💻 Department / Branch", className="preview-field-label"),
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
                        className="preview-form-select"
                    )
                ], className="preview-field-wrapper"),

                # 5. Track
                html.Div([
                    html.Label("🎯 Specialization Track", className="preview-field-label"),
                    dbc.Select(
                        id="curriculum-spec-select",
                        options=spec_options,
                        value=def_spec,
                        className="preview-form-select"
                    )
                ], className="preview-field-wrapper"),

                # 6. Semester
                html.Div([
                    html.Label("📅 Active Semester", className="preview-field-label"),
                    dbc.Select(
                        id="student-semester-dropdown",
                        options=[{"label": f"Semester {i}", "value": str(i)} for i in range(1, 9)],
                        value=def_sem,
                        className="preview-form-select"
                    )
                ], className="preview-field-wrapper")
            ], className="curriculum-dropdown-grid")
        ], className="cockpit-preview-container-card"),

        # Hidden/Compact Banner Hook
        html.Div(id="curriculum-confirmation-banner", style={"display": "none"}),

        # Route Header with Instrument Serif
        route_header,

        # Active Subpage Content Container
        html.Div(id="dashboard-subpage-content", children=subpage_content),

        # Modals
                                dbc.Modal([
            dbc.ModalHeader([
                html.Div([
                    html.Div([
                        html.Span("✦", className="text-info me-2 fs-5"),
                        dbc.ModalTitle(id="marks-modal-title", children="Academic Grade Points & Marks Workspace", className="d-inline-block fw-bold text-white fs-5 mb-0")
                    ], className="d-flex align-items-center"),
                    html.P("Record your official grade points (0.00 – 10.00) for real-time SGPA calculation.", className="text-secondary small mb-0 mt-1")
                ])
            ], close_button=True, className="modal-header"),
            dbc.ModalBody([
                html.Div(id="marks-modal-alert"),
                dcc.Loading(html.Div(id="marks-modal-subjects-container", className="py-1")),
            ], className="modal-body", style={"maxHeight": "72vh", "overflowY": "auto"}),
            dbc.ModalFooter([
                dbc.Button("✕ Cancel", id="marks-modal-cancel-btn", className="btn-modal-cancel"),
                dbc.Button([
                    html.Span("✓"),
                    html.Span("Save & Recalculate SGPA / CGPA", className="ms-1")
                ], id="marks-modal-save-btn", className="btn-modal-save")
            ], className="modal-footer")
        ], id="student-marks-modal", is_open=False, size="lg", centered=True),

        dbc.Modal([
            dbc.ModalHeader([
                html.Div([
                    html.Div([
                        html.Span("⭐", className="text-warning me-2 fs-5"),
                        dbc.ModalTitle(id="elective-modal-title", children="Select Curriculum Elective / Honor Track", className="d-inline-block fw-bold text-white fs-5 mb-0")
                    ], className="d-flex align-items-center"),
                    html.P("Customize your semester transcript with Professional Electives, Open Electives, and Honors tracks.", className="text-secondary small mb-0 mt-1")
                ])
            ], close_button=True, className="modal-header"),
            dbc.ModalBody([
                html.Div(id="elective-modal-alert"),
                dcc.Loading(html.Div(id="elective-modal-options-container", className="py-1")),
            ], className="modal-body", style={"maxHeight": "72vh", "overflowY": "auto"}),
            dbc.ModalFooter([
                dbc.Button("✕ Cancel", id="elective-modal-cancel-btn", className="btn-modal-cancel"),
                dbc.Button([
                    html.Span("✓"),
                    html.Span("Confirm & Add to Marksheet", className="ms-1")
                ], id="elective-modal-save-btn", className="btn-modal-save")
            ], className="modal-footer")
        ], id="student-elective-modal", is_open=False, size="lg", centered=True),

        # Stores & Downloads
        dcc.Store(id="marks-refresh-trigger", data=0),
        dcc.Store(id="current-elective-modal-category", data="PROFESSIONAL_ELECTIVE"),
        dcc.Download(id="download-student-excel"),
        dcc.Download(id="download-student-pdf")
    ], fluid=True, className="cockpit-main-wrapper pb-5")


def create_demo_cockpit_layout(active_path: str = "/overview"):
    """
    Renders the complete interactive Demo Cockpit with persistent navbar and overview page.
    Automatically populates demo session state.
    """
    from flask import session, has_request_context
    if has_request_context():
        session["is_demo"] = True
        session["student_id"] = "STU2024001"
        session["college_name"] = "Raghu Engineering College"
        session["degree"] = "B.Tech"
        session["regulation_name"] = "AR23"
        session["branch_name"] = "CSE"
        session["specialization"] = "Core Computer Science"
        session["active_semester"] = 3
        session["student_name"] = "Rahul Kumar"
        session["student_dept"] = "Computer Science & Engineering"
        session["curriculum_id"] = "RAGHU_BTECH_AR23_CSE_CORE_COMPUTER_SCIENCE"

    return build_dashboard_shell(active_path=active_path)

# Aliases for robust backwards compatibility
create_dashboard_layout = build_dashboard_shell
render_demo_page = create_demo_cockpit_layout
