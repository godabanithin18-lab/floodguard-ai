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