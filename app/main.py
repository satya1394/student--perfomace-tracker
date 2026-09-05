"""
Application Entry Point.
StudIQ.ai — Operational Student Intelligence (Permanent Unblocked Video Background)
"""

import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from flask import Flask, request, redirect, url_for, render_template_string, flash, session, Response
from flask_login import current_user, login_required, logout_user
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

from app.config import Config
from app.database import init_db, get_db_session, College, Regulation, Branch
from app.auth import login_manager, authenticate_user, seed_default_users, register_student_user, login_demo_user
from app.dashboards.layout_shell import build_dashboard_shell, create_framer_navbar_with_active
from app.callbacks import register_callbacks

# 1. Initialize Flask Application
server = Flask(__name__, static_folder=str(BASE_DIR / "assets"), static_url_path="/assets")
server.config["SECRET_KEY"] = Config.SECRET_KEY
login_manager.init_app(server)

# Direct Landing Page Route (Instant, Pure Black, Zero Flash, Zero JS Overhead)
@server.route("/")
@server.route("/home")
def index_route():
    index_file = BASE_DIR / "index.html"
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
        return Response(content, mimetype="text/html")
    return "<h1>StudIQ.ai</h1>", 200

# 2. Pure Black Vesper Authentication Template
LOGIN_TEMPLATE = '''<!DOCTYPE html>
<html lang="en" style="background:#000000 !important; color:#ffffff;">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudIQ.ai &mdash; Student Sign In</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cg transform='rotate(-30 12 12)'%3E%3Ccircle cx='7.3' cy='3.2' r='1.45'/%3E%3Crect x='5.5' y='4.7' width='3.6' height='14.6' rx='1.8'/%3E%3Crect x='14.9' y='4.7' width='3.6' height='14.6' rx='1.8'/%3E%3Ccircle cx='16.7' cy='20.8' r='1.45'/%3E%3C/g%3E%3C/svg%3E">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        html, body { background: #000000 !important; color: #ffffff !important; font-family: 'Inter', sans-serif; min-height: 100vh; margin: 0; }
        .hero-photo { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; overflow: hidden; pointer-events: none; }
        .hero-photo video { width: 100%; height: 100%; object-fit: cover; opacity: 1; }
        .hero-photo::after { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.75) 100%); pointer-events: none; }
        .grain { position: fixed; inset: 0; z-index: 1; pointer-events: none; }
        .auth-container { position: relative; z-index: 10; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px; }
        .portal-card { width: 100%; max-width: 440px; background: rgba(10, 14, 24, 0.7); border: 1px solid rgba(255, 255, 255, 0.16); border-radius: 14px; padding: 32px; backdrop-filter: blur(24px); box-shadow: 0 25px 60px rgba(0,0,0,0.85); }
        .form-control, .form-select { background: rgba(5, 8, 15, 0.7) !important; border: 1px solid rgba(255, 255, 255, 0.15) !important; color: #ffffff !important; border-radius: 8px; font-size: 0.88rem; padding: 10px 14px; }
        .form-control:focus, .form-select:focus { border-color: rgba(255,255,255,0.4) !important; box-shadow: 0 0 0 2px rgba(255,255,255,0.1) !important; }
        .btn-solid { background: linear-gradient(180deg, #ffffff 0%, #e7e7e7 48%, #cfcfcf 100%); color: #111; font-weight: 600; border: 1px solid #fff; border-radius: 8px; padding: 10px; width: 100%; transition: all 0.2s ease; }
        .btn-solid:hover { background: #ffffff; color: #000; box-shadow: 0 0 20px rgba(255,255,255,0.3); }
        .btn-ghost { background: rgba(255,255,255,0.05); color: #ffffff; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 10px; width: 100%; text-align: center; text-decoration: none; display: block; font-size: 0.88rem; transition: all 0.2s ease; }
        .btn-ghost:hover { background: rgba(255,255,255,0.1); color: #ffffff; border-color: rgba(255,255,255,0.3); }
        .nav-tabs .nav-link { color: #9a9a9a; border: none; font-size: 0.88rem; padding: 8px 16px; border-radius: 8px; }
        .nav-tabs .nav-link.active { background: rgba(255,255,255,0.1); color: #ffffff; font-weight: 600; }
    </style>
</head>
<body style="background:#000;color:#fff">
    <div class="hero-photo">
        <video autoplay loop muted playsinline src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260818_072341_50851634-bbc3-4c33-9acc-7647d4db44aa.mp4"></video>
    </div>
    <div class="grain"></div>
    <!-- Global SVG Gradient Definitions for Plotly Charts -->
    <svg style="position: absolute; width: 0; height: 0; overflow: hidden;" aria-hidden="true">
      <defs>
        <linearGradient id="bar-vertical-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#38BDF8" stop-opacity="1" />
          <stop offset="50%" stop-color="#3B82F6" stop-opacity="0.9" />
          <stop offset="100%" stop-color="#1E1B4B" stop-opacity="0.8" />
        </linearGradient>
      </defs>
    </svg>

    <div class="auth-container">
        <div class="portal-card">
            <div class="text-center mb-4">
                <a href="/" class="d-inline-flex align-items-center gap-2 text-decoration-none text-white mb-2">
                    <svg viewBox="0 0 24 24" fill="currentColor" width="26" height="26">
                        <g transform="rotate(-30 12 12)">
                          <circle cx="7.3" cy="3.2" r="1.45"/>
                          <rect x="5.5" y="4.7" width="3.6" height="14.6" rx="1.8"/>
                          <rect x="14.9" y="4.7" width="3.6" height="14.6" rx="1.8"/>
                          <circle cx="16.7" cy="20.8" r="1.45"/>
                        </g>
                    </svg>
                    <span class="fs-4 fw-bold">StudIQ<span style="font-weight:400;opacity:0.8;">.ai</span></span>
                </a>
                <p class="text-secondary small mb-0">Operational Student Intelligence</p>
            </div>

            {% with messages = get_flashed_messages(with_categories=true) %}
              {% if messages %}
                {% for category, message in messages %}
                  <div class="alert alert-{{ category }} py-2 px-3 small rounded-2 mb-3 bg-dark border border-secondary text-white">{{ message }}</div>
                {% endfor %}
              {% endif %}
            {% endwith %}

            <ul class="nav nav-tabs justify-content-center mb-4 border-0" id="authTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link {% if active_tab != 'register' %}active{% endif %}" id="login-tab" data-bs-toggle="tab" data-bs-target="#login-panel" type="button" role="tab">Sign In</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link {% if active_tab == 'register' %}active{% endif %}" id="register-tab" data-bs-toggle="tab" data-bs-target="#register-panel" type="button" role="tab">Register</button>
                </li>
            </ul>

            <div class="tab-content" id="authTabsContent">
                <div class="tab-pane fade {% if active_tab != 'register' %}show active{% endif %}" id="login-panel" role="tabpanel">
                    <form method="POST" action="/login">
                        <div class="mb-3">
                            <label class="form-label small text-secondary">Username or Email</label>
                            <input type="text" name="username" class="form-control" placeholder="e.g. demo_user" required autofocus>
                        </div>
                        <div class="mb-4">
                            <label class="form-label small text-secondary">Password</label>
                            <input type="password" name="password" class="form-control" placeholder="••••••••" required>
                        </div>
                        <button type="submit" class="btn-solid mb-3">Sign In &rarr;</button>
                    </form>
                    <div class="pt-3 border-top border-secondary border-opacity-25">
                        <a href="/demo" class="btn-ghost">✦ Launch Interactive Demo Mode</a>
                    </div>
                </div>

                <div class="tab-pane fade {% if active_tab == 'register' %}show active{% endif %}" id="register-panel" role="tabpanel">
                    <form method="POST" action="/register">
                        <div class="mb-2">
                            <label class="form-label small text-secondary">Full Name</label>
                            <input type="text" name="full_name" class="form-control" placeholder="e.g. Rahul Kumar" required>
                        </div>
                        <div class="mb-2">
                            <label class="form-label small text-secondary">Username</label>
                            <input type="text" name="username" class="form-control" placeholder="e.g. rahul_k" required>
                        </div>
                        <div class="mb-2">
                            <label class="form-label small text-secondary">Email</label>
                            <input type="email" name="email" class="form-control" placeholder="rahul@example.com" required>
                        </div>
                        <div class="mb-2">
                            <label class="form-label small text-secondary">Password</label>
                            <input type="password" name="password" class="form-control" placeholder="••••••••" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small text-secondary">Confirm Password</label>
                            <input type="password" name="confirm_password" class="form-control" placeholder="••••••••" required>
                        </div>
                        <button type="submit" class="btn-solid mb-2">Create Account &rarr;</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@server.route("/login", methods=["GET", "POST"])
def login_route():
    if current_user.is_authenticated:
        return redirect("/app/overview")
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        success, user, err = authenticate_user(username, password)
        if success and user:
            session['is_demo'] = False
            return redirect("/app/overview")
        flash(err or "Invalid credentials", "danger")
        return render_template_string(LOGIN_TEMPLATE, active_tab="login")
    return render_template_string(LOGIN_TEMPLATE, active_tab="login")

@server.route("/register", methods=["GET", "POST"])
def register_route():
    if current_user.is_authenticated:
        return redirect("/app/overview")
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        db = get_db_session()
        try:
            col = db.query(College).first()
            reg = db.query(Regulation).first()
            br = db.query(Branch).first()
            college_id = col.id if col else 1
            regulation_id = reg.id if reg else 1
            branch_id = br.id if br else 1
        finally:
            db.close()
        success, user, err = register_student_user(
            full_name=full_name,
            username=username,
            email=email,
            department="Computer Science & Engineering",
            semester=3,
            password=password,
            confirm_password=confirm_password,
            college_id=college_id,
            regulation_id=regulation_id,
            branch_id=branch_id
        )
        if err:
            flash(err, "danger")
            return render_template_string(LOGIN_TEMPLATE, active_tab="register")
        session['is_demo'] = False
        return redirect("/app/overview")
    return render_template_string(LOGIN_TEMPLATE, active_tab="register")

@server.route("/demo")
def demo_route():
    success, user = login_demo_user()
    if success:
        return redirect("/app/overview")
    return redirect("/login")

@server.route("/student")
@server.route("/dashboard")
@server.route("/dashboard/student")
def dashboard_redirect():
    return redirect("/app/overview")

@server.route("/logout")
def logout_route():
    logout_user()
    session.clear()
    return redirect("/")

# 3. Initialize Plotly Dash Application under /app/
app = Dash(
    __name__,
    server=server,
    routes_pathname_prefix="/app/",
    requests_pathname_prefix="/app/",
    assets_folder=str(BASE_DIR / "assets"),
    suppress_callback_exceptions=True,
    title="StudIQ.ai \u2014 Operational Student Intelligence"
)

app.index_string = '''<!DOCTYPE html>
<html lang="en" style="background:#000000 !important; color:#ffffff !important;">
    <head>
        {%metas%}
        <title>StudIQ.ai &mdash; Operational Student Intelligence</title>
        <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cg transform='rotate(-30 12 12)'%3E%3Ccircle cx='7.3' cy='3.2' r='1.45'/%3E%3Crect x='5.5' y='4.7' width='3.6' height='14.6' rx='1.8'/%3E%3Crect x='14.9' y='4.7' width='3.6' height='14.6' rx='1.8'/%3E%3Ccircle cx='16.7' cy='20.8' r='1.45'/%3E%3C/g%3E%3C/svg%3E">
        {%favicon%}
        {%css%}
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Instrument+Serif:ital@1&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="/assets/styles.css?v=35.0">
    </head>
    <body style="background:#000;color:#fff">
        <!-- Permanent 100% Unblocked Video Background Layer -->
        <div class="hero-photo">
            <video autoplay loop muted playsinline src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260818_072341_50851634-bbc3-4c33-9acc-7647d4db44aa.mp4"></video>
        </div>
        <div class="grain"></div>
    <!-- Global SVG Gradient Definitions for Plotly Charts -->
    <svg style="position: absolute; width: 0; height: 0; overflow: hidden;" aria-hidden="true">
      <defs>
        <linearGradient id="bar-vertical-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#38BDF8" stop-opacity="1" />
          <stop offset="50%" stop-color="#3B82F6" stop-opacity="0.9" />
          <stop offset="100%" stop-color="#1E1B4B" stop-opacity="0.8" />
        </linearGradient>
      </defs>
    </svg>


        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# 4. Define Root Layout & Dynamic Page Switcher
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="navbar-container"),
    html.Div(id="page-content")
])

@app.callback(
    [Output("navbar-container", "children"),
     Output("page-content", "children")],
    [Input("url", "pathname")]
)
def display_page(pathname):
    pathname = pathname or "/app/overview"
    is_auth = (current_user and current_user.is_authenticated) or session.get("is_demo", False)

    # Protected Dashboard Routes
    if not is_auth:
        return None, html.Div([
            dcc.Location(href="/login", id="auth-redirect"),
            html.Div("Redirecting to login...", className="text-secondary p-4 text-center")
        ])

    target_subroute = pathname.replace("/app", "")
    if target_subroute not in ("/overview", "/analytics", "/marks-subjects", "/attendance", "/academic-profile", "/settings"):
        target_subroute = "/overview"
    nav = create_framer_navbar_with_active(active_path=target_subroute)
    return nav, build_dashboard_shell(active_path=target_subroute)

# 5. Register All Reactive Callbacks
register_callbacks(app)

def bootstrap_application():
    """Initializes schema and default demo users upon startup."""
    init_db()
    seed_default_users()

if __name__ == "__main__":
    bootstrap_application()
    print(f"[*] Starting StudIQ on http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=False, dev_tools_ui=False, dev_tools_props_check=False)
