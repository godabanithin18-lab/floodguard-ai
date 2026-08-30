"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { motion } from "framer-motion";
import { ShieldAlert, AlertTriangle, TrendingUp, Activity } from "lucide-react";
import Link from "next/link";
import { stations } from "../data/stations";
import { getPrediction, notifyAuthorities } from "../lib/api";
import { getRiskColor } from "../lib/riskColors";
import PredictionForm from "../components/PredictionForm";
import { AlertTriangle as AlertIcon } from "lucide-react";
import HistoricalValidation from "../components/HistoricalValidation";
import LiveConditions from "../components/LiveConditions";

// Leaflet map must load client-side only
const FloodMap = dynamic(() => import("../components/FloodMap"), {
  ssr: false,
  loading: () => (
    <div className="h-full w-full flex items-center justify-center text-slate-500">
      Loading map...
    </div>
  ),
});

interface StationResult {
  id: string;
  name: string;
  district: string;
  lat: number;
  lng: number;
  risk_percentage: number;
  risk_level: string;
}

export default function Dashboard() {
  const [results, setResults] = useState<StationResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [notifyStatus, setNotifyStatus] = useState<"idle" | "sending" | "sent" | "error">("idle");

const handleNotify = async () => {
  setNotifyStatus("sending");
  try {
    const severeStations = results.filter((r) => r.risk_level === "Severe");
    await notifyAuthorities("godabanithin18@gmail.com", severeStations);
    setNotifyStatus("sent");
  } catch (err) {
    console.error(err);
    setNotifyStatus("error");
  }
};

  useEffect(() => {
    async function fetchAllPredictions() {
      try {
        const predictions = await Promise.all(
          stations.map(async (station) => {
            const prediction = await getPrediction(station.riskFactors);
            return {
              id: station.id,
              name: station.name,
              district: station.district,
              lat: station.lat,
              lng: station.lng,
              risk_percentage: prediction.risk_percentage,
              risk_level: prediction.risk_level,
            };
          })
        );
        setResults(predictions);
      } catch (err) {
        console.error(err);
        setError(true);
      } finally {
        setLoading(false);
      }
    }
    fetchAllPredictions();
  }, []);

  const severeCount = results.filter((r) => r.risk_level === "Severe").length;
  const highCount = results.filter((r) => r.risk_level === "High").length;
  const avgRisk =
    results.length > 0
      ? (results.reduce((sum, r) => sum + r.risk_percentage, 0) / results.length).toFixed(1)
      : "0";

  return (
    <main className="min-h-screen bg-[#0a0e17] p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-6 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <ShieldAlert className="w-6 h-6 text-blue-400" />
          <span className="text-lg font-bold text-white">FloodGuard AI</span>
        </Link>
        <div className="flex items-center gap-2 text-sm text-slate-400">
          <Activity className="w-4 h-4 text-green-400 animate-pulse" />
          Live Monitoring
        </div>
      </div>

      {error && (
        <div className="max-w-7xl mx-auto mb-6 bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400 text-sm">
          Could not reach the prediction API. Make sure your FastAPI backend is running on
          http://127.0.0.1:8000
        </div>
      )}

      {/* Stat Cards */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-[#111827] border border-slate-800 rounded-2xl p-5"
        >
          <div className="text-slate-400 text-sm mb-1">Stations Monitored</div>
          <div className="text-3xl font-bold text-white">{stations.length}</div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-[#111827] border border-slate-800 rounded-2xl p-5"
        >
          <div className="text-slate-400 text-sm mb-1">Average Risk</div>
          <div className="text-3xl font-bold text-white">{avgRisk}%</div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-[#111827] border border-slate-800 rounded-2xl p-5"
        >
          <div className="text-slate-400 text-sm mb-1 flex items-center gap-1.5">
            <AlertTriangle className="w-4 h-4 text-orange-400" />
            High Risk Zones
          </div>
          <div className="text-3xl font-bold text-orange-400">{highCount}</div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-[#111827] border border-slate-800 rounded-2xl p-5"
        >
          <div className="text-slate-400 text-sm mb-1 flex items-center gap-1.5">
            <TrendingUp className="w-4 h-4 text-red-400" />
            Severe Risk Zones
          </div>
          <div className="text-3xl font-bold text-red-400">{severeCount}</div>
        </motion.div>
      </div>
            {!loading && severeCount > 0 && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ type: "spring", stiffness: 200, damping: 20 }}
          className="max-w-7xl mx-auto mb-6 bg-red-500/10 border border-red-500/40 rounded-2xl p-5 flex items-center gap-4"
        >
          <motion.div
            animate={{ scale: [1, 1.15, 1] }}
            transition={{ repeat: Infinity, duration: 1.5 }}
          >
            <AlertIcon className="w-8 h-8 text-red-400 flex-shrink-0" />
          </motion.div>
          <div>
            <div className="text-red-400 font-semibold text-lg">
              ⚠ Severe Flood Risk Alert
            </div>
            <div className="text-slate-300 text-sm">
              {severeCount} station{severeCount > 1 ? "s are" : " is"} currently showing severe
              flood risk. Immediate monitoring and preparedness measures recommended.
            </div>
          </div>
                      <button
              onClick={handleNotify}
              disabled={notifyStatus === "sending" || notifyStatus === "sent"}
              className="ml-auto flex-shrink-0 px-4 py-2 bg-red-600 hover:bg-red-700 disabled:opacity-60 text-white text-sm font-semibold rounded-lg transition-colors"
            >
              {notifyStatus === "idle" && "Notify Authorities"}
              {notifyStatus === "sending" && "Sending..."}
              {notifyStatus === "sent" && "✓ Alert Sent"}
              {notifyStatus === "error" && "Failed — Retry"}
            </button>
        </motion.div>
      )}

      {/* Map + Station List */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-[#111827] border border-slate-800 rounded-2xl p-4 h-[550px]">
          {loading ? (
            <div className="h-full flex items-center justify-center text-slate-500">
              Loading predictions...
            </div>
          ) : (
            <FloodMap stations={results} />
          )}
        </div>

        <div className="bg-[#111827] border border-slate-800 rounded-2xl p-5 h-[550px] overflow-y-auto">
          <h3 className="text-white font-semibold mb-4">Station Risk Levels</h3>
          <div className="space-y-3">
            {results
              .sort((a, b) => b.risk_percentage - a.risk_percentage)
              .map((station) => (
                <div
                  key={station.id}
                  className="bg-[#1a2332] rounded-xl p-4 border border-slate-800"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-white font-medium text-sm">{station.name}</span>
                    <span
                      className="text-xs font-semibold px-2 py-0.5 rounded-full"
                      style={{
                        color: getRiskColor(station.risk_level),
                        backgroundColor: `${getRiskColor(station.risk_level)}20`,
                      }}
                    >
                      {station.risk_level}
                    </span>
                  </div>
                  <div className="text-slate-500 text-xs mb-2">{station.district}</div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5">
                    <div
                      className="h-1.5 rounded-full"
                      style={{
                        width: `${station.risk_percentage}%`,
                        backgroundColor: getRiskColor(station.risk_level),
                      }}
                    />
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto mt-6">
        <PredictionForm />
      </div>
      <div className="max-w-7xl mx-auto mt-6">
        <LiveConditions />
      </div>
      <div className="max-w-7xl mx-auto mt-6">
        <HistoricalValidation />
      </div>
    </main>
  );
}