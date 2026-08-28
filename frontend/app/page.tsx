import Link from "next/link";
import { ShieldAlert, MapPin, TrendingUp, Zap } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0a0e17] relative overflow-hidden">
      {/* Background glow effect */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Navbar */}
      <nav className="relative z-10 flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-7 h-7 text-blue-400" />
          <span className="text-xl font-bold text-white">FloodGuard AI</span>
        </div>
        <Link
          href="/dashboard"
          className="px-5 py-2 bg-blue-600 hover:bg-blue-700 transition-colors rounded-lg text-white text-sm font-medium"
        >
          Open Dashboard
        </Link>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 max-w-5xl mx-auto text-center px-6 pt-20 pb-24">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-500/10 border border-blue-500/20 rounded-full text-blue-400 text-sm font-medium mb-8">
          <Zap className="w-4 h-4" />
          AI-Powered Early Warning System
        </div>

        <h1 className="text-5xl md:text-6xl font-bold text-white leading-tight mb-6">
          Predicting Flash Floods
          <br />
          <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            Before They Strike
          </span>
        </h1>

        <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-10">
          A machine learning system that analyzes rainfall, terrain, drainage,
          and infrastructure data to predict flash flood risk in hilly regions
          of India — giving communities critical hours to prepare.
        </p>

        <div className="flex items-center justify-center gap-4">
          <Link
            href="/dashboard"
            className="px-8 py-3 bg-blue-600 hover:bg-blue-700 transition-colors rounded-lg text-white font-semibold"
          >
            View Live Risk Map
          </Link>
        </div>
      </section>

      {/* Feature Cards */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 pb-24 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-[#111827] border border-slate-800 rounded-2xl p-6">
          <MapPin className="w-8 h-8 text-blue-400 mb-4" />
          <h3 className="text-white font-semibold text-lg mb-2">
            Regional Risk Mapping
          </h3>
          <p className="text-slate-400 text-sm">
            Real-time risk visualization across monitoring stations in
            flood-prone hilly terrain.
          </p>
        </div>

        <div className="bg-[#111827] border border-slate-800 rounded-2xl p-6">
          <TrendingUp className="w-8 h-8 text-cyan-400 mb-4" />
          <h3 className="text-white font-semibold text-lg mb-2">
            Predictive Analytics
          </h3>
          <p className="text-slate-400 text-sm">
            ML model trained on 20+ risk factors including rainfall,
            drainage, deforestation, and infrastructure quality.
          </p>
        </div>

        <div className="bg-[#111827] border border-slate-800 rounded-2xl p-6">
          <ShieldAlert className="w-8 h-8 text-orange-400 mb-4" />
          <h3 className="text-white font-semibold text-lg mb-2">
            Early Warning Alerts
          </h3>
          <p className="text-slate-400 text-sm">
            Automatic severity classification — Low, Moderate, High, Severe —
            for rapid decision-making.
          </p>
        </div>
      </section>
    </main>
  );
}