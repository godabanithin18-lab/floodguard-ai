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
  recommended_actions?: string[];
  confidence?: {
    input_range_confidence: string;
    extreme_factor_count: number;
    note: string;
  };
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
export interface LiveWeatherResult {
  source: string;
  rainfall_mm: number;
  temperature_c: number;
  derived_monsoon_intensity: number;
  fetched_at: string;
}

export async function getLiveWeather(lat: number, lon: number): Promise<LiveWeatherResult> {
  const response = await axios.get(`${API_BASE_URL}/live-weather`, {
    params: { lat, lon },
  });
  return response.data;
}

export async function getLivePrediction(
  lat: number,
  lon: number,
  otherFactors: Record<string, number>
): Promise<{ weather: LiveWeatherResult; prediction: PredictionResult }> {
  const weather = await getLiveWeather(lat, lon);

  const safeMonsoonIntensity =
    typeof weather.derived_monsoon_intensity === "number"
      ? weather.derived_monsoon_intensity
      : (otherFactors.MonsoonIntensity ?? 8);

  const combinedFactors = {
    ...otherFactors,
    MonsoonIntensity: safeMonsoonIntensity,
  };
  const prediction = await getPrediction(combinedFactors);
  return { weather, prediction };
}
export interface ValidationEvent {
  event: string;
  date: string;
  expected: string;
  actual_rainfall_mm: number;
  derived_monsoon_intensity: number;
  predicted_risk_percentage: number;
  predicted_severity: string;
  correctly_classified: boolean;
}

export interface ValidationSetResult {
  flood_events_tested: number;
  flood_events_correctly_flagged: number;
  control_days_tested: number;
  control_days_correctly_avoided_false_alarm: number;
  results: ValidationEvent[];
  note: string;
}
export async function getValidationSet(): Promise<ValidationSetResult> {
  const response = await axios.get(`${API_BASE_URL}/historical-validation-set`);
  return response.data;
}