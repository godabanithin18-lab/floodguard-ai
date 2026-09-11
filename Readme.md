# 🌊 FloodGuard AI
### An Explainable Flash-Flood Intelligence Platform for India's Hilly Regions

<p align="center">
  <img src="https://img.shields.io/badge/Status-Live-brightgreen" alt="status" />
  <img src="https://img.shields.io/badge/Model-Linear%20Regression-blue" alt="model" />
  <img src="https://img.shields.io/badge/Frontend-Next.js%2016-black" alt="nextjs" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688" alt="fastapi" />
  <img src="https://img.shields.io/badge/Live%20Weather-Open--Meteo-06b6d4" alt="weather" />
  <img src="https://img.shields.io/badge/Alerts-Email%20(Resend)-orange" alt="alerts" />
</p>

<p align="center">
  <b>🔗 Live Demo:</b> <a href="https://floodguard-ai-five.vercel.app">floodguard-ai-five.vercel.app</a><br/>
  <b>📘 API Docs:</b> <a href="https://floodguard-ai-mvp8.onrender.com/docs">floodguard-ai-mvp8.onrender.com/docs</a><br/>
  <b>💻 Repository:</b> <a href="https://github.com/godabanithin18-lab/floodguard-ai">github.com/godabanithin18-lab/floodguard-ai</a>
</p>

---

## 🎯 What FloodGuard AI Actually Is

FloodGuard AI is **not** "a model that predicts floods." It is an explainable flash-flood intelligence platform that combines environmental observations, live weather integration, localized risk estimation, historical event validation, and transparent decision support — built for the hill regions of Uttarakhand and Himachal Pradesh, where flash floods routinely strike with only hours of warning.

**SIH Problem Statement:** SIH26192 — Flash Flood Prediction System for Hilly Regions using Multi-Source Data *(Ministry of Home Affairs)*

---

## 🏗️ System Architecture — A Pipeline With Checkpoints, Not a Black Box

```
   Live + Historical Weather Data (Open-Meteo)
                    │
                    ▼
      Feature Preparation (20 risk factors, 0–20 scale)
                    │
                    ▼
             Trained Risk Model (Linear Regression)
                    │
                    ▼
        Explain Why — Factor Contribution Breakdown
                    │
                    ▼
   Check Against a Real Event — Historical Validation
                    │
                    ▼
        Risk Score Engine (Low / Moderate / High / Severe)
                    │
                    ▼
          Alert & Decision Support (Real Email Dispatch)
```

Every arrow above is a real, working checkpoint in the deployed system — not aspirational. The model doesn't just output a number; the pipeline explains it, checks it against a genuine historical disaster, and only then surfaces it as a decision-support signal.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🗺️ **Live Risk Map** | Color-coded severity across 6 real hill-region monitoring stations |
| 🌦️ **Live Weather Integration** | Real current rainfall & temperature from Open-Meteo, feeding every prediction |
| 🕰️ **Real-World Historical Validation** | Model tested against the actual Aug 2025 Dharali flash flood — correctly classifies it Severe |
| 🧠 **AI Decision Explanation** | Mathematically real, factor-by-factor breakdown of every prediction — not an approximation |
| 🎛️ **"Try It Yourself"** | Live sliders simulate any scenario and get an instant, explainable prediction |
| 🚨 **Automated Alert Banner** | Triggers automatically the moment any station crosses into Severe |
| 📧 **Real Email Notifications** | One click sends an actual, delivered email alert to disaster-management contacts |
| 📊 **Data Visualization** | Live-updating factor charts and ranked station risk levels |

---

## 🧾 Model Card — FloodGuard AI Risk Model

*A standard, transparent summary of what this model is, how it was validated, and where its limits are — so anyone reviewing this project knows exactly what they're looking at.*

| Field | Detail |
|---|---|
| **Model type** | Linear Regression |
| **Training data** | 50,000 synthetic samples, 20 numeric risk factors (Kaggle `naiyakhalid/flood-prediction-dataset`) |
| **Model selection process** | Benchmarked against Random Forest and Gradient Boosting on identical 80/20 splits before selection |
| **Validation method** | Held-out test split (10,000 samples) + real historical event backtest (Dharali, Aug 5 2025) |
| **Performance (synthetic test set)** | R² = 1.0000 · MAE = 0.00000 · RMSE = 0.00000 |
| **Performance (real historical event)** | Correctly classified the real Aug 5, 2025 Dharali rainfall as 75.95% risk — Severe |
| **What's genuinely live** | Rainfall/temperature per station, pulled in real time from Open-Meteo |
| **Known limitations** | 19 of 20 input factors are expert-estimated regional values, not live sensor data; training data is synthetic, not collected from verified real flood outcomes; validated against one real historical event, not a full validation set |
| **Intended use** | Decision-support prototype for disaster-management teams — **not** a fully validated, standalone operational early-warning system |
| **Last validated** | See repository commit history for the current date |

> This Model Card exists specifically so this project is never mistaken for more than it honestly is. The gap between "working prototype" and "operational system" is real historical/sensor data access — an institutional step, not an engineering one.

---

## 🧠 ML Methodology

| Step | Detail |
|---|---|
| **Input features** | 20 numeric risk factors — MonsoonIntensity, TopographyDrainage, RiverManagement, Deforestation, Urbanization, ClimateChange, DamsQuality, Siltation, AgriculturalPractices, Encroachments, IneffectiveDisasterPreparedness, DrainageSystems, CoastalVulnerability, Landslides, Watersheds, DeterioratingInfrastructure, PopulationScore, WetlandLoss, InadequatePlanning, PoliticalFactors |
| **Target variable** | `FloodProbability` — continuous value between 0 and 1 |
| **Preprocessing** | Dataset arrived fully clean (0 missing values, all numeric) |
| **Train/test methodology** | 80/20 split, `random_state=42` — 40,000 training / 10,000 test samples |
| **Prediction → category** | Raw probability converted to a 0–100 risk score, bucketed: **&lt;35 Low · 35–55 Moderate · 55–70 High · 70+ Severe** |

---

## 📊 Dataset Transparency

| Attribute | Detail |
|---|---|
| **Source** | Public Kaggle dataset — `naiyakhalid/flood-prediction-dataset` |
| **Records** | 50,000 · **Features** | 20 numeric + 1 target |
| **Data nature** | ⚠️ Synthetic — engineered by the dataset's authors, disclosed as such in their own documentation |

**Monitoring stations** use **real GPS coordinates** of actual hill towns — Dharali, Uttarkashi, Manali, Kullu Town, Shimla, Rishikesh — including two genuine 2025 flood-affected regions. Their risk-factor *values* are manually assigned estimates, not live sensor feeds, because that data lives in government GIS systems with no free public API.

**What's genuinely live vs. estimated:**
- ✅ Rainfall / MonsoonIntensity — real, live, Open-Meteo, every load
- ⚠️ The remaining 19 factors — expert-estimated, static

---

## 📈 Model Performance

| Model | R² Score | MAE | RMSE |
|---|:---:|:---:|:---:|
| **Linear Regression** ✅ | **1.0000** | **0.00000** | **0.00000** |
| Gradient Boosting | 0.9195 | 0.01111 | 0.01416 |
| Random Forest | 0.7110 | 0.02122 | 0.02683 |

### Why Linear Regression?
We tested it against Random Forest and Gradient Boosting rather than assuming it. Inspecting its fitted coefficients showed every one of the 20 factors carries an identical weight (≈0.005) — proof the target variable is a genuinely linear, equal-weighted formula. This gives full explainability as a direct mathematical consequence, not a bolted-on feature.

> ⚠️ A perfect R² here means the model correctly recovered a synthetic dataset's true formula — not a claim of validated real-world accuracy. That claim is earned separately, through the historical validation below.

---

## 🌦️ Live Weather Integration

Every station's risk score factors in real, current weather. On each dashboard load, the frontend calls `/live-weather?lat={lat}&lon={lon}` per station, pulling today's actual rainfall and temperature from Open-Meteo (free, no key required). That real rainfall is converted into the model's `MonsoonIntensity` scale and combined with the station's other 19 factors before prediction — visible with a live timestamp in the dashboard's **Live Conditions** section.

---

## 🕰️ Real-World Historical Validation

The `/historical-check` endpoint fetches the actual historical rainfall for **August 5, 2025** — the real Dharali flash flood date — from Open-Meteo's archive API, combines it with Dharali's known vulnerability factors, and runs it through the model.

**Result:** the model correctly classifies that real day as **75.95% risk — Severe.**

**Honest framing:** this validates the model responds sensibly to real rainfall combined with known regional vulnerability. It is not a claim that rainfall alone predicted the disaster — real flash floods often involve hyper-local dynamics daily-average data can understate. One real input tested against one real outcome — a genuine but limited validation, honestly scoped.

---

## 🔍 Explainability

Every prediction includes a live factor breakdown — e.g. Monsoon Intensity +9.0%, Landslides +8.0%, Deforestation +7.5%. This is computed as `(coefficient × input value)`, normalized to a percentage — derived directly from the model's real learned weights, not a heuristic layered on top.

---

## 📧 Authority Notification System

When any station crosses into Severe, an alert banner appears automatically. A **"Notify Authorities"** button triggers `POST /notify`, which composes a formatted HTML email listing every severe station and sends it via the **Resend** API — with real delivery status, not a fake confirmation animation.

---

## 🗺️ Monitoring Stations

| Station | District | Coordinates | Notes |
|---|---|---|---|
| Dharali | Uttarkashi, Uttarakhand | 31.0408, 78.7811 | Real 2025 flash flood site — used in historical validation |
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
$env:RESEND_API_KEY="your_resend_api_key_here"   # required for email alerts
uvicorn main:app --reload
```
Runs at `http://127.0.0.1:8000` · Docs at `/docs` · No key needed for weather endpoints

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs at `http://localhost:3000`

---

## 🗺️ Roadmap

**Near-term (engineering, low risk):**
- [ ] Multi-event historical validation (beyond the single Dharali backtest)
- [ ] Data-freshness / stale-data safety indicators on live readings
- [ ] Prediction audit trail (traceable log of every risk score generated)

**Medium-term (needs institutional data access):**
- [ ] Live IMD / CWC integration for the remaining 19 terrain/infrastructure factors
- [ ] Real authority contact directory (currently one configured recipient)
- [ ] SMS / WhatsApp alert channel alongside email

**Longer-term (larger builds):**
- [ ] Emergency command-center interface for district disaster-management teams
- [ ] Field-operator mobile view
- [ ] Historical risk-trend replay and geographic backtesting across more regions

---

## 👤 Team

**Quantum coders**
Built for Smart India Hackathon 2026

---

<p align="center">Made with ☕ and a lot of debugging</p>