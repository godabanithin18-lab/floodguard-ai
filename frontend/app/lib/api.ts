import axios from "axios";

const API_BASE_URL = "https://floodguard-ai-mvp8.onrender.com";
export interface FactorContribution {
  factor: string;
  contribution_percent: number;
}

export interface PredictionResult {
  flood_probability: number;
  risk_percentage: number;
  risk_level: string;
  factor_breakdown: FactorContribution[];
  primary_driver: string;
}

export async function getPrediction(riskFactors: Record<string, number>): Promise<PredictionResult> {
  const response = await axios.post(`${API_BASE_URL}/predict`, riskFactors);
  return response.data;
}
export async function notifyAuthorities(recipientEmail: string, stations: any[]) {
  const response = await axios.post(`${API_BASE_URL}/notify`, {
    recipient_email: recipientEmail,
    stations: stations,
  });
  return response.data;
}
export interface HistoricalCheckResult {
  event: string;
  actual_event_date: string;
  actual_rainfall_mm: number;
  derived_monsoon_intensity: number;
  model_predicted_risk_percentage: number;
  model_predicted_severity: string;
  note: string;
}

export async function getHistoricalCheck(): Promise<HistoricalCheckResult> {
  const response = await axios.get(`${API_BASE_URL}/historical-check`);
  return response.data;
}