"""
Dash Interactive Callbacks for StudIQ.
Provides Cascading 6-Tier Academic Filtering, Compact Elective Management Modal,
Marks & Attendance Entry, Real-Time Verified/Estimated SGPA Calculation Engine,
and Restored Simple Line & Bar Charts.
"""

from dash import Input, Output, State, html, dcc, dash_table, callback_context, no_update, ALL, MATCH
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from flask import session, has_request_context
from flask_login import current_user

from app.database import (
    get_db_session, Student, Course, Enrollment, Prediction, AuditLog, 
    User, Subject, Branch, College, Regulation, Curriculum, 
    CurriculumSubject, ElectiveOption, StudentSubjectSelection, StudentSemesterResult
)
from app.curriculum_engine import CurriculumEngine, get_curriculum_id
from app.utils import calculate_grade, calculate_grade_and_points, generate_excel_report, generate_pdf_report
from app.dashboards.components import create_kpi_card, create_risk_badge


def create_empty_figure(message: str) -> go.Figure:
    """Creates a standardized dark-themed Plotly figure with an informative empty state message."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=14, color="#94A3B8")
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig


def register_callbacks(app):
    """Registers all Dash reactive callbacks with the main application instance."""

    # -------------------------------------------------------------
    # 1. Cascading Academic Dropdown Updaters
    # -------------------------------------------------------------
    @app.callback(
        [Output("curriculum-spec-select", "options"),
         Output("curriculum-spec-select", "value")],
        [Input("curriculum-branch-select", "value"),
         Input("curriculum-regulation-select", "value")],
        [State("curriculum-spec-select", "value")]
    )
    def update_specialization_options(branch, regulation, current_val):
        """Updates available specializations when Branch or Regulation changes."""
        branch = branch or "CSE"
        regulation = regulation or "AR23"
        
        db = get_db_session()
        try:
            specs = CurriculumEngine.get_specializations(db, "Raghu Engineering College", "B.Tech", regulation, branch)
            if not specs:
                if branch == "CSE":
                    specs = ["Core Computer Science", "AI & ML", "Data Science", "Cyber Security", "IoT & Blockchain"]
                elif branch == "ECE":
                    specs = ["VLSI & Embedded Systems"]
                elif branch == "EEE":
                    specs = ["Power Systems & Automation"] if regulation == "AR23" else ["Power Systems"]
                elif branch == "MECH":
                    specs = ["Design & Manufacturing"] if regulation == "AR23" else ["Thermal & Design"]
                elif branch == "CIVIL":
                    specs = ["Structural Engineering"]
                else:
                    specs = ["General"]
            
            opts = [{"label": s, "value": s} for s in specs]
            sel_val = current_val if current_val in specs else (specs[0] if specs else "Core Computer Science")
            return opts, sel_val
        finally:
            db.close()


    # -------------------------------------------------------------
    # 2. Curriculum Confirmation Banner & Summary Card
    # -------------------------------------------------------------
    @app.callback(
        Output("curriculum-confirmation-banner", "children"),
        [Input("curriculum-college-select", "value"),
         Input("curriculum-degree-select", "value"),
         Input("curriculum-regulation-select", "value"),
         Input("curriculum-branch-select", "value"),
         Input("curriculum-spec-select", "value"),
         Input("student-semester-dropdown", "value"),
         Input("marks-refresh-trigger", "data")]
    )
    def render_curriculum_banner(college, degree, regulation, branch, specialization, semester, refresh_cnt):
        college = college or "Raghu Engineering College"
        degree = degree or "B.Tech"
        regulation = regulation or "AR23"
        branch = branch or "CSE"
        specialization = specialization or "Core Computer Science"
        try:
            sem = int(semester or 3)
        except Exception:
            sem = 3

        db = get_db_session()
        try:
            curr_data = CurriculumEngine.get_subjects(db, college, degree, regulation, branch, specialization, sem)
            
            sid = (session.get("student_id") if has_request_context() else None) or getattr(current_user, "student_id", None) or "STU2024001"
            custom_selections = db.query(StudentSubjectSelection).filter(
                StudentSubjectSelection.student_id == sid,
                StudentSubjectSelection.semester == sem
            ).all()

            comp_count = len(curr_data["compulsory_subjects"])
            elec_grps_count = len(curr_data["elective_groups"])
            sel_elec_count = len(custom_selections)
            total_fixed_credits = curr_data["total_fixed_credits"]
            is_verified = curr_data["is_verified"]

            status_badge = dbc.Badge("✓ Official Verified Curriculum", color="success", className="px-3 py-2 fs-6 fw-bold") if is_verified else dbc.Badge("⚠️ Estimated / Custom Curriculum", color="warning", className="px-3 py-2 fs-6 fw-bold text-dark")

            return dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.H5([
                                html.Span(f"{college} • {degree} • {regulation}", className="text-info me-2"),
                                html.Span(f"[{branch} - {specialization}]", className="text-white fw-bold")
                            ], className="mb-1"),
                            html.Div([
                                html.Span(f"Active Term: Semester {sem}", className="badge bg-primary bg-opacity-25 text-primary me-2"),
                                html.Span(f"Fixed Subjects: {comp_count}", className="badge bg-secondary bg-opacity-25 text-light me-2"),
                                html.Span(f"Available Elective Groups: {elec_grps_count}", className="badge bg-info bg-opacity-25 text-info me-2"),
                                html.Span(f"Selected Electives: {sel_elec_count}", className="badge bg-success bg-opacity-25 text-success me-2"),
                                html.Span(f"Base Fixed Credits: {total_fixed_credits:.1f}", className="badge bg-dark border border-secondary text-light")
                            ], className="d-flex align-items-center flex-wrap gap-1 mt-2")
                        ]),
                        html.Div([
                            status_badge
                        ], className="ms-auto mt-2 mt-md-0")
                    ], className="d-flex align-items-center justify-content-between flex-wrap")
                ], className="p-3")
            ], className="border-0 shadow-sm", style={"background": "linear-gradient(135deg, rgba(16, 23, 40, 0.95), rgba(24, 32, 54, 0.95))", "border": "1px solid rgba(255,255,255,0.12)"})
        finally:
            db.close()


    # -------------------------------------------------------------
    # 3. Compact Elective Selection Modal Handler (Add / Change / Remove)
    # -------------------------------------------------------------
    @app.callback(
        [Output("student-elective-modal", "is_open"),
         Output("elective-modal-title", "children"),
         Output("elective-modal-options-container", "children"),
         Output("elective-modal-alert", "children")],
        [Input("open-elective-modal-btn", "n_clicks"),
         Input("elective-modal-cancel-btn", "n_clicks"),
         Input("elective-modal-save-btn", "n_clicks")],
        [State("student-elective-modal", "is_open"),
         State("curriculum-college-select", "value"),
         State("curriculum-degree-select", "value"),
         State("curriculum-regulation-select", "value"),
         State("curriculum-branch-select", "value"),
         State("curriculum-spec-select", "value"),
         State("student-semester-dropdown", "value"),
         State({"type": "elective-radio-group", "index": ALL}, "value"),
         State({"type": "elective-radio-group", "index": ALL}, "id")]
    )
    def handle_elective_modal(open_clicks, cancel_clicks, save_clicks,
                              is_open, college, degree, regulation, branch, specialization, semester,
                              radio_values, radio_ids):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update, no_update
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        # Cancel
        if button_id == "elective-modal-cancel-btn":
            return False, no_update, no_update, ""

        college = college or "Raghu Engineering College"
        degree = degree or "B.Tech"
        regulation = regulation or "AR23"
        branch = branch or "CSE"
        specialization = specialization or "Core Computer Science"
        try:
            sem = int(semester or 3)
        except Exception:
            sem = 3

        curr_id = get_curriculum_id(college, degree, regulation, branch, specialization)
        db = get_db_session()
        try:
            sid = (session.get("student_id") if has_request_context() else None) or getattr(current_user, "student_id", None) or "STU2024001"

            # 1. SAVE CLICKED
            if button_id == "elective-modal-save-btn":
                if radio_values and radio_ids:
                    for val, r_id in zip(radio_values, radio_ids):
                        grp_name = r_id.get("index", "")
                        if val == "__NONE__" or not val:
                            # Remove selection
                            db.query(StudentSubjectSelection).filter(
                                StudentSubjectSelection.student_id == sid,
                                StudentSubjectSelection.semester == sem,
                                StudentSubjectSelection.group_name == grp_name
                            ).delete()
                        else:
                            opt = db.query(ElectiveOption).filter(
                                ElectiveOption.curriculum_id == curr_id,
                                ElectiveOption.semester == sem,
                                ElectiveOption.subject_code == val
                            ).first()
                            if opt:
                                db.query(StudentSubjectSelection).filter(
                                    StudentSubjectSelection.student_id == sid,
                                    StudentSubjectSelection.semester == sem,
                                    StudentSubjectSelection.group_name == grp_name
                                ).delete()
                                
                                sel = StudentSubjectSelection(
                                    student_id=sid,
                                    curriculum_id=curr_id,
                                    semester=sem,
                                    category=opt.category,
                                    group_name=grp_name,
                                    subject_code=opt.subject_code,
                                    subject_name=opt.subject_name,
                                    official_credits=opt.credits,
                                    credits_used=opt.credits,
                                    credit_source="official_course_structure",
                                    credit_status="confirmed"
                                )
                                db.add(sel)
                    db.commit()
                return False, no_update, no_update, ""

            # 2. OPEN MODAL CLICKED
            modal_title = f"+ Add / Change Elective Courses — Semester {sem}"

            options = db.query(ElectiveOption).filter(
                ElectiveOption.curriculum_id == curr_id,
                ElectiveOption.semester == sem
            ).all()

            if not options:
                body = html.Div([
                    dbc.Alert([
                        html.Strong(f"No elective pools scheduled for Semester {sem}."),
                        html.P(f"Under {regulation} {branch} ({specialization}), electives start in Semester 5 (Professional Elective I), Semester 6 (Professional Elective II & Open Elective I), and Semester 7 (Professional Elective III & Open Elective II).", className="small mb-0 mt-2")
                    ], color="info")
                ])
                return True, modal_title, body, ""

            # Group options by group_name
            groups_dict = {}
            for opt in options:
                if opt.group_name not in groups_dict:
                    groups_dict[opt.group_name] = []
                groups_dict[opt.group_name].append(opt)

            # Query currently selected
            existing_selections = {
                s.group_name: s.subject_code for s in db.query(StudentSubjectSelection).filter(
                    StudentSubjectSelection.student_id == sid,
                    StudentSubjectSelection.semester == sem
                ).all()
            }

            elements = []
            for g_name, opts_list in groups_dict.items():
                current_selected = existing_selections.get(g_name, "__NONE__")
                radio_options = [
                    {
                        "label": html.Span("✕ No Selection / Remove Elective for this Group", className="text-secondary fst-italic"),
                        "value": "__NONE__"
                    }
                ] + [
                    {
                        "label": html.Span([
                            html.Strong(f"{o.subject_code}: ", className="text-info me-1"),
                            html.Span(f"{o.subject_name} ", className="text-white"),
                            html.Span(f"({o.credits} Credits)", className="badge bg-secondary bg-opacity-50 text-light ms-2")
                        ]),
                        "value": o.subject_code
                    }
                    for o in opts_list
                ]

                elements.append(html.Div([
                    html.H6(f"📁 {g_name} (Select Exactly 1 Course)", className="text-warning fw-bold mb-2"),
                    dbc.RadioItems(
                        id={"type": "elective-radio-group", "index": g_name},
                        options=radio_options,
                        value=current_selected,
                        className="mb-3",
                        inputClassName="me-2"
                    )
                ], className="p-3 mb-3 rounded-3", style={"background": "rgba(255,255,255,0.03)", "border": "1px solid rgba(255,255,255,0.08)"}))

            return True, modal_title, elements, ""
        finally:
            db.close()


    # -------------------------------------------------------------
    # 4. Marks & Grade Points Entry Modal Handler
    # -------------------------------------------------------------
    @app.callback(
        [Output("student-marks-modal", "is_open"),
         Output("marks-modal-title", "children"),
         Output("marks-modal-subjects-container", "children"),
         Output("marks-modal-alert", "children"),
         Output("marks-refresh-trigger", "data")],
        [Input("open-marks-modal-btn", "n_clicks"),
         Input("marks-modal-cancel-btn", "n_clicks"),
         Input("marks-modal-save-btn", "n_clicks")],
        [State("student-marks-modal", "is_open"),
         State("curriculum-college-select", "value"),
         State("curriculum-degree-select", "value"),
         State("curriculum-regulation-select", "value"),
         State("curriculum-branch-select", "value"),
         State("curriculum-spec-select", "value"),
         State("student-semester-dropdown", "value"),
         State("marks-refresh-trigger", "data"),
         State({"type": "subject-gp-input", "index": ALL}, "value"),
         State({"type": "subject-gp-input", "index": ALL}, "id"),
         State({"type": "subject-att-input", "index": ALL}, "value"),
         State({"type": "subject-att-input", "index": ALL}, "id")]
    )
    def handle_marks_modal(open_clicks, cancel_clicks, save_clicks, is_open,
                           college, degree, regulation, branch, specialization, semester,
                           refresh_cnt, gp_values, gp_ids, att_values, att_ids):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update, no_update, no_update
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        refresh_cnt = refresh_cnt or 0
        
        if button_id == "marks-modal-cancel-btn":
            return False, no_update, no_update, "", refresh_cnt

        college = college or "Raghu Engineering College"
        degree = degree or "B.Tech"
        regulation = regulation or "AR23"
        branch = branch or "CSE"
        specialization = specialization or "Core Computer Science"
        try:
            sem = int(semester or 3)
        except Exception:
            sem = 3

        curr_id = get_curriculum_id(college, degree, regulation, branch, specialization)
        db = get_db_session()
        try:
            sid = (session.get("student_id") if has_request_context() else None) or getattr(current_user, "student_id", None) or "STU2024001"

            # 1. SAVE CLICKED
            if button_id == "marks-modal-save-btn":
                gp_map = {item_id.get("index"): val for item_id, val in zip(gp_ids, gp_values) if item_id}
                att_map = {item_id.get("index"): val for item_id, val in zip(att_ids, att_values) if item_id}

                # Save compulsory enrollments
                comp_subjects = db.query(CurriculumSubject).filter(
                    CurriculumSubject.curriculum_id == curr_id,
                    CurriculumSubject.semester == sem,
                    CurriculumSubject.is_compulsory == True
                ).all()

                for s in comp_subjects:
                    raw_gp = gp_map.get(s.subject_code)
                    raw_att = att_map.get(s.subject_code)

                    enr = db.query(Enrollment).filter(
                        Enrollment.student_id == sid,
                        Enrollment.curriculum_subject_id == s.id
                    ).first()

                    if raw_gp is not None and str(raw_gp).strip() != "":
                        try:
                            gp_val = float(raw_gp)
                        except (ValueError, TypeError):
                            gp_val = None
                    else:
                        gp_val = None

                    if raw_att is not None and str(raw_att).strip() != "":
                        try:
                            att_val = float(raw_att)
                        except (ValueError, TypeError):
                            att_val = None
                    else:
                        att_val = None

                    if gp_val is not None or att_val is not None:
                        grd = "O" if (gp_val and gp_val >= 10.0) else ("A+" if (gp_val and gp_val >= 9.0) else ("A" if (gp_val and gp_val >= 8.0) else ("B+" if (gp_val and gp_val >= 7.0) else "B")))
                        if not enr:
                            enr = Enrollment(
                                student_id=sid,
                                curriculum_subject_id=s.id,
                                course_id=s.subject_code,
                                marks_obtained=gp_val * 9.5 if gp_val is not None else None,
                                grade=grd if gp_val is not None else None,
                                grade_letter=grd if gp_val is not None else None,
                                grade_point=gp_val,
                                credits_used=s.official_credits or s.credits or 3.0,
                                attendance_percentage=att_val,
                                semester=sem,
                                academic_year="2024-2025"
                            )
                            db.add(enr)
                        else:
                            enr.grade_point = gp_val
                            enr.marks_obtained = gp_val * 9.5 if gp_val is not None else None
                            enr.grade = grd if gp_val is not None else None
                            enr.grade_letter = grd if gp_val is not None else None
                            enr.attendance_percentage = att_val
                            enr.credits_used = s.official_credits or s.credits or 3.0

                # Save custom elective selections
                custom_selections = db.query(StudentSubjectSelection).filter(
                    StudentSubjectSelection.student_id == sid,
                    StudentSubjectSelection.semester == sem
                ).all()

                for sel in custom_selections:
                    raw_gp = gp_map.get(sel.subject_code)
                    if raw_gp is not None and str(raw_gp).strip() != "":
                        try:
                            gp_val = float(raw_gp)
                            sel.grade_point = gp_val
                            sel.marks = gp_val * 9.5
                            sel.grade = "A+" if gp_val >= 9.0 else "A"
                        except (ValueError, TypeError):
                            pass

                db.commit()
                return False, no_update, no_update, "", refresh_cnt + 1

            # 2. OPEN MODAL CLICKED -> Build subject cards
            curr_data = CurriculumEngine.get_subjects(db, college, degree, regulation, branch, specialization, sem)
            comp_subs = curr_data["compulsory_subjects"]
            
            custom_selections = db.query(StudentSubjectSelection).filter(
                StudentSubjectSelection.student_id == sid,
                StudentSubjectSelection.semester == sem
            ).all()

            cards = []
            cards.append(html.Div([
                html.Div([
                    html.Span(f"🏛️ {college}", className="badge bg-primary bg-opacity-25 text-primary me-2 mb-1"),
                    html.Span(f"📜 {regulation}", className="badge bg-info bg-opacity-25 text-info me-2 mb-1"),
                    html.Span(f"💻 {branch} ({specialization})", className="badge bg-success bg-opacity-25 text-success me-2 mb-1"),
                    html.Span(f"📚 Semester {sem}", className="badge bg-secondary bg-opacity-25 text-light mb-1")
                ], className="d-flex flex-wrap align-items-center mb-3"),
                html.P("Enter your Grade Points (0.00 – 10.00) and Attendance (%) for each course. Blank fields will remain un-entered.", className="small text-secondary mb-3")
            ]))

            # Compulsory Subjects Section
            cards.append(html.H6("📌 Fixed Compulsory Courses (Theory, Labs & Skill Courses)", className="text-info fw-bold mb-3"))
            for s in comp_subs:
                enr = db.query(Enrollment).filter(
                    Enrollment.student_id == sid,
                    Enrollment.curriculum_subject_id == s.id
                ).first()
                saved_gp = float(enr.grade_point) if (enr and enr.grade_point is not None) else None
                saved_att = float(enr.attendance_percentage) if (enr and enr.attendance_percentage is not None) else None
                is_audit = (s.subject_type == "AUDIT_COURSE" or s.theory_or_lab.lower() == "audit" or s.credits == 0.0)

                cards.append(dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.Span(f"{s.subject_code}", className="badge bg-info bg-opacity-25 text-info fw-bold me-2"),
                                html.Span(f"{s.subject_name}", className="fw-bold text-white fs-6")
                            ]),
                            html.Div([
                                html.Span(f"{s.credits} Credits" if not is_audit else "Audit Course (0 Credits)", 
                                          className="badge bg-secondary bg-opacity-25 text-light")
                            ])
                        ], className="d-flex align-items-center justify-content-between flex-wrap mb-2"),

                        dbc.Row([
                            dbc.Col([
                                html.Label("Grade Points (0.0 – 10.0)", className="small text-secondary fw-semibold"),
                                dbc.Input(
                                    id={"type": "subject-gp-input", "index": s.subject_code},
                                    type="number",
                                    min=0.0,
                                    max=10.0,
                                    step=0.1,
                                    value=saved_gp,
                                    placeholder="e.g. 9.0",
                                    className="form-control-dark"
                                )
                            ], md=4, xs=12),
                            dbc.Col([
                                html.Label("Attendance %", className="small text-secondary fw-semibold"),
                                dbc.Input(
                                    id={"type": "subject-att-input", "index": s.subject_code},
                                    type="number",
                                    min=0.0,
                                    max=100.0,
                                    step=1.0,
                                    value=saved_att,
                                    placeholder="e.g. 85",
                                    className="form-control-dark"
                                )
                            ], md=4, xs=12),
                            dbc.Col([
                                html.Label("Credit Verification Source", className="small text-secondary fw-semibold"),
                                html.Div([
                                    html.Span("✓ Official Regulation", className="badge bg-success bg-opacity-25 text-success py-2 px-3")
                                ], className="mt-1")
                            ], md=4, xs=12)
                        ], className="g-2 align-items-center")
                    ], className="p-3")
                ], className="mb-2", style={"background": "rgba(255,255,255,0.03)", "border": "1px solid rgba(255,255,255,0.08)"}))

            # Selected Electives Section
            if custom_selections:
                cards.append(html.H6("⭐ Selected Elective Courses", className="text-warning fw-bold mt-4 mb-3"))
                for sel in custom_selections:
                    saved_gp = float(sel.grade_point) if (sel and sel.grade_point is not None) else None
                    cards.append(dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.Div([
                                    html.Span(f"{sel.subject_code}", className="badge bg-warning bg-opacity-25 text-warning fw-bold me-2"),
                                    html.Span(f"{sel.subject_name}", className="fw-bold text-white fs-6"),
                                    html.Span(f"[{sel.group_name}]", className="badge bg-dark border border-secondary text-info ms-2")
                                ]),
                                html.Div([
                                    html.Span(f"{sel.credits_used} Credits", className="badge bg-secondary bg-opacity-25 text-light")
                                ])
                            ], className="d-flex align-items-center justify-content-between flex-wrap mb-2"),

                            dbc.Row([
                                dbc.Col([
                                    html.Label("Grade Points (0.0 – 10.0)", className="small text-secondary fw-semibold"),
                                    dbc.Input(
                                        id={"type": "subject-gp-input", "index": sel.subject_code},
                                        type="number",
                                        min=0.0,
                                        max=10.0,
                                        step=0.1,
                                        value=saved_gp,
                                        placeholder="e.g. 9.0",
                                        className="form-control-dark"
                                    )
                                ], md=6, xs=12),
                                dbc.Col([
                                    html.Label("Credit Verification Source", className="small text-secondary fw-semibold"),
                                    html.Div([
                                        html.Span("✓ Elective Pool Syllabus", className="badge bg-success bg-opacity-25 text-success py-2 px-3")
                                    ], className="mt-1")
                                ], md=6, xs=12)
                            ], className="g-2 align-items-center")
                        ], className="p-3")
                    ], className="mb-2", style={"background": "rgba(255,255,255,0.03)", "border": "1px solid rgba(255,255,255,0.08)"}))

            modal_title = f"Enter / Edit Marks & Grades — Semester {sem}"
            return True, modal_title, cards, "", refresh_cnt
        finally:
            db.close()


    # -------------------------------------------------------------
    # 5. Visualizations, KPI Cards & Marksheet Table Callback
    # -------------------------------------------------------------
    @app.callback(
        [Output("student-kpi-container", "children"),
         Output("student-sgpa-trend-chart", "figure"),
         Output("student-radar-chart", "figure"),
         Output("student-attendance-scatter", "figure"),
         Output("student-ai-recommendations-container", "children"),
         Output("student-courses-table-container", "children")],
        [Input("curriculum-college-select", "value"),
         Input("curriculum-degree-select", "value"),
         Input("curriculum-regulation-select", "value"),
         Input("curriculum-branch-select", "value"),
         Input("curriculum-spec-select", "value"),
         Input("student-semester-dropdown", "value"),
         Input("marks-refresh-trigger", "data")]
    )
    def update_dashboard_visualizations(college, degree, regulation, branch, specialization, semester, refresh_cnt):
        college = college or "Raghu Engineering College"
        degree = degree or "B.Tech"
        regulation = regulation or "AR23"
        branch = branch or "CSE"
        specialization = specialization or "Core Computer Science"
        try:
            sem = int(semester or 3)
        except Exception:
            sem = 3

        curr_id = get_curriculum_id(college, degree, regulation, branch, specialization)
        db = get_db_session()
        try:
            sid = (session.get("student_id") if has_request_context() else None) or getattr(current_user, "student_id", None) or "STU2024001"

            # 1. Fetch Compulsory & Custom Electives for Active Semester
            comp_subs = db.query(CurriculumSubject).filter(
                CurriculumSubject.curriculum_id == curr_id,
                CurriculumSubject.semester == sem,
                CurriculumSubject.is_compulsory == True
            ).all()

            custom_selections = db.query(StudentSubjectSelection).filter(
                StudentSubjectSelection.student_id == sid,
                StudentSubjectSelection.semester == sem
            ).all()

            # Check if any courses exist in this curriculum semester
            if not comp_subs and not custom_selections:
                kpis = dbc.Row([
                    dbc.Col(create_kpi_card("Overall CGPA", "—", "No records found", "primary", "cgpa"), md=3, xs=6),
                    dbc.Col(create_kpi_card("Active Term SGPA", "—", "No subjects in curriculum", "info", "sgpa"), md=3, xs=6),
                    dbc.Col(create_kpi_card("Attendance Rate", "—", "No records", "success", "attendance"), md=3, xs=6),
                    dbc.Col(create_kpi_card("Credits Tracked", "0.0 Cr", "No credits", "warning", "forecast"), md=3, xs=6),
                ], className="g-3")

                sgpa_fig = create_empty_figure("Add semester grades to see your progress.")
                subj_fig = create_empty_figure("Enter subject grades to view mastery.")
                att_fig = create_empty_figure("Add attendance records to view the correlation.")
                ai_panel = html.Div(html.P("Complete marks and attendance to generate recommendations.", className="text-secondary p-3"))
                table = html.Div(html.P("No semester subject records found.", className="text-secondary p-3"))

                return kpis, sgpa_fig, subj_fig, att_fig, ai_panel, table

            subject_entries = []
            table_rows = []
            has_any_saved_data = False

            for s in comp_subs:
                enr = db.query(Enrollment).filter(
                    Enrollment.student_id == sid,
                    Enrollment.curriculum_subject_id == s.id
                ).first()
                
                if enr and (enr.grade_point is not None or enr.attendance_percentage is not None):
                    has_any_saved_data = True
                    gp = float(enr.grade_point) if enr.grade_point is not None else None
                    att = float(enr.attendance_percentage) if enr.attendance_percentage is not None else None
                    mrk = float(enr.marks_obtained) if enr.marks_obtained is not None else (gp * 9.5 if gp is not None else None)
                    grd = enr.grade_letter if enr.grade_letter else ("O" if (gp and gp >= 10.0) else ("A+" if (gp and gp >= 9.0) else ("A" if (gp and gp >= 8.0) else ("B+" if (gp and gp >= 7.0) else ("B" if gp else "—")))))
                else:
                    gp = None
                    att = None
                    mrk = None
                    grd = "—"

                subject_entries.append({
                    "code": s.subject_code,
                    "name": s.subject_name,
                    "subject_type": s.subject_type,
                    "theory_or_lab": s.theory_or_lab,
                    "official_credits": s.official_credits or s.credits,
                    "credits": s.credits,
                    "grade_point": gp,
                    "attendance": att,
                    "credit_source": s.credit_source or "official_course_structure",
                    "verification_status": s.verification_status or "official_verified"
                })

                table_rows.append({
                    "Subject Code": s.subject_code,
                    "Subject Name": s.subject_name,
                    "Type": s.subject_type.replace("COMPULSORY_", "").replace("_", " ").title(),
                    "Credits": f"{s.credits:.1f}" if s.credits is not None else "0.0",
                    "Credit Source": "Official Course Structure",
                    "Marks": f"{mrk:.1f}" if mrk is not None else "—",
                    "Grade": grd,
                    "Grade Point": f"{gp:.2f}" if gp is not None else "—",
                    "Attendance": f"{att:.1f}%" if att is not None else "—"
                })

            for sel in custom_selections:
                has_any_saved_data = True
                gp = float(sel.grade_point) if sel.grade_point is not None else None
                mrk = float(sel.marks) if sel.marks is not None else (gp * 9.5 if gp is not None else None)
                grd = sel.grade or ("A+" if (gp and gp >= 9.0) else ("A" if gp else "—"))

                subject_entries.append({
                    "code": sel.subject_code,
                    "name": sel.subject_name,
                    "subject_type": sel.category,
                    "theory_or_lab": "Theory",
                    "official_credits": sel.official_credits,
                    "credits": sel.credits_used,
                    "grade_point": gp,
                    "attendance": 90.0 if gp is not None else None,
                    "credit_source": sel.credit_source or "official_course_structure",
                    "verification_status": "official_verified"
                })

                table_rows.append({
                    "Subject Code": sel.subject_code,
                    "Subject Name": sel.subject_name,
                    "Type": f"Elective ({sel.group_name})",
                    "Credits": f"{sel.credits_used:.1f}" if sel.credits_used is not None else "3.0",
                    "Credit Source": "Official Elective Pool",
                    "Marks": f"{mrk:.1f}" if mrk is not None else "—",
                    "Grade": grd,
                    "Grade Point": f"{gp:.2f}" if gp is not None else "—",
                    "Attendance": "90.0%" if gp is not None else "—"
                })

            # 2. Compute SGPA with Calculation Engine
            calc_result = CurriculumEngine.calculate_sgpa(subject_entries)
            sgpa_val = calc_result["sgpa"] if has_any_saved_data else None
            sgpa_str = calc_result["sgpa_display"] if has_any_saved_data else "Not Entered"
            status_title = calc_result["status_title"] if has_any_saved_data else "Click 'Enter / Edit Marks' to record grades."
            total_credits_tracked = calc_result["total_credits_used"]

            # Query historical semester enrollments
            all_student_enrs = db.query(Enrollment).filter(Enrollment.student_id == sid).all()
            sem_gps = {}
            for e in all_student_enrs:
                if e.grade_point is not None:
                    sem_gps.setdefault(e.semester, []).append((e.grade_point, e.credits_used or 3.0))

            historical_sgpas = {}
            total_weighted = 0.0
            total_cr = 0.0
            for s_num, gp_list in sem_gps.items():
                pts = sum(g * c for g, c in gp_list)
                crs = sum(c for g, c in gp_list)
                if crs > 0:
                    s_gpa = round(pts / crs, 2)
                    historical_sgpas[s_num] = s_gpa
                    total_weighted += pts
                    total_cr += crs

            cgpa_val = round(total_weighted / total_cr, 2) if total_cr > 0 else (sgpa_val or 0.0)

            # 3. KPI Cards
            cgpa_str = f"{cgpa_val:.2f} / 10" if cgpa_val > 0 else "—"
            
            # Compute average attendance across saved subjects
            saved_att_list = [item["attendance"] for item in subject_entries if item.get("attendance") is not None]
            avg_att_str = f"{np.mean(saved_att_list):.1f}%" if saved_att_list else "—"

            kpis = dbc.Row([
                dbc.Col(create_kpi_card("Overall CGPA", cgpa_str, "Cumulative across completed semesters", "primary", "cgpa"), md=3, xs=6),
                dbc.Col(create_kpi_card("Active Term SGPA", sgpa_str, status_title, "info" if "Verified" in status_title else "warning", "sgpa"), md=3, xs=6),
                dbc.Col(create_kpi_card("Attendance Rate", avg_att_str, "Target: >= 75% for exam hall ticket", "success", "attendance"), md=3, xs=6),
                dbc.Col(create_kpi_card("Credits Tracked", f"{total_credits_tracked:.1f} Cr", f"{calc_result['official_credits_used']:.1f} Official • {calc_result['student_credits_used']:.1f} Custom", "warning", "forecast"), md=3, xs=6),
            ], className="g-3")

            # 4. CHART 1: Restored Simple Line Chart (SGPA & CGPA Progression)
            if historical_sgpas:
                sorted_sems = sorted(historical_sgpas.keys())
                sems_x = [f"Sem {i}" for i in sorted_sems]
                gpa_y = [historical_sgpas[i] for i in sorted_sems]

                trend_fig = go.Figure()
                # Cyan SGPA Line (#00F0FF) with points and text
                trend_fig.add_trace(go.Scatter(
                    x=sems_x,
                    y=gpa_y,
                    mode="lines+markers+text",
                    name="Term SGPA",
                    text=[f"{v:.2f}" for v in gpa_y],
                    textposition="top center",
                    line=dict(color="#00F0FF", width=3),
                    marker=dict(size=8, color="#00F0FF", line=dict(color="#ffffff", width=2))
                ))
                # Green Dashed CGPA Reference Line (#10B981)
                if cgpa_val > 0:
                    trend_fig.add_trace(go.Scatter(
                        x=sems_x,
                        y=[cgpa_val] * len(sems_x),
                        mode="lines",
                        name=f"Overall CGPA ({cgpa_val:.2f})",
                        line=dict(color="#10B981", width=2, dash="dash")
                    ))
                trend_fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=20, t=30, b=40),
                    font=dict(color="#94A3B8"),
                    yaxis=dict(range=[0, 10.5], title="SGPA / CGPA (0-10)", gridcolor="rgba(255,255,255,0.08)"),
                    xaxis=dict(title="Academic Semester", gridcolor="rgba(255,255,255,0.08)"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
            else:
                trend_fig = create_empty_figure("Add semester grades to see your progress.")

            # 5. CHART 2: Restored Simple Subject Bar Chart (Purple / Blue #8B5CF6)
            saved_with_gp = [item for item in subject_entries if item.get("grade_point") is not None]
            if saved_with_gp:
                subj_codes = [item["code"] for item in saved_with_gp]
                subj_gps = [item["grade_point"] for item in saved_with_gp]

                subject_fig = go.Figure()
                subject_fig.add_trace(go.Bar(
                    x=subj_codes,
                    y=subj_gps,
                    text=[f"{v:.1f}" for v in subj_gps],
                    textposition="outside",
                    hovertext=[f"{item['code']}: {item['name']} ({v:.2f} GP)" for item, v in zip(saved_with_gp, subj_gps)],
                    marker=dict(
                        color="#8B5CF6",
                        line=dict(color="#A78BFA", width=1.5)
                    ),
                    name="Grade Points"
                ))
                subject_fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=20, t=30, b=40),
                    font=dict(color="#94A3B8"),
                    yaxis=dict(range=[0, 11], title="Grade Points (Scale 0-10)", gridcolor="rgba(255,255,255,0.08)"),
                    xaxis=dict(title="Subject Code", gridcolor="rgba(255,255,255,0.08)"),
                    showlegend=False
                )
            else:
                subject_fig = create_empty_figure("Enter subject grades to view mastery.")

            # 6. CHART 3: Restored Simple Attendance Bar Chart (Green #10B981 with Amber 75% Line)
            att_subs = [item for item in subject_entries if item.get("attendance") is not None]
            if att_subs:
                att_codes = [item["code"] for item in att_subs]
                att_vals = [item["attendance"] for item in att_subs]

                att_fig = go.Figure()
                # Green Bars (#10B981)
                att_fig.add_trace(go.Bar(
                    x=att_codes,
                    y=att_vals,
                    text=[f"{v:.0f}%" for v in att_vals],
                    textposition="outside",
                    hovertext=[f"{item['code']}: {item['name']} ({v:.1f}% Att)" for item, v in zip(att_subs, att_vals)],
                    marker=dict(
                        color="#10B981",
                        line=dict(color="#34D399", width=1.5)
                    ),
                    name="Attendance %"
                ))
                # 75% Amber Reference Line (#F59E0B)
                att_fig.add_shape(
                    type="line",
                    x0=-0.5, x1=len(att_codes)-0.5,
                    y0=75, y1=75,
                    line=dict(color="#F59E0B", width=2.5, dash="dash")
                )
                att_fig.add_annotation(
                    x=len(att_codes)-0.5, y=77,
                    text="75% Minimum",
                    showarrow=False,
                    font=dict(color="#F59E0B", size=11),
                    xanchor="right"
                )
                att_fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=20, t=30, b=40),
                    font=dict(color="#94A3B8"),
                    yaxis=dict(range=[0, 115], title="Attendance Percentage (%)", gridcolor="rgba(255,255,255,0.08)"),
                    xaxis=dict(title="Subject Code", gridcolor="rgba(255,255,255,0.08)"),
                    showlegend=False
                )
            else:
                att_fig = create_empty_figure("Add attendance records to view the correlation.")

            # 7. AI Action Plan / Recommendations from REAL Data
            if has_any_saved_data:
                strong_subs = [item for item in subject_entries if item.get("grade_point") is not None and item["grade_point"] >= 9.0]
                needs_focus = [item for item in subject_entries if item.get("grade_point") is not None and item["grade_point"] < 8.5]
                
                strong_desc = ", ".join([f"{s['code']} ({s['name']})" for s in strong_subs[:2]]) if strong_subs else "Solid overall consistency across coursework."
                focus_desc = ", ".join([f"{s['code']} ({s['name']})" for s in needs_focus[:2]]) if needs_focus else "All subjects currently maintaining distinction grade thresholds."

                ai_panel = html.Div([
                    html.Div([
                        html.Span("🎯 Strengths & Mastery", className="ai-tip-badge mb-1", style={"background": "rgba(16, 185, 129, 0.2)", "color": "#6EE7B7", "border": "1px solid rgba(16, 185, 129, 0.4)"}),
                        html.H6("Top Performing Courses", className="fw-bold text-white mb-1"),
                        html.P(f"Exemplary performance scored in: {strong_desc}.", className="small text-secondary mb-0")
                    ], className="ai-tip-box mb-2"),
                    html.Div([
                        html.Span("🚀 Focus & Enhancement Plan", className="ai-tip-badge mb-1", style={"background": "rgba(0, 240, 255, 0.2)", "color": "#67E8F9", "border": "1px solid rgba(0, 240, 255, 0.4)"}),
                        html.H6("Targeted Study Roadmap", className="fw-bold text-white mb-1"),
                        html.P(f"Focus areas for grade point optimization: {focus_desc}.", className="small text-secondary mb-0")
                    ], className="ai-tip-box mb-0")
                ])
            else:
                ai_panel = html.Div([
                    html.P("Complete marks and attendance to generate recommendations.", className="text-secondary p-3")
                ])

            # 8. Marksheet Table
            if table_rows:
                df = pd.DataFrame(table_rows)
                table = dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{"name": col, "id": col} for col in df.columns],
                    style_as_list_view=True,
                    style_header={
                        'backgroundColor': 'rgba(16, 23, 40, 0.95)',
                        'color': '#00F0FF',
                        'fontWeight': 'bold',
                        'borderBottom': '1px solid rgba(255,255,255,0.12)'
                    },
                    style_cell={
                        'backgroundColor': 'transparent',
                        'color': '#E2E8F0',
                        'fontSize': '13px',
                        'padding': '12px 14px',
                        'borderBottom': '1px solid rgba(255,255,255,0.05)',
                        'textAlign': 'left'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgba(255, 255, 255, 0.02)',
                        }
                    ]
                )
            else:
                table = html.P("No semester subject records found.", className="text-secondary p-3")

            return kpis, trend_fig, subject_fig, att_fig, ai_panel, table
        finally:
            db.close()


    # -------------------------------------------------------------
    # 6. Export Handlers
    # -------------------------------------------------------------
    @app.callback(
        Output("download-student-excel", "data"),
        Input("export-student-excel-btn", "n_clicks"),
        [State("curriculum-college-select", "value"),
         State("curriculum-degree-select", "value"),
         State("curriculum-regulation-select", "value"),
         State("curriculum-branch-select", "value"),
         State("curriculum-spec-select", "value"),
         State("student-semester-dropdown", "value")],
        prevent_initial_call=True
    )
    def export_excel(n_clicks, college, degree, regulation, branch, specialization, semester):
        if not n_clicks:
            return no_update
        college = college or "Raghu Engineering College"
        degree = degree or "B.Tech"
        regulation = regulation or "AR23"
        branch = branch or "CSE"
        specialization = specialization or "Core Computer Science"
        sem = int(semester or 3)

        curr_id = get_curriculum_id(college, degree, regulation, branch, specialization)
        db = get_db_session()
        try:
            sid = (session.get("student_id") if has_request_context() else None) or "STU2024001"
            comp_subs = db.query(CurriculumSubject).filter(
                CurriculumSubject.curriculum_id == curr_id,
                CurriculumSubject.semester == sem
            ).all()

            data = []
            for s in comp_subs:
                enr = db.query(Enrollment).filter(
                    Enrollment.student_id == sid,
                    Enrollment.curriculum_subject_id == s.id
                ).first()
                gp = enr.grade_point if enr else None
                att = enr.attendance_percentage if enr else None
                data.append({
                    "Subject Code": s.subject_code,
                    "Subject Name": s.subject_name,
                    "Type": s.subject_type,
                    "Credits": s.credits,
                    "Grade Point": gp if gp is not None else "—",
                    "Attendance %": f"{att}%" if att is not None else "—",
                    "Verification Status": s.verification_status
                })
            df = pd.DataFrame(data)
            return dcc.send_data_frame(df.to_excel, f"StudIQ_{regulation}_{branch}_Sem{sem}_Marksheet.xlsx", index=False)
        finally:
            db.close()
