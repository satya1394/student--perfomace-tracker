"""
StudIQ - Vesper.ai Operational Academic Infrastructure Landing Page
Pure Black #000000 | Background Video | Liquid-Metal Nav | Instrument Serif Italic Accent | 3-Stat Footer
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def build_hero_page_layout():
    """Builds the single-viewport Vesper.ai landing page."""
    return html.Div([
        # Background Video Layer (100% opacity, no overlay)
        html.Video(
            children=[
                html.Source(
                    src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260818_072341_50851634-bbc3-4c33-9acc-7647d4db44aa.mp4",
                    type="video/mp4"
                )
            ],
            autoPlay=True,
            loop=True,
            muted=True,
            playsInline=True,
            className="hero-video-bg"
        ),

        # Scrim / Grain overlay
        html.Div(className="grain"),

        # Page Container
        html.Div([
            # Menu Backdrop (for mobile)
            html.Div(className="menu-backdrop"),

            # 1. Header — 3-Column Grid
            html.Header([
                # Left: Logo + Mark SVG
                html.A([
                    html.Span([
                        html.Img(
                            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cg transform='rotate(-30 12 12)'%3E%3Ccircle cx='7.3' cy='3.2' r='1.45'/%3E%3Crect x='5.5' y='4.7' width='3.6' height='14.6' rx='1.8'/%3E%3Crect x='14.9' y='4.7' width='3.6' height='14.6' rx='1.8'/%3E%3Ccircle cx='16.7' cy='20.8' r='1.45'/%3E%3C/g%3E%3C/svg%3E",
                            alt="Vesper mark",
                            className="logo-mark"
                        )
                    ], className="d-inline-flex align-items-center me-1"),
                    html.Span("Vesper", className="fw-bold"),
                    html.Span(".ai", className="logo-suffix")
                ], href="#top", className="logo appear appear--scale", style={"--d": "0.08s"}, **{"aria-label": "Vesper.ai"}),

                # Center: Liquid-Metal Nav Pills
                html.Nav([
                    html.A("Benefits", href="#benefits", className="nav-pill appear appear--scale", style={"--d": "0.16s"}),
                    html.A("How It Works", href="#how-it-works", className="nav-pill appear appear--soft", style={"--d": "0.28s"}),
                    html.A("FAQs", href="#faqs", className="nav-pill appear appear--scale", style={"--d": "0.40s"}),
                    html.A("Pricing", href="#pricing", className="nav-pill appear appear--soft", style={"--d": "0.52s"}),
                ], id="site-nav", **{"aria-label": "Primary"}),

                # Right: Header CTA
                html.A("Start for Free", href="/demo", className="btn btn-solid header-cta appear appear--scale", style={"--d": "0.34s"})
            ], className="header"),

            # 2. Main Hero (Bottom-Centered)
            html.Main([
                html.Div([
                    # Sparkle Badge
                    html.Div([
                        html.Img(
                            src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M12 2.6C12.55 2.6 12.88 3.15 13.08 4.7c.62 4.7 1.52 5.6 6.22 6.22 1.55.2 2.1.53 2.1 1.08s-.55.88-2.1 1.08c-4.7.62-5.6 1.52-6.22 6.22-.2 1.55-.53 2.1-1.08 2.1s-.88-.55-1.08-2.1c-.62-4.7-1.52-5.6-6.22-6.22C3.15 12.88 2.6 12.55 2.6 12s.55-.88 2.1-1.08c4.7-.62 5.6-1.52 6.22-6.22C11.12 3.15 11.45 2.6 12 2.6Z'/%3E%3C/svg%3E",
                            alt="Sparkle",
                            className="badge-star"
                        ),
                        html.Span("Operational AI Infrastructure")
                    ], className="badge appear appear--pop", style={"--d": "0.22s"}),

                    # H1 Headline (Masked 2 lines with Instrument Serif italic em)
                    html.H1([
                        html.Span([
                            "Train ",
                            html.Em("AI agents"),
                            " on your"
                        ], className="headline-line appear appear--mask", style={"--d": "0.42s"}),
                        html.Span(
                            "workflows in minutes.",
                            className="headline-line appear appear--mask", style={"--d": "0.62s"}
                        )
                    ]),

                    # Lede
                    html.P(
                        "Deploy adaptive AI agents that learn, execute, and scale operational tasks across your business.",
                        className="lede appear appear--soft", style={"--d": "0.82s", "animationDuration": "1.25s"}
                    ),

                    # Action Buttons
                    html.Div([
                        html.A("Start for Free", href="/demo", className="btn btn-solid hero-btn appear appear--btn", style={"--d": "0.96s"}),
                        html.A("See it in action", href="/demo", className="btn btn-ghost hero-btn appear appear--side", style={"--d": "1.10s"})
                    ], className="hero-actions")
                ], className="hero-copy")
            ], className="hero", id="top"),

            # 3. Footer Stats (3 Clean Items)
            html.Footer([
                # Stat 1: Dual-Pill / Workflow Icon
                html.Div([
                    html.Img(
                        src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cdefs%3E%3ClinearGradient id='g1' x1='3' y1='2' x2='14' y2='22' gradientUnits='userSpaceOnUse'%3E%3Cstop offset='0' stop-color='%23ffffff' stop-opacity='0.38'/%3E%3Cstop offset='1' stop-color='%233a3a3a' stop-opacity='0.62'/%3E%3C/linearGradient%3E%3ClinearGradient id='g2' x1='13' y1='2' x2='24' y2='22' gradientUnits='userSpaceOnUse'%3E%3Cstop offset='0' stop-color='%233a3a3a' stop-opacity='0.38'/%3E%3Cstop offset='1' stop-color='%23ffffff' stop-opacity='0.62'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect x='3.4' y='2.6' width='7.2' height='18.8' rx='3.6' fill='url(%23g1)'/%3E%3Crect x='13.4' y='2.6' width='7.2' height='18.8' rx='3.6' fill='url(%23g2)'/%3E%3Crect x='9.2' y='10.9' width='5.6' height='2.2' rx='1.1' fill='%234a4a4a'/%3E%3C/svg%3E",
                        alt="Workflows",
                        className="stat-icon"
                    ),
                    html.Span("4.2M+ workflows automated")
                ], className="stat appear appear--stat", style={"--d": "1.12s"}),

                # Stat 2: Download Rounded Tile Icon
                html.Div([
                    html.Img(
                        src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='2.4' y='2.4' width='19.2' height='19.2' rx='6.2' fill='%23ffffff'/%3E%3Cpath d='M12 7.1v7.4M8.15 12.35L12 16.2l3.85-3.85' stroke='%23111111' stroke-width='1.85' stroke-linecap='round' stroke-linejoin='round' fill='none'/%3E%3C/svg%3E",
                        alt="Download tile",
                        className="stat-icon"
                    ),
                    html.Span("92% reduction in manual operations")
                ], className="stat appear appear--stat", style={"--d": "1.28s"}),

                # Stat 3: Three Avatars Icon
                html.Div([
                    html.Img(
                        src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 22'%3E%3Ccircle cx='10.2' cy='11' r='9.2' fill='%232b2b2b'/%3E%3Cellipse cx='10.2' cy='12.1' rx='4.15' ry='3.7' fill='%23f4f4f4'/%3E%3Cpolygon points='8,4 10.2,7 6.8,6.5' fill='%232b2b2b'/%3E%3Cpolygon points='12.4,4 10.2,7 13.6,6.5' fill='%232b2b2b'/%3E%3Ccircle cx='9' cy='11.5' r='0.7' fill='%231a1a1a'/%3E%3Ccircle cx='11.4' cy='11.5' r='0.7' fill='%231a1a1a'/%3E%3Ccircle cx='20.2' cy='11' r='9.2' fill='%23ffffff'/%3E%3Ccircle cx='17.5' cy='10' r='1.7' fill='%23111111'/%3E%3Ccircle cx='22.9' cy='10' r='1.7' fill='%23111111'/%3E%3Cpath d='M18 14.5 Q20.2 16.5 22.4 14.5' stroke='%23111111' stroke-width='1.2' fill='none' stroke-linecap='round'/%3E%3Ccircle cx='30.2' cy='11' r='9.2' fill='%23f26b1d'/%3E%3Ctext x='30.2' y='15.1' font-family='Inter, sans-serif' font-size='12.5' font-weight='700' fill='white' text-anchor='middle'%3Ee%3C/text%3E%3C/svg%3E",
                        alt="Avatars",
                        className="stat-icon-wide"
                    ),
                    html.Span("180+ operational teams onboarded")
                ], className="stat appear appear--stat", style={"--d": "1.44s"})
            ], className="stats")
        ], className="page")
    ], style={"background": "#000", "color": "#fff"})
