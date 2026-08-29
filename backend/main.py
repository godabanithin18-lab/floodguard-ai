from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd

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