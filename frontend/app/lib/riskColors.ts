export function getRiskColor(riskLevel: string): string {
  switch (riskLevel) {
    case "Low":
      return "#10b981"; // green
    case "Moderate":
      return "#f59e0b"; // amber
    case "High":
      return "#f97316"; // orange
    case "Severe":
      return "#ef4444"; // red
    default:
      return "#64748b"; // slate
  }
}