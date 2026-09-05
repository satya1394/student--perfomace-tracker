"""
StudIQ - Marks & Subjects Marksheet (High-Clarity Preview Card Layout)
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from app.dashboards.components import create_export_controls


def build_marks_subjects_page():
    """Builds the clean, structured Marks & Subjects subpage."""
    return html.Div([
        # Action Toolbar Container
        html.Div([
            html.Div([
                html.Div([
                    html.Span("📋 Official Marksheet & Course Roster", className="preview-card-heading"),
                    html.P("Manage grades, marks, and elective specializations", className="text-secondary small mb-0 mt-1")
                ]),
                html.Div([
                    create_export_controls("student")
                ], className="d-flex align-items-center gap-2")
            ], className="preview-card-top-header"),

            # Action Buttons Row (Streamlined)
            html.Div([
                dbc.Button("+ Enter / Edit Marks & Grades", id="open-marks-modal-btn", className="btn-solid-white")
            ], className="d-flex align-items-center flex-wrap gap-2 mt-2")
        ], className="cockpit-preview-container-card mb-4"),

        # Detailed Transcript Table Container
        html.Div([
            html.Div([
                html.Div([
                    html.Span("📊 Semester Subject Transcript", className="preview-card-heading"),
                    html.P("Course code, category, credit weights, and official status", className="text-secondary small mb-0 mt-1")
                ]),
                html.Span("● Verified Autonomous Roster", className="preview-card-status-pill mono-font")
            ], className="preview-card-top-header"),

            dcc.Loading(
                id="loading-student-courses-table",
                type="dot",
                children=html.Div(id="student-courses-table-container", className="table-responsive")
            )
        ], className="cockpit-preview-container-card")
    ])
