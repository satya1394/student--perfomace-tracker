"""
StudIQ - Clean, Minimalist, Spacious Hero Landing Page
Design: Agenciy Framer + BetterStack Dark Aesthetic
Theme: Minimal, Uncluttered, Editorial Scale, Generous Whitespace.
Strictly Student Self-Service.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def build_hero_page_layout():
    """Builds the spacious, uncluttered, editorial dark Hero page for StudIQ."""
    return html.Div([
        # Ambient Lighting Blooms (Soft Cyan & Purple)
        html.Div(className="hero-glow-cyan"),
        html.Div(className="hero-glow-purple"),

        # 1. Navigation Bar (Top Sticky Glass Dock)
        html.Div([
            dbc.Container([
                html.Div([
                    # Logo & Brand Name
                    html.A([
                        html.Div("⚡", className="celestial-orb"),
                        html.Span("StudIQ", className="celestial-title fs-3 fw-bold")
                    ], href="/", className="celestial-brand me-4 text-decoration-none"),

                    # Center Nav Links
                    html.Div([
                        html.A("Features", href="#features", className="celestial-nav-link"),
                        html.A("How It Works", href="#how-it-works", className="celestial-nav-link"),
                        html.A("About", href="#benefits", className="celestial-nav-link"),
                    ], className="d-none d-md-flex align-items-center me-auto gap-2"),

                    # Right Action Buttons
                    html.Div([
                        html.A("Try Demo", href="/demo", className="btn btn-neon me-2", style={"padding": "8px 18px", "fontSize": "0.85rem"}),
                        html.A("Login", href="/login", className="btn btn-celestial-outline me-2", style={"padding": "8px 18px", "fontSize": "0.85rem"}),
                        html.A("Register →", href="/register", className="btn btn-gradient", style={"padding": "8px 20px", "fontSize": "0.85rem"})
                    ], className="d-flex align-items-center")
                ], className="d-flex align-items-center justify-content-between celestial-dock py-2 px-4")
            ], fluid=True, style={"maxWidth": "1280px"})
        ], className="celestial-navbar-container", style={"position": "sticky", "top": "0", "zIndex": "100"}),

        # 2. Hero Section (Centered, Grand Editorial Scale, Spacious & Clean)
        dbc.Container([
            html.Div([
                # Small Pill Badge
                html.Div([
                    html.Span([
                        html.Span("●", className="me-2", style={"color": "#22D3EE", "fontSize": "0.75rem"}),
                        "Student Academic Intelligence"
                    ], className="badge px-3 py-2 rounded-pill fw-bold text-white",
                       style={
                           "background": "#101728",
                           "border": "1px solid rgba(34, 211, 238, 0.35)",
                           "fontSize": "0.85rem",
                           "letterSpacing": "0.06em",
                           "boxShadow": "0 0 16px rgba(34, 211, 238, 0.2)"
                       })
                ], className="text-center mb-4 pt-4 anim-hero-label"),

                # Main Heading (Two Editorial Lines with Staggered Upward Fade)
                html.H1([
                    html.Div("Understand Your Progress.", className="anim-hero-heading-1 text-white mb-2", style={"letterSpacing": "-0.03em"}),
                    html.Div([
                        "Improve Your ",
                        html.Span("Performance.", className="gradient-text")
                    ], className="anim-hero-heading-2")
                ], className="text-center fw-extrabold display-3 mb-4", style={"lineHeight": "1.15", "fontFamily": "'Space Grotesk', sans-serif"}),

                # Supporting Text
                html.P(
                    "Track marks, attendance, SGPA, CGPA, and academic progress in one intelligent student dashboard.",
                    className="text-center text-secondary fs-5 mb-5 anim-hero-subtext",
                    style={"maxWidth": "680px", "margin": "0 auto", "lineHeight": "1.7", "color": "#94A3B8"}
                ),

                # Modern Rounded CTA Buttons
                html.Div([
                    html.A("✦ Try Interactive Demo →", href="/demo", className="btn btn-gradient px-4 py-3 me-3 fs-6 rounded-pill fw-bold"),
                    html.A("Create Free Account →", href="/register", className="btn btn-neon px-4 py-3 fs-6 rounded-pill fw-bold")
                ], className="d-flex justify-content-center flex-wrap gap-3 mb-5 anim-hero-buttons"),

                # Central Visual Hero: Wide, Clean Floating Dashboard Preview
                html.Div([
                    html.Div([
                        # Window Header
                        html.Div([
                            html.Div([
                                html.Span(className="d-inline-block rounded-circle me-1", style={"width": "10px", "height": "10px", "background": "#EF4444"}),
                                html.Span(className="d-inline-block rounded-circle me-1", style={"width": "10px", "height": "10px", "background": "#F59E0B"}),
                                html.Span(className="d-inline-block rounded-circle", style={"width": "10px", "height": "10px", "background": "#10B981"}),
                            ], className="d-flex align-items-center me-3"),
                            html.Span("⚡ StudIQ — Rahul Kumar (2024CSE001) • Raghu Engineering College R23", 
                                      className="small text-secondary fw-semibold text-truncate", style={"fontSize": "0.82rem"}),
                            html.Span("SEM 3 • 8.52 SGPA", className="badge bg-success bg-opacity-25 text-success ms-auto py-1 px-3 rounded-pill fw-bold small")
                        ], className="d-flex align-items-center px-4 py-3 border-bottom border-secondary border-opacity-20 bg-black bg-opacity-30"),

                        # Window Body Content
                        html.Div([
                            # 3 Clean KPI Cards
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Div("Cumulative CGPA", className="kpi-label", style={"fontSize": "0.72rem", "color": "#94A3B8"}),
                                        html.Div("8.34", className="stat-big-num fs-2 mb-0 text-white fw-bold"),
                                        html.Div("Overall Scale 0 - 10.0", className="small", style={"color": "#64748B", "fontSize": "0.75rem"})
                                    ], className="p-3 rounded-3 border border-secondary border-opacity-20", style={"background": "#070A13"})
                                ], md=4, xs=12, className="mb-3 mb-md-0"),
                                dbc.Col([
                                    html.Div([
                                        html.Div("Term SGPA (Sem 3)", className="kpi-label", style={"fontSize": "0.72rem", "color": "#94A3B8"}),
                                        html.Div("8.52", className="stat-big-num fs-2 mb-0 text-info fw-bold"),
                                        html.Div("21 Credits Weighted", className="small", style={"color": "#64748B", "fontSize": "0.75rem"})
                                    ], className="p-3 rounded-3 border border-secondary border-opacity-20", style={"background": "#070A13"})
                                ], md=4, xs=12, className="mb-3 mb-md-0"),
                                dbc.Col([
                                    html.Div([
                                        html.Div("Class Attendance", className="kpi-label", style={"fontSize": "0.72rem", "color": "#94A3B8"}),
                                        html.Div("78.5%", className="stat-big-num fs-2 mb-0 text-success fw-bold"),
                                        html.Div("Safe Exam Eligibility (75%+)", className="small", style={"color": "#64748B", "fontSize": "0.75rem"})
                                    ], className="p-3 rounded-3 border border-secondary border-opacity-20", style={"background": "#070A13"})
                                ], md=4, xs=12),
                            ], className="g-3 mb-4"),

                            # Wide Progression Graph & Subject Mastery
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            html.Span("📈 ", className="me-1"),
                                            html.Span("Multi-Term SGPA Progression", className="fw-bold text-white small")
                                        ], className="mb-2"),
                                        html.Img(
                                            src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 135' fill='none'><defs><linearGradient id='grad' x1='0%' y1='0%' x2='100%' y2='0%'><stop offset='0%' stop-color='%2322D3EE'/><stop offset='100%' stop-color='%238B5CF6'/></linearGradient><linearGradient id='area' x1='0%' y1='0%' x2='0%' y2='100%'><stop offset='0%' stop-color='%2322D3EE' stop-opacity='0.25'/><stop offset='100%' stop-color='%2322D3EE' stop-opacity='0.0'/></linearGradient></defs><line x1='30' y1='50' x2='570' y2='50' stroke='%2310B981' stroke-width='1.5' stroke-dasharray='3 3'/><text x='490' y='45' fill='%2310B981' font-size='9' font-family='sans-serif'>8.00 Distinction</text><path d='M 30 100 Q 150 70 260 80 T 420 40 T 570 20 L 570 125 L 30 125 Z' fill='url(%23area)'/><path d='M 30 100 Q 150 70 260 80 T 420 40 T 570 20' stroke='url(%23grad)' stroke-width='3.5' stroke-linecap='round'/><circle cx='30' cy='100' r='5' fill='%23FFFFFF' stroke='%2322D3EE' stroke-width='2'/><circle cx='260' cy='80' r='5' fill='%23FFFFFF' stroke='%2322D3EE' stroke-width='2'/><circle cx='420' cy='40' r='5' fill='%23FFFFFF' stroke='%238B5CF6' stroke-width='2'/><circle cx='570' cy='20' r='6' fill='%2322D3EE' stroke='%23FFFFFF' stroke-width='2'/><text x='25' y='126' fill='%2394A3B8' font-size='10' font-family='sans-serif'>Sem 1 (8.00)</text><text x='240' y='126' fill='%2394A3B8' font-size='10' font-family='sans-serif'>Sem 2 (8.15)</text><text x='400' y='126' fill='%2394A3B8' font-size='10' font-family='sans-serif'>Sem 3 (8.52)</text></svg>",
                                            style={"width": "100%", "height": "auto"}
                                        )
                                    ], className="p-3 rounded-3 border border-secondary border-opacity-20 h-100", style={"background": "#070A13"})
                                ], lg=7, xs=12, className="mb-3 mb-lg-0"),

                                dbc.Col([
                                    html.Div([
                                        html.Div([
                                            html.Span("🎯 ", className="me-1"),
                                            html.Span("Subject Mastery", className="fw-bold text-white small")
                                        ], className="mb-2"),
                                        
                                        html.Div([
                                            html.Div([
                                                html.Span("Data Structures", className="small text-secondary"),
                                                html.Span("85% (Grade A)", className="small text-info fw-bold")
                                            ], className="d-flex justify-content-between mb-1"),
                                            dbc.Progress(value=85, color="info", className="mb-2", style={"height": "5px", "backgroundColor": "#1E293B"}),

                                            html.Div([
                                                html.Span("Digital Logic Design", className="small text-secondary"),
                                                html.Span("92% (Grade S)", className="small text-success fw-bold")
                                            ], className="d-flex justify-content-between mb-1"),
                                            dbc.Progress(value=92, color="success", className="mb-2", style={"height": "5px", "backgroundColor": "#1E293B"}),

                                            html.Div([
                                                html.Span("Database Management", className="small text-secondary"),
                                                html.Span("78% (Grade B)", className="small text-warning fw-bold")
                                            ], className="d-flex justify-content-between mb-1"),
                                            dbc.Progress(value=78, color="warning", className="mb-3", style={"height": "5px", "backgroundColor": "#1E293B"}),

                                            html.Div([
                                                html.Span("🤖 ML Tip: ", className="fw-bold text-info small"),
                                                html.Span("Focus on DBMS unit tests to reach 8.80+ term GPA.", className="small text-secondary")
                                            ], className="p-2 rounded-2 border border-info border-opacity-25", style={"background": "#070A13"})
                                        ])
                                    ], className="p-3 rounded-3 border border-secondary border-opacity-20 h-100", style={"background": "#070A13"})
                                ], lg=5, xs=12)
                            ], className="g-3")
                        ], className="p-4")
                    ], className="preview-glass-card")
                ], className="anim-hero-preview preview-floating-container mb-5", style={"maxWidth": "1060px", "margin": "0 auto"})
            ], className="py-3")
        ], fluid=True, style={"maxWidth": "1280px"}),

        # 3. Moving Feature Ticker (Infinite Seamless Marquee)
        html.Div([
            html.Div([
                html.Div([
                    html.Span("SGPA Tracking", className="ticker-item"),
                    html.Span("•", className="ticker-dot"),
                    html.Span("CGPA Insights", className="ticker-item"),
                    html.Span("•", className="ticker-dot"),
                    html.Span("Attendance Analytics", className="ticker-item"),
                    html.Span("•", className="ticker-dot"),
                    html.Span("Subject Performance", className="ticker-item"),
                    html.Span("•", className="ticker-dot"),
                    html.Span("Smart Study Tips", className="ticker-item"),
                    html.Span("•", className="ticker-dot"),

                    # Duplicate for infinite loop
                    html.Span("SGPA Tracking", className="ticker-item"),
                    html.Span("•", className="ticker-dot"),
                    html.Span("CGPA Insights", className="ticker-item"),
                    html.Span("•", className="ticker-dot"),
                    html.Span("Attendance Analytics", className="ticker-item"),
                    html.Span("•", className="ticker-dot"),
                    html.Span("Subject Performance", className="ticker-item"),
                    html.Span("•", className="ticker-dot"),
                    html.Span("Smart Study Tips", className="ticker-item"),
                    html.Span("•", className="ticker-dot"),
                ], className="ticker-track")
            ], className="ticker-wrap")
        ]),

        # 4. Features Section: "What StudIQ Helps You Do"
        html.Div(id="features", children=[
            dbc.Container([
                html.Div([
                    html.Span("CORE CAPABILITIES", className="badge px-3 py-1 rounded-pill mb-2", 
                              style={"background": "rgba(34, 211, 238, 0.15)", "color": "#22D3EE", "border": "1px solid rgba(34, 211, 238, 0.3)"}),
                    html.H2("What StudIQ Helps You Do", className="fw-bold display-5 text-white mb-3", style={"fontFamily": "'Space Grotesk', sans-serif"}),
                    html.P("Engineered exclusively for engineering and university scholars to master their academic trajectory.", className="text-secondary fs-5 mb-5", style={"maxWidth": "680px", "color": "#94A3B8"})
                ], className="reveal-on-scroll text-center mx-auto"),

                dbc.Row([
                    # Card 01: Track
                    dbc.Col([
                        html.Div([
                            html.Span("01 — Track", className="editorial-num"),
                            html.H3("Track", className="editorial-title"),
                            html.P("Monitor marks, credits, attendance, and semester progress.", className="editorial-desc")
                        ], className="editorial-card h-100")
                    ], md=6, lg=3, xs=12, className="mb-4 reveal-on-scroll"),

                    # Card 02: Calculate
                    dbc.Col([
                        html.Div([
                            html.Span("02 — Calculate", className="editorial-num"),
                            html.H3("Calculate", className="editorial-title"),
                            html.P("Automatically calculate regulation-based SGPA and CGPA.", className="editorial-desc")
                        ], className="editorial-card h-100")
                    ], md=6, lg=3, xs=12, className="mb-4 reveal-on-scroll"),

                    # Card 03: Understand
                    dbc.Col([
                        html.Div([
                            html.Span("03 — Understand", className="editorial-num"),
                            html.H3("Understand", className="editorial-title"),
                            html.P("Explore subject performance through interactive visualizations.", className="editorial-desc")
                        ], className="editorial-card h-100")
                    ], md=6, lg=3, xs=12, className="mb-4 reveal-on-scroll"),

                    # Card 04: Improve
                    dbc.Col([
                        html.Div([
                            html.Span("04 — Improve", className="editorial-num"),
                            html.H3("Improve", className="editorial-title"),
                            html.P("Use academic insights to focus on the areas that need attention.", className="editorial-desc")
                        ], className="editorial-card h-100")
                    ], md=6, lg=3, xs=12, className="mb-4 reveal-on-scroll"),
                ], className="g-4")
            ], fluid=True, style={"maxWidth": "1280px"}, className="py-5")
        ]),

        # 5. How It Works Section (4-Step Process)
        html.Div(id="how-it-works", children=[
            dbc.Container([
                html.Div([
                    html.Span("FOUR-STEP WORKFLOW", className="badge px-3 py-1 rounded-pill mb-2", 
                              style={"background": "rgba(34, 211, 238, 0.15)", "color": "#22D3EE", "border": "1px solid rgba(34, 211, 238, 0.3)"}),
                    html.H2("How It Works", className="fw-bold display-5 text-white mb-3", style={"fontFamily": "'Space Grotesk', sans-serif"}),
                    html.P("A streamlined four-step journey to full academic clarity.", className="text-secondary fs-5 mb-5", style={"maxWidth": "680px", "color": "#94A3B8"})
                ], className="reveal-on-scroll text-center mx-auto"),

                html.Div([
                    dbc.Row([
                        # Step 1
                        dbc.Col([
                            html.Div([
                                html.Div("01", className="process-pill"),
                                html.H4("01 — Register", className="fw-bold text-white mb-2 fs-5"),
                                html.P("Create your profile with your college, regulation, branch, and semester.", className="editorial-desc")
                            ], className="process-card h-100")
                        ], md=6, lg=3, xs=12, className="mb-4 reveal-on-scroll"),

                        # Step 2
                        dbc.Col([
                            html.Div([
                                html.Div("02", className="process-pill"),
                                html.H4("02 — Add Marks", className="fw-bold text-white mb-2 fs-5"),
                                html.P("Enter your subject marks, credits, and attendance information.", className="editorial-desc")
                            ], className="process-card h-100")
                        ], md=6, lg=3, xs=12, className="mb-4 reveal-on-scroll"),

                        # Step 3
                        dbc.Col([
                            html.Div([
                                html.Div("03", className="process-pill"),
                                html.H4("03 — Analyze", className="fw-bold text-white mb-2 fs-5"),
                                html.P("View SGPA, CGPA, performance trends, and subject insights.", className="editorial-desc")
                            ], className="process-card h-100")
                        ], md=6, lg=3, xs=12, className="mb-4 reveal-on-scroll"),

                        # Step 4
                        dbc.Col([
                            html.Div([
                                html.Div("04", className="process-pill"),
                                html.H4("04 — Improve", className="fw-bold text-white mb-2 fs-5"),
                                html.P("Use your insights to focus on the areas that need attention.", className="editorial-desc")
                            ], className="process-card h-100")
                        ], md=6, lg=3, xs=12, className="mb-4 reveal-on-scroll"),
                    ], className="g-4")
                ], className="process-step-container")
            ], fluid=True, style={"maxWidth": "1280px"}, className="py-5")
        ]),

        # 6. Statistics Section
        html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div("8", className="stat-big-num"),
                            html.Div("Semesters Supported", className="stat-label-text")
                        ], className="stat-item-card h-100")
                    ], md=3, xs=6, className="mb-3 mb-md-0 reveal-on-scroll"),

                    dbc.Col([
                        html.Div([
                            html.Div("10", className="stat-big-num"),
                            html.Div("Point Grading Scale", className="stat-label-text")
                        ], className="stat-item-card h-100")
                    ], md=3, xs=6, className="mb-3 mb-md-0 reveal-on-scroll"),

                    dbc.Col([
                        html.Div([
                            html.Div("4", className="stat-big-num"),
                            html.Div("Academic Journey Steps", className="stat-label-text")
                        ], className="stat-item-card h-100")
                    ], md=3, xs=6, className="reveal-on-scroll"),

                    dbc.Col([
                        html.Div([
                            html.Div("1", className="stat-big-num"),
                            html.Div("Student-Focused Platform", className="stat-label-text")
                        ], className="stat-item-card h-100")
                    ], md=3, xs=6, className="reveal-on-scroll"),
                ], className="g-3")
            ], fluid=True, style={"maxWidth": "1280px"}, className="py-4")
        ]),

        # 7. Student Benefits Section ("Built Around the Student Journey")
        html.Div(id="benefits", children=[
            dbc.Container([
                html.Div([
                    html.Span("STUDENT ADVANTAGE", className="badge px-3 py-1 rounded-pill mb-2", 
                              style={"background": "rgba(139, 92, 246, 0.15)", "color": "#C4B5FD", "border": "1px solid rgba(139, 92, 246, 0.3)"}),
                    html.H2("Built Around the Student Journey", className="fw-bold display-5 text-white mb-3", style={"fontFamily": "'Space Grotesk', sans-serif"}),
                    html.P("Designed from the ground up to solve the exact problems engineering students face each term.", className="text-secondary fs-5 mb-5", style={"maxWidth": "720px", "color": "#94A3B8"})
                ], className="reveal-on-scroll text-center mx-auto"),

                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H5("Less Manual Calculation", className="fw-bold text-white mb-2"),
                            html.P("No more messy Excel formulas or hand calculations. Instant credit-weighted math automatically.", className="text-secondary small mb-0")
                        ], className="editorial-card h-100")
                    ], md=4, xs=12, className="mb-4 reveal-on-scroll"),

                    dbc.Col([
                        html.Div([
                            html.H5("Clearer Academic Progress", className="fw-bold text-white mb-2"),
                            html.P("See your cumulative growth across terms 1 through 8 in clean, high-contrast visual spline charts.", className="text-secondary small mb-0")
                        ], className="editorial-card h-100")
                    ], md=4, xs=12, className="mb-4 reveal-on-scroll"),

                    dbc.Col([
                        html.Div([
                            html.H5("Faster Understanding of Weak Subjects", className="fw-bold text-white mb-2"),
                            html.P("Pinpoint exactly which subjects pull your GPA down and how many marks you need to recover.", className="text-secondary small mb-0")
                        ], className="editorial-card h-100")
                    ], md=4, xs=12, className="mb-4 reveal-on-scroll"),

                    dbc.Col([
                        html.Div([
                            html.H5("Regulation-Aware Results", className="fw-bold text-white mb-2"),
                            html.P("Tailored to your exact college framework — whether R23, R20, or autonomous credit scales.", className="text-secondary small mb-0")
                        ], className="editorial-card h-100")
                    ], md=4, xs=12, className="mb-4 reveal-on-scroll"),

                    dbc.Col([
                        html.Div([
                            html.H5("Interactive Student Dashboard", className="fw-bold text-white mb-2"),
                            html.P("Explore terms, filter by semester, review marksheets, and test scenarios seamlessly.", className="text-secondary small mb-0")
                        ], className="editorial-card h-100")
                    ], md=4, xs=12, className="mb-4 reveal-on-scroll"),

                    dbc.Col([
                        html.Div([
                            html.H5("Data-Based Study Recommendations", className="fw-bold text-white mb-2"),
                            html.P("Machine-learning models provide personalized target scores and attendance risk alerts.", className="text-secondary small mb-0")
                        ], className="editorial-card h-100")
                    ], md=4, xs=12, className="mb-4 reveal-on-scroll"),
                ], className="g-4")
            ], fluid=True, style={"maxWidth": "1280px"}, className="py-5")
        ]),

        # 8. Final Call to Action ("Make Every Semester Count")
        dbc.Container([
            html.Div([
                html.H2("Make Every Semester Count", className="fw-bold display-5 text-white mb-3", style={"fontFamily": "'Space Grotesk', sans-serif"}),
                html.P(
                    "Your marks contain more than a score. They show your progress, your strengths, and your next opportunity to improve.",
                    className="text-secondary fs-5 mb-5",
                    style={"maxWidth": "680px", "margin": "0 auto", "lineHeight": "1.7", "color": "#94A3B8"}
                ),
                html.Div([
                    html.A("✦ Try the Demo →", href="/demo", className="btn btn-gradient px-4 py-3 me-3 fs-6 rounded-pill fw-bold"),
                    html.A("Create Your Account →", href="/register", className="btn btn-neon px-4 py-3 fs-6 rounded-pill fw-bold")
                ], className="d-flex justify-content-center flex-wrap gap-3")
            ], className="editorial-card text-center p-5 mb-5", 
               style={
                   "background": "linear-gradient(145deg, #101728 0%, #070A13 100%)",
                   "border": "1px solid rgba(34, 211, 238, 0.4)",
                   "boxShadow": "0 25px 80px rgba(0, 0, 0, 0.95), 0 0 35px rgba(34, 211, 238, 0.2)"
               })
        ], fluid=True, style={"maxWidth": "1180px"}, className="py-4"),

        # 9. Footer (Clean, Minimalist, No Faculty/Admin)
        html.Footer([
            dbc.Container([
                dbc.Row([
                    # Left: Brand & Tagline
                    dbc.Col([
                        html.Div([
                            html.Span("⚡ StudIQ", className="fw-bold text-white fs-4 me-2"),
                            html.Span("Student Academic Intelligence", className="text-info small fw-bold")
                        ], className="d-flex align-items-center mb-2"),
                        html.P("Understand your progress. Improve your performance.", className="text-secondary small mb-3"),
                        html.P("Built for students, by students.", className="text-secondary small mb-0")
                    ], md=6, xs=12, className="mb-4 mb-md-0"),

                    # Right: Quick Navigation Links
                    dbc.Col([
                        html.Div([
                            html.A("Home", href="/", className="text-secondary small text-decoration-none me-3 mb-2"),
                            html.A("Features", href="#features", className="text-secondary small text-decoration-none me-3 mb-2"),
                            html.A("Demo", href="/demo", className="text-secondary small text-decoration-none me-3 mb-2"),
                            html.A("Login", href="/login", className="text-secondary small text-decoration-none me-3 mb-2"),
                            html.A("Register", href="/register", className="text-secondary small text-decoration-none me-3 mb-2"),
                            html.A("Dashboard", href="/student", className="text-secondary small text-decoration-none me-3 mb-2"),
                            html.A("GitHub", href="#", className="text-info small text-decoration-none mb-2")
                        ], className="d-flex flex-wrap justify-content-md-end")
                    ], md=6, xs=12, className="d-flex align-items-center justify-content-md-end")
                ], className="py-4 border-top border-secondary border-opacity-20"),

                html.Div([
                    html.Span("© 2026 StudIQ. All rights reserved.", className="text-secondary small")
                ], className="text-center pb-4")
            ], fluid=True, style={"maxWidth": "1280px"})
        ])
    ])
