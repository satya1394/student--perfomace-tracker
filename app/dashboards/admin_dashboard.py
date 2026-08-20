"""
Admin Dashboard Layout and Institutional Visualizations.
Provides macro-level institutional KPIs, department benchmarks, cohort analytics, and audit logging.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from app.dashboards.components import create_kpi_card, create_export_controls


def build_admin_dashboard_layout():
    """Renders the executive-level Administrator Dashboard."""
    return dbc.Container([
        # Admin Header & Export Strip
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Span("🏛️", className="fs-3 me-2"),
                            html.Span("Institutional Analytics & Executive Governance", className="fw-bold fs-4 text-white")
                        ], className="d-flex align-items-center mb-1"),
                        html.P("Executive overview across all academic programs, cohorts, and accreditation benchmarks.", className="text-secondary small mb-0")
                    ], md=8, xs=12),
                    dbc.Col([
                        html.Div(create_export_controls("admin"), className="mt-1")
                    ], md=4, xs=12, className="d-flex justify-content-md-end align-items-center mt-2 mt-md-0")
                ])
            ], className="p-3")
        ], className="card mb-4"),

        # Executive KPIs
        html.Div(id="admin-kpi-container", children=[
            dbc.Row([
                dbc.Col(create_kpi_card("Total Enrolled Students", "...", "All Departments", "primary", "👥"), md=3, xs=6),
                dbc.Col(create_kpi_card("Institute Average CGPA", "...", "Benchmark: 7.0", "info", "🌟"), md=3, xs=6),
                dbc.Col(create_kpi_card("Annual Retention Rate", "...", "YoY Academic Retention", "success", "📈"), md=3, xs=6),
                dbc.Col(create_kpi_card("Accreditation Health Index", "98.4%", "Tier-1 Compliance", "warning", "🏆"), md=3, xs=6),
            ], className="mb-3")
        ]),

        # Row 1: Department Comparisons & Enrollment Cohort Trends
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("📊", className="me-2 fs-5"),
                        html.Span("Department Comparative CGPA & Benchmark", className="fw-bold text-white fs-6")
                    ], className="d-flex align-items-center"),
                    dbc.CardBody([
                        dcc.Loading(dcc.Graph(id="admin-dept-comparison-chart", config={"displayModeBar": False})),
                        html.Div([
                            html.Strong("Comparative Insights: "),
                            "Compares overall academic achievement across engineering disciplines to assist dean-level resource allocation."
                        ], className="desc-callout")
                    ], className="p-3")
                ], className="card mb-4 h-100")
            ], lg=6, xs=12),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("📉", className="me-2 fs-5"),
                        html.Span("Cohort Progression & Retention Trend", className="fw-bold text-white fs-6")
                    ], className="d-flex align-items-center"),
                    dbc.CardBody([
                        dcc.Loading(dcc.Graph(id="admin-cohort-trend-chart", config={"displayModeBar": False})),
                        html.Div([
                            html.Strong("Longitudinal Tracking: "),
                            "Tracks semester-over-semester marks to detect systemic drop-offs across class cohorts."
                        ], className="desc-callout")
                    ], className="p-3")
                ], className="card mb-4 h-100")
            ], lg=6, xs=12)
        ], className="mb-3"),

        # Row 2: Audit Trail Log Table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("🛡️", className="me-2 fs-5"),
                        html.Span("System Security & Academic Audit Trail", className="fw-bold text-white fs-6")
                    ], className="d-flex align-items-center"),
                    dbc.CardBody([
                        html.Div(id="admin-audit-log-table-container"),
                        html.Div([
                            html.Strong("Compliance Trail: "),
                            "Cryptographically logs all authentication events, grade alterations, and ML predictions."
                        ], className="desc-callout mt-3")
                    ], className="p-3")
                ], className="card mb-4")
            ], xs=12)
        ]),

        # Hidden downloads
        dcc.Download(id="download-admin-excel"),
        dcc.Download(id="download-admin-pdf")
    ], fluid=True, className="px-4 pb-5")
