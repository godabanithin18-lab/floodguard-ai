from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
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


def get_risk_level(probability: float) -> str:
    if probability < 0.35:
        return "Low"
    elif probability < 0.55:
        return "Moderate"
    elif probability < 0.70:
        return "High"
    else:
        return "Severe"


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

    return {
        "flood_probability": round(probability, 4),
        "risk_percentage": round(probability * 100, 2),
        "risk_level": risk_level,
        "factor_breakdown": factor_breakdown,
        "primary_driver": primary_driver,
        "input_summary": input_dict
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
        return {
            "status": "sent",
            "recipient": data.recipient_email,
            "dispatched_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}