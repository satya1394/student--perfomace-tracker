"""
StudIQ - Performance Analytics & AI Study Roadmap (SVG Gradient Chart Layout)
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def build_analytics_page():
    """Builds the clean, structured Analytics subpage with SVG LinearGradient definitions."""
    return html.Div([
        # Hidden SVG Definitions for True Vertical Bar Gradients
        html.Div([
            html.Iframe(
                srcDoc='''
                <svg width="0" height="0" style="position:absolute;display:none;">
                  <defs>
                    <linearGradient id="bar-vertical-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="#38BDF8" stop-opacity="1" />
                      <stop offset="60%" stop-color="#3B82F6" stop-opacity="0.9" />
                      <stop offset="100%" stop-color="#1E1B4B" stop-opacity="0.8" />
                    </linearGradient>
                  </defs>
                </svg>
                ''',
                style={"display": "none"}
            )
        ], style={"display": "none"}),

        dbc.Row([
            # Left: Subject Competency & Mastery (7 Cols)
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("🎯 Subject Mastery & Grade Point Spread", className="preview-card-heading"),
                            html.P("Course-by-course performance vs 8.0 Distinction benchmark", className="text-secondary small mb-0 mt-1")
                        ]),
                        html.Span("● 10.0 GP Scale", className="preview-card-status-pill mono-font")
                    ], className="preview-card-top-header"),

                    dcc.Loading(
                        id="loading-student-radar-chart",
                        type="dot",
                        children=dcc.Graph(
                            id="student-radar-chart",
                            config={"displayModeBar": False, "responsive": True},
                            style={"height": "340px"}
                        )
                    )
                ], className="cockpit-preview-container-card h-100 mb-4 mb-lg-0")
            ], lg=7, xs=12),

            # Right: AI Study Roadmap (5 Cols)
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span("⚡ AI Study Roadmap & Priority Actions", className="preview-card-heading"),
                            html.P("Automated mastery analysis & target grade guidance", className="text-secondary small mb-0 mt-1")
                        ]),
                        html.Span("● AI Generated", className="preview-card-status-pill mono-font")
                    ], className="preview-card-top-header"),

                    dcc.Loading(
                        id="loading-student-ai-recommendations",
                        type="dot",
                        children=html.Div(id="student-ai-recommendations-container")
                    )
                ], className="cockpit-preview-container-card h-100")
            ], lg=5, xs=12)
        ], className="g-4 w-100 m-0")
    ], className="w-100")
