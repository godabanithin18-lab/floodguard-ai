"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { CloudRain, Thermometer, RadioTower } from "lucide-react";
import { stations } from "../data/stations";
import { getLivePrediction } from "../lib/api";
import { getRiskColor } from "../lib/riskColors";

interface StationLiveData {
  stationName: string;
  district: string;
  rainfall_mm: number;
  temperature_c: number;
  fetched_at: string;
  risk_percentage: number;
  risk_level: string;
}

export default function LiveConditions() {
  const [data, setData] = useState<StationLiveData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    async function fetchAll() {
      try {
        const results = await Promise.all(
          stations.map(async (station) => {
            const { weather, prediction } = await getLivePrediction(
              station.lat,
              station.lng,
              station.riskFactors
            );
            return {
              stationName: station.name,
              district: station.district,
              rainfall_mm: weather.rainfall_mm,
              temperature_c: weather.temperature_c,
              fetched_at: weather.fetched_at,
              risk_percentage: prediction.risk_percentage,
              risk_level: prediction.risk_level,
            };
          })
        );
        setData(results);
      } catch (err) {
        console.error(err);
        setError(true);
      } finally {
        setLoading(false);
      }
    }
    fetchAll();
  }, []);

  const formatTime = (isoString: string) => {
    try {
      const date = new Date(isoString);
      return date.toLocaleString("en-IN", {
        day: "2-digit",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return isoString;
    }
  };

  return (
    <div className="bg-[#111827] border border-slate-800 rounded-2xl p-6">
      <div className="flex items-center gap-2 mb-1">
        <RadioTower className="w-5 h-5 text-green-400" />
        <h3 className="text-white font-semibold text-lg">Live Conditions</h3>
      </div>
      <p className="text-slate-500 text-sm mb-5">
        Real-time weather pulled live from Open-Meteo, fed directly into the AI model for a live risk score.
      </p>

      {loading && (
        <div className="text-slate-500 text-sm py-4">Fetching live weather and running predictions...</div>
      )}

      {error && (
        <div className="text-red-400 text-sm py-4">
          Could not fetch live weather data right now.
        </div>
      )}

      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {data.map((station, index) => (
            <motion.div
              key={station.stationName}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.08 }}
              className="bg-[#0d1420] border border-slate-800 rounded-xl p-4"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="text-white font-medium text-sm">{station.stationName}</div>
                <div className="flex items-center gap-1 text-green-400 text-[10px] font-medium">
                  <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
                  LIVE
                </div>
              </div>
              <div className="text-slate-500 text-xs mb-3">{station.district}</div>

              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-1.5">
                  <CloudRain className="w-4 h-4 text-blue-400" />
                  <span className="text-white text-sm font-semibold">
                    {station.rainfall_mm} mm
                  </span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Thermometer className="w-4 h-4 text-orange-400" />
                  <span className="text-white text-sm font-semibold">
                    {station.temperature_c}°C
                  </span>
                </div>
              </div>

              <div
                className="rounded-lg px-3 py-2 flex items-center justify-between"
                style={{
                  backgroundColor: `${getRiskColor(station.risk_level)}15`,
                  border: `1px solid ${getRiskColor(station.risk_level)}40`,
                }}
              >
                <span
                  className="text-xs font-semibold"
                  style={{ color: getRiskColor(station.risk_level) }}
                >
                  {station.risk_level}
                </span>
                <span className="text-white text-sm font-bold">
                  {station.risk_percentage}%
                </span>
              </div>

              <div className="text-slate-600 text-[10px] mt-3 pt-2 border-t border-slate-800/50">
                Updated: {formatTime(station.fetched_at)}
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}