"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { History, CloudRain } from "lucide-react";
import { getHistoricalCheck, HistoricalCheckResult } from "../lib/api";
import { getRiskColor } from "../lib/riskColors";

export default function HistoricalValidation() {
  const [data, setData] = useState<HistoricalCheckResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    getHistoricalCheck()
      .then(setData)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="bg-[#111827] border border-slate-800 rounded-2xl p-6 text-slate-500 text-sm">
        Loading historical validation...
      </div>
    );
  }

  if (error || !data) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-[#111827] border border-slate-800 rounded-2xl p-6"
    >
      <div className="flex items-center gap-2 mb-1">
        <History className="w-5 h-5 text-purple-400" />
        <h3 className="text-white font-semibold text-lg">Real-World Validation</h3>
      </div>
      <p className="text-slate-500 text-sm mb-5">
        Testing our model against genuine historical weather data from a real flood event.
      </p>

      <div className="bg-[#0d1420] border border-slate-800 rounded-xl p-5">
        <div className="text-white font-medium mb-1">{data.event}</div>
        <div className="text-slate-500 text-xs mb-4">{data.actual_event_date}</div>

        <div className="grid grid-cols-3 gap-4 mb-4">
          <div>
            <div className="flex items-center gap-1.5 text-slate-400 text-xs mb-1">
              <CloudRain className="w-3.5 h-3.5" />
              Actual Rainfall
            </div>
            <div className="text-white font-bold text-lg">{data.actual_rainfall_mm} mm</div>
          </div>
          <div>
            <div className="text-slate-400 text-xs mb-1">Derived Intensity</div>
            <div className="text-white font-bold text-lg">{data.derived_monsoon_intensity}/20</div>
          </div>
          <div>
            <div className="text-slate-400 text-xs mb-1">Model Prediction</div>
            <div
              className="font-bold text-lg"
              style={{ color: getRiskColor(data.model_predicted_severity) }}
            >
              {data.model_predicted_risk_percentage}% — {data.model_predicted_severity}
            </div>
          </div>
        </div>

        <div className="text-slate-500 text-xs italic pt-3 border-t border-slate-800">
          {data.note}
        </div>
      </div>
    </motion.div>
  );
}