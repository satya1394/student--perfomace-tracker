"""
Application Entry Point.
Initializes Flask server, integrates Flask-Login, binds Plotly Dash, and routes views.
Dedicated Student Self-Service Academic Performance Platform.
"""

import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from flask import Flask, request, redirect, url_for, render_template_string, flash, session
from flask_login import current_user, login_required, logout_user
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

from app.config import Config
from app.database import init_db
from app.auth import login_manager, authenticate_user, seed_default_users, register_student_user, login_demo_user
from app.dashboards.components import create_navbar
from app.dashboards.hero_page import build_hero_page_layout
from app.dashboards.student_dashboard import build_student_dashboard_layout
from app.callbacks import register_callbacks

# 1. Initialize Flask Application
server = Flask(__name__)
server.config["SECRET_KEY"] = Config.SECRET_KEY
login_manager.init_app(server)

# 2. Flask Authentication Routes (HTML Form & Demo Quick-Login)
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudIQ | Student Self-Service Academic Analytics</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        @keyframes auroraFloat {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: #0A0E1A;
            background-image: 
                radial-gradient(ellipse 90% 60% at 50% -10%, rgba(0, 240, 255, 0.18), transparent 65%),
                radial-gradient(circle 800px at 90% 25%, rgba(168, 85, 247, 0.18), transparent 50%),
                radial-gradient(circle 700px at 10% 75%, rgba(16, 185, 129, 0.12), transparent 50%);
            background-size: 200% 200%;
            animation: auroraFloat 15s ease infinite;
            background-attachment: fixed;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF;
            padding: 24px 16px;
        }
        .portal-card {
            background: linear-gradient(160deg, rgba(17, 24, 39, 0.95) 0%, rgba(10, 14, 26, 0.98) 100%);
            backdrop-filter: blur(28px) saturate(180%);
            -webkit-backdrop-filter: blur(28px) saturate(180%);
            border: 1px solid rgba(0, 240, 255, 0.35);
            border-radius: 24px;
            box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.95), 0 0 35px rgba(0, 240, 255, 0.2);
            width: 100%;
            max-width: 540px;
            padding: 2.2rem;
            position: relative;
            overflow: hidden;
        }
        .portal-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00F0FF, #A855F7);
            box-shadow: 0 0 14px rgba(0, 240, 255, 0.6);
        }
        .brand-orb {
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00F0FF 0%, #A855F7 100%);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
            box-shadow: 0 0 25px rgba(0, 240, 255, 0.65);
        }
        .brand-text {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.85rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFFFFF 20%, #00F0FF 60%, #A855F7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .nav-tabs {
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        .nav-tabs .nav-link {
            color: #9CA3AF;
            border: none;
            border-radius: 9999px;
            padding: 8px 18px;
            font-weight: 700;
            font-size: 0.85rem;
            margin-right: 8px;
            transition: all 0.2s ease;
        }
        .nav-tabs .nav-link:hover {
            color: #FFFFFF;
            background: rgba(255, 255, 255, 0.05);
        }
        .nav-tabs .nav-link.active {
            color: #FFFFFF;
            background: linear-gradient(135deg, rgba(0, 240, 255, 0.25), rgba(168, 85, 247, 0.3));
            border: 1px solid rgba(0, 240, 255, 0.4);
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.25);
        }
        .form-control, .form-select {
            background-color: #111827;
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #FFFFFF;
            border-radius: 10px;
            padding: 0.65rem 0.9rem;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }
        .form-control:focus, .form-select:focus {
            background-color: #1F2937;
            border-color: #00F0FF;
            box-shadow: 0 0 0 3px rgba(0, 240, 255, 0.25);
            color: #FFFFFF;
        }
        .form-control::placeholder { color: #6B7280; }
        .form-label {
            font-size: 0.75rem;
            font-weight: 700;
            color: #9CA3AF;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.3rem;
        }
        .btn-portal {
            background: linear-gradient(135deg, #00F0FF 0%, #A855F7 100%);
            border: none;
            color: white;
            font-weight: 700;
            padding: 0.75rem;
            border-radius: 12px;
            font-size: 0.95rem;
            letter-spacing: 0.02em;
            box-shadow: 0 4px 18px rgba(0, 240, 255, 0.45);
            transition: all 0.25s ease;
        }
        .btn-portal:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 240, 255, 0.65);
            color: white;
        }
        .demo-btn {
            background: rgba(0, 240, 255, 0.08);
            border: 1px solid rgba(0, 240, 255, 0.3);
            color: #FFFFFF;
            padding: 0.75rem 1rem;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.875rem;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.2s ease;
        }
        .demo-btn:hover {
            background: rgba(0, 240, 255, 0.2);
            border-color: #00F0FF;
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.35);
            color: #FFFFFF;
            transform: translateY(-2px);
        }
        .validation-note {
            font-size: 0.7rem;
            color: #00F0FF;
            margin-top: 3px;
        }
    </style>
</head>
<body>
    <div class="portal-card">
        <div class="text-center mb-3">
            <a href="/" style="text-decoration: none;">
                <div class="brand-orb mb-2">⚡</div>
                <div class="brand-text">StudIQ</div>
            </a>
            <p class="text-secondary small mb-0">Student Self-Service Academic Performance Platform</p>
        </div>

        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="alert alert-{{ category }} py-2 px-3 small rounded-3 border-0 mb-3" style="background: rgba(0, 240, 255, 0.18); border: 1px solid rgba(0, 240, 255, 0.4); color: #E0F2FE;">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <!-- Navigation Tabs for Sign In vs Register -->
        <ul class="nav nav-tabs justify-content-center mb-3" id="authTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link {% if active_tab != 'register' %}active{% endif %}" id="login-tab" data-bs-toggle="tab" data-bs-target="#login-panel" type="button" role="tab">✦ Sign In</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link {% if active_tab == 'register' %}active{% endif %}" id="register-tab" data-bs-toggle="tab" data-bs-target="#register-panel" type="button" role="tab">✦ New Student Registration</button>
            </li>
        </ul>

        <div class="tab-content" id="authTabsContent">
            <!-- Sign In Panel -->
            <div class="tab-pane fade {% if active_tab != 'register' %}show active{% endif %}" id="login-panel" role="tabpanel">
                <form method="POST" action="/login">
                    <div class="mb-3">
                        <label class="form-label">Username or Academic Email</label>
                        <input type="text" name="username" class="form-control" placeholder="e.g. demo_user" required autofocus>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" placeholder="••••••••" required>
                    </div>
                    <button type="submit" class="btn btn-portal w-100 mb-3">Sign In to StudIQ →</button>
                </form>

                <div class="pt-3 border-top border-secondary border-opacity-25">
                    <div class="d-flex align-items-center justify-content-between mb-2">
                        <span class="small fw-bold text-uppercase text-muted" style="letter-spacing: 0.08em; font-size: 0.68rem;">Instant Access</span>
                        <span class="badge rounded-pill bg-info bg-opacity-25 text-info" style="font-size: 0.65rem;">SAMPLE DATA</span>
                    </div>
                    <a href="/demo" class="demo-btn">
                        <span>✦ Launch Interactive Demo Mode (Rahul Kumar)</span>
                        <span class="badge bg-info bg-opacity-25 text-info">R23 CSE</span>
                    </a>
                </div>
            </div>

            <!-- Registration Panel -->
            <div class="tab-pane fade {% if active_tab == 'register' %}show active{% endif %}" id="register-panel" role="tabpanel">
                <form method="POST" action="/register">
                    <div class="row g-2 mb-2">
                        <div class="col-6">
                            <label class="form-label">Full Name</label>
                            <input type="text" name="full_name" class="form-control" placeholder="e.g. Rohan Sharma" required>
                        </div>
                        <div class="col-6">
                            <label class="form-label">Roll Number</label>
                            <input type="text" name="roll_number" class="form-control" placeholder="e.g. 2024CSE102" required>
                        </div>
                    </div>
                    <div class="mb-2">
                        <label class="form-label">Username</label>
                        <input type="text" name="username" class="form-control" placeholder="Must contain Roll No, e.g. rohan_2024CSE102" required>
                        <div class="validation-note">✦ Rule: Username must contain your Roll Number</div>
                    </div>
                    <div class="mb-2">
                        <label class="form-label">Academic Email</label>
                        <input type="email" name="email" class="form-control" placeholder="rohan@university.edu" required>
                    </div>
                    <div class="mb-2">
                        <label class="form-label">College / University</label>
                        <select name="college_id" id="college_select" class="form-select" required>
                            <option value="1" selected>Raghu Engineering College</option>
                            <option value="2">Apex Institute of Engineering & Technology</option>
                            <option value="3">Indian Institute of Technology (IIT)</option>
                            <option value="4">National Institute of Technology (NIT)</option>
                            <option value="5">Delhi Technological University (DTU)</option>
                            <option value="6">Birla Institute of Technology and Science (BITS)</option>
                            <option value="7">Vellore Institute of Technology (VIT)</option>
                        </select>
                    </div>
                    <div class="row g-2 mb-2">
                        <div class="col-6">
                            <label class="form-label">Regulation Framework</label>
                            <select name="regulation_id" id="regulation_select" class="form-select" required>
                                <option value="1" selected>R23 - JNTU 2023 Syllabus</option>
                                <option value="2">R20 - CBCS Autonomous 2020</option>
                                <option value="3">R19 - Outcome Based Curriculum</option>
                                <option value="4">R21 - AICTE Model Curriculum</option>
                                <option value="5">R22 - Industry 4.0 Standard</option>
                            </select>
                        </div>
                        <div class="col-6">
                            <label class="form-label">Current Semester</label>
                            <select name="semester" class="form-select" required>
                                <option value="1">Semester 1</option>
                                <option value="2">Semester 2</option>
                                <option value="3" selected>Semester 3</option>
                                <option value="4">Semester 4</option>
                                <option value="5">Semester 5</option>
                                <option value="6">Semester 6</option>
                                <option value="7">Semester 7</option>
                                <option value="8">Semester 8</option>
                            </select>
                        </div>
                    </div>
                    <div class="mb-2">
                        <label class="form-label">Branch & Specialization</label>
                        <select name="branch_id" id="branch_select" class="form-select" required>
                            <option value="2" selected>CSD - Computer Science & Engineering (Data Science)</option>
                            <option value="1">CSE - Computer Science & Engineering (Core)</option>
                            <option value="3">CSM - Computer Science & Engineering (AI & ML)</option>
                            <option value="4">CSC - Computer Science & Engineering (Cyber Security)</option>
                            <option value="5">CSI - Computer Science & Engineering (IoT & Embedded Systems)</option>
                            <option value="6">ECE - Electronics & Communication (VLSI & Embedded)</option>
                            <option value="7">IT - Information Technology (Cloud & Web)</option>
                        </select>
                    </div>
                    <div class="row g-2 mb-3">
                        <div class="col-6">
                            <label class="form-label">Password</label>
                            <input type="password" name="password" class="form-control" placeholder="Min 8 chars" required>
                            <div class="validation-note">✦ Min 8 chars</div>
                        </div>
                        <div class="col-6">
                            <label class="form-label">Confirm Password</label>
                            <input type="password" name="confirm_password" class="form-control" placeholder="Repeat password" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-portal w-100 mb-2">Create StudIQ Profile & Enter →</button>
                </form>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


@server.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        success, res = authenticate_user(username, password)
        if success:
            session['is_demo'] = False
            flash("Successfully authenticated to StudIQ.", "success")
            return redirect("/student")
        flash(str(res), "danger")
        return render_template_string(LOGIN_TEMPLATE, active_tab="login")
    return render_template_string(LOGIN_TEMPLATE, active_tab="login")


@server.route("/register", methods=["GET", "POST"])
def register_route():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        roll_number = request.form.get("roll_number")
        username = request.form.get("username")
        email = request.form.get("email")
        college_id = request.form.get("college_id")
        regulation_id = request.form.get("regulation_id")
        branch_id = request.form.get("branch_id")
        semester = request.form.get("semester", 3)
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user, err = register_student_user(
            full_name=full_name,
            roll_number=roll_number,
            username=username,
            email=email,
            department="Computer Science & Engineering",
            semester=semester,
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
        flash(f"Welcome to StudIQ, {full_name}! Your academic profile is ready.", "success")
        return redirect("/student")
    return render_template_string(LOGIN_TEMPLATE, active_tab="register")


@server.route("/demo")
def demo_route():
    success, user = login_demo_user()
    if success:
        return redirect("/student")
    return redirect("/login")


@server.route("/logout")
def logout_route():
    logout_user()
    session.clear()
    return redirect("/")


# 3. Initialize Plotly Dash Application
app = Dash(
    __name__,
    server=server,
    url_base_pathname="/",
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="StudIQ | Intelligent Academic Performance Platform"
)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    </head>
    <body>
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
    if pathname in ("/", "/home") and not session.get("is_demo") and not (current_user and current_user.is_authenticated):
        return None, build_hero_page_layout()

    if pathname == "/demo":
        login_demo_user()
        nav = create_navbar(current_user)
        return nav, build_student_dashboard_layout()

    if pathname in ("/student", "/dashboard", "/"):
        nav = create_navbar(current_user)
        return nav, build_student_dashboard_layout()

    # Fallback
    return None, build_hero_page_layout()


# 5. Register All Reactive Callbacks
register_callbacks(app)


def bootstrap_application():
    """Initializes schema and default demo users upon startup."""
    init_db()
    seed_default_users()


if __name__ == "__main__":
    bootstrap_application()
    print(f"[*] Starting StudIQ Student Platform on http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=False, dev_tools_ui=False, dev_tools_props_check=False)
