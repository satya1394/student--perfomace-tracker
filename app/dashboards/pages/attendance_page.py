"""
StudIQ - Attendance Tracking & Exam Eligibility (100% Full-Width Layout)
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def build_attendance_page():
    """Builds the clean, structured Attendance subpage with elite spacing."""
    return html.Div([
        dbc.Row([
            # Left: Course-wise Attendance Bars (7 Cols)
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Span("⏱️", className="me-2", style={"fontSize": "1.1rem"}),
                                html.Span("Course-wise Attendance Tracking", className="fw-bold text-white", style={"fontSize": "1rem", "letterSpacing": "-0.01em"}),
                            ], className="d-flex align-items-center mb-1"),
                            html.P(
                                "Subject attendance percentages vs 75% Statutory Autonomous Cutoff",
                                className="text-secondary small mb-0 mt-1",
                                style={"lineHeight": "1.4", "color": "#94A3B8"}
                            )
                        ], className="d-flex flex-column pe-3"),
                        html.Span("● 75% Statutory Threshold", className="preview-card-status-pill mono-font flex-shrink-0")
                    ], className="preview-card-top-header mb-4 pb-3",
                       style={"display": "flex", "alignItems": "flex-start", "justifyContent": "space-between", "borderBottom": "1px solid rgba(255, 255, 255, 0.08)"}),

                    dcc.Loading(
                        id="loading-student-attendance-scatter",
                        type="dot",
                        children=dcc.Graph(
                            id="student-attendance-scatter",
                            config={"displayModeBar": False, "responsive": True},
                            style={"height": "350px"}
                        )
                    )
                ], className="cockpit-preview-container-card p-4 p-md-5 h-100 mb-4 mb-lg-0",
                   style={"background": "rgba(0, 0, 0, 0.50)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "16px"})
            ], lg=7, xs=12),

            # Right: Hall Ticket & Eligibility Status (5 Cols)
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Span("📜", className="me-2", style={"fontSize": "1.1rem"}),
                                html.Span("Examination Eligibility & Hall Ticket", className="fw-bold text-white", style={"fontSize": "1rem", "letterSpacing": "-0.01em"}),
                            ], className="d-flex align-items-center mb-1"),
                            html.P(
                                "University condonation rules and statutory hall ticket qualification",
                                className="text-secondary small mb-0 mt-1",
                                style={"lineHeight": "1.4", "color": "#94A3B8"}
                            )
                        ], className="d-flex flex-column pe-3"),
                        html.Span("● Regulatory Compliance", className="preview-card-status-pill mono-font flex-shrink-0")
                    ], className="preview-card-top-header mb-4 pb-3",
                       style={"display": "flex", "alignItems": "flex-start", "justifyContent": "space-between", "borderBottom": "1px solid rgba(255, 255, 255, 0.08)"}),

                    dcc.Loading(
                        id="loading-attendance-compliance",
                        type="dot",
                        children=html.Div(id="attendance-compliance-summary")
                    )
                ], className="cockpit-preview-container-card p-4 p-md-5 h-100",
                   style={"background": "rgba(0, 0, 0, 0.50)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "16px"})
            ], lg=5, xs=12)
        ], className="g-4 w-100 m-0")
    ], className="w-100")
