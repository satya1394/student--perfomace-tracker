"""
StudIQ - Student Settings & Data Preferences (High-Clarity Layout)
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def build_settings_page():
    """Builds the clean, structured Settings subpage with zero button overlaps."""
    return html.Div([
        dbc.Row([
            # Card 1: Session & Authentication Controls
            dbc.Col([
                html.Div([
                    # Header
                    html.Div([
                        html.Span("🔐 Session & Authentication", className="preview-card-heading"),
                        html.Span("● Secure Active", className="preview-card-status-pill mono-font")
                    ], className="preview-card-top-header mb-3"),

                    # Description Text
                    html.P(
                        "Manage your active student authentication tokens, credentials, and secure login sessions.",
                        className="text-secondary small mb-3",
                        style={"lineHeight": "1.5"}
                    ),

                    # Authenticated Session Box
                    html.Div([
                        html.Span("AUTHENTICATED IDENTITY", className="profile-micro-label mb-1"),
                        html.Div([
                            html.Span("Active Session: ", className="text-secondary small"),
                            html.Span("STU2024001 (Verified Token)", className="mono-font text-info small fw-bold")
                        ])
                    ], className="p-3 rounded-3 mb-3", style={"background": "rgba(0, 0, 0, 0.40)", "border": "1px solid rgba(255, 255, 255, 0.08)"}),

                    # Dedicated Sign Out Button Container (Explicit mt-4, clear block, zero overlap)
                    html.Div([
                        html.A(
                            "Sign Out of Session →",
                            href="/logout",
                            className="btn btn-solid-white w-100 py-2 text-center",
                            style={"display": "block", "width": "100%", "textAlign": "center"}
                        )
                    ], className="mt-4 pt-2", style={"marginTop": "24px", "width": "100%"})
                ], className="cockpit-preview-container-card p-4 p-md-5 h-100 d-flex flex-column justify-content-between mb-4 mb-lg-0",
                   style={"background": "rgba(0, 0, 0, 0.50)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "16px"})
            ], lg=4, md=6, xs=12),

            # Card 2: Curriculum Preferences (Clean Switch List)
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("🔔 Automated Alerts", className="preview-card-heading"),
                        html.Span("● Enabled", className="preview-card-status-pill mono-font")
                    ], className="preview-card-top-header mb-3"),

                    html.P(
                        "Configure real-time automated alerts for statutory attendance thresholds and grade recalculations.",
                        className="text-secondary small mb-3",
                        style={"lineHeight": "1.5"}
                    ),

                    html.Div([
                        dbc.Checklist(
                            id="alert-preferences-checklist",
                            options=[
                                {"label": " 75% Statutory Attendance Alerts", "value": "ATT_ALERT"},
                                {"label": " Real-Time SGPA Recalculations", "value": "SGPA_ALERT"},
                                {"label": " Autonomous Regulation Updates", "value": "REG_ALERT"}
                            ],
                            value=["ATT_ALERT", "SGPA_ALERT", "REG_ALERT"],
                            switch=True,
                            className="settings-switch-list"
                        )
                    ], className="mt-2")
                ], className="cockpit-preview-container-card p-4 p-md-5 h-100 mb-4 mb-lg-0",
                   style={"background": "rgba(0, 0, 0, 0.50)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "16px"})
            ], lg=4, md=6, xs=12),

            # Card 3: Data Export Controls
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("📥 Data & Transcript Export", className="preview-card-heading"),
                        html.Span("● XLSX Ready", className="preview-card-status-pill mono-font")
                    ], className="preview-card-top-header mb-3"),

                    html.P(
                        "Export your verified semester marksheet, course structure, and calculated grade points to Excel.",
                        className="text-secondary small mb-3",
                        style={"lineHeight": "1.5"}
                    ),

                    html.Div([
                        html.Span("EXPORT FORMAT", className="profile-micro-label mb-1"),
                        html.P("Official AR23 Transcript Spreadsheet (.xlsx)", className="text-light small mb-0")
                    ], className="p-3 rounded-3 mb-3", style={"background": "rgba(0, 0, 0, 0.40)", "border": "1px solid rgba(255, 255, 255, 0.08)"}),

                    # Dedicated Export Action Row
                    html.Div([
                        dbc.Button("📥 Export Excel Marksheet (.xlsx)", id="export-student-excel-btn", className="btn-celestial-outline w-100 py-2")
                    ], className="mt-4 pt-2", style={"marginTop": "24px", "width": "100%"})
                ], className="cockpit-preview-container-card p-4 p-md-5 h-100",
                   style={"background": "rgba(0, 0, 0, 0.50)", "border": "1px solid rgba(255, 255, 255, 0.10)", "borderRadius": "16px"})
            ], lg=4, md=12, xs=12)
        ], className="g-4 w-100 m-0")
    ], className="w-100")
