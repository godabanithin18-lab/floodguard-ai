from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from collections import deque
import joblib
import pandas as pd
import os
import requests

# Load trained model and feature list
model = joblib.load("flood_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")

app = FastAPI(
    title="Flash Flood Prediction API",
    description="AI-powered flood risk prediction for hilly regions",
    version="1.0.0"
)

# Allow frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the shape of incoming prediction requests
class FloodInput(BaseModel):
    MonsoonIntensity: float = Field(..., ge=0, le=20)
    TopographyDrainage: float = Field(..., ge=0, le=20)
    RiverManagement: float = Field(..., ge=0, le=20)
    Deforestation: float = Field(..., ge=0, le=20)
    Urbanization: float = Field(..., ge=0, le=20)
    ClimateChange: float = Field(..., ge=0, le=20)
    DamsQuality: float = Field(..., ge=0, le=20)
    Siltation: float = Field(..., ge=0, le=20)
    AgriculturalPractices: float = Field(..., ge=0, le=20)
    Encroachments: float = Field(..., ge=0, le=20)
    IneffectiveDisasterPreparedness: float = Field(..., ge=0, le=20)
    DrainageSystems: float = Field(..., ge=0, le=20)
    CoastalVulnerability: float = Field(..., ge=0, le=20)
    Landslides: float = Field(..., ge=0, le=20)
    Watersheds: float = Field(..., ge=0, le=20)
    DeterioratingInfrastructure: float = Field(..., ge=0, le=20)
    PopulationScore: float = Field(..., ge=0, le=20)
    WetlandLoss: float = Field(..., ge=0, le=20)
    InadequatePlanning: float = Field(..., ge=0, le=20)
    PoliticalFactors: float = Field(..., ge=0, le=20)


class NotifyRequest(BaseModel):
    recipient_email: str
    stations: list[dict]
audit_log = deque(maxlen=50)

def log_audit(event_type: str, details: dict):
    audit_log.appendleft({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": event_type,
        "details": details,
    })

@app.get("/audit-log")
def get_audit_log():
    return {"count": len(audit_log), "entries": list(audit_log)}

def get_risk_level(probability: float) -> str:
    if probability < 0.35:
        return "Low"
    elif probability < 0.55:
        return "Moderate"
    elif probability < 0.70:
        return "High"
    else:
        return "Severe"

def get_recommended_actions(risk_level: str) -> list[str]:
    actions_map = {
        "Low": [
            "Continue routine monitoring",
            "No immediate action required",
        ],
        "Moderate": [
            "Increase observation frequency",
            "Notify local monitoring station",
            "Review drainage and preparedness status",
        ],
        "High": [
            "Alert district disaster-management authority",
            "Monitor downstream settlements",
            "Increase observation frequency",
            "Pre-position emergency response resources",
        ],
        "Severe": [
            "Alert district disaster-management authority",
            "Monitor downstream settlements",
            "Prepare evacuation routes",
            "Increase observation frequency to continuous",
            "Issue public warning if threshold persists",
        ],
    }
    return actions_map.get(risk_level, [])


def get_confidence_assessment(input_dict: dict) -> dict:
    extreme_count = sum(1 for v in input_dict.values() if v <= 1 or v >= 19)
    if extreme_count >= 5:
        input_confidence = "Low — multiple factors at extreme boundary values"
    elif extreme_count >= 2:
        input_confidence = "Moderate — some factors at boundary values"
    else:
        input_confidence = "High — inputs within typical operating range"

    return {
        "input_range_confidence": input_confidence,
        "extreme_factor_count": extreme_count,
        "note": "Reflects how typical the input values are, not a fitted statistical margin of error — the model's test-set residual error is effectively zero by construction (see Model Card).",
    }
@app.get("/")
def root():
    return {"message": "Flash Flood Prediction API is running", "status": "healthy"}


@app.post("/predict")
def predict_flood(data: FloodInput):
    input_dict = data.dict()
    input_df = pd.DataFrame([input_dict])[feature_columns]

    probability = float(model.predict(input_df)[0])
    probability = max(0.0, min(1.0, probability))

    risk_level = get_risk_level(probability)

    contributions = {}
    for i, feature in enumerate(feature_columns):
        coef = model.coef_[i]
        value = input_dict[feature]
        contributions[feature] = coef * value

    total_contribution = sum(contributions.values())

    factor_breakdown = []
    if total_contribution > 0:
        for feature, contribution in sorted(contributions.items(), key=lambda x: x[1], reverse=True)[:5]:
            percentage = (contribution / total_contribution) * probability * 100
            factor_breakdown.append({
                "factor": feature,
                "contribution_percent": round(percentage, 1)
            })

    primary_driver = factor_breakdown[0]["factor"] if factor_breakdown else None
    log_audit("prediction", {
        "risk_percentage": round(probability * 100, 2),
        "risk_level": risk_level,
        "primary_driver": primary_driver,
    })

    return {
        "flood_probability": round(probability, 4),
        "risk_percentage": round(probability * 100, 2),
        "risk_level": risk_level,
        "factor_breakdown": factor_breakdown,
        "primary_driver": primary_driver,
        "input_summary": input_dict,
        "recommended_actions": get_recommended_actions(risk_level),
        "confidence_assessment": get_confidence_assessment(input_dict)
    }
@app.get("/model-transparency")
def model_transparency():
    coefficients = {
        feature: round(float(coef), 4)
        for feature, coef in zip(feature_columns, model.coef_)
    }
    return {
        "model_type": "Linear Regression",
        "intercept": round(float(model.intercept_), 6),
        "coefficients": coefficients,
        "note": "All 20 coefficients are nearly identical (~0.005), confirming the target variable was constructed as an equal-weighted linear combination."
    }



def rainfall_to_monsoon_intensity(rainfall_mm: float) -> float:
    intensity = rainfall_mm / 10
    return round(min(max(intensity, 0), 20), 1)


@app.get("/live-weather")
def get_live_weather(lat: float, lon: float):
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "precipitation,rain,temperature_2m",
                "timezone": "auto",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()["current"]
        rainfall_mm = data.get("precipitation", 0)
        return {
            "source": "Open-Meteo (live)",
            "rainfall_mm": rainfall_mm,
            "temperature_c": data.get("temperature_2m"),
            "derived_monsoon_intensity": rainfall_to_monsoon_intensity(rainfall_mm),
            "fetched_at": data.get("time"),
        }
    except Exception as e:
        return {"error": str(e), "source": "Open-Meteo (live)", "status": "unavailable"}


@app.get("/historical-check")
def historical_flood_check():
    try:
        response = requests.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params={
                "latitude": 31.0408,
                "longitude": 78.7811,
                "start_date": "2025-08-05",
                "end_date": "2025-08-05",
                "daily": "precipitation_sum",
                "timezone": "auto",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        actual_rainfall_mm = data["daily"]["precipitation_sum"][0]
        derived_intensity = rainfall_to_monsoon_intensity(actual_rainfall_mm)

        test_input = {
            "MonsoonIntensity": derived_intensity,
            "TopographyDrainage": 4, "RiverManagement": 4, "Deforestation": 13,
            "Urbanization": 4, "ClimateChange": 14, "DamsQuality": 4, "Siltation": 12,
            "AgriculturalPractices": 6, "Encroachments": 5,
            "IneffectiveDisasterPreparedness": 13, "DrainageSystems": 4,
            "CoastalVulnerability": 1, "Landslides": 16, "Watersheds": 8,
            "DeterioratingInfrastructure": 12, "PopulationScore": 4,
            "WetlandLoss": 7, "InadequatePlanning": 12, "PoliticalFactors": 7,
        }
        input_df = pd.DataFrame([test_input])[feature_columns]
        probability = max(0.0, min(1.0, float(model.predict(input_df)[0])))

        return {
            "event": "2025 Uttarakhand Flash Flood — Dharali",
            "actual_event_date": "2025-08-05",
            "actual_rainfall_mm": actual_rainfall_mm,
            "derived_monsoon_intensity": derived_intensity,
            "model_predicted_risk_percentage": round(probability * 100, 2),
            "model_predicted_severity": get_risk_level(probability),
            "note": "Rainfall is real historical data (Open-Meteo archive). Other 19 factors are estimated regional values, not verified historical records.",
        }
    except Exception as e:
        return {"error": str(e), "status": "unavailable"}

HISTORICAL_EVENTS = [
    {"event": "Dharali Flash Flood, Uttarakhand", "date": "2025-08-05", "lat": 31.0408, "lon": 78.7811, "expected": "flood",
     "vulnerability": {"TopographyDrainage": 4, "RiverManagement": 4, "Deforestation": 13, "Urbanization": 4, "ClimateChange": 14, "DamsQuality": 4, "Siltation": 12, "AgriculturalPractices": 6, "Encroachments": 5, "IneffectiveDisasterPreparedness": 13, "DrainageSystems": 4, "CoastalVulnerability": 1, "Landslides": 16, "Watersheds": 8, "DeterioratingInfrastructure": 12, "PopulationScore": 4, "WetlandLoss": 7, "InadequatePlanning": 12, "PoliticalFactors": 7}},
    {"event": "Kedarnath Floods, Uttarakhand", "date": "2013-06-17", "lat": 30.7346, "lon": 79.0669, "expected": "flood",
     "vulnerability": {"TopographyDrainage": 3, "RiverManagement": 3, "Deforestation": 11, "Urbanization": 5, "ClimateChange": 12, "DamsQuality": 3, "Siltation": 13, "AgriculturalPractices": 5, "Encroachments": 6, "IneffectiveDisasterPreparedness": 15, "DrainageSystems": 3, "CoastalVulnerability": 1, "Landslides": 18, "Watersheds": 9, "DeterioratingInfrastructure": 13, "PopulationScore": 8, "WetlandLoss": 6, "InadequatePlanning": 14, "PoliticalFactors": 6}},
    {"event": "Wayanad Floods, Kerala", "date": "2018-08-16", "lat": 11.6854, "lon": 76.1320, "expected": "flood",
     "vulnerability": {"TopographyDrainage": 5, "RiverManagement": 5, "Deforestation": 12, "Urbanization": 6, "ClimateChange": 13, "DamsQuality": 6, "Siltation": 10, "AgriculturalPractices": 8, "Encroachments": 6, "IneffectiveDisasterPreparedness": 11, "DrainageSystems": 5, "CoastalVulnerability": 4, "Landslides": 14, "Watersheds": 7, "DeterioratingInfrastructure": 9, "PopulationScore": 7, "WetlandLoss": 8, "InadequatePlanning": 10, "PoliticalFactors": 6}},
    {"event": "Chennai Floods, Tamil Nadu", "date": "2015-12-02", "lat": 13.0827, "lon": 80.2707, "expected": "flood",
     "vulnerability": {"TopographyDrainage": 6, "RiverManagement": 6, "Deforestation": 5, "Urbanization": 15, "ClimateChange": 11, "DamsQuality": 7, "Siltation": 9, "AgriculturalPractices": 4, "Encroachments": 14, "IneffectiveDisasterPreparedness": 12, "DrainageSystems": 15, "CoastalVulnerability": 12, "Landslides": 1, "Watersheds": 6, "DeterioratingInfrastructure": 11, "PopulationScore": 16, "WetlandLoss": 13, "InadequatePlanning": 13, "PoliticalFactors": 8}},
    {"event": "Mumbai Deluge, Maharashtra", "date": "2005-07-26", "lat": 19.0760, "lon": 72.8777, "expected": "flood",
     "vulnerability": {"TopographyDrainage": 6, "RiverManagement": 5, "Deforestation": 4, "Urbanization": 17, "ClimateChange": 10, "DamsQuality": 6, "Siltation": 10, "AgriculturalPractices": 3, "Encroachments": 15, "IneffectiveDisasterPreparedness": 13, "DrainageSystems": 16, "CoastalVulnerability": 14, "Landslides": 1, "Watersheds": 5, "DeterioratingInfrastructure": 12, "PopulationScore": 17, "WetlandLoss": 14, "InadequatePlanning": 12, "PoliticalFactors": 8}},
    {"event": "Srinagar Floods, J&K", "date": "2014-09-07", "lat": 34.0837, "lon": 74.7973, "expected": "flood",
     "vulnerability": {"TopographyDrainage": 5, "RiverManagement": 4, "Deforestation": 8, "Urbanization": 8, "ClimateChange": 11, "DamsQuality": 5, "Siltation": 11, "AgriculturalPractices": 6, "Encroachments": 9, "IneffectiveDisasterPreparedness": 12, "DrainageSystems": 6, "CoastalVulnerability": 2, "Landslides": 7, "Watersheds": 9, "DeterioratingInfrastructure": 10, "PopulationScore": 9, "WetlandLoss": 12, "InadequatePlanning": 11, "PoliticalFactors": 8}},
    {"event": "Kolhapur Floods, Maharashtra", "date": "2019-08-06", "lat": 16.7050, "lon": 74.2433, "expected": "flood",
     "vulnerability": {"TopographyDrainage": 6, "RiverManagement": 5, "Deforestation": 7, "Urbanization": 9, "ClimateChange": 11, "DamsQuality": 6, "Siltation": 12, "AgriculturalPractices": 9, "Encroachments": 8, "IneffectiveDisasterPreparedness": 11, "DrainageSystems": 7, "CoastalVulnerability": 1, "Landslides": 5, "Watersheds": 8, "DeterioratingInfrastructure": 9, "PopulationScore": 8, "WetlandLoss": 9, "InadequatePlanning": 10, "PoliticalFactors": 7}},
    {"event": "Patna Floods, Bihar", "date": "2019-09-28", "lat": 25.5941, "lon": 85.1376, "expected": "flood",
     "vulnerability": {"TopographyDrainage": 7, "RiverManagement": 6, "Deforestation": 5, "Urbanization": 10, "ClimateChange": 10, "DamsQuality": 6, "Siltation": 14, "AgriculturalPractices": 7, "Encroachments": 11, "IneffectiveDisasterPreparedness": 13, "DrainageSystems": 13, "CoastalVulnerability": 2, "Landslides": 1, "Watersheds": 7, "DeterioratingInfrastructure": 13, "PopulationScore": 12, "WetlandLoss": 10, "InadequatePlanning": 13, "PoliticalFactors": 9}},
    {"event": "Chamoli GLOF Flood, Uttarakhand", "date": "2021-02-07", "lat": 30.4157, "lon": 79.5680, "expected": "flood",
     "vulnerability": {"TopographyDrainage": 3, "RiverManagement": 4, "Deforestation": 10, "Urbanization": 3, "ClimateChange": 15, "DamsQuality": 5, "Siltation": 11, "AgriculturalPractices": 4, "Encroachments": 3, "IneffectiveDisasterPreparedness": 14, "DrainageSystems": 4, "CoastalVulnerability": 1, "Landslides": 17, "Watersheds": 10, "DeterioratingInfrastructure": 11, "PopulationScore": 3, "WetlandLoss": 5, "InadequatePlanning": 13, "PoliticalFactors": 6}},
    {"event": "Leh Cloudburst Flood, Ladakh", "date": "2010-08-06", "lat": 34.1526, "lon": 77.5771, "expected": "flood",
     "vulnerability": {"TopographyDrainage": 4, "RiverManagement": 3, "Deforestation": 3, "Urbanization": 4, "ClimateChange": 12, "DamsQuality": 4, "Siltation": 9, "AgriculturalPractices": 3, "Encroachments": 4, "IneffectiveDisasterPreparedness": 14, "DrainageSystems": 3, "CoastalVulnerability": 1, "Landslides": 13, "Watersheds": 6, "DeterioratingInfrastructure": 10, "PopulationScore": 4, "WetlandLoss": 4, "InadequatePlanning": 12, "PoliticalFactors": 6}},
    {"event": "Dharali — Dry Winter Day (control)", "date": "2025-02-05", "lat": 31.0408, "lon": 78.7811, "expected": "no_flood",
     "vulnerability": {"TopographyDrainage": 4, "RiverManagement": 4, "Deforestation": 13, "Urbanization": 4, "ClimateChange": 14, "DamsQuality": 4, "Siltation": 12, "AgriculturalPractices": 6, "Encroachments": 5, "IneffectiveDisasterPreparedness": 13, "DrainageSystems": 4, "CoastalVulnerability": 1, "Landslides": 16, "Watersheds": 8, "DeterioratingInfrastructure": 12, "PopulationScore": 4, "WetlandLoss": 7, "InadequatePlanning": 12, "PoliticalFactors": 7}},
    {"event": "Kedarnath — Dry Winter Day (control)", "date": "2013-01-17", "lat": 30.7346, "lon": 79.0669, "expected": "no_flood",
     "vulnerability": {"TopographyDrainage": 3, "RiverManagement": 3, "Deforestation": 11, "Urbanization": 5, "ClimateChange": 12, "DamsQuality": 3, "Siltation": 13, "AgriculturalPractices": 5, "Encroachments": 6, "IneffectiveDisasterPreparedness": 15, "DrainageSystems": 3, "CoastalVulnerability": 1, "Landslides": 18, "Watersheds": 9, "DeterioratingInfrastructure": 13, "PopulationScore": 8, "WetlandLoss": 6, "InadequatePlanning": 14, "PoliticalFactors": 6}},
]


@app.get("/historical-validation-set")
def historical_validation_set():
    results = []
    for ev in HISTORICAL_EVENTS:
        try:
            response = requests.get(
                "https://archive-api.open-meteo.com/v1/archive",
                params={
                    "latitude": ev["lat"], "longitude": ev["lon"],
                    "start_date": ev["date"], "end_date": ev["date"],
                    "daily": "precipitation_sum", "timezone": "auto",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            actual_rainfall = data["daily"]["precipitation_sum"][0]
            derived_intensity = rainfall_to_monsoon_intensity(actual_rainfall)

            test_input = {"MonsoonIntensity": derived_intensity, **ev["vulnerability"]}
            input_df = pd.DataFrame([test_input])[feature_columns]
            probability = max(0.0, min(1.0, float(model.predict(input_df)[0])))
            severity = get_risk_level(probability)

            correct = (
                severity in ["High", "Severe"] if ev["expected"] == "flood"
                else severity in ["Low", "Moderate"]
            )

            results.append({
                "event": ev["event"],
                "date": ev["date"],
                "expected": ev["expected"],
                "actual_rainfall_mm": actual_rainfall,
                "derived_monsoon_intensity": derived_intensity,
                "predicted_risk_percentage": round(probability * 100, 2),
                "predicted_severity": severity,
                "correctly_classified": correct,
            })
        except Exception as e:
            results.append({"event": ev["event"], "date": ev["date"], "error": str(e)})

    flood_events = [r for r in results if r.get("expected") == "flood"]
    control_events = [r for r in results if r.get("expected") == "no_flood"]
    flood_correct = sum(1 for r in flood_events if r.get("correctly_classified"))
    control_correct = sum(1 for r in control_events if r.get("correctly_classified"))

    return {
        "flood_events_tested": len(flood_events),
        "flood_events_correctly_flagged": flood_correct,
        "control_days_tested": len(control_events),
        "control_days_correctly_avoided_false_alarm": control_correct,
        "results": results,
        "note": "Rainfall is real historical data (Open-Meteo archive) for each event's actual date and location. Other 19 factors are estimated regional vulnerability values, not verified historical records. Control days test whether the model avoids false Severe alarms on non-flood days at the same high-vulnerability locations.",
    }
@app.post("/notify")
def notify_authorities(data: NotifyRequest):
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        return {"status": "error", "message": "Email service not configured on server."}

    station_rows = "".join(
        f"<tr><td style='padding:8px 12px;border-bottom:1px solid #334155;'>{s['name']}</td>"
        f"<td style='padding:8px 12px;border-bottom:1px solid #334155;'>{s['district']}</td>"
        f"<td style='padding:8px 12px;border-bottom:1px solid #334155;color:#ef4444;font-weight:bold;'>{s['risk_level']}</td>"
        f"<td style='padding:8px 12px;border-bottom:1px solid #334155;'>{s['risk_percentage']}%</td></tr>"
        for s in data.stations
    )

    html_body = f"""
    <div style="font-family:sans-serif;background:#0a0e17;color:#f8fafc;padding:24px;">
      <h2 style="color:#ef4444;">🚨 Severe Flood Risk Alert — FloodGuard AI</h2>
      <p>The following station(s) are currently showing <b>Severe</b> flood risk and require immediate attention:</p>
      <table style="border-collapse:collapse;width:100%;margin-top:12px;">
        <tr style="background:#111827;">
          <th style="padding:8px 12px;text-align:left;">Station</th>
          <th style="padding:8px 12px;text-align:left;">District</th>
          <th style="padding:8px 12px;text-align:left;">Severity</th>
          <th style="padding:8px 12px;text-align:left;">Risk Score</th>
        </tr>
        {station_rows}
      </table>
      <p style="margin-top:20px;color:#94a3b8;font-size:13px;">
        This is an automated alert from FloodGuard AI — a prototype early warning system.
        Prediction based on trained model, not an official meteorological forecast.
      </p>
    </div>
    """

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "from": "FloodGuard AI <onboarding@resend.dev>",
                "to": [data.recipient_email],
                "subject": f"🚨 Severe Flood Risk Alert — {len(data.stations)} Station(s) Affected",
                "html": html_body,
            },
            timeout=10,
        )
        response.raise_for_status()
        log_audit("alert_dispatched", {
            "recipient": data.recipient_email,
            "stations": [s["name"] for s in data.stations],
        })
        return {
            "status": "sent",
            "recipient": data.recipient_email,
            "dispatched_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
class ResponseAction(BaseModel):
    station_name: str
    action: str
    notes: str = ""


@app.post("/respond-to-alert")
def respond_to_alert(data: ResponseAction):
    log_audit("response_action", {
        "station": data.station_name,
        "action": data.action,
        "notes": data.notes,
    })
    return {
        "status": "logged",
        "station": data.station_name,
        "action": data.action,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }    