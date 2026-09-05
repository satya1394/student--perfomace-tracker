"""
StudIQ - Academic Profile (Multi-Column Grid Architecture)
"""

from dash import html
import dash_bootstrap_components as dbc
from flask import session, has_request_context
from flask_login import current_user
from app.database import get_db_session, Student


def build_academic_profile_page():
    """Builds the structured multi-column Academic Profile subpage."""
    sid = (session.get("student_id") if has_request_context() else None) or getattr(current_user, "student_id", None) or "STU2024001"
    
    db = get_db_session()
    try:
        student = db.query(Student).filter(Student.student_id == sid).first()
        name = student.name if student else "Rahul Kumar"
        email = student.email if student else "rahul.kumar@raghuengg.edu"
        roll = getattr(student, "student_id", None) or sid
        col_name = (student.college_name if student else None) or "Raghu Engineering College (Autonomous)"
        reg_name = (student.regulation_name if student else None) or "AR23 Autonomous Framework"
        br_name = (student.branch_name if student else None) or "Computer Science & Engineering"
    finally:
        db.close()

    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Span("🎓 Verified Student Academic Profile", className="preview-card-heading"),
                    html.P("Institutional credentials, regulation governance, and department affiliation", className="text-secondary small mb-0 mt-1")
                ]),
                html.Span("● Enrolled & Verified", className="preview-card-status-pill mono-font")
            ], className="preview-card-top-header mb-4"),

            # 6-Card Responsive CSS Grid (grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6)
            html.Div([
                # 1. Full Name
                html.Div([
                    html.Span("STUDENT FULL NAME", className="profile-micro-label"),
                    html.H5(name, className="profile-micro-value text-white")
                ], className="profile-micro-card", style={"background": "rgba(0, 0, 0, 0.45)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "14px", "padding": "20px 22px"}),

                # 2. Roll / ID
                html.Div([
                    html.Span("REGISTRATION / ROLL ID", className="profile-micro-label"),
                    html.H5(roll, className="profile-micro-value text-info mono-font")
                ], className="profile-micro-card", style={"background": "rgba(0, 0, 0, 0.45)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "14px", "padding": "20px 22px"}),

                # 3. Institutional Email
                html.Div([
                    html.Span("INSTITUTIONAL EMAIL", className="profile-micro-label"),
                    html.H5(email, className="profile-micro-value text-white text-truncate")
                ], className="profile-micro-card", style={"background": "rgba(0, 0, 0, 0.45)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "14px", "padding": "20px 22px"}),

                # 4. Affiliated College
                html.Div([
                    html.Span("AFFILIATED INSTITUTION", className="profile-micro-label"),
                    html.H5(col_name, className="profile-micro-value text-white")
                ], className="profile-micro-card", style={"background": "rgba(0, 0, 0, 0.45)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "14px", "padding": "20px 22px"}),

                # 5. Regulation
                html.Div([
                    html.Span("REGULATORY MODEL", className="profile-micro-label"),
                    html.H5(reg_name, className="profile-micro-value text-warning mono-font")
                ], className="profile-micro-card", style={"background": "rgba(0, 0, 0, 0.45)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "14px", "padding": "20px 22px"}),

                # 6. Branch / Department
                html.Div([
                    html.Span("DEPARTMENT & BRANCH", className="profile-micro-label"),
                    html.H5(br_name, className="profile-micro-value text-white")
                ], className="profile-micro-card", style={"background": "rgba(0, 0, 0, 0.45)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "14px", "padding": "20px 22px"}),
            ], className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 profile-cards-grid",
               style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(280px, 1fr))", "gap": "20px", "width": "100%"})
        ], className="cockpit-preview-container-card p-4 p-md-5",
           style={"background": "rgba(0, 0, 0, 0.50)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "16px"})
    ], className="w-100")
