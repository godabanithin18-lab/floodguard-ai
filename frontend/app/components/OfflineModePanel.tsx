"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { WifiOff, MessageSquare, MapPin } from "lucide-react";
import { getSMSFormat, SMSFormatResult } from "../lib/api";

interface Props {
  stationName: string;
  riskLevel: string;
  riskPercentage: number;
}

export default function OfflineModePanel({ stationName, riskLevel, riskPercentage }: Props) {
  const [result, setResult] = useState<SMSFormatResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  const handleGenerate = async () => {
    setOpen(true);
    setLoading(true);
    try {
      const data = await getSMSFormat(stationName, riskLevel, riskPercentage);
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-3">
      <button
        onClick={handleGenerate}
        className="flex items-center gap-2 text-xs font-medium text-slate-400 hover:text-white transition-colors border border-slate-700 rounded-lg px-3 py-1.5"
      >
        <WifiOff className="w-3.5 h-3.5" />
        Generate Offline / SMS Alert
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden"
          >
            <div className="mt-3 bg-[#0d1420] border border-slate-800 rounded-xl p-4">
              {loading ? (
                <div className="text-slate-500 text-sm">Formatting for low-bandwidth gateway...</div>
              ) : result ? (
                <>
                  <div className="flex items-center gap-2 mb-2">
                    <MessageSquare className="w-4 h-4 text-cyan-400" />
                    <span className="text-cyan-400 text-xs font-semibold">SMS GATEWAY FORMAT</span>
                    <span className="text-slate-600 text-xs ml-auto">
                      {result.character_count}/160 chars
                    </span>
                  </div>
                  <div className="bg-black/30 border border-slate-800 rounded-lg p-3 font-mono text-sm text-slate-200 mb-3">
                    {result.sms_text}
                  </div>
                  <div className="flex items-center gap-1.5 text-xs text-slate-400">
                    <MapPin className="w-3.5 h-3.5 text-amber-400" />
                    Routed to: <span className="text-white font-medium">{result.routed_to}</span>
                  </div>
                  <div className="text-slate-600 text-[11px] italic mt-2">{result.note}</div>
                </>
              ) : null}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}