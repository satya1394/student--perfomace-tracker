"""
StudIQ - Overview Page (100% Full-Width Balanced Grid Layout)
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def build_overview_page():
    """Builds the clean, structured Overview subpage with full-width 4-column metric grid."""
    return html.Div([
        # 1. Full-Width Balanced 4-Column Key Performance Metrics Grid
        dcc.Loading(
            id="loading-student-kpi",
            type="dot",
            className="w-100",
            style={"width": "100%", "display": "block"},
            parent_style={"width": "100%", "display": "block"},
            children=html.Div(id="student-kpi-container", className="kpi-grid-cols-4 w-100")
        ),

        # 2. Main Analytics & Standing Bento Grid (2 Columns)
        dbc.Row([
            # Left: SGPA Progression Spline Chart (8 Cols)
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("📈 Semester SGPA & CGPA Velocity", className="preview-card-heading"),
                            html.P("Multi-term progression spline vs 8.00 Distinction threshold", className="text-secondary small mb-0 mt-1")
                        ]),
                        html.Span("● 8.00 Distinction Marker", className="preview-card-status-pill mono-font")
                    ], className="preview-card-top-header"),

                    dcc.Loading(
                        id="loading-student-sgpa-trend-chart",
                        type="dot",
                        children=dcc.Graph(
                            id="student-sgpa-trend-chart",
                            config={"displayModeBar": False, "responsive": True},
                            style={"height": "320px"}
                        )
                    )
                ], className="cockpit-preview-container-card h-100 mb-4 mb-lg-0")
            ], lg=8, xs=12),

            # Right: Academic Standing & Credits Summary (4 Cols)
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("🏛️ Academic Standing & Credits", className="preview-card-heading"),
                            html.P("Regulation compliance & credit summary", className="text-secondary small mb-0 mt-1")
                        ]),
                        html.Span("● Verified", className="preview-card-status-pill mono-font")
                    ], className="preview-card-top-header"),

                    dcc.Loading(
                        id="loading-overview-summary",
                        type="dot",
                        children=html.Div(id="overview-summary-container")
                    )
                ], className="cockpit-preview-container-card h-100")
            ], lg=4, xs=12)
        ], className="g-4 w-100 m-0")
    ], className="w-100")
