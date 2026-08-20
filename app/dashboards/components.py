"""
Reusable UI Components and Layout Elements.
Bioluminescent Vector Flows & Celestial Surrealism.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def get_bioluminescent_svg(icon_type: str, color_hex: str = "#06B6D4"):
    """Renders a modern, luxury bioluminescent SVG vector graphic."""
    if icon_type == "cgpa":
        # Bioluminescent Trend Vector Flow
        return html.Div(
            html.Img(src=f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23{color_hex.lstrip('#')}' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='M3 3v18h18'/><path d='m7 15 4-4 4 4 6-6'/><circle cx='21' cy='9' r='2' fill='%23{color_hex.lstrip('#')}'/></svg>",
                     style={"width": "26px", "height": "26px"}),
            className="kpi-vector-badge",
            style={"boxShadow": f"0 0 16px {color_hex}40", "borderColor": f"{color_hex}60"}
        )
    elif icon_type == "sgpa":
        # Bioluminescent Orbital Target
        return html.Div(
            html.Img(src=f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23{color_hex.lstrip('#')}' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><circle cx='12' cy='12' r='6'/><circle cx='12' cy='12' r='2' fill='%23{color_hex.lstrip('#')}'/></svg>",
                     style={"width": "26px", "height": "26px"}),
            className="kpi-vector-badge",
            style={"boxShadow": f"0 0 16px {color_hex}40", "borderColor": f"{color_hex}60"}
        )
    elif icon_type == "attendance":
        # Bioluminescent Chrono Pulse Matrix
        return html.Div(
            html.Img(src=f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23{color_hex.lstrip('#')}' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><rect width='18' height='18' x='3' y='4' rx='2' ry='2'/><line x1='16' x2='16' y1='2' y2='6'/><line x1='8' x2='8' y1='2' y2='6'/><line x1='3' x2='21' y1='10' y2='10'/><circle cx='12' cy='15' r='2' fill='%23{color_hex.lstrip('#')}'/></svg>",
                     style={"width": "26px", "height": "26px"}),
            className="kpi-vector-badge",
            style={"boxShadow": f"0 0 16px {color_hex}40", "borderColor": f"{color_hex}60"}
        )
    elif icon_type == "forecast" or icon_type == "ai":
        # Bioluminescent Neural Core Synapse
        return html.Div(
            html.Img(src=f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23{color_hex.lstrip('#')}' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83'/><circle cx='12' cy='12' r='3' fill='%23{color_hex.lstrip('#')}'/></svg>",
                     style={"width": "26px", "height": "26px"}),
            className="kpi-vector-badge",
            style={"boxShadow": f"0 0 16px {color_hex}40", "borderColor": f"{color_hex}60"}
        )
    elif icon_type == "risk":
        # Bioluminescent Alert Pulse Vector
        return html.Div(
            html.Img(src=f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23{color_hex.lstrip('#')}' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z'/><line x1='12' x2='12' y1='9' y2='13'/><line x1='12' x2='12.01' y1='17' y2='17'/></svg>",
                     style={"width": "26px", "height": "26px"}),
            className="kpi-vector-badge",
            style={"boxShadow": f"0 0 16px {color_hex}40", "borderColor": f"{color_hex}60"}
        )
    elif icon_type == "pass":
        # Bioluminescent Shield Vector
        return html.Div(
            html.Img(src=f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23{color_hex.lstrip('#')}' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/><path d='m9 12 2 2 4-4'/></svg>",
                     style={"width": "26px", "height": "26px"}),
            className="kpi-vector-badge",
            style={"boxShadow": f"0 0 16px {color_hex}40", "borderColor": f"{color_hex}60"}
        )
    else:
        # Default Astral Vector Flow
        return html.Div(
            html.Img(src=f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23{color_hex.lstrip('#')}' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><path d='m10 15 5-3-5-3v6Z'/></svg>",
                     style={"width": "26px", "height": "26px"}),
            className="kpi-vector-badge",
            style={"boxShadow": f"0 0 16px {color_hex}40", "borderColor": f"{color_hex}60"}
        )


def create_navbar(current_user=None):
    """Generates a high-end, floating BetterStack-inspired Student Dock Navigation Bar."""
    from app.database import get_db_session, Student
    from flask import session, has_request_context
    
    is_demo = session.get("is_demo", False) if has_request_context() else False
    username = getattr(current_user, "username", "Guest") if current_user else "Guest"

    # Static Profile Badge Query
    student_profile_badge = None
    sid = (session.get("student_id") if has_request_context() else None) or getattr(current_user, "student_id", None) or "2024CSE001"
    db = get_db_session()
    try:
        s_obj = db.query(Student).filter(Student.student_id == sid).first() if sid else db.query(Student).first()
        if s_obj:
            s_name = s_obj.name
            s_roll = s_obj.student_id
            s_spec = s_obj.specialization or s_obj.department
            badge_text = f"{s_roll} - {s_name} | {s_spec}"
            student_profile_badge = html.Div([
                html.Span("🎓", className="me-2", style={"fontSize": "1rem"}),
                html.Span(badge_text, style={
                    "fontWeight": "700",
                    "fontSize": "0.85rem",
                    "color": "#FFFFFF",
                    "letterSpacing": "0.02em",
                    "whiteSpace": "nowrap",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                    "maxWidth": "460px"
                })
            ], className="d-none d-lg-flex align-items-center px-3 py-1 rounded-pill mx-2 flex-nowrap",
               style={
                   "background": "rgba(17, 24, 39, 0.95)",
                   "border": "1px solid rgba(0, 240, 255, 0.4)",
                   "boxShadow": "0 0 16px rgba(0, 240, 255, 0.2)",
                   "whiteSpace": "nowrap",
                   "flexShrink": "0"
               })
    finally:
        db.close()

    return html.Div([
        dbc.Container([
            html.Div([
                # Left: StudIQ Brand
                html.A([
                    html.Div("⚡", className="celestial-orb"),
                    html.Div([
                        html.Span("StudIQ", className="celestial-title"),
                        html.Span(" ✦", style={"color": "#00F0FF", "fontWeight": "800", "fontSize": "1.1rem", "marginLeft": "4px"})
                    ])
                ], href="/", className="celestial-brand me-3 flex-shrink-0"),

                # Center: Profile Pill
                html.Div(student_profile_badge, className="d-flex justify-content-center flex-grow-1 overflow-hidden") if student_profile_badge else html.Div(className="me-auto"),

                # Right: Actions (Add Marks, Download, Sign Out)
                html.Div([
                    dbc.Button(
                        "✦ Add / Edit My Marks", 
                        id="open-marks-modal-btn", 
                        className="btn-gradient me-2 flex-shrink-0", 
                        size="sm"
                    ),
                    html.A(
                        "Sign Out" if not is_demo else "Exit Demo", 
                        href="/logout", 
                        className="btn-neon flex-shrink-0 text-decoration-none",
                        style={"padding": "6px 14px", "fontSize": "0.8rem"}
                    )
                ], className="d-flex align-items-center ms-auto flex-shrink-0 gap-2")
            ], className="celestial-dock d-flex align-items-center justify-content-between flex-nowrap")
        ], fluid=True, style={"maxWidth": "1380px"})
    ], className="celestial-navbar-container")


def create_kpi_card(title: str, value: str, subtitle: str, color_class: str = "primary", icon_type: str = "cgpa"):
    """Generates a luminous Bioluminescent Vector Flow KPI card with descriptive breakdown."""
    accent_color = "#06B6D4"
    accent_gradient = "linear-gradient(90deg, #06B6D4, #8B5CF6)"
    
    if color_class == "success":
        accent_color = "#10B981"
        accent_gradient = "linear-gradient(90deg, #10B981, #34D399)"
    elif color_class == "danger":
        accent_color = "#F43F5E"
        accent_gradient = "linear-gradient(90deg, #F43F5E, #FB7185)"
    elif color_class == "warning":
        accent_color = "#F59E0B"
        accent_gradient = "linear-gradient(90deg, #F59E0B, #FBBF24)"
    elif color_class == "info":
        accent_color = "#8B5CF6"
        accent_gradient = "linear-gradient(90deg, #8B5CF6, #A78BFA)"

    return html.Div([
        html.Div(className="kpi-bio-indicator", style={"background": accent_gradient, "boxShadow": f"0 0 12px {accent_color}60"}),
        dbc.Row([
            dbc.Col([
                html.Div(title, className="kpi-bio-label"),
                html.Div(value, className="kpi-bio-val"),
                html.Div(subtitle, className="kpi-bio-desc")
            ], xs=8),
            dbc.Col([
                get_bioluminescent_svg(icon_type, accent_color)
            ], xs=4, className="d-flex align-items-center justify-content-end")
        ], className="align-items-center")
    ], className="kpi-bio-card h-100")


def create_risk_badge(risk_level: str):
    """Renders a bioluminescent status pill badge."""
    risk_level = str(risk_level).upper()
    if risk_level == "HIGH":
        return html.Span("🚨 High Risk", style={
            "background": "rgba(244, 63, 94, 0.18)",
            "color": "#FDA4AF",
            "border": "1px solid rgba(244, 63, 94, 0.45)",
            "padding": "4px 12px",
            "borderRadius": "9999px",
            "fontSize": "0.75rem",
            "fontWeight": "700",
            "boxShadow": "0 0 10px rgba(244, 63, 94, 0.3)"
        })
    elif risk_level == "MEDIUM":
        return html.Span("⚠️ Medium Risk", style={
            "background": "rgba(245, 158, 11, 0.18)",
            "color": "#FDE68A",
            "border": "1px solid rgba(245, 158, 11, 0.45)",
            "padding": "4px 12px",
            "borderRadius": "9999px",
            "fontSize": "0.75rem",
            "fontWeight": "700",
            "boxShadow": "0 0 10px rgba(245, 158, 11, 0.3)"
        })
    else:
        return html.Span("✅ Low Risk", style={
            "background": "rgba(16, 185, 129, 0.18)",
            "color": "#A7F3D0",
            "border": "1px solid rgba(16, 185, 129, 0.45)",
            "padding": "4px 12px",
            "borderRadius": "9999px",
            "fontSize": "0.75rem",
            "fontWeight": "700",
            "boxShadow": "0 0 10px rgba(16, 185, 129, 0.3)"
        })


def create_export_controls(export_prefix: str = "report"):
    """Download controls with celestial styling."""
    return html.Div([
        dbc.Button([
            html.Span("✦ ", className="me-1"),
            "Excel"
        ], id=f"{export_prefix}-btn-excel", className="btn-celestial-outline me-2", size="sm"),
        dbc.Button([
            html.Span("✦ ", className="me-1"),
            "PDF"
        ], id=f"{export_prefix}-btn-pdf", className="btn-celestial", size="sm"),
    ], className="d-flex")
