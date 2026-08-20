"""
Faculty Dashboard Layout and Visualizations.
Provides class performance heatmaps, at-risk early warnings, grade distributions, and drill-downs.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from app.dashboards.components import create_kpi_card, create_export_controls


def build_faculty_dashboard_layout():
    """Constructs the multi-faceted Faculty Dashboard layout."""
    return dbc.Container([
        # Faculty Filter Bar
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("DEPARTMENT", className="fw-bold small text-secondary", style={"letterSpacing": "0.06em", "fontSize": "0.75rem"}),
                        dcc.Dropdown(
                            id="faculty-dept-dropdown",
                            placeholder="All Departments",
                            clearable=True,
                            className="dash-dropdown"
                        )
                    ], md=3, xs=12),
                    dbc.Col([
                        html.Label("SEMESTER", className="fw-bold small text-secondary", style={"letterSpacing": "0.06em", "fontSize": "0.75rem"}),
                        dcc.Dropdown(
                            id="faculty-sem-dropdown",
                            placeholder="All Semesters",
                            clearable=True,
                            className="dash-dropdown"
                        )
                    ], md=3, xs=6),
                    dbc.Col([
                        html.Label("RISK STATUS", className="fw-bold small text-secondary", style={"letterSpacing": "0.06em", "fontSize": "0.75rem"}),
                        dcc.Dropdown(
                            id="faculty-risk-filter",
                            options=[
                                {"label": "All Students", "value": "ALL"},
                                {"label": "High Risk Only (🚨)", "value": "HIGH"},
                                {"label": "Medium Risk (⚠️)", "value": "MEDIUM"},
                                {"label": "Low Risk (✅)", "value": "LOW"}
                            ],
                            value="ALL",
                            clearable=False,
                            className="dash-dropdown"
                        )
                    ], md=3, xs=6),
                    dbc.Col([
                        html.Label("EXPORT REPORT", className="fw-bold small text-secondary", style={"letterSpacing": "0.06em", "fontSize": "0.75rem"}),
                        html.Div(create_export_controls("faculty"), className="mt-1")
                    ], md=3, xs=12, className="d-flex flex-column justify-content-end align-items-md-end")
                ], className="g-3 align-items-center")
            ], className="p-3")
        ], className="card mb-4"),

        # Faculty Class KPIs
        html.Div(id="faculty-kpi-container", children=[
            dbc.Row([
                dbc.Col(create_kpi_card("Batch Mean CGPA", "...", "Scale 10.0", "primary", "🏛️"), md=3, xs=6),
                dbc.Col(create_kpi_card("Overall Pass Rate", "...", "Threshold >= 40%", "success", "✅"), md=3, xs=6),
                dbc.Col(create_kpi_card("At-Risk Students", "...", "Urgent Attention", "danger", "🚨"), md=3, xs=6),
                dbc.Col(create_kpi_card("Average Attendance", "...", "Class-wide Mean", "info", "📊"), md=3, xs=6),
            ], className="mb-3")
        ]),

        # Row 1: Class Performance Heatmap & Grade Distribution Histogram
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("🗺️", className="me-2 fs-5"),
                        html.Span("Department & Semester Grade Heatmap", className="fw-bold text-white fs-6")
                    ], className="d-flex align-items-center"),
                    dbc.CardBody([
                        dcc.Loading(dcc.Graph(id="faculty-heatmap-chart", config={"displayModeBar": False})),
                        html.Div([
                            html.Strong("Heatmap Interpretation: "),
                            "Color intensity indicates average marks. Darker/saturated tiles highlight bottleneck semesters requiring curricular adjustments."
                        ], className="desc-callout")
                    ], className="p-3")
                ], className="card mb-4 h-100")
            ], lg=7, xs=12),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Span("📊", className="me-2 fs-5"),
                        html.Span("Grade Distribution Spread Histogram", className="fw-bold text-white fs-6")
                    ], className="d-flex align-items-center"),
                    dbc.CardBody([
                        dcc.Loading(dcc.Graph(id="faculty-grade-histogram", config={"displayModeBar": False})),
                        html.Div([
                            html.Strong("Bell Curve: "),
                            "Bars show the frequency of letter grades. Right-skewed spreads reflect high achievement; clusters in F/P indicate difficulty."
                        ], className="desc-callout")
                    ], className="p-3")
                ], className="card mb-4 h-100")
            ], lg=5, xs=12)
        ], className="mb-3"),

        # Row 2: Early Warning At-Risk Student Alert Table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col([
                                html.Span("🚨", className="me-2 fs-5"),
                                html.Span("Early Warning System: Intervention Targets", className="fw-bold text-white fs-6")
                            ], md=8, className="d-flex align-items-center"),
                            dbc.Col(
                                dbc.Button("🔔 Dispatch Alerts", id="btn-dispatch-alerts", color="danger", size="sm", className="float-end fw-bold rounded-pill px-3"),
                                md=4
                            )
                        ], className="align-items-center")
                    ]),
                    dbc.CardBody([
                        html.Div(id="faculty-alert-toast-container"),
                        html.Div(id="faculty-at-risk-table-container"),
                        html.Div([
                            html.Strong("Early Warning: "),
                            "XGBoost identifies students with degraded attendance (<65%) or failing trajectory 4-6 weeks prior to final examinations."
                        ], className="desc-callout mt-3")
                    ], className="p-3")
                ], className="card mb-4")
            ], xs=12)
        ]),

        # Drill-down Student Details Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("👤 Detailed Student Academic Profile", className="fw-bold")),
            dbc.ModalBody(id="faculty-student-modal-body"),
            dbc.ModalFooter(
                dbc.Button("Close", id="btn-close-faculty-modal", className="ms-auto", n_clicks=0)
            )
        ], id="faculty-student-drilldown-modal", size="lg", is_open=False),

        # Hidden downloads
        dcc.Download(id="download-faculty-excel"),
        dcc.Download(id="download-faculty-pdf")
    ], fluid=True, className="px-4 pb-5")
