"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { ShieldCheck } from "lucide-react";
import { getValidationSet, ValidationSetResult } from "../lib/api";
import { getRiskColor } from "../lib/riskColors";

export default function ValidationSet() {
  const [data, setData] = useState<ValidationSetResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getValidationSet().then(setData).catch(console.error).finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="bg-[#111827] border border-slate-800 rounded-2xl p-6 text-slate-500 text-sm">Loading validation set...</div>;
  }
  if (!data) return null;

  return (
    <div className="bg-[#111827] border border-slate-800 rounded-2xl p-6">
      <div className="flex items-center gap-2 mb-1">
        <ShieldCheck className="w-5 h-5 text-purple-400" />
        <h3 className="text-white font-semibold text-lg">Multi-Event Validation Set</h3>
      </div>
      <p className="text-slate-500 text-sm mb-5">
        Testing against {data.events_tested} real historical flood disasters — {data.flagged_severe_or_high} of {data.events_tested} correctly flagged High/Severe.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {data.results.map((ev, i) => (
          <motion.div
            key={ev.event}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="bg-[#0d1420] border border-slate-800 rounded-xl p-4"
          >
            <div className="text-white font-medium text-sm mb-1">{ev.event}</div>
            <div className="text-slate-500 text-xs mb-3">{ev.date}</div>
            <div className="text-slate-400 text-xs mb-2">Real rainfall: {ev.actual_rainfall_mm} mm</div>
            <div
              className="rounded-lg px-3 py-2 flex items-center justify-between"
              style={{ backgroundColor: `${getRiskColor(ev.predicted_severity)}15`, border: `1px solid ${getRiskColor(ev.predicted_severity)}40` }}
            >
              <span className="text-xs font-semibold" style={{ color: getRiskColor(ev.predicted_severity) }}>{ev.predicted_severity}</span>
              <span className="text-white text-sm font-bold">{ev.predicted_risk_percentage}%</span>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="text-slate-500 text-xs italic mt-4 pt-3 border-t border-slate-800">{data.note}</div>
    </div>
  );
}