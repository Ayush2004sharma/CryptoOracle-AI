"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  TrendingUp,
  Newspaper,
  BarChart3,
  Activity,
  ShieldCheck,
  ChevronRight,
  Loader2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { ThemeToggle } from "@/components/theme-toggle";
import { useRouter } from "next/navigation";
import { COIN_CONFIG, SupportedCoin } from "@/lib/coins";
import AnalysisControls from "@/components/AnalysisControls"
import TradingViewChart from "./TradingViewChart";
import DashboardFooter from "./DashboardFooter";
import DashboardLoading from "./DashboardLoading";
import DashboardResult from "./DashboardResult";
import DashboardTabs from "./DashboardTabs";

// Define API response type based on requirements
type AnalysisResult = {
  asset: string;
  recommendation: "BUY" | "HOLD" | "SELL";
  confidence: number;
  time_horizon: string;
  news: string;
  fundamentals: string;
  technical: {
    rsi: number;
    macd: string;
    trend: string;
    bollinger?: string;
  };
  sentiment: {
    fear_greed_index: number;
    label: string;
  };
  summary: string;
};

const containerVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, staggerChildren: 0.1 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: { opacity: 1, y: 0 },
};
type DashboardProps = {
  coin: SupportedCoin
  setCoin: (coin: SupportedCoin) => void
}
export function CryptoDashboard({ coin, setCoin }: DashboardProps) {
  const [loading, setLoading] = React.useState(false);
  const [result, setResult] = React.useState<AnalysisResult | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const router = useRouter();
  const [profile, setProfile] = React.useState("new_buyer");
  const [duration, setDuration] = React.useState("short_term");

  React.useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      router.push("/login");
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_name");
    localStorage.removeItem("user_email");
    router.push("/login");
  };

  const handleAnalyze = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem("token");

      const response = await fetch("/api/trade/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // JWT ready (future)
          // Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          coin,
          trader_position: profile,
          duration,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Analysis failed");
        return;
      }

      /**
       * FastAPI returns:
       * {
       *   status: "success",
       *   data: { ...pipeline output... }
       * }
       */
      setResult({
        asset: data.data.coin.toUpperCase(),
        recommendation: data.data.final_decision,
        confidence: data.data.confidence,
        time_horizon: data.data.horizon,
        news: data.data.reports.news.raw,
        fundamentals: data.data.reports.fundamentals.raw,
        technical: {
          rsi: 50, // map properly later
          macd: "N/A",
          trend: "N/A",
        },
        sentiment: {
          fear_greed_index: 50,
          label: "Neutral",
        },
        summary: data.data.research_summary,
      });
    } catch (err) {
      console.error(err);
      setError("Failed to fetch analysis. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="max-w-7xl mx-auto px-4 py-6 md:px-8 lg:py-10"
    >

<div className="grid grid-cols-[260px_1fr] gap-10 items-start">
  
  {/* LEFT: Analysis Controls */}
  <AnalysisControls
    coin={coin}
    setCoin={setCoin}
    profile={profile}
    setProfile={setProfile}
    duration={duration}
    setDuration={setDuration}
    loading={loading}
    onAnalyze={handleAnalyze}
  />

  {/* RIGHT: MAIN INTERACTIVE CHART */}
  <div className="relative rounded-2xl border border-border bg-card/60 backdrop-blur-md">

    <TradingViewChart
      symbol={COIN_CONFIG[coin].tv}
      height={420}
    />

  </div>
</div>

     <AnimatePresence mode="wait">
  {loading && <DashboardLoading />}

  {result && !loading && (
    <>
      <DashboardResult result={result} />
      <DashboardTabs result={result} />
    </>
  )}
</AnimatePresence>

<DashboardFooter
  showEmptyState={!loading && !result}
/>

   
    </motion.div>
  );
}
