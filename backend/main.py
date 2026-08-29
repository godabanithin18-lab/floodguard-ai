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

    # Predict
    probability = float(model.predict(input_df)[0])
    probability = max(0.0, min(1.0, probability))

    risk_level = get_risk_level(probability)

    # Calculate each factor's real contribution using the model's actual coefficients
    contributions = {}
    for i, feature in enumerate(feature_columns):
        coef = model.coef_[i]
        value = input_dict[feature]
        contributions[feature] = coef * value

    total_contribution = sum(contributions.values())

    # Convert to percentage of total predicted risk, sorted highest first
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