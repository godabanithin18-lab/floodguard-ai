"use client";

import { FileText } from "lucide-react";

export default function ModelCard() {
  return (
    <div className="bg-[#111827] border border-slate-800 rounded-2xl p-6">
      <div className="flex items-center gap-2 mb-4">
        <FileText className="w-5 h-5 text-purple-400" />
        <h3 className="text-white font-semibold text-lg">Model Card</h3>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-3 text-sm">
        <div><span className="text-slate-500">Model Type</span><div className="text-white font-medium">Linear Regression</div></div>
        <div><span className="text-slate-500">Training Data</span><div className="text-white font-medium">50,000 synthetic samples, 20 features</div></div>
        <div><span className="text-slate-500">Test Performance</span><div className="text-white font-medium">R²=1.00 · MAE=0.00000</div></div>
        <div><span className="text-slate-500">Real-World Backtest</span><div className="text-white font-medium">75.95% Severe — Dharali, Aug 2025</div></div>
        <div><span className="text-slate-500">Known Limitations</span><div className="text-white font-medium">19/20 factors expert-estimated, not sensor-fed</div></div>
        <div><span className="text-slate-500">Intended Use</span><div className="text-white font-medium">Decision-support prototype, not operational system</div></div>
      </div>
    </div>
  );
}