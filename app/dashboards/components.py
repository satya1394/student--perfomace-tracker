"""
Reusable UI Components for StudIQ Dashboard.
Framer Liquid Glass Navbar Component & KPI Cards.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from flask import session, has_request_context
from flask_login import current_user

from app.database import get_db_session, Student, College, Regulation, Branch


def create_navbar(user=None):
    """
    Creates the Framer Superellipse Liquid Glass Navbar.
    """
    is_demo = session.get("is_demo", False) if has_request_context() else False
    
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
                html.Div([
                    dcc.Link("Overview", href="/app/overview", className="framer-nav-link active", id="framer-tab-overview"),
                    dcc.Link("Analytics", href="/app/analytics", className="framer-nav-link", id="framer-tab-analytics"),
                    dcc.Link("Marks & Subjects", href="/app/marks-subjects", className="framer-nav-link", id="framer-tab-marks"),
                    dcc.Link("Attendance", href="/app/attendance", className="framer-nav-link", id="framer-tab-attendance"),
                    dcc.Link("Academic Profile", href="/app/academic-profile", className="framer-nav-link", id="framer-tab-profile"),
                    dcc.Link("Settings", href="/app/settings", className="framer-nav-link", id="framer-tab-settings"),
                ], className="framer-nav-links"),

                # Right: Liquid Glass CTA Button
                html.A(
                    "Exit Demo" if is_demo else "Sign Out",
                    href="/logout",
                    className="framer-glass-cta"
                )
            ], className="framer-liquid-glass-inner")
        ], className="framer-liquid-glass-nav")
    ], className="framer-navbar-outer-wrapper")


def create_kpi_card(title: str, value: str, subtitle: str, color_class: str = "primary", icon_type: str = "cgpa"):
    """Generates a luminous liquid-metal stat summary card."""
    pill_class = "kpi-trend-pill--cyan"
    orb_emoji = "📊"

    if color_class == "success" or icon_type == "attendance":
        pill_class = "kpi-trend-pill--green"
        orb_emoji = "⏱️"
    elif color_class == "warning" or icon_type == "forecast":
        pill_class = "kpi-trend-pill--amber"
        orb_emoji = "⚡"
    elif color_class == "danger":
        pill_class = "kpi-trend-pill--rose"
        orb_emoji = "⚠️"
    elif color_class == "primary" or icon_type == "cgpa":
        pill_class = "kpi-trend-pill--purple"
        orb_emoji = "🏆"
    elif color_class == "info" or icon_type == "sgpa":
        pill_class = "kpi-trend-pill--cyan"
        orb_emoji = "📈"

    return html.Div([
        html.Div([
            html.Span(title, className="kpi-title"),
            html.Div(orb_emoji, className="kpi-orb")
        ], className="kpi-header-row"),
        html.Div(value, className="kpi-value-num mono-font"),
        html.Div([
            html.Span(subtitle, className="small fw-semibold")
        ], className="kpi-trend-pill " + pill_class)
    ], className="luxury-kpi-card")


def create_risk_badge(risk_level: str):
    """Generates standardized academic standing badge."""
    level = (risk_level or "LOW").upper()
    if level == "HIGH":
        return dbc.Badge("⚠️ Critical Attention Required", color="danger", className="px-3 py-1 fs-6 fw-semibold")
    elif level == "MEDIUM":
        return dbc.Badge("⚡ Performance Enhancement", color="warning", className="px-3 py-1 fs-6 fw-semibold text-dark")
    return dbc.Badge("✓ High Academic Standing", color="success", className="px-3 py-1 fs-6 fw-semibold")


def create_export_controls(prefix: str = "student"):
    """Generates clean data export controls."""
    return html.Div([
        dbc.Button("📥 Excel Export", id=f"export-{prefix}-excel-btn", className="btn-celestial-outline btn-sm"),
    ], className="d-inline-flex align-items-center")
