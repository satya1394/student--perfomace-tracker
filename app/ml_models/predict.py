"""
Prediction and AI Recommendation Engine.
Applies trained models, computes SHAP feature importance, and generates personalized study roadmaps.
"""

import os
import sys
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.config import Config

# Cache for loaded models
_MODELS = {}


def load_ml_models():
    """Loads and caches ML artifacts from disk."""
    global _MODELS
    if _MODELS:
        return _MODELS

    model_dir = Path(Config.MODEL_DIR)
    try:
        _MODELS["scaler"] = joblib.load(model_dir / "scaler.pkl")
        _MODELS["rf_reg"] = joblib.load(model_dir / "rf_exam_score.pkl")
        _MODELS["log_reg"] = joblib.load(model_dir / "logreg_pass_fail.pkl")
        _MODELS["risk_model"] = joblib.load(model_dir / "risk_assessment_model.pkl")
        _MODELS["feature_names"] = joblib.load(model_dir / "feature_names.pkl")
    except Exception as e:
        # If models don't exist yet, lazily train them
        from app.ml_models.train_models import train_and_export_models
        train_and_export_models()
        _MODELS["scaler"] = joblib.load(model_dir / "scaler.pkl")
        _MODELS["rf_reg"] = joblib.load(model_dir / "rf_exam_score.pkl")
        _MODELS["log_reg"] = joblib.load(model_dir / "logreg_pass_fail.pkl")
        _MODELS["risk_model"] = joblib.load(model_dir / "risk_assessment_model.pkl")
        _MODELS["feature_names"] = joblib.load(model_dir / "feature_names.pkl")

    return _MODELS


def predict_student_performance(metrics: dict) -> dict:
    """
    Computes performance forecast, pass probability, risk level, and feature contributions.
    
    Args:
        metrics: dict containing past_cgpa, attendance_rate, internal_assessment, 
                 assignments_completed, study_hours_per_week, credit_load.
                 
    Returns:
        dict with predicted_score, pass_prob, risk_level, confidence, and shap_contributions.
    """
    models = load_ml_models()
    feat_names = models["feature_names"]

    # Build input row
    row = [
        float(metrics.get("past_cgpa", 7.0)),
        float(metrics.get("attendance_rate", 75.0)),
        float(metrics.get("internal_assessment", 20.0)),
        float(metrics.get("assignments_completed", 7)),
        float(metrics.get("study_hours_per_week", 18.0)),
        float(metrics.get("credit_load", 20.0))
    ]
    df_input = pd.DataFrame([row], columns=feat_names)

    # 1. Final Exam Score Regression
    pred_score = float(models["rf_reg"].predict(df_input)[0])
    pred_score = round(float(np.clip(pred_score, 0.0, 100.0)), 1)

    # 2. Pass/Fail Probability
    scaled_input = models["scaler"].transform(df_input)
    pass_prob = float(models["log_reg"].predict_proba(scaled_input)[0][1])
    pass_prob = round(pass_prob, 3)

    # 3. Risk Level Classification
    risk_idx = int(models["risk_model"].predict(df_input)[0])
    risk_map = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
    risk_level = risk_map.get(risk_idx, "LOW")

    risk_probs = models["risk_model"].predict_proba(df_input)[0]
    confidence = round(float(risk_probs[risk_idx]), 3)

    # 4. Feature Importance / Contribution breakdown
    importances = models["rf_reg"].feature_importances_
    contributions = {
        feat: round(float(imp * 100.0), 1) 
        for feat, imp in zip(feat_names, importances)
    }

    return {
        "predicted_score": pred_score,
        "pass_probability": pass_prob,
        "risk_level": risk_level,
        "confidence_score": confidence,
        "shap_contributions": contributions
    }


def generate_study_roadmap(metrics: dict, prediction: dict, weak_courses: list = None) -> dict:
    """
    Synthesizes topic-wise priorities and tailored remedial actions based on ML insights.
    """
    cgpa = metrics.get("past_cgpa", 7.0)
    attendance = metrics.get("attendance_rate", 75.0)
    risk = prediction.get("risk_level", "LOW")

    roadmap_steps = []
    if attendance < 75.0:
        roadmap_steps.append({
            "priority": "CRITICAL",
            "category": "Attendance & Engagement",
            "action": f"Current attendance is {attendance:.1f}%. Attend 100% of upcoming lectures to avoid exam debarment.",
            "target": "Reach >= 80% within 3 weeks"
        })

    if risk == "HIGH":
        roadmap_steps.append({
            "priority": "HIGH",
            "category": "Remedial Coaching",
            "action": "Enroll in weekly faculty office hours and peer-tutoring circles for foundational subjects.",
            "target": "Complete 4 mandatory problem sets weekly"
        })

    if weak_courses:
        for course in weak_courses[:2]:
            roadmap_steps.append({
                "priority": "HIGH",
                "category": f"Subject Focus: {course.get('course_name', 'Core Course')}",
                "action": f"Current Marks: {course.get('marks_obtained', 0):.1f}. Review previous exam papers and core theory.",
                "target": f"Improve to >= 65% in {course.get('course_code', 'Course')}"
            })

    roadmap_steps.append({
        "priority": "MEDIUM",
        "category": "Self-Study Strategy",
        "action": "Dedicate 3 blocks of 45-minute active recall & spaced repetition daily.",
        "target": "Maintain consistent 18+ study hours/week"
    })

    return {
        "status": "Roadmap Generated",
        "primary_focus": "Core Deficit Mitigation" if risk != "LOW" else "Excellence & Honors Track",
        "steps": roadmap_steps
    }
