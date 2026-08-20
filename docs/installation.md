# Installation and Deployment Guide

## 1. Prerequisites
- **Python**: 3.11 or higher
- **PostgreSQL**: Version 14+ (or Docker)
- **Git**

---

## 2. Local Environment Setup

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/your-org/student-performance-tracker.git
cd student-performance-tracker

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### Step 2: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env` and set your credentials:
```bash
cp .env.example .env
```

### Step 4: Generate Seed Data & Train ML Models
```bash
# Generate 1000+ students and seed database
python data/generate_seed_data.py

# Train Random Forest, Logistic Regression, and XGBoost models
python app/ml_models/train_models.py
```

### Step 5: Run Automated Tests
```bash
python -m unittest tests/test_platform.py -v
```

### Step 6: Start Web Application
```bash
python app/main.py
```
Open your browser at `http://127.0.0.1:8050`.

---

## 3. Docker Deployment (Recommended for Production)

### Run with Docker Compose
```bash
cd docker
docker-compose up --build -d
```
This automatically boots:
- PostgreSQL 16 on port `5432` with pre-loaded database schema and volume persistence.
- Web Application on port `8050` with all dependencies pre-configured.

---

## 4. Default Demo Credentials

| Role | Username | Password | Default Path |
|---|---|---|---|
| **Student** | `student_demo` | `Student@123` | `/student` |
| **Faculty** | `faculty_demo` | `Faculty@123` | `/faculty` |
| **Admin** | `admin_demo` | `Admin@123` | `/admin` |
