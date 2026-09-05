"""
Dash Interactive Callbacks for StudIQ (High-Contrast Visualizations).
"""

from dash import Input, Output, State, html, dcc, dash_table, callback_context, no_update, ALL, MATCH
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
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
    """Standardized dark-themed Plotly figure with high-contrast text."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=14, color="#94A3B8", family="Inter, sans-serif")
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig


def update_overview_page_logic(college, degree, regulation, branch, specialization, semester, refresh_cnt):
    """Overview KPI cards, SGPA spline progression chart, and academic standing."""
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

        comp_subs = db.query(CurriculumSubject).filter(
            CurriculumSubject.curriculum_id == curr_id,
            CurriculumSubject.semester == sem,
            CurriculumSubject.is_compulsory == True
        ).all()

        custom_selections = db.query(StudentSubjectSelection).filter(
            StudentSubjectSelection.student_id == sid,
            StudentSubjectSelection.semester == sem
        ).all()

        if not comp_subs and not custom_selections:
            kpis = html.Div([
                create_kpi_card("Cumulative CGPA", "—", "No records found", "primary", "cgpa"),
                create_kpi_card("Active Term SGPA", "—", "No subjects enrolled", "info", "sgpa"),
                create_kpi_card("Attendance Rate", "—", "No records", "success", "attendance"),
                create_kpi_card("Credits Tracked", "0.0 Cr", "No credits", "warning", "forecast"),
            ], className="kpi-grid-container")

            sgpa_fig = create_empty_figure("Add semester grades in Marks & Subjects to see progression.")
            summary = html.Div([
                html.P("No semester subject records found for this curriculum selection.", className="text-secondary small mb-0")
            ])
            return kpis, sgpa_fig, summary

        subject_entries = []
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
            else:
                gp = None
                att = None

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

        for sel in custom_selections:
            has_any_saved_data = True
            gp = float(sel.grade_point) if sel.grade_point is not None else None

            subject_entries.append({
                "code": sel.subject_code,
                "name": sel.subject_name,
                "subject_type": sel.category,
                "theory_or_lab": "Theory",
                "official_credits": sel.official_credits,
                "credits": sel.credits_used,
                "grade_point": gp,
                "attendance": None,
                "credit_source": sel.credit_source or "official_course_structure",
                "verification_status": "official_verified"
            })

        calc_result = CurriculumEngine.calculate_sgpa(subject_entries)
        sgpa_val = calc_result["sgpa"] if has_any_saved_data else None
        sgpa_str = calc_result["sgpa_display"] if has_any_saved_data else "Not Entered"
        total_credits_tracked = calc_result["total_credits_used"]

        # Historical calculation
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
        cgpa_str = f"{cgpa_val:.2f}" if cgpa_val > 0 else "—"

        saved_att_list = [item["attendance"] for item in subject_entries if item.get("attendance") is not None]
        avg_att_str = f"{np.mean(saved_att_list):.1f}%" if saved_att_list else "—"
        att_safe_pill = "✓ Safe (>=75%)" if saved_att_list and np.mean(saved_att_list) >= 75.0 else ("⚠️ Shortage" if saved_att_list else "Not Recorded")

        # 1. High-Contrast KPI Cards (Full-Width 4-Column CSS Grid)
        kpis = html.Div([
            create_kpi_card("Cumulative CGPA", cgpa_str, f"{cgpa_val:.2f} / 10.0 Scale" if cgpa_val > 0 else "Scale 0-10", "primary", "cgpa"),
            create_kpi_card("Active Term SGPA", sgpa_str, f"Semester {sem} Weighted", "info", "sgpa"),
            create_kpi_card("Attendance Rate", avg_att_str, att_safe_pill, "success" if "Safe" in att_safe_pill else "danger", "attendance"),
            create_kpi_card("Credits Tracked", f"{total_credits_tracked:.1f} Cr", f"{len(subject_entries)} Courses Enrolled", "warning", "forecast"),
        ], className="kpi-grid-cols-4 w-100")

        # 2. Living SGPA Progression Spline Chart
        if historical_sgpas:
            sorted_sems = sorted(historical_sgpas.keys())
            sems_x = [f"Sem {i}" for i in sorted_sems]
            gpa_y = [historical_sgpas[i] for i in sorted_sems]

            trend_fig = go.Figure()
            trend_fig.add_trace(go.Scatter(
                x=sems_x,
                y=gpa_y,
                mode="lines+markers+text",
                name="Term SGPA",
                text=[f"{v:.2f}" for v in gpa_y],
                textposition="top center",
                line=dict(color="#38BDF8", width=3, shape="spline"),
                marker=dict(size=9, color="#FFFFFF", line=dict(color="#38BDF8", width=2.5)),
                fill="tozeroy",
                fillcolor="rgba(56, 189, 248, 0.15)"
            ))
            if cgpa_val > 0:
                trend_fig.add_trace(go.Scatter(
                    x=sems_x,
                    y=[cgpa_val] * len(sems_x),
                    mode="lines",
                    name=f"CGPA Average ({cgpa_val:.2f})",
                    line=dict(color="#34D399", width=2, dash="dash")
                ))
            trend_fig.add_shape(
                type="line",
                x0=-0.5, x1=len(sems_x)-0.5,
                y0=8.0, y1=8.0,
                line=dict(color="#FBBF24", width=1.5, dash="dot")
            )
            trend_fig.add_annotation(
                x=len(sems_x)-0.5, y=8.2,
                text="8.00 Distinction",
                showarrow=False,
                font=dict(color="#FBBF24", size=11, family="Inter, sans-serif"),
                xanchor="right"
            )
            trend_fig.update_layout(
                autosize=True,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=20, t=25, b=35),
                font=dict(color="#FFFFFF", family="Inter, sans-serif", size=12),
                yaxis=dict(range=[0, 10.8], title="Grade Points", gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#E2E8F0")),
                xaxis=dict(title="Semester", gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#E2E8F0")),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#FFFFFF"))
            )
        else:
            trend_fig = create_empty_figure("Add semester grades to see your progression curve.")

        # 3. High-Contrast Standing Card (Structured Grid)
        standing_badge = html.Span([
            html.Span("🏆", className="me-1"),
            html.Span("First Class with Distinction" if cgpa_val >= 8.5 else ("First Class" if cgpa_val >= 7.0 else "Good Academic Standing"))
        ], className="badge bg-success bg-opacity-25 text-success border border-success border-opacity-25 px-3 py-1 mb-2 fw-semibold")

        summary = html.Div([
            html.Div([
                standing_badge,
                html.H6(f"Semester {sem} Standing", className="fw-bold text-white mb-1 fs-6"),
                html.P(f"Enrolled in {len(subject_entries)} courses under {regulation} {branch} ({specialization}). Total of {total_credits_tracked:.1f} credits verified.", className="small text-secondary mb-3")
            ]),
            html.Div([
                html.Div([
                    html.Span("Program:", className="text-muted small"),
                    html.Span(f"{college} ({degree})", className="text-white fw-semibold small")
                ], className="standing-param-row"),
                html.Div([
                    html.Span("Regulation:", className="text-muted small"),
                    html.Span(f"{regulation} Autonomous Scheme", className="text-light fw-semibold small")
                ], className="standing-param-row"),
                html.Div([
                    html.Span("Calculation:", className="text-muted small"),
                    html.Span(calc_result["status_title"], className="text-success fw-semibold small" if "Verified" in calc_result["status_title"] else "text-warning fw-semibold small")
                ], className="standing-param-row"),
                html.Div([
                    html.Span("Attendance:", className="text-muted small"),
                    html.Span(f"{avg_att_str} ({att_safe_pill})", className="text-success fw-semibold small" if "Safe" in att_safe_pill else "text-danger fw-semibold small")
                ], className="standing-param-row")
            ], className="standing-param-grid"),
            html.Div([
                dcc.Link("Performance Analytics →", href="/app/analytics", className="btn btn-celestial-outline btn-sm me-2 mb-1"),
                dcc.Link("Open Marksheet →", href="/app/marks-subjects", className="btn btn-solid-white btn-sm mb-1")
            ], className="d-flex flex-wrap")
        ])

        return kpis, trend_fig, summary
    finally:
        db.close()


def update_analytics_page_logic(college, degree, regulation, branch, specialization, semester, refresh_cnt):
    """Subject Mastery and AI Study Roadmap."""
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

        comp_subs = db.query(CurriculumSubject).filter(
            CurriculumSubject.curriculum_id == curr_id,
            CurriculumSubject.semester == sem,
            CurriculumSubject.is_compulsory == True
        ).all()

        custom_selections = db.query(StudentSubjectSelection).filter(
            StudentSubjectSelection.student_id == sid,
            StudentSubjectSelection.semester == sem
        ).all()

        if not comp_subs and not custom_selections:
            subject_fig = create_empty_figure("Enter subject grades to view mastery.")
            ai_panel = html.Div(html.P("No course records found for this curriculum semester.", className="text-secondary p-3"))
            return subject_fig, ai_panel

        subject_entries = []
        has_any_saved_data = False

        for s in comp_subs:
            enr = db.query(Enrollment).filter(
                Enrollment.student_id == sid,
                Enrollment.curriculum_subject_id == s.id
            ).first()
            
            if enr and (enr.grade_point is not None):
                has_any_saved_data = True
                gp = float(enr.grade_point)
            else:
                gp = None

            subject_entries.append({
                "code": s.subject_code,
                "name": s.subject_name,
                "is_custom": False,
                "credits": s.credits,
                "grade_point": gp
            })

        for sel in custom_selections:
            has_any_saved_data = True
            gp = float(sel.grade_point) if sel.grade_point is not None else None

            subject_entries.append({
                "code": sel.subject_code,
                "name": f"[Elective] {sel.subject_name}",
                "is_custom": True,
                "credits": sel.credits_used,
                "grade_point": gp
            })

        # 1. Premium Gradient Subject Mastery Bar Chart (#3b82f6 -> #10b981)
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
                textfont=dict(color="#FFFFFF", size=11, family="Inter, sans-serif"),
                hovertext=[f"<b>{item['code']}</b>: {item['name']}<br>Grade Points: {v:.2f}" for item, v in zip(saved_with_gp, subj_gps)],
                marker=dict(
                    color="#38BDF8",
                    line=dict(color="rgba(255, 255, 255, 0.45)", width=1.5),
                    opacity=0.95
                ),
                name="Grade Points"
            ))
            # Distinction Reference Line (8.00)
            subject_fig.add_shape(
                type="line",
                x0=-0.5, x1=len(subj_codes)-0.5,
                y0=8.0, y1=8.0,
                line=dict(color="#FBBF24", width=2, dash="dash")
            )
            subject_fig.add_annotation(
                x=len(subj_codes)-0.5, y=8.25,
                text="8.00 Distinction Reference",
                showarrow=False,
                font=dict(color="#FBBF24", size=10, family="Inter, sans-serif"),
                xanchor="right"
            )
            subject_fig.update_layout(
                autosize=True,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=20, t=30, b=35),
                font=dict(color="#FFFFFF", family="Inter, sans-serif", size=12),
                yaxis=dict(range=[0, 11], title="Grade Points (Scale 10.0)", gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#E2E8F0")),
                xaxis=dict(title="Subject Code", gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#E2E8F0")),
                showlegend=False
            )
        else:
            subject_fig = create_empty_figure("Enter subject grades under Marks & Subjects to view mastery.")

        # 2. Polished Frosted AI Study Roadmap Cards
        if has_any_saved_data and saved_with_gp:
            strong_subs = [item for item in saved_with_gp if item["grade_point"] >= 9.0]
            needs_focus = [item for item in saved_with_gp if item["grade_point"] < 8.5]
            
            strong_desc = ", ".join([f"{s['code']} ({s['name']})" for s in strong_subs[:2]]) if strong_subs else "Solid academic baseline maintained across courses."
            focus_desc = ", ".join([f"{s['code']} ({s['name']})" for s in needs_focus[:2]]) if needs_focus else "All evaluated courses are currently at or above distinction threshold (8.5+ GP)."

            ai_panel = html.Div([
                # Card 1: Strengths & High Mastery
                html.Div([
                    html.Div([
                        html.Span("✦ High Competency Tier", className="ai-card-badge ai-card-badge--strength"),
                        html.Span("● Verified", className="text-secondary small mono-font")
                    ], className="ai-card-header-row"),
                    html.H6([
                        html.Span("🏆"),
                        html.Span("Top Performing Competencies", className="ms-1")
                    ], className="ai-card-title"),
                    html.P(f"Strong mastery recorded in: {strong_desc}. Demonstrates solid conceptual grasp and consistent performance.", className="ai-card-text")
                ], className="ai-roadmap-card ai-roadmap-card--strength"),

                # Card 2: Priority Focus & Improvement Plan
                html.Div([
                    html.Div([
                        html.Span("⚡ Actionable Plan", className="ai-card-badge ai-card-badge--focus"),
                        html.Span("● Priority", className="text-secondary small mono-font")
                    ], className="ai-card-header-row"),
                    html.H6([
                        html.Span("🎯"),
                        html.Span("Targeted Study Roadmap", className="ms-1")
                    ], className="ai-card-title"),
                    html.P(f"Priority review recommended for: {focus_desc}. Raising these grade points to 9.0+ will accelerate CGPA progression.", className="ai-card-text")
                ], className="ai-roadmap-card ai-roadmap-card--focus"),

                # Card 3: Strategic Trajectory
                html.Div([
                    html.Div([
                        html.Span("📈 Progression Guidance", className="ai-card-badge ai-card-badge--guidance"),
                        html.Span("● Milestone", className="text-secondary small mono-font")
                    ], className="ai-card-header-row"),
                    html.H6([
                        html.Span("💡"),
                        html.Span("Strategic CGPA Trajectory", className="ms-1")
                    ], className="ai-card-title"),
                    html.P("Maintaining current momentum across high-credit courses qualifies for Autonomous First Class with Distinction (>8.50 CGPA).", className="ai-card-text")
                ], className="ai-roadmap-card ai-roadmap-card--guidance")
            ])
        else:
            ai_panel = html.Div([
                html.Div([
                    html.Div([
                        html.Span("⚡ Insight Engine", className="ai-card-badge ai-card-badge--focus"),
                        html.Span("● Idle", className="text-secondary small mono-font")
                    ], className="ai-card-header-row"),
                    html.H6("Awaiting Grade Point Input", className="ai-card-title"),
                    html.P("Click 'Enter / Edit Marks & Grades' under Marks & Subjects to input your semester grade points and generate enterprise competency analytics.", className="ai-card-text")
                ], className="ai-roadmap-card ai-roadmap-card--focus text-center py-4")
            ])

        return subject_fig, ai_panel
    finally:
        db.close()


def update_marks_subjects_page_logic(college, degree, regulation, branch, specialization, semester, refresh_cnt):
    """Marks & Subjects DataTable."""
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

        comp_subs = db.query(CurriculumSubject).filter(
            CurriculumSubject.curriculum_id == curr_id,
            CurriculumSubject.semester == sem,
            CurriculumSubject.is_compulsory == True
        ).all()

        custom_selections = db.query(StudentSubjectSelection).filter(
            StudentSubjectSelection.student_id == sid,
            StudentSubjectSelection.semester == sem
        ).all()

        if not comp_subs and not custom_selections:
            return html.Div([
                dbc.Alert("No course structure records found for this semester curriculum selection.", color="info", className="mb-0")
            ], className="p-3")

        table_rows = []

        for s in comp_subs:
            enr = db.query(Enrollment).filter(
                Enrollment.student_id == sid,
                Enrollment.curriculum_subject_id == s.id
            ).first()
            
            gp = float(enr.grade_point) if (enr and enr.grade_point is not None) else None
            grd = enr.grade_letter or enr.grade or ("O" if gp and gp >= 10.0 else ("A+" if gp and gp >= 9.0 else ("A" if gp and gp >= 8.0 else ("B+" if gp and gp >= 7.0 else "B")))) if gp is not None else "—"
            is_audit = (s.subject_type == "AUDIT_COURSE" or (s.theory_or_lab and s.theory_or_lab.lower() == "audit") or s.credits == 0.0)

            table_rows.append({
                "Subject Code": s.subject_code,
                "Subject Name": s.subject_name,
                "Credits": f"{s.credits:.1f}" if not is_audit else "0.0",
                "Grade": grd,
                "Grade Points": f"{gp:.2f}" if gp is not None else "—"
            })

        for sel in custom_selections:
            gp = float(sel.grade_point) if sel.grade_point is not None else None
            grd = sel.grade or ("A+" if gp and gp >= 9.0 else "A") if gp is not None else "—"

            table_rows.append({
                "Subject Code": sel.subject_code,
                "Subject Name": f"⭐ {sel.subject_name} [{sel.group_name}]",
                "Credits": f"{sel.credits_used:.1f}" if sel.credits_used is not None else "3.0",
                "Grade": grd,
                "Grade Points": f"{gp:.2f}" if gp is not None else "—"
            })

        df = pd.DataFrame(table_rows)
        return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": col, "id": col} for col in df.columns],
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'rgba(16, 24, 40, 0.85)',
                'color': '#94A3B8',
                'fontWeight': '700',
                'borderBottom': '1px solid rgba(255,255,255,0.12)',
                'fontSize': '12px',
                'textTransform': 'uppercase',
                'letterSpacing': '0.05em',
                'padding': '14px 18px'
            },
            style_cell={
                'backgroundColor': 'transparent',
                'color': '#F1F5F9',
                'fontSize': '13.5px',
                'padding': '14px 18px',
                'borderBottom': '1px solid rgba(255,255,255,0.06)',
                'textAlign': 'left',
                'fontFamily': 'Inter, sans-serif',
                'whiteSpace': 'normal'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Subject Code'}, 'width': '16%'},
                {'if': {'column_id': 'Subject Name'}, 'width': '44%'},
                {'if': {'column_id': 'Credits'}, 'width': '12%', 'textAlign': 'center'},
                {'if': {'column_id': 'Grade'}, 'width': '12%', 'textAlign': 'center'},
                {'if': {'column_id': 'Grade Points'}, 'width': '16%', 'textAlign': 'center'},
            ],
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgba(255, 255, 255, 0.02)',
                },
                {
                    'if': {'column_id': 'Subject Code'},
                    'fontFamily': 'JetBrains Mono, monospace',
                    'fontWeight': '700',
                    'color': '#38BDF8'
                },
                {
                    'if': {'column_id': 'Grade Points'},
                    'fontFamily': 'JetBrains Mono, monospace',
                    'fontWeight': '700',
                    'color': '#C7D2FE',
                    'textAlign': 'center'
                },
                {
                    'if': {'column_id': 'Grade'},
                    'fontWeight': '800',
                    'color': '#34D399',
                    'textAlign': 'center'
                },
                {
                    'if': {'column_id': 'Credits'},
                    'fontFamily': 'JetBrains Mono, monospace',
                    'color': '#E2E8F0',
                    'textAlign': 'center'
                }
            ],
            style_table={'width': '100%', 'minWidth': '100%'}
        )
    finally:
        db.close()


def update_attendance_page_logic(college, degree, regulation, branch, specialization, semester, refresh_cnt):
    """Subject Attendance Bar Chart & 75% Cutoff Indicator with Modern SaaS Visuals."""
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

        comp_subs = db.query(CurriculumSubject).filter(
            CurriculumSubject.curriculum_id == curr_id,
            CurriculumSubject.semester == sem,
            CurriculumSubject.is_compulsory == True
        ).all()

        if not comp_subs:
            att_fig = create_empty_figure("No subjects in curriculum.")
            summary = html.Div(html.P("No course records found for this curriculum semester.", className="text-secondary p-3"))
            return att_fig, summary

        subject_entries = []
        for s in comp_subs:
            enr = db.query(Enrollment).filter(
                Enrollment.student_id == sid,
                Enrollment.curriculum_subject_id == s.id
            ).first()
            
            if enr and enr.attendance_percentage is not None:
                att = float(enr.attendance_percentage)
            else:
                att = None

            subject_entries.append({
                "code": s.subject_code,
                "name": s.subject_name,
                "subject_type": s.subject_type,
                "theory_or_lab": s.theory_or_lab,
                "attendance": att
            })

        # 1. Futuristic SaaS Attendance Bar Chart (Glowing Cyan/Teal Gradient Look)
        saved_with_att = [item for item in subject_entries if item.get("attendance") is not None]
        if saved_with_att:
            att_codes = [item["code"] for item in saved_with_att]
            att_vals = [item["attendance"] for item in saved_with_att]
            att_names = [item["name"] for item in saved_with_att]
            att_status = ["Statutory Clear" if v >= 75.0 else "Shortage Warning" for v in att_vals]

            bar_colors = ["rgba(45, 212, 191, 0.75)" if v >= 75.0 else "rgba(248, 113, 113, 0.75)" for v in att_vals]
            border_colors = ["#2DD4BF" if v >= 75.0 else "#F87171" for v in att_vals]

            att_fig = go.Figure()
            att_fig.add_trace(go.Bar(
                x=att_codes,
                y=att_vals,
                customdata=list(zip(att_codes, att_names, att_status)),
                text=[f"{v:.0f}%" for v in att_vals],
                textposition="outside",
                textfont=dict(color="#FFFFFF", size=12, family="JetBrains Mono, monospace", weight="bold"),
                hovertemplate=(
                    "<div style='padding: 6px 8px;'>"
                    "<b style='color:#38BDF8; font-size:13px;'>%{customdata[0]}</b><br>"
                    "<span style='color:#94A3B8;'>Course:</span> <b>%{customdata[1]}</b><br>"
                    "<span style='color:#2DD4BF;'>Attendance:</span> <b>%{y:.1f}%</b><br>"
                    "<span style='color:#FBBF24;'>Status:</span> <b>%{customdata[2]}</b>"
                    "</div><extra></extra>"
                ),
                marker=dict(
                    color=bar_colors,
                    line=dict(color=border_colors, width=2),
                    cornerradius=10
                ),
                width=0.45 if len(att_codes) <= 4 else 0.55,
                name="Attendance %"
            ))

            # Glowing 75% Cutoff Threshold Line
            att_fig.add_shape(
                type="line",
                x0=-0.6, x1=len(att_codes)-0.4,
                y0=75, y1=75,
                line=dict(color="#FBBF24", width=2, dash="dash")
            )
            att_fig.add_annotation(
                x=len(att_codes)-0.5, y=79,
                text="● 75% Statutory Cutoff",
                showarrow=False,
                font=dict(color="#FDE68A", size=10, family="JetBrains Mono, monospace", weight="bold"),
                bgcolor="rgba(251, 191, 36, 0.20)",
                bordercolor="rgba(251, 191, 36, 0.50)",
                borderwidth=1,
                borderpad=4,
                xanchor="right"
            )

            att_fig.update_layout(
                autosize=True,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=35, r=20, t=30, b=35),
                font=dict(color="#FFFFFF", family="Inter, sans-serif", size=12),
                yaxis=dict(
                    range=[0, 115],
                    dtick=25,
                    title="",
                    gridcolor="rgba(255, 255, 255, 0.07)",
                    gridwidth=1,
                    zeroline=True,
                    zerolinecolor="rgba(255, 255, 255, 0.12)",
                    tickfont=dict(color="#94A3B8", family="JetBrains Mono, monospace", size=10),
                    ticksuffix="%"
                ),
                xaxis=dict(
                    title="",
                    showgrid=False,
                    tickfont=dict(color="#FFFFFF", family="JetBrains Mono, monospace", size=11, weight="bold")
                ),
                hoverlabel=dict(
                    bgcolor="rgba(10, 14, 26, 0.95)",
                    bordercolor="rgba(56, 189, 248, 0.40)",
                    font=dict(family="Inter, sans-serif", size=12, color="#FFFFFF")
                ),
                bargap=0.35,
                showlegend=False
            )
        else:
            att_fig = create_empty_figure("No attendance records synchronized for this term.")

        # 2. Examination Eligibility Verification Card & 3-Column Micro-Grid
        if saved_with_att:
            avg_att = float(np.mean([item["attendance"] for item in saved_with_att]))
            shortages = [item for item in saved_with_att if item["attendance"] < 75.0]
            is_eligible = (avg_att >= 75.0 and len(shortages) == 0)

            if is_eligible:
                status_card = html.Div([
                    html.Div([
                        html.Span("✓ Exam Eligible", className="badge bg-success bg-opacity-20 text-success border border-success border-opacity-30 px-3 py-1 fw-bold mb-2 d-inline-block"),
                        html.H5("Hall Ticket Status: Approved", className="fw-bold text-white mb-2 fs-6"),
                        html.P(f"Semester average attendance is {avg_att:.1f}%. All enrolled courses meet the statutory 75% autonomous threshold.", className="text-secondary small mb-0")
                    ])
                ], className="attendance-verification-card mb-3", style={"borderColor": "rgba(52, 211, 153, 0.4)", "background": "rgba(0, 0, 0, 0.50)", "borderRadius": "16px", "padding": "20px"})
            else:
                shortage_codes = ", ".join([f"{s['code']} ({s['attendance']:.0f}%)" for s in shortages])
                status_card = html.Div([
                    html.Div([
                        html.Span("⚠️ Attendance Warning", className="badge bg-danger bg-opacity-20 text-danger border border-danger border-opacity-30 px-3 py-1 fw-bold mb-2 d-inline-block"),
                        html.H5("Condonation Required", className="fw-bold text-white mb-2 fs-6"),
                        html.P(f"Attendance shortage in: {shortage_codes}. Minimum 75% required for regular hall ticket clearance.", className="text-secondary small mb-0")
                    ])
                ], className="attendance-verification-card mb-3", style={"borderColor": "rgba(248, 113, 113, 0.4)", "background": "rgba(0, 0, 0, 0.50)", "borderRadius": "16px", "padding": "20px"})

            # Proper CSS Grid: 3-column micro-grid with bold typography and proper padding
            stats_grid = html.Div([
                # Col 1: Average Semester Attendance
                html.Div([
                    html.Span("AVG ATTENDANCE", className="profile-micro-label text-center mb-1", style={"fontSize": "0.72rem"}),
                    html.H4(f"{avg_att:.1f}%", className="fw-bold text-white mono-font mb-0 text-center")
                ], className="attendance-stat-box", style={"background": "rgba(0, 0, 0, 0.50)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "14px", "padding": "16px 12px"}),

                # Col 2: Tracked Courses
                html.Div([
                    html.Span("ENROLLED COURSES", className="profile-micro-label text-center mb-1", style={"fontSize": "0.72rem"}),
                    html.H4(f"{len(saved_with_att)}", className="fw-bold text-info mono-font mb-0 text-center")
                ], className="attendance-stat-box", style={"background": "rgba(0, 0, 0, 0.50)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "14px", "padding": "16px 12px"}),

                # Col 3: Statutory Model
                html.Div([
                    html.Span("STATUTORY MODEL", className="profile-micro-label text-center mb-1", style={"fontSize": "0.72rem"}),
                    html.H4(f"{regulation} (75%)", className="fw-bold text-warning mono-font mb-0 text-center", style={"fontSize": "1.05rem"})
                ], className="attendance-stat-box", style={"background": "rgba(0, 0, 0, 0.50)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "14px", "padding": "16px 12px"}),
            ], className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-3 attendance-stats-grid",
               style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(130px, 1fr))", "gap": "14px", "width": "100%"})

            summary = html.Div([
                status_card,
                stats_grid,
                dcc.Link("View Marks & Performance →", href="/app/marks-subjects", className="btn btn-solid-white btn-sm w-100 py-2")
            ])
        else:
            summary = html.Div([
                html.Div([
                    html.Span("Attendance Record", className="badge bg-white bg-opacity-10 text-light mb-2"),
                    html.H6("No Attendance Data Available", className="fw-bold text-white mb-2 fs-6"),
                    html.P("Attendance records synchronized from the institutional registrar.", className="text-secondary small mb-3"),
                    dcc.Link("View Marks & Subjects →", href="/app/marks-subjects", className="btn btn-solid-white btn-sm")
                ], className="attendance-verification-card text-center p-4",
                   style={"background": "rgba(0, 0, 0, 0.50)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "16px"})
            ])

        return att_fig, summary
    finally:
        db.close()

def register_callbacks(app):
    """Registers Dash reactive callbacks."""

    # 1. Cascading Academic Dropdowns
    @app.callback(
        [Output("curriculum-spec-select", "options"),
         Output("curriculum-spec-select", "value")],
        [Input("curriculum-branch-select", "value"),
         Input("curriculum-regulation-select", "value")],
        [State("curriculum-spec-select", "value")]
    )
    def update_specialization_options(branch, regulation, current_val):
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


    # 2. Curriculum Confirmation Banner
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

            status_badge = dbc.Badge("✓ Verified Curriculum", color="success", className="px-3 py-1 small fw-bold") if is_verified else dbc.Badge("⚠️ Custom Model", color="warning", className="px-3 py-1 small fw-bold text-dark")

            return html.Div([
                html.Div([
                    html.Div([
                        html.Span("🏛️ ", className="me-1"),
                        html.Strong(f"{college} • {degree} {regulation} ", className="text-white small"),
                        html.Span(f"[{branch} - {specialization}]", className="text-secondary small fw-semibold me-2"),
                        html.Span(f"Active: Sem {sem}", className="badge bg-secondary bg-opacity-50 text-white me-2 small mono-font"),
                        html.Span(f"{comp_count} Compulsory Courses", className="badge bg-dark border border-secondary text-light me-2 small mono-font"),
                        html.Span(f"{sel_elec_count}/{elec_grps_count} Electives", className="badge bg-dark border border-secondary text-light me-2 small mono-font"),
                        html.Span(f"{total_fixed_credits:.1f} Fixed Cr", className="badge bg-dark border border-secondary text-light small mono-font")
                    ], className="d-flex align-items-center flex-wrap gap-1"),
                    html.Div(status_badge, className="ms-auto mt-2 mt-md-0")
                ], className="d-flex align-items-center justify-content-between flex-wrap py-2 px-3 rounded-2", style={"background": "#111827", "border": "1px solid rgba(255,255,255,0.12)"})
            ])
        finally:
            db.close()


    # 3. Elective Selection Modal
    @app.callback(
        [Output("student-elective-modal", "is_open"),
         Output("elective-modal-title", "children"),
         Output("elective-modal-options-container", "children"),
         Output("elective-modal-alert", "children")],
        [Input("open-elective-modal-btn", "n_clicks"),
         Input("open-open-elective-modal-btn", "n_clicks"),
         Input("open-honors-modal-btn", "n_clicks"),
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
         State({"type": "elective-radio-group", "index": ALL}, "id")],
        prevent_initial_call=True
    )
    def handle_elective_modal(pe_clicks, oe_clicks, hn_clicks, cancel_clicks, save_clicks,
                              is_open, college, degree, regulation, branch, specialization, semester,
                              radio_values, radio_ids):
        if not callback_context.triggered:
            return False, no_update, no_update, ""

        triggered_id = callback_context.triggered_id or callback_context.triggered[0]["prop_id"].split(".")[0]

        if triggered_id == "elective-modal-cancel-btn" and cancel_clicks:
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

            if triggered_id == "elective-modal-save-btn":
                if not save_clicks:
                    return False, no_update, no_update, ""
                if radio_values and radio_ids:
                    for val, r_id in zip(radio_values, radio_ids):
                        grp_name = r_id.get("index", "")
                        if val == "__NONE__" or not val:
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

            if triggered_id in ("open-elective-modal-btn", "open-open-elective-modal-btn", "open-honors-modal-btn"):
                clicks = pe_clicks if triggered_id == "open-elective-modal-btn" else (oe_clicks if triggered_id == "open-open-elective-modal-btn" else hn_clicks)
                if not clicks or clicks <= 0:
                    return False, no_update, no_update, ""

                modal_title = f"Select Elective Courses — Semester {sem}"

                options = db.query(ElectiveOption).filter(
                    ElectiveOption.curriculum_id == curr_id,
                    ElectiveOption.semester == sem
                ).all()

                if not options:
                    body = html.Div([
                        dbc.Alert([
                            html.Strong(f"No elective pools scheduled for Semester {sem}."),
                            html.P(f"Under {regulation} {branch} ({specialization}), electives start in Semester 5 (PE I), Semester 6 (PE II & OE I), and Semester 7 (PE III & OE II).", className="small mb-0 mt-2")
                        ], color="info")
                    ])
                    return True, modal_title, body, ""

                groups_dict = {}
                for opt in options:
                    if opt.group_name not in groups_dict:
                        groups_dict[opt.group_name] = []
                    groups_dict[opt.group_name].append(opt)

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
                            "label": html.Span("✕ No Selection / Remove Elective for this Group", className="text-secondary fst-italic small"),
                            "value": "__NONE__"
                        }
                    ] + [
                        {
                            "label": html.Span([
                                html.Span(f"{o.subject_code}", className="badge bg-info bg-opacity-20 text-info fw-bold me-2 mono-font"),
                                html.Span(f"{o.subject_name}", className="fw-semibold text-white me-2"),
                                html.Span(f"{o.credits} Cr", className="badge bg-white bg-opacity-10 border border-white border-opacity-15 text-light mono-font ms-auto")
                            ], className="d-flex align-items-center flex-wrap w-100 py-1"),
                            "value": o.subject_code
                        }
                        for o in opts_list
                    ]

                    elements.append(html.Div([
                        html.Div([
                            html.Div([
                                html.Span("✦ Elective Selection Pool", className="badge bg-warning bg-opacity-15 text-warning border border-warning border-opacity-25 px-3 py-1 mb-2 fw-semibold"),
                                html.H6(f"📁 {g_name} — Select Exactly 1 Course", className="text-white fw-bold mb-1 fs-6")
                            ]),
                            html.Span("● Autonomous Pool", className="preview-card-status-pill mono-font")
                        ], className="d-flex align-items-center justify-content-between flex-wrap mb-3 pb-2 border-bottom border-white border-opacity-10"),

                        dbc.RadioItems(
                            id={"type": "elective-radio-group", "index": g_name},
                            options=radio_options,
                            value=current_selected,
                            className="w-100",
                            inputClassName="me-2 mt-1",
                            labelClassName="w-100 mb-2 p-2 rounded-2 border border-white border-opacity-10 d-block"
                        )
                    ], className="elective-group-card"))

                return True, modal_title, elements, ""

            return False, no_update, no_update, ""
        finally:
            db.close()


    # 4. Marks Entry Modal (Resilient Pattern-Matching Callbacks & Single-Line Layout)
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
         State({"type": "subject-credits-input", "index": ALL}, "value"),
         State({"type": "subject-credits-input", "index": ALL}, "id"),
         State({"type": "custom-mark-sub-code", "index": ALL}, "value"),
         State({"type": "custom-mark-sub-name", "index": ALL}, "value"),
         State({"type": "custom-mark-sub-cat", "index": ALL}, "value"),
         State({"type": "custom-mark-sub-credits", "index": ALL}, "value"),
         State({"type": "custom-mark-sub-gp", "index": ALL}, "value")],
        prevent_initial_call=True
    )
    def handle_marks_modal(open_clicks, cancel_clicks, save_clicks, is_open,
                           college, degree, regulation, branch, specialization, semester,
                           refresh_cnt, gp_values, gp_ids, credit_values, credit_ids,
                           cust_codes, cust_names, cust_cats, cust_credits, cust_gps):
        if not callback_context.triggered:
            return False, no_update, no_update, no_update, refresh_cnt or 0
        
        triggered_id = callback_context.triggered_id or callback_context.triggered[0]["prop_id"].split(".")[0]
        refresh_cnt = refresh_cnt or 0
        
        if triggered_id == "marks-modal-cancel-btn":
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

            # SAVE CLICKED
            if triggered_id == "marks-modal-save-btn":
                if not save_clicks or save_clicks <= 0:
                    return False, no_update, no_update, "", refresh_cnt

                gp_map = {item_id.get("index"): val for item_id, val in zip(gp_ids, gp_values) if item_id} if gp_ids else {}
                credit_map = {item_id.get("index"): val for item_id, val in zip(credit_ids, credit_values) if item_id} if credit_ids else {}

                comp_subjects = db.query(CurriculumSubject).filter(
                    CurriculumSubject.curriculum_id == curr_id,
                    CurriculumSubject.semester == sem,
                    CurriculumSubject.is_compulsory == True
                ).all()

                for s in comp_subjects:
                    raw_gp = gp_map.get(s.subject_code)
                    raw_cr = credit_map.get(s.subject_code)

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

                    cr_val = float(raw_cr) if raw_cr is not None else (s.official_credits or s.credits or 3.0)

                    if gp_val is not None:
                        grd = "O" if gp_val >= 10.0 else ("A+" if gp_val >= 9.0 else ("A" if gp_val >= 8.0 else ("B+" if gp_val >= 7.0 else "B")))
                        if not enr:
                            enr = Enrollment(
                                student_id=sid,
                                curriculum_subject_id=s.id,
                                course_id=s.subject_code,
                                marks_obtained=gp_val * 9.5,
                                grade=grd,
                                grade_letter=grd,
                                grade_point=gp_val,
                                credits_used=cr_val,
                                semester=sem,
                                academic_year="2024-2025"
                            )
                            db.add(enr)
                        else:
                            enr.grade_point = gp_val
                            enr.marks_obtained = gp_val * 9.5
                            enr.grade = grd
                            enr.grade_letter = grd
                            enr.credits_used = cr_val

                custom_selections = db.query(StudentSubjectSelection).filter(
                    StudentSubjectSelection.student_id == sid,
                    StudentSubjectSelection.semester == sem
                ).all()

                for sel in custom_selections:
                    raw_gp = gp_map.get(sel.subject_code)
                    raw_cr = credit_map.get(sel.subject_code)
                    if raw_gp is not None and str(raw_gp).strip() != "":
                        try:
                            gp_val = float(raw_gp)
                            sel.grade_point = gp_val
                            sel.marks = gp_val * 9.5
                            sel.grade = "A+" if gp_val >= 9.0 else "A"
                        except (ValueError, TypeError):
                            pass
                    if raw_cr is not None:
                        try:
                            sel.credits_used = float(raw_cr)
                        except (ValueError, TypeError):
                            pass

                # If custom course entry was filled
                if cust_codes and cust_names:
                    for c_code, c_name, c_cat, c_cr_raw, c_gp_raw in zip(cust_codes, cust_names, cust_cats or [], cust_credits or [], cust_gps or []):
                        if c_code and str(c_code).strip() != "" and c_name and str(c_name).strip() != "":
                            try:
                                c_gp = float(c_gp_raw) if c_gp_raw is not None and str(c_gp_raw).strip() != "" else None
                                c_cr = float(c_cr_raw) if c_cr_raw is not None else 3.0
                                existing_cust = db.query(StudentSubjectSelection).filter(
                                    StudentSubjectSelection.student_id == sid,
                                    StudentSubjectSelection.semester == sem,
                                    StudentSubjectSelection.subject_code == str(c_code).strip().upper()
                                ).first()
                                if not existing_cust:
                                    new_custom_sel = StudentSubjectSelection(
                                        student_id=sid,
                                        curriculum_id=curr_id,
                                        semester=sem,
                                        category=c_cat or "CUSTOM_COURSE",
                                        group_name=c_cat or "Custom Subject",
                                        subject_code=str(c_code).strip().upper(),
                                        subject_name=str(c_name).strip(),
                                        official_credits=c_cr,
                                        credits_used=c_cr,
                                        grade_point=c_gp,
                                        marks=c_gp * 9.5 if c_gp is not None else None,
                                        grade="A+" if c_gp and c_gp >= 9.0 else ("A" if c_gp else None),
                                        credit_source="student_custom",
                                        credit_status="confirmed"
                                    )
                                    db.add(new_custom_sel)
                            except Exception:
                                pass

                db.commit()
                return False, no_update, no_update, "", refresh_cnt + 1

            # OPEN MODAL CLICKED
            if triggered_id == "open-marks-modal-btn":
                if not open_clicks or open_clicks <= 0:
                    return False, no_update, no_update, "", refresh_cnt

                curr_data = CurriculumEngine.get_subjects(db, college, degree, regulation, branch, specialization, sem)
                comp_subs = curr_data["compulsory_subjects"]
                
                custom_selections = db.query(StudentSubjectSelection).filter(
                    StudentSubjectSelection.student_id == sid,
                    StudentSubjectSelection.semester == sem
                ).all()

                cards = []
                
                # Clean Native Transparent Header
                cards.append(html.Div([
                    html.Div([
                        html.Span(f"Semester {sem} Official Evaluation", className="badge bg-info bg-opacity-15 text-info border border-info border-opacity-30 px-3 py-1 me-2 fw-semibold"),
                        html.Span(f"{regulation} Autonomous Scheme", className="badge bg-white bg-opacity-10 text-light border border-white border-opacity-15 px-3 py-1 fw-semibold mono-font")
                    ], className="d-flex align-items-center flex-wrap gap-2 mb-2"),
                    html.P("Enter official Grade Points (0.00 – 10.00) and credits for each course. Your SGPA and cumulative CGPA will recalculate automatically.", className="text-secondary small mb-4")
                ]))

                cards.append(html.Div([
                    html.Span("Core Course Structure", className="badge bg-info bg-opacity-15 text-info border border-info border-opacity-25 px-3 py-1 mb-2 fw-semibold"),
                    html.H6("Institutional Compulsory Courses", className="fw-bold text-white mb-3 fs-6")
                ]))

                # Column Headers for Pixel-Perfect Grid Alignment
                cards.append(html.Div([
                    html.Span("Course Code"),
                    html.Span("Course Title"),
                    html.Span("Credits", className="text-center"),
                    html.Span("Grade (0-10)", className="text-end")
                ], className="modal-table-col-header"))

                for s in comp_subs:
                    enr = db.query(Enrollment).filter(
                        Enrollment.student_id == sid,
                        Enrollment.curriculum_subject_id == s.id
                    ).first()
                    saved_gp = float(enr.grade_point) if (enr and enr.grade_point is not None) else None
                    is_audit = (s.subject_type == "AUDIT_COURSE" or (s.theory_or_lab and s.theory_or_lab.lower() == "audit") or s.credits == 0.0)
                    default_cr = float(enr.credits_used if (enr and enr.credits_used is not None) else (s.credits if s.credits is not None else 3.0))

                    cards.append(html.Div([
                        # 1. Subject Code Badge
                        html.Span(f"{s.subject_code}", className="badge bg-cyan-subtle text-cyan mono-font fw-bold px-2 py-1 text-center"),
                        
                        # 2. Full Subject Name
                        html.Span(f"{s.subject_name}", className="fw-semibold text-white fs-6 text-truncate pe-2"),
                        
                        # 3. Editable Credits Input Field
                        html.Div([
                            dbc.Input(
                                id={"type": "subject-credits-input", "index": s.subject_code},
                                type="number",
                                min=0.0,
                                max=6.0,
                                step=0.5,
                                value=default_cr if not is_audit else 0.0,
                                className="modal-grade-input text-center w-100"
                            )
                        ], className="d-flex justify-content-center"),
                        
                        # 4. Grade Points Input Box
                        html.Div([
                            dbc.Input(
                                id={"type": "subject-gp-input", "index": s.subject_code},
                                type="number",
                                min=0.0,
                                max=10.0,
                                step=0.1,
                                value=saved_gp,
                                placeholder="0.0 - 10.0",
                                className="modal-grade-input text-end w-100"
                            )
                        ], className="d-flex justify-content-end")
                    ], className="modal-grading-grid-card"))

                if custom_selections:
                    cards.append(html.Div([
                        html.Span("Custom Track & Electives", className="badge bg-warning bg-opacity-15 text-warning border border-warning border-opacity-25 px-3 py-1 mt-4 mb-2 fw-semibold"),
                        html.H6("⭐ Selected Elective & Honor Courses", className="fw-bold text-white mb-3 fs-6")
                    ]))

                    # Column Headers for Electives
                    cards.append(html.Div([
                        html.Span("Course Code"),
                        html.Span("Course Title & Pool"),
                        html.Span("Credits", className="text-center"),
                        html.Span("Grade (0-10)", className="text-end")
                    ], className="modal-table-col-header"))

                    for sel in custom_selections:
                        saved_gp = float(sel.grade_point) if (sel and sel.grade_point is not None) else None
                        default_cr = float(sel.credits_used if sel.credits_used is not None else 3.0)

                        cards.append(html.Div([
                            # 1. Subject Code Badge
                            html.Span(f"{sel.subject_code}", className="badge bg-warning bg-opacity-20 text-warning mono-font fw-bold px-2 py-1 text-center"),
                            
                            # 2. Full Subject Name & Group
                            html.Span([
                                html.Span(f"{sel.subject_name}", className="fw-semibold text-white fs-6 me-2"),
                                html.Span(f"[{sel.group_name}]", className="badge bg-secondary bg-opacity-30 text-light small")
                            ], className="text-truncate pe-2"),
                            
                            # 3. Editable Credits Input Field
                            html.Div([
                                dbc.Input(
                                    id={"type": "subject-credits-input", "index": sel.subject_code},
                                    type="number",
                                    min=0.0,
                                    max=6.0,
                                    step=0.5,
                                    value=default_cr,
                                    className="modal-grade-input text-center w-100"
                                )
                            ], className="d-flex justify-content-center"),
                            
                            # 4. Grade Points Input Box
                            html.Div([
                                dbc.Input(
                                    id={"type": "subject-gp-input", "index": sel.subject_code},
                                    type="number",
                                    min=0.0,
                                    max=10.0,
                                    step=0.1,
                                    value=saved_gp,
                                    placeholder="0.0 - 10.0",
                                    className="modal-grade-input text-end w-100"
                                )
                            ], className="d-flex justify-content-end")
                        ], className="modal-grading-grid-card"))

                # Embedded Expandable Custom Subject Builder Form inside Edit Marks
                cards.append(html.Div([
                    html.Div([
                        html.Span("✦ Custom Course Builder", className="badge bg-warning bg-opacity-15 text-warning border border-warning border-opacity-25 px-3 py-1 mb-2 fw-semibold"),
                        html.H6("+ Add Custom Subject / Elective / Minor / Honor", className="fw-bold text-white mb-2 fs-6"),
                        html.P("Type in custom courses or unlisted electives to add directly to your semester marksheet.", className="text-secondary small mb-3")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Course Code", className="profile-micro-label mb-1"),
                            dbc.Input(id={"type": "custom-mark-sub-code", "index": "new"}, placeholder="e.g. 23CS309", className="modal-grade-input w-100")
                        ], lg=3, md=6, xs=12, className="mb-3"),
                        dbc.Col([
                            html.Label("Course Name", className="profile-micro-label mb-1"),
                            dbc.Input(id={"type": "custom-mark-sub-name", "index": "new"}, placeholder="e.g. Cloud Architecture", className="modal-grade-input w-100")
                        ], lg=4, md=6, xs=12, className="mb-3"),
                        dbc.Col([
                            html.Label("Category", className="profile-micro-label mb-1"),
                            dbc.Select(
                                id={"type": "custom-mark-sub-cat", "index": "new"},
                                options=[
                                    {"label": "Professional Elective (PE)", "value": "PROFESSIONAL_ELECTIVE"},
                                    {"label": "Open Elective (OE)", "value": "OPEN_ELECTIVE"},
                                    {"label": "Honors Track", "value": "HONORS"},
                                    {"label": "Minor Track", "value": "MINOR"},
                                    {"label": "Custom Course", "value": "CUSTOM"}
                                ],
                                value="PROFESSIONAL_ELECTIVE",
                                className="preview-form-select w-100"
                            )
                        ], lg=3, md=6, xs=12, className="mb-3"),
                        dbc.Col([
                            html.Label("Credits", className="profile-micro-label mb-1"),
                            dbc.Input(id={"type": "custom-mark-sub-credits", "index": "new"}, type="number", min=1.0, max=6.0, step=0.5, value=3.0, className="modal-grade-input w-100")
                        ], lg=2, md=6, xs=12, className="mb-3"),
                    ], className="g-3 mb-2"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Grade Points (0.00 – 10.00)", className="profile-micro-label mb-1"),
                            dbc.Input(id={"type": "custom-mark-sub-gp", "index": "new"}, type="number", min=0.0, max=10.0, step=0.1, placeholder="e.g. 9.5", className="modal-grade-input w-100")
                        ], lg=4, md=6, xs=12, className="mb-2"),
                        dbc.Col([
                            html.P("Will be saved directly to your transcript when you click 'Save & Recalculate'.", className="text-secondary small mb-0 mt-2 mt-md-4")
                        ], lg=8, md=6, xs=12)
                    ], className="g-3 align-items-center")
                ], className="modal-grading-card mt-4", style={"border": "1px dashed rgba(245, 158, 11, 0.4)", "background": "rgba(0, 0, 0, 0.40)"}))

                modal_title = f"Enter Marks & Grades — Semester {sem}"
                return True, modal_title, cards, "", refresh_cnt

            return False, no_update, no_update, "", refresh_cnt
        finally:
            db.close()


    # 5. Overview Callbacks
    @app.callback(
        [Output("student-kpi-container", "children"),
         Output("student-sgpa-trend-chart", "figure"),
         Output("overview-summary-container", "children")],
        [Input("curriculum-college-select", "value"),
         Input("curriculum-degree-select", "value"),
         Input("curriculum-regulation-select", "value"),
         Input("curriculum-branch-select", "value"),
         Input("curriculum-spec-select", "value"),
         Input("student-semester-dropdown", "value"),
         Input("marks-refresh-trigger", "data")]
    )
    def update_overview_page(college, degree, regulation, branch, specialization, semester, refresh_cnt):
        return update_overview_page_logic(college, degree, regulation, branch, specialization, semester, refresh_cnt)


    # 6. Analytics Callbacks
    @app.callback(
        [Output("student-radar-chart", "figure"),
         Output("student-ai-recommendations-container", "children")],
        [Input("curriculum-college-select", "value"),
         Input("curriculum-degree-select", "value"),
         Input("curriculum-regulation-select", "value"),
         Input("curriculum-branch-select", "value"),
         Input("curriculum-spec-select", "value"),
         Input("student-semester-dropdown", "value"),
         Input("marks-refresh-trigger", "data")]
    )
    def update_analytics_page(college, degree, regulation, branch, specialization, semester, refresh_cnt):
        return update_analytics_page_logic(college, degree, regulation, branch, specialization, semester, refresh_cnt)


    # 7. Marks & Subjects Callback
    @app.callback(
        Output("student-courses-table-container", "children"),
        [Input("curriculum-college-select", "value"),
         Input("curriculum-degree-select", "value"),
         Input("curriculum-regulation-select", "value"),
         Input("curriculum-branch-select", "value"),
         Input("curriculum-spec-select", "value"),
         Input("student-semester-dropdown", "value"),
         Input("marks-refresh-trigger", "data")]
    )
    def update_marks_subjects_page(college, degree, regulation, branch, specialization, semester, refresh_cnt):
        return update_marks_subjects_page_logic(college, degree, regulation, branch, specialization, semester, refresh_cnt)


    # 8. Attendance Callback
    @app.callback(
        [Output("student-attendance-scatter", "figure"),
         Output("attendance-compliance-summary", "children")],
        [Input("curriculum-college-select", "value"),
         Input("curriculum-degree-select", "value"),
         Input("curriculum-regulation-select", "value"),
         Input("curriculum-branch-select", "value"),
         Input("curriculum-spec-select", "value"),
         Input("student-semester-dropdown", "value"),
         Input("marks-refresh-trigger", "data")]
    )
    def update_attendance_page(college, degree, regulation, branch, specialization, semester, refresh_cnt):
        return update_attendance_page_logic(college, degree, regulation, branch, specialization, semester, refresh_cnt)


    # 9. Marksheet Excel Export Handler
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
                    "Status": s.verification_status
                })
            df = pd.DataFrame(data)
            return dcc.send_data_frame(df.to_excel, f"StudIQ_{regulation}_{branch}_Sem{sem}_Marksheet.xlsx", index=False)
        finally:
            db.close()
