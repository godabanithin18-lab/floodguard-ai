"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Loader2 } from "lucide-react";
import { getPrediction, PredictionResult } from "../lib/api";
import { getRiskColor } from "../lib/riskColors";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { FactorContribution } from "../lib/api";

const sliderFields = [
  { key: "MonsoonIntensity", label: "Monsoon Intensity" },
  { key: "Deforestation", label: "Deforestation Level" },
  { key: "RiverManagement", label: "River Management Quality (inverse)" },
  { key: "DamsQuality", label: "Dams Quality (inverse)" },
  { key: "DrainageSystems", label: "Drainage Systems Quality (inverse)" },
  { key: "Landslides", label: "Landslide Susceptibility" },
  { key: "Urbanization", label: "Urbanization Level" },
  { key: "ClimateChange", label: "Climate Change Impact" },
];
const factorIcons: Record<string, string> = {
  MonsoonIntensity: "🌧️",
  Landslides: "🏔️",
  Deforestation: "🌲",
  DrainageSystems: "🌊",
  DeterioratingInfrastructure: "🏗️",
  RiverManagement: "🌊",
  ClimateChange: "🌡️",
  IneffectiveDisasterPreparedness: "⚠️",
  DamsQuality: "🚧",
  Urbanization: "🏙️",
};

function getFactorIcon(factor: string): string {
  return factorIcons[factor] || "📊";
}

function formatFactorName(factor: string): string {
  return factor.replace(/([A-Z])/g, " $1").trim();
}

// Default mid-values for the fields not exposed as sliders
const defaultFactors: Record<string, number> = {
  MonsoonIntensity: 8, TopographyDrainage: 8, RiverManagement: 8, Deforestation: 8,
  Urbanization: 8, ClimateChange: 8, DamsQuality: 8, Siltation: 8,
  AgriculturalPractices: 8, Encroachments: 8, IneffectiveDisasterPreparedness: 8,
  DrainageSystems: 8, CoastalVulnerability: 8, Landslides: 8, Watersheds: 8,
  DeterioratingInfrastructure: 8, PopulationScore: 8, WetlandLoss: 8,
  InadequatePlanning: 8, PoliticalFactors: 8,
};

export default function PredictionForm() {
  const [values, setValues] = useState<Record<string, number>>(defaultFactors);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (key: string, value: number) => {
    setValues((prev) => ({ ...prev, [key]: value }));
  };

  const handlePredict = async () => {
    setLoading(true);
    try {
      const prediction = await getPrediction(values);
      setResult(prediction);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
    const chartData = sliderFields.map((field) => ({
    name: field.label.split(" ")[0], // short label for chart
    value: values[field.key],
  }));

  return (
    <div className="bg-[#111827] border border-slate-800 rounded-2xl p-6">
      <div className="flex items-center gap-2 mb-1">
        <Sparkles className="w-5 h-5 text-blue-400" />
        <h3 className="text-white font-semibold text-lg">Try It Yourself</h3>
      </div>
      <p className="text-slate-500 text-sm mb-6">
        Adjust the risk factors below and see the AI predict flood risk in real time.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
        {sliderFields.map((field) => (
          <div key={field.key}>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-slate-300 text-sm">{field.label}</label>
              <span className="text-blue-400 text-sm font-medium">{values[field.key]}</span>
            </div>
            <input
              type="range"
              min="0"
              max="20"
              value={values[field.key]}
              onChange={(e) => handleChange(field.key, Number(e.target.value))}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
          </div>
        ))}
      </div>

      <button
        onClick={handlePredict}
        disabled={loading}
        className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 transition-colors rounded-xl text-white font-semibold flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" /> Analyzing...
          </>
        ) : (
          "Predict Flood Risk"
        )}
      </button>

            <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-5 overflow-hidden"
          >
            <div
              className="rounded-xl p-5 border"
              style={{
                backgroundColor: `${getRiskColor(result.risk_level)}15`,
                borderColor: `${getRiskColor(result.risk_level)}40`,
              }}
            >
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-slate-400 text-sm">Predicted Risk Level</div>
                  <div
                    className="text-2xl font-bold"
                    style={{ color: getRiskColor(result.risk_level) }}
                  >
                    {result.risk_level}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-slate-400 text-sm">Risk Score</div>
                  <div className="text-2xl font-bold text-white">
                    {result.risk_percentage}/100
                  </div>
                </div>
              </div>
              <div className="text-slate-500 text-xs mt-3 italic">
                Prototype estimate based on trained model — not a calibrated probability or official forecast.
              </div>
            </div>

            <div className="mt-4 bg-[#0d1420] border border-slate-800 rounded-xl p-5">
              <h4 className="text-white font-medium text-sm mb-4">
                Why this location is {result.risk_level}
              </h4>
              <div className="space-y-2.5">
                {result.factor_breakdown.map((item: FactorContribution, index: number) => (
                  <motion.div
                    key={item.factor}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-center justify-between text-sm"
                  >
                    <span className="text-slate-300 flex items-center gap-2">
                      <span>{getFactorIcon(item.factor)}</span>
                      {formatFactorName(item.factor)}
                    </span>
                    <span className="text-blue-400 font-medium">
                      +{item.contribution_percent}%
                    </span>
                  </motion.div>
                ))}
                <div className="border-t border-slate-800 pt-2.5 mt-2.5 flex items-center justify-between text-sm">
                  <span className="text-slate-400">Predicted Risk</span>
                  <span className="text-white font-bold">{result.risk_percentage}%</span>
                </div>
              </div>
              <div className="mt-3 text-xs text-slate-500">
                Primary driver: <span className="text-slate-300">{formatFactorName(result.primary_driver)}</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="mt-6 pt-6 border-t border-slate-800">
        <h4 className="text-slate-300 text-sm font-medium mb-4">
          Current Risk Factor Levels
        </h4>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 12 }} />
            <YAxis domain={[0, 20]} tick={{ fill: "#94a3b8", fontSize: 12 }} />
            <Tooltip
              contentStyle={{
                backgroundColor: "#111827",
                border: "1px solid #334155",
                borderRadius: "8px",
                color: "#f8fafc",
              }}
            />
            <Bar dataKey="value" fill="#3b82f6" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}