"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { ShieldCheck, AlertTriangle, CheckCircle2, XCircle } from "lucide-react";
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

  const floodEvents = data.results.filter((r) => r.expected === "flood");
  const controlEvents = data.results.filter((r) => r.expected === "no_flood");

  return (
    <div className="bg-[#111827] border border-slate-800 rounded-2xl p-6">
      <div className="flex items-center gap-2 mb-1">
        <ShieldCheck className="w-5 h-5 text-purple-400" />
        <h3 className="text-white font-semibold text-lg">Multi-Event Validation & False-Alarm Testing</h3>
      </div>
      <p className="text-slate-500 text-sm mb-5">
        {data.flood_events_correctly_flagged}/{data.flood_events_tested} real flood events correctly flagged High/Severe ·{" "}
        {data.control_days_correctly_avoided_false_alarm}/{data.control_days_tested} non-flood control days correctly avoided a false alarm
      </p>

      <h4 className="text-slate-300 text-xs font-semibold uppercase tracking-wide mb-2">Real Flood Events</h4>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-5">
        {floodEvents.map((ev, i) => (
          <motion.div
            key={ev.event}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.06 }}
            className="bg-[#0d1420] border border-slate-800 rounded-xl p-4"
          >
            <div className="flex items-center justify-between mb-1">
              <div className="text-white font-medium text-sm">{ev.event}</div>
              {ev.correctly_classified ? (
                <CheckCircle2 className="w-4 h-4 text-green-400 flex-shrink-0" />
              ) : (
                <XCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
              )}
            </div>
            <div className="text-slate-500 text-xs mb-2">{ev.date} · {ev.actual_rainfall_mm}mm real rainfall</div>
            <div
              className="rounded-lg px-3 py-1.5 flex items-center justify-between"
              style={{ backgroundColor: `${getRiskColor(ev.predicted_severity)}15`, border: `1px solid ${getRiskColor(ev.predicted_severity)}40` }}
            >
              <span className="text-xs font-semibold" style={{ color: getRiskColor(ev.predicted_severity) }}>{ev.predicted_severity}</span>
              <span className="text-white text-sm font-bold">{ev.predicted_risk_percentage}%</span>
            </div>
          </motion.div>
        ))}
      </div>

      <h4 className="text-slate-300 text-xs font-semibold uppercase tracking-wide mb-2 flex items-center gap-1.5">
        <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
        False-Alarm Test — Non-Flood Control Days
      </h4>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
        {controlEvents.map((ev) => (
          <div key={ev.event} className="bg-[#0d1420] border border-amber-900/40 rounded-xl p-4">
            <div className="flex items-center justify-between mb-1">
              <div className="text-white font-medium text-sm">{ev.event}</div>
              <XCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
            </div>
            <div className="text-slate-500 text-xs mb-2">{ev.date} · only {ev.actual_rainfall_mm}mm rainfall</div>
            <div
              className="rounded-lg px-3 py-1.5 flex items-center justify-between"
              style={{ backgroundColor: `${getRiskColor(ev.predicted_severity)}15`, border: `1px solid ${getRiskColor(ev.predicted_severity)}40` }}
            >
              <span className="text-xs font-semibold" style={{ color: getRiskColor(ev.predicted_severity) }}>{ev.predicted_severity} (false alarm)</span>
              <span className="text-white text-sm font-bold">{ev.predicted_risk_percentage}%</span>
            </div>
          </div>
        ))}
      </div>

      <div className="text-slate-500 text-xs italic pt-3 border-t border-slate-800">
        <b className="text-slate-400">Finding:</b> static regional vulnerability factors currently dominate the linear formula, causing elevated risk scores even on low-rainfall days. Identified limitation — see Model Card for planned mitigation.
      </div>
    </div>
  );
}