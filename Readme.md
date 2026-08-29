# 🌊 FloodGuard AI
### AI-Powered Flash Flood Early Warning System

<p align="center">
  <img src="https://img.shields.io/badge/Status-Live-brightgreen" alt="status" />
  <img src="https://img.shields.io/badge/Model-Linear%20Regression-blue" alt="model" />
  <img src="https://img.shields.io/badge/Frontend-Next.js%2016-black" alt="nextjs" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688" alt="fastapi" />
</p>

<p align="center">
  <b>🔗 Live Demo:</b> <a href="https://floodguard-ai-five.vercel.app">floodguard-ai-five.vercel.app</a><br/>
  <b>📘 API Docs:</b> <a href="https://floodguard-ai-mvp8.onrender.com/docs">floodguard-ai-mvp8.onrender.com/docs</a><br/>
  <b>💻 Repository:</b> <a href="https://github.com/godabanithin18-lab/floodguard-ai">github.com/godabanithin18-lab/floodguard-ai</a>
</p>

---

## 🎯 Problem Statement

**SIH26192** — Flash Flood Prediction System for Hilly Regions using Multi-Source Data
*Ministry of Home Affairs*

Flash floods in India's hill states (Uttarakhand, Himachal Pradesh) often strike with only hours — sometimes minutes — of warning. Manual risk assessment is slow, and rainfall/terrain/infrastructure data is fragmented across departments. **FloodGuard AI** fuses these factors into a single, real-time, explainable risk score, giving communities and disaster-response teams critical hours to prepare.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🗺️ **Live Risk Map** | Interactive dark-themed map with color-coded severity markers across 6 hill-region monitoring stations |
| 🤖 **AI-Powered Prediction** | ML model trained on 20 real-world-style flood risk factors |
| 🎛️ **"Try It Yourself"** | Live sliders let anyone simulate conditions and get instant AI predictions |
| 🧠 **AI Decision Explanation** | Transparent factor-by-factor breakdown of *why* a location is high-risk — not a black box |
| 🚨 **Automated Alerts** | Animated warning banner triggers automatically when any station shows severe risk |
| 📊 **Data Visualization** | Live-updating bar chart of current risk factor levels |
| 📋 **Station Risk Rankings** | All monitored locations ranked by predicted risk, updated in real time |

---

## 🏗️ System Architecture

```
   Risk Factor Inputs (Monsoon, Terrain, Drainage, Infrastructure...)
                              │
                              ▼
                     Feature Preparation
                    (20 numeric inputs, 0–20 scale)
                              │
                              ▼
                  Trained ML Model (Linear Regression)
                              │
                              ▼
                     Risk Score Engine
             (probability → Low / Moderate / High / Severe)
                              │
                              ▼
                    FastAPI REST API (/predict)
                              │
                              ▼
                    Next.js Dashboard (React)
                              │
                              ▼
          Live Map · Station Rankings · Alerts · Explainability Charts
```

**Flow in practice:** the frontend sends a station's (or a user's custom) risk-factor values to the backend → the model returns a risk score, severity label, and a ranked factor-contribution breakdown → the dashboard renders all of it live, with an automated alert banner triggering when any location crosses into Severe.

---

## 🖥️ Tech Stack

**Frontend**
`Next.js 16` · `TypeScript` · `Tailwind CSS` · `Leaflet.js` · `Recharts` · `Framer Motion`

**Backend**
`FastAPI` · `Python` · `scikit-learn` · `pandas`

**Deployment**
`Vercel` (frontend) · `Render` (backend)

---

## 🧠 ML Methodology

| Step | Detail |
|---|---|
| **Input features** | 20 numeric risk factors — MonsoonIntensity, TopographyDrainage, RiverManagement, Deforestation, Urbanization, ClimateChange, DamsQuality, Siltation, AgriculturalPractices, Encroachments, IneffectiveDisasterPreparedness, DrainageSystems, CoastalVulnerability, Landslides, Watersheds, DeterioratingInfrastructure, PopulationScore, WetlandLoss, InadequatePlanning, PoliticalFactors |
| **Target variable** | `FloodProbability` — continuous value between 0 and 1 |
| **Preprocessing** | Dataset arrived fully clean (0 missing values, all numeric) — no imputation or encoding needed |
| **Train/test methodology** | 80/20 split, `random_state=42` — 40,000 training samples / 10,000 test samples |
| **Model selection** | Benchmarked 3 regressors — Linear Regression, Random Forest, Gradient Boosting — on identical splits |
| **Evaluation metrics** | R², MAE, RMSE on held-out test data |
| **Prediction → category** | Raw probability (0–1) converted to a 0–100 risk score, then bucketed: **&lt;35 Low · 35–55 Moderate · 55–70 High · 70+ Severe** |

---

## 📊 Dataset

| Attribute | Detail |
|---|---|
| **Source** | Public Kaggle dataset — `naiyakhalid/flood-prediction-dataset` |
| **Records** | 50,000 |
| **Features** | 20 numeric risk factors + 1 target (`FloodProbability`) |
| **Geographic coverage** | Not region-tagged in the source data — generalized risk-factor scoring, not GPS-linked |
| **Time period** | Not time-series — static, per-record risk snapshots |
| **Missing values** | None — dataset arrived fully clean |
| **Data nature** | ⚠️ **Synthetic** — engineered by the dataset's original authors to mirror real flood-risk relationships. No verified real-world ground-truth source (disclosed in the dataset's own documentation) |

**Monitoring stations shown on the live map** use **real GPS coordinates** of actual hill towns — Dharali, Uttarkashi, Manali, Kullu Town, Shimla, and Rishikesh — including two genuine flood-affected regions from the 2025 Uttarakhand flash flood. Their risk-factor *values*, however, are **manually assigned static estimates** based on general regional characteristics (e.g., higher deforestation/landslide risk for less-developed high-altitude towns) — **not live sensor or real-time government data feeds.**

**What this means:** FloodGuard AI is a fully functional, end-to-end proof-of-concept demonstrating the complete ML + early-warning pipeline. It is not currently connected to live sensors or verified real-time meteorological feeds. Production deployment would require retraining on verified real rainfall/flood records (e.g., IMD, CWC river gauge data) and replacing manual station values with live data sources.

---

## 📈 Model Performance

⚠️ **Read this before the numbers below:** A perfect R² does not mean "near-perfect real-world flood prediction." It means our model correctly recovered the *exact mathematical formula* the dataset's authors used to synthetically generate the target variable — each of the 20 factors was combined with equal linear weight (confirmed via coefficient inspection). This is a meaningful result for **model correctness and interpretability**, not a claim about real-world predictive accuracy, which would require validation against genuine historical flood records.

| Model | R² Score | MAE | RMSE |
|---|:---:|:---:|:---:|
| **Linear Regression** ✅ | **1.0000** | **0.00000** | **0.00000** |
| Gradient Boosting | 0.9195 | 0.01111 | 0.01416 |
| Random Forest | 0.7110 | 0.02122 | 0.02683 |

### Why Linear Regression?

We didn't assume it — we tested it against Random Forest and Gradient Boosting. Linear Regression won because inspecting its fitted coefficients revealed the target variable is a genuinely linear, equally-weighted combination of all 20 factors (each coefficient ≈ 0.005). This isn't a shortcut — it's the mathematically correct fit for this data, and it comes with a major bonus: **every prediction is fully explainable** as a transparent weighted sum, which matters when officials need to trust *why* a location is flagged high-risk, not just accept a black-box score.

> ⚠️ **Honesty note:** The Risk Score shown in the app is a prototype model estimate based on manually-assigned station data — not a statistically calibrated probability, live sensor reading, or official meteorological forecast.

---

## 🔍 Explainability — How Contributions Are Calculated

Every prediction includes a live factor breakdown, e.g.:

```
Monsoon Intensity        ██████████  9.0%
Landslides                ████████   8.0%
Deforestation              ███████   7.5%
Climate Change              ██████   7.0%
Ineffective Preparedness    █████    6.5%
```

**How it's computed:** since the model is Linear Regression, each factor's contribution to a given prediction is `(coefficient × input value)`, normalized against the total predicted risk and expressed as a percentage. This is **not a heuristic or approximation layered on top** — it's derived directly from the model's own learned weights, so the explanation shown is mathematically identical to what actually drove the prediction.

---

## 🧪 Example Prediction

**Input (sample high-risk scenario):**

| Factor | Value (0–20 scale) |
|---|:---:|
| MonsoonIntensity | 18 |
| Landslides | 16 |
| Deforestation | 15 |
| ClimateChange | 14 |
| IneffectiveDisasterPreparedness | 13 |
| *(remaining 15 factors)* | moderate/low values |

**Output:**
```
Predicted Risk Score:  86.5 / 100
Severity:              SEVERE
Primary Driver:        Monsoon Intensity

Top Contributing Factors:
  Monsoon Intensity           +9.0%
  Landslides                  +8.0%
  Deforestation                +7.5%
  Climate Change                +7.0%
  Ineffective Preparedness      +6.5%
```

This exact scenario is reproducible live on the dashboard's **"Try It Yourself"** panel.

---

## 🗺️ Monitoring Stations

| Station | District | Coordinates | Notes |
|---|---|---|---|
| Dharali | Uttarkashi, Uttarakhand | 31.0408, 78.7811 | Real 2025 flash flood site |
| Uttarkashi | Uttarkashi, Uttarakhand | 30.7268, 78.4354 | Real 2025 flash flood affected region |
| Manali | Kullu, Himachal Pradesh | 32.2432, 77.1892 | — |
| Kullu Town | Kullu, Himachal Pradesh | 31.9576, 77.1095 | — |
| Shimla | Shimla, Himachal Pradesh | 31.1048, 77.1734 | — |
| Rishikesh | Dehradun, Uttarakhand | 30.0869, 78.2676 | — |

---

## 🚀 Local Setup

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Runs at `http://127.0.0.1:8000` · Interactive docs at `/docs`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs at `http://localhost:3000`

---

## 🗺️ Roadmap

- [ ] Live sensor / IMD API integration to replace manually-assigned station data
- [ ] Validation against verified historical flood records
- [ ] Confidence interval calibration for risk scores
- [ ] Expand coverage to additional hill-region states

---

## 👤 Team

**[Your Name / Team Name]**
Built for Smart India Hackathon 2026

---

<p align="center">Made with ☕ and a lot of debugging</p>