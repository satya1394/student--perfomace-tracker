"""
Modern Hero Landing Page for StudIQ.
Design Inspired by BetterStack.com + Wope.com.
Pure SaaS Aesthetic with Neon Cyan, Vibrant Purple, and Deep Slate Glass.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def build_hero_page_layout():
    """Builds the comprehensive, high-converting Hero/Landing page for StudIQ."""
    return html.Div([
        # 1. Top Navbar
        html.Div([
            dbc.Container([
                html.Div([
                    # Logo & Brand
                    html.A([
                        html.Div("⚡", className="celestial-orb"),
                        html.Span("StudIQ", className="celestial-title fs-3 fw-bold")
                    ], href="/", className="celestial-brand me-4"),

                    # Nav Links
                    html.Div([
                        html.A("Features", href="#features", className="celestial-nav-link"),
                        html.A("Demo", href="#demo", className="celestial-nav-link"),
                        html.A("How It Works", href="#how-it-works", className="celestial-nav-link"),
                    ], className="d-none d-md-flex align-items-center me-auto"),

                    # Action Buttons (Login & Register)
                    html.Div([
                        html.A("Try Demo", href="/demo", className="btn btn-celestial-outline me-2"),
                        html.A("Login", href="/login", className="btn btn-celestial-outline me-2"),
                        html.A("Get Started →", href="/register", className="btn btn-celestial")
                    ], className="d-flex align-items-center")
                ], className="d-flex align-items-center justify-content-between celestial-dock py-2 px-4")
            ], fluid=True, style={"maxWidth": "1320px"})
        ], className="celestial-navbar-container"),

        # 2. Hero Section
        dbc.Container([
            html.Div([
                # Top Glowing Pill Badge
                html.Div([
                    html.Span("🎓 Track Your Academic Performance with AI-Powered Insights", 
                              className="badge px-3 py-2 rounded-pill fw-bold text-white",
                              style={
                                  "background": "linear-gradient(90deg, rgba(0, 240, 255, 0.2), rgba(168, 85, 247, 0.2))",
                                  "border": "1px solid rgba(0, 240, 255, 0.4)",
                                  "fontSize": "0.9rem",
                                  "letterSpacing": "0.04em",
                                  "boxShadow": "0 0 20px rgba(0, 240, 255, 0.2)"
                              })
                ], className="text-center mb-4 pt-4"),

                # Main Hero Headline
                html.H1([
                    "Calculate SGPA, CGPA, and Visualize Your Academic Journey with ",
                    html.Span("Intelligent Analytics", className="gradient-text")
                ], className="text-center fw-extrabold display-4 mb-4 text-white", style={"lineHeight": "1.2", "maxWidth": "950px", "margin": "0 auto"}),

                # Subtitle
                html.P(
                    "StudIQ is the student-first self-service academic tracker designed for modern engineering scholars. "
                    "Get instant multi-college regulation compliance, AI study roadmaps, and grade forecasting.",
                    className="text-center text-secondary fs-5 mb-5",
                    style={"maxWidth": "780px", "margin": "0 auto", "lineHeight": "1.6"}
                ),

                # Hero Call To Action Buttons
                html.Div([
                    html.A("✦ Try Interactive Demo →", href="/demo", className="btn btn-gradient px-4 py-3 me-3 fs-6"),
                    html.A("Create Free Account →", href="/register", className="btn btn-neon px-4 py-3 fs-6")
                ], className="d-flex justify-content-center flex-wrap gap-3 mb-5"),

                # Value Proposition Checklist
                html.Div([
                    html.Div([
                        html.Span("✓", className="text-info fw-bold me-2"),
                        html.Span("Multi-College Support", className="text-white-50 small fw-semibold")
                    ], className="me-4 mb-2"),
                    html.Div([
                        html.Span("✓", className="text-info fw-bold me-2"),
                        html.Span("Regulation-Based SGPA (R23, R20)", className="text-white-50 small fw-semibold")
                    ], className="me-4 mb-2"),
                    html.Div([
                        html.Span("✓", className="text-info fw-bold me-2"),
                        html.Span("Real-Time Analytics & Radar Mastery", className="text-white-50 small fw-semibold")
                    ], className="me-4 mb-2"),
                    html.Div([
                        html.Span("✓", className="text-info fw-bold me-2"),
                        html.Span("Personalized AI Study Tips", className="text-white-50 small fw-semibold")
                    ], className="mb-2"),
                ], className="d-flex justify-content-center flex-wrap text-center pb-5")
            ], className="animate-on-load")
        ], fluid=True, style={"maxWidth": "1200px"}),

        # 3. Features Section (3 Cards)
        html.Div(id="features", children=[
            dbc.Container([
                html.Div([
                    html.H2([
                        "Engineered for ",
                        html.Span("Academic Excellence", className="gradient-text")
                    ], className="text-center fw-bold display-6 mb-2 text-white"),
                    html.P("Everything you need to master your university grades in one unified dashboard.", className="text-center text-secondary mb-5")
                ]),

                dbc.Row([
                    # Feature Card 1: Smart GPA
                    dbc.Col([
                        html.Div([
                            html.Div("📊", className="kpi-vector-badge mb-3 fs-3"),
                            html.H5("Smart GPA Calculation", className="fw-bold text-white mb-2"),
                            html.P(
                                "Automatic credit-weighted SGPA & CGPA calculation tailored specifically to your college's syllabus regulation (R23, R20, R19).",
                                className="text-secondary small mb-0", style={"lineHeight": "1.6"}
                            )
                        ], className="feature-card h-100 p-4")
                    ], md=4, xs=12, className="mb-4"),

                    # Feature Card 2: Visual Insights
                    dbc.Col([
                        html.Div([
                            html.Div("📈", className="kpi-vector-badge mb-3 fs-3"),
                            html.H5("Visual Insights & Trends", className="fw-bold text-white mb-2"),
                            html.P(
                                "Interactive Plotly progression graphs, subject mastery bar charts with peer benchmarks, and attendance correlation scatter plots.",
                                className="text-secondary small mb-0", style={"lineHeight": "1.6"}
                            )
                        ], className="feature-card h-100 p-4")
                    ], md=4, xs=12, className="mb-4"),

                    # Feature Card 3: AI Study Tips
                    dbc.Col([
                        html.Div([
                            html.Div("🤖", className="kpi-vector-badge mb-3 fs-3"),
                            html.H5("AI Study Recommendations", className="fw-bold text-white mb-2"),
                            html.P(
                                "Personalized machine-learning roadmaps that highlight weak subjects, predict final exam scores, and recommend optimal study hours.",
                                className="text-secondary small mb-0", style={"lineHeight": "1.6"}
                            )
                        ], className="feature-card h-100 p-4")
                    ], md=4, xs=12, className="mb-4"),
                ], className="g-4")
            ], fluid=True, style={"maxWidth": "1200px"}, className="py-5")
        ]),

        # 4. Demo Preview Section
        html.Div(id="demo", children=[
            dbc.Container([
                html.Div([
                    html.Div([
                        html.Span("INTERACTIVE PREVIEW", className="ai-tip-badge mb-2"),
                        html.H2("See StudIQ in Action", className="fw-bold display-6 text-white mb-3"),
                        html.P("Explore a fully functional student dashboard pre-loaded with Raghu Engineering College R23 semester data.", className="text-secondary mb-4"),
                    ], className="text-center"),

                    # Live Mockup Frame Card
                    html.Div([
                        html.Div([
                            # Mock Navbar
                            html.Div([
                                html.Span("⚡ StudIQ", className="fw-bold text-info me-3"),
                                html.Span("🎓 Rahul Kumar • 2024CSE001 | CSE (Data Science)", className="student-meta-badge py-1 px-3 mb-0"),
                                html.Span("SEM 3: 8.52 SGPA", className="badge bg-success ms-auto py-2 px-3 rounded-pill")
                            ], className="d-flex align-items-center p-3 border-bottom border-secondary border-opacity-25"),

                            # Mock KPI Row
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.Div("Cumulative CGPA", className="kpi-label"),
                                            html.Div("8.34", className="kpi-value fs-4"),
                                            html.Div("Overall scale 0-10", className="small text-secondary")
                                        ], className="p-3 rounded-3 bg-black bg-opacity-40 border border-secondary border-opacity-25")
                                    ], md=3, xs=6, className="mb-2"),
                                    dbc.Col([
                                        html.Div([
                                            html.Div("Semester SGPA", className="kpi-label"),
                                            html.Div("8.52", className="kpi-value fs-4"),
                                            html.Div("Sem 3 Earned credits", className="small text-secondary")
                                        ], className="p-3 rounded-3 bg-black bg-opacity-40 border border-secondary border-opacity-25")
                                    ], md=3, xs=6, className="mb-2"),
                                    dbc.Col([
                                        html.Div([
                                            html.Div("Attendance", className="kpi-label"),
                                            html.Div("78.5%", className="kpi-value fs-4 text-info"),
                                            html.Div("Regularity target 75%", className="small text-secondary")
                                        ], className="p-3 rounded-3 bg-black bg-opacity-40 border border-secondary border-opacity-25")
                                    ], md=3, xs=6, className="mb-2"),
                                    dbc.Col([
                                        html.Div([
                                            html.Div("ML Forecast", className="kpi-label"),
                                            html.Div("82/100", className="kpi-value fs-4 text-success"),
                                            html.Div("Low Risk • Honors Track", className="small text-secondary")
                                        ], className="p-3 rounded-3 bg-black bg-opacity-40 border border-secondary border-opacity-25")
                                    ], md=3, xs=6, className="mb-2"),
                                ], className="g-2 p-3")
                            ]),

                            # Mock CTA Inside Mockup
                            html.Div([
                                html.A("✦ Launch Interactive Demo Mode →", href="/demo", className="btn btn-gradient px-4 py-2 fw-bold fs-6"),
                                html.P("No registration required • Try with sample curriculum data", className="small text-secondary mt-2 mb-0")
                            ], className="text-center p-4 bg-black bg-opacity-30 border-top border-secondary border-opacity-25")
                        ], className="card p-0 overflow-hidden", style={"border": "1px solid rgba(0, 240, 255, 0.35)", "boxShadow": "0 20px 60px rgba(0, 0, 0, 0.9), 0 0 30px rgba(0, 240, 255, 0.2)"})
                    ], className="mb-5")
                ])
            ], fluid=True, style={"maxWidth": "1050px"}, className="py-4")
        ]),

        # 5. How It Works (3 Steps)
        html.Div(id="how-it-works", children=[
            dbc.Container([
                html.Div([
                    html.H2([
                        "Three Simple Steps to ",
                        html.Span("Academic Clarity", className="gradient-text")
                    ], className="text-center fw-bold display-6 mb-2 text-white"),
                    html.P("Self-service analytics made fast, private, and effortless.", className="text-center text-secondary mb-5")
                ]),

                dbc.Row([
                    # Step 1
                    dbc.Col([
                        html.Div([
                            html.Div("01", className="fw-extrabold fs-1 gradient-text mb-2", style={"fontFamily": "Space Grotesk"}),
                            html.H5("Register Account", className="fw-bold text-white mb-2"),
                            html.P("Select your College, Regulation, and Branch specialization to instantly map your syllabus.", className="text-secondary small")
                        ], className="feature-card p-4 h-100 text-center")
                    ], md=4, xs=12, className="mb-4"),

                    # Step 2
                    dbc.Col([
                        html.Div([
                            html.Div("02", className="fw-extrabold fs-1 gradient-text mb-2", style={"fontFamily": "Space Grotesk"}),
                            html.H5("Enter Your Marks", className="fw-bold text-white mb-2"),
                            html.P("Type your exact grade points or numerical scores per subject directly into the streamlined modal.", className="text-secondary small")
                        ], className="feature-card p-4 h-100 text-center")
                    ], md=4, xs=12, className="mb-4"),

                    # Step 3
                    dbc.Col([
                        html.Div([
                            html.Div("03", className="fw-extrabold fs-1 gradient-text mb-2", style={"fontFamily": "Space Grotesk"}),
                            html.H5("Unlock Insights", className="fw-bold text-white mb-2"),
                            html.P("Explore real-time SGPA trends, radar mastery comparisons, and AI study roadmaps.", className="text-secondary small")
                        ], className="feature-card p-4 h-100 text-center")
                    ], md=4, xs=12, className="mb-4"),
                ], className="g-4 mb-5")
            ], fluid=True, style={"maxWidth": "1200px"}, className="py-4")
        ]),

        # 6. Final Call To Action Banner
        dbc.Container([
            html.Div([
                html.H3("Ready to Master Your Semester GPA?", className="fw-bold text-white mb-3"),
                html.P("Join hundreds of students taking control of their academic trajectory.", className="text-secondary mb-4"),
                html.Div([
                    html.A("✦ Get Started Free →", href="/register", className="btn btn-gradient px-4 py-3 me-3 fs-6"),
                    html.A("Try Demo Mode", href="/demo", className="btn btn-neon px-4 py-3 fs-6")
                ], className="d-flex justify-content-center flex-wrap gap-2")
            ], className="card text-center p-5 mb-5", style={"background": "linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(10, 14, 26, 0.95))", "border": "1px solid rgba(0, 240, 255, 0.35)"})
        ], fluid=True, style={"maxWidth": "1100px"}),

        # 7. Footer
        html.Footer([
            dbc.Container([
                html.Div([
                    html.Div([
                        html.Span("⚡ StudIQ", className="fw-bold text-white fs-5 me-3"),
                        html.Span("Built for students, by students", className="text-secondary small")
                    ], className="mb-3 mb-md-0"),
                    html.Div([
                        html.Span("© 2026 StudIQ Platform. All rights reserved.", className="text-secondary small me-4"),
                        html.A("Terms", href="#", className="text-secondary small text-decoration-none me-3"),
                        html.A("Privacy", href="#", className="text-secondary small text-decoration-none me-3"),
                        html.A("GitHub", href="#", className="text-info small text-decoration-none")
                    ], className="d-flex align-items-center flex-wrap")
                ], className="d-flex flex-column flex-md-row align-items-center justify-content-between py-4 border-top border-secondary border-opacity-25")
            ], fluid=True, style={"maxWidth": "1200px"})
        ])
    ])
