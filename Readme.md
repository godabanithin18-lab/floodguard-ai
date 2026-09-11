# 🌊 FloodGuard AI
### An Explainable Flash-Flood Intelligence Platform for India's Hilly Regions

<p align="center">
  <img src="https://img.shields.io/badge/Status-Live-brightgreen" alt="status" />
  <img src="https://img.shields.io/badge/Model-Linear%20Regression-blue" alt="model" />
  <img src="https://img.shields.io/badge/Validated-3%20Real%20Events-purple" alt="validation" />
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

FloodGuard AI is **not** "a model that predicts floods." It is an explainable flash-flood intelligence platform that combines environmental observations, live weather integration, localized risk estimation, multi-event historical validation, and transparent, auditable decision support — built for the hill regions of Uttarakhand and Himachal Pradesh, where flash floods routinely strike with only hours of warning.

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
   Check Against Real Events — Multi-Event Historical Validation
                    │
                    ▼
        Risk Score Engine (Low / Moderate / High / Severe)
                    │
                    ▼
     Alert & Decision Support (Real Email Dispatch + Audit Log)
```

Every arrow above is a real, working checkpoint in the deployed system.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🗺️ **Live Risk Map** | Color-coded severity across 6 real hill-region monitoring stations |
| 🌦️ **Live Weather Integration** | Real current rainfall & temperature from Open-Meteo, feeding every prediction — with a stale-data badge if a reading is more than 30 minutes old |
| 🕰️ **Multi-Event Historical Validation** | Model tested against **3 real Indian flood disasters** — all correctly flagged High/Severe |
| 🧠 **AI Decision Explanation** | Mathematically real, factor-by-factor breakdown of every prediction |
| 🧾 **Model Card** | Transparent, standard summary of model type, training data, performance, and known limitations |
| 🪪 **Prediction Audit Trail** | Every prediction and alert dispatch is logged and traceable via `/audit-log` |
| 🎛️ **"Try It Yourself"** | Live sliders simulate any scenario and get an instant, explainable prediction |
| 🚨 **Automated Alert Banner** | Triggers automatically when any station crosses into Severe |
| 📧 **Real Email Notifications** | One click sends an actual, delivered email alert to disaster-management contacts |

---

## 🧾 Model Card — FloodGuard AI Risk Model

| Field | Detail |
|---|---|
| **Model type** | Linear Regression |
| **Training data** | 50,000 synthetic samples, 20 numeric risk factors (Kaggle `naiyakhalid/flood-prediction-dataset`) |
| **Model selection process** | Benchmarked against Random Forest and Gradient Boosting before selection |
| **Validation method** | Held-out test split (10,000 samples) + **3 real historical event backtests** |
| **Performance (synthetic test set)** | R² = 1.0000 · MAE = 0.00000 · RMSE = 0.00000 |
| **Performance (real historical events)** | 3 of 3 real disasters correctly classified High/Severe — Dharali 2025 (75.95%), Kedarnath 2013 (84.85%), Kerala/Wayanad 2018 (77.85%) |
| **What's genuinely live** | Rainfall/temperature per station (Open-Meteo), with freshness validation |
| **Known limitations** | 19 of 20 input factors are expert-estimated regional values, not live sensor data; training data is synthetic; validated against 3 real events, not a comprehensive validation study |
| **Intended use** | Decision-support prototype for disaster-management teams — **not** a fully validated, standalone operational early-warning system |
| **Traceability** | Every prediction and alert is logged with a timestamp via the audit trail (`/audit-log`) |

---

## 🕰️ Multi-Event Historical Validation

The `/historical-validation-set` endpoint tests the model against **3 real Indian flood disasters**, each using genuine archived rainfall for that event's actual date and location:

| Event | Date | Real Rainfall | Predicted Risk | Result |
|---|---|---|---|---|
| Dharali Flash Flood | Aug 5, 2025 | 19.1 mm | 75.95% | ✅ Severe |
| Kedarnath Floods | Jun 17, 2013 | 157.2 mm | 84.85% | ✅ Severe |
| Kerala Floods (Wayanad) | Aug 16, 2018 | 36.9 mm | 77.85% | ✅ Severe |

**3 of 3 real disasters correctly flagged High/Severe.** Notably, predicted risk stays in a similar high range even though real rainfall varies by 8x across events (19.1mm to 157.2mm) — evidence the model's regional vulnerability factors are doing real work, not just echoing rainfall alone.

**Honest framing:** this is a small, real validation set — not a comprehensive study. Each event combines genuine historical rainfall with expert-estimated (not verified historical) vulnerability factors.

---

## 🌦️ Live Weather Integration & Data Freshness

Every station's risk score factors in real, current weather from Open-Meteo, converted into the model's `MonsoonIntensity` scale. The dashboard's **Live Conditions** section shows a live timestamp per station — and flags readings older than 30 minutes with a **"STALE"** badge instead of silently presenting outdated data as current.

---

## 🪪 Prediction Audit Trail

Every call to `/predict` and every alert dispatched via `/notify` is logged with a timestamp, accessible via `GET /audit-log`. This makes every risk score and every alert traceable — a basic but real trust and accountability feature, not just a black-box output.

---

## 🔍 Explainability

Every prediction includes a live factor breakdown — e.g. Monsoon Intensity +9.0%, Landslides +8.0%. Computed as `(coefficient × input value)`, normalized to a percentage — derived directly from the model's real learned weights.

---

## 📧 Authority Notification System

When any station crosses into Severe, an alert banner appears automatically. **"Notify Authorities"** sends a real, formatted email via the **Resend** API — with genuine delivery status, logged in the audit trail.

---

## 📈 Model Performance (Synthetic Test Set)

| Model | R² Score | MAE | RMSE |
|---|:---:|:---:|:---:|
| **Linear Regression** ✅ | **1.0000** | **0.00000** | **0.00000** |
| Gradient Boosting | 0.9195 | 0.01111 | 0.01416 |
| Random Forest | 0.7110 | 0.02122 | 0.02683 |

### Why Linear Regression?
Tested against Random Forest and Gradient Boosting rather than assumed. Its coefficients showed every one of the 20 factors carries an identical weight (≈0.005) — proof the target variable is a genuinely linear formula, giving full explainability as a direct consequence.

> ⚠️ A perfect R² means the model recovered a synthetic dataset's true formula — real-world accuracy is earned separately, through the multi-event historical validation above.

---

## 📊 Dataset Transparency

| Attribute | Detail |
|---|---|
| **Source** | Public Kaggle dataset — `naiyakhalid/flood-prediction-dataset` |
| **Records** | 50,000 · **Features** | 20 numeric + 1 target |
| **Data nature** | ⚠️ Synthetic |

**Monitoring stations** use real GPS coordinates of actual hill towns. Their risk-factor *values* are manually assigned estimates, not live sensor feeds.

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
$env:RESEND_API_KEY="your_resend_api_key_here"
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🗺️ Roadmap

**Near-term:**
- [x] Multi-event historical validation
- [x] Data-freshness safety indicators
- [x] Prediction audit trail

**Medium-term:**
- [ ] Live IMD / CWC integration for the remaining 19 factors
- [ ] Real authority contact directory
- [ ] SMS / WhatsApp alert channel

**Longer-term:**
- [ ] Emergency command-center interface
- [ ] Field-operator mobile view
- [ ] Broader geographic backtesting

---

## 👤 Team

**Developes**
Built for Smart India Hackathon 2026

---

<p align="center">Made with ☕ and a lot of debugging</p>