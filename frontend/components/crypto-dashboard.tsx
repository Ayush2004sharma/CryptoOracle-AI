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

      <section className="mb-10">
        <Card className="border-border/40 shadow-xl shadow-black/[0.02] dark:shadow-white/[0.01] bg-card/60 backdrop-blur-md">
          <CardContent className="pt-6">
            <form
              onSubmit={handleAnalyze}
              className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 items-end"
            >
              {/* Select fields updated with better styling ... */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-muted-foreground uppercase tracking-widest px-1">
                  Cryptocurrency
                </label>
                <Select
                  value={coin}
                  onValueChange={(v) => setCoin(v as SupportedCoin)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select Asset" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(COIN_CONFIG).map(([key, c]) => (
                      <SelectItem key={key} value={key}>
                        {c.label} ({c.short})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-muted-foreground uppercase tracking-widest px-1">
                  Investor Profile
                </label>
                <Select value={profile} onValueChange={setProfile}>
                  <SelectTrigger className="bg-background/80 border-border/60 hover:border-primary/30 transition-colors">
                    <SelectValue placeholder="Profile" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="new_buyer">New Investor</SelectItem>
                    <SelectItem value="existing_buyer">
                      Existing Holder
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-muted-foreground uppercase tracking-widest px-1">
                  Duration
                </label>
                <Select value={duration} onValueChange={setDuration}>
                  <SelectTrigger className="bg-background/80 border-border/60 hover:border-primary/30 transition-colors">
                    <SelectValue placeholder="Horizon" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="short_term">Short Term</SelectItem>
                    <SelectItem value="medium_term">Medium Term</SelectItem>
                    <SelectItem value="long_term">Long Term</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <motion.div
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.98 }}
              >
                <Button
                  type="submit"
                  className="w-full h-11 text-base font-bold shadow-lg shadow-primary/10 transition-all"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Synthesizing...
                    </>
                  ) : (
                    <>
                      Run Analysis
                      <ChevronRight className="ml-2 h-4 w-4" />
                    </>
                  )}
                </Button>
              </motion.div>
            </form>
          </CardContent>
        </Card>
      </section>

      <AnimatePresence mode="wait">
        {loading && (
          <motion.div
            key="loading"
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.98 }}
            className="space-y-8 py-12"
          >
            <div className="flex flex-col items-center justify-center text-center space-y-6">
              <div className="relative">
                <Loader2 className="w-16 h-16 text-primary animate-spin opacity-20" />
                <Activity className="w-8 h-8 text-primary absolute inset-0 m-auto animate-pulse" />
              </div>
              <div className="space-y-2">
                <h3 className="text-2xl font-bold tracking-tight">
                  Oracle-v4 Working
                </h3>
                <p className="text-muted-foreground max-w-sm mx-auto">
                  Performing deep multi-agent synthesis of current market
                  dynamics and sentiment pools.
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {result && !loading && (
          <motion.div
            key="result"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            <Card className="border-none shadow-2xl shadow-black/[0.04] dark:shadow-white/[0.02] overflow-hidden bg-gradient-to-br from-card to-secondary/10">
              <div
                className={`h-1.5 w-full ${
                  result.recommendation === "BUY"
                    ? "bg-buy"
                    : result.recommendation === "SELL"
                    ? "bg-sell"
                    : "bg-hold"
                }`}
              />
              <CardHeader className="flex flex-col sm:flex-row items-center justify-between gap-8 pb-8 pt-10 px-8">
                <div className="space-y-2 text-center sm:text-left">
                  <Badge
                    variant="outline"
                    className="uppercase tracking-[0.25em] font-black text-[10px] text-muted-foreground px-3 bg-secondary/30 border-border/40"
                  >
                    Primary Verdict
                  </Badge>
                  <CardTitle
                    className={`text-6xl md:text-7xl font-black tracking-tighter ${
                      result.recommendation === "BUY"
                        ? "text-buy"
                        : result.recommendation === "SELL"
                        ? "text-sell"
                        : "text-hold"
                    }`}
                  >
                    {result.recommendation}
                  </CardTitle>
                </div>
                <div className="flex flex-col items-center sm:items-end gap-3 bg-secondary/20 p-6 rounded-2xl border border-border/40">
                  <span className="uppercase tracking-widest text-[10px] font-black text-muted-foreground">
                    Oracle Confidence
                  </span>
                  <div className="flex items-center gap-4">
                    <span className="text-4xl font-black tabular-nums tracking-tighter">
                      {(result.confidence * 100).toFixed(0)}%
                    </span>
                    <div className="w-32 h-2.5 bg-secondary rounded-full overflow-hidden shadow-inner">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${result.confidence * 100}%` }}
                        transition={{ duration: 1.5, ease: "circOut" }}
                        className="h-full bg-primary"
                      />
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pb-8">
                <div className="flex flex-wrap gap-4 items-center">
                  <Badge
                    variant="outline"
                    className="px-3 py-1 text-sm bg-muted/50 border-border/40"
                  >
                    Horizon: {result.time_horizon}
                  </Badge>
                  <Badge
                    variant="outline"
                    className="px-3 py-1 text-sm bg-muted/50 border-border/40"
                  >
                    Asset: {result.asset}
                  </Badge>
                  <div className="h-1 flex-1 border-t border-dashed border-border" />
                  <span className="text-sm text-muted-foreground italic">
                    Generated by Oracle-v4 Multi-Agent System
                  </span>
                </div>
              </CardContent>
            </Card>

            <Tabs defaultValue="summary" className="w-full">
              <TabsList className="flex flex-wrap md:grid md:grid-cols-5 gap-1.5 h-auto p-1.5 bg-secondary/40 rounded-2xl mb-8 border border-border/40">
                {[
                  "summary",
                  "technical",
                  "sentiment",
                  "news",
                  "fundamentals",
                ].map((tab) => (
                  <TabsTrigger
                    key={tab}
                    value={tab}
                    className="flex-1 py-3 px-4 data-[state=active]:bg-background data-[state=active]:shadow-lg data-[state=active]:shadow-black/[0.05] rounded-xl font-bold text-xs uppercase tracking-wider transition-all"
                  >
                    {tab}
                  </TabsTrigger>
                ))}
              </TabsList>

              <TabsContent
                value="summary"
                className="focus-visible:outline-none"
              >
                <Card className="border-border/60 shadow-sm bg-card">
                  <CardContent className="pt-8">
                    <div className="flex gap-4 items-start">
                      <div className="mt-1 p-2 bg-primary/5 rounded-lg">
                        <TrendingUp className="w-6 h-6 text-primary" />
                      </div>
                      <div className="space-y-4">
                        <h3 className="text-xl font-bold tracking-tight">
                          Final AI Reasoning
                        </h3>
                        <p className="text-lg leading-relaxed text-foreground/90 font-medium">
                          {result.summary}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent
                value="technical"
                className="focus-visible:outline-none outline-none"
              >
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <Card className="border-border/40 shadow-xl shadow-black/[0.02] bg-card/80 backdrop-blur-sm">
                    <CardHeader className="border-b border-border/30 pb-4">
                      <CardTitle className="text-base flex items-center gap-2 font-bold uppercase tracking-wider">
                        <BarChart3 className="w-4 h-4 text-primary" />
                        Momentum Pool
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-10 pt-8">
                      {/* ... existing RSI gauge with better visual polish ... */}
                      <div className="space-y-4">
                        <div className="flex justify-between items-end">
                          <span className="text-xs font-black uppercase tracking-widest text-muted-foreground">
                            RSI (14)
                          </span>
                          <span className="text-3xl font-black tracking-tighter">
                            {result.technical.rsi}
                          </span>
                        </div>
                        <div className="relative h-5 bg-secondary/60 rounded-full overflow-hidden shadow-inner">
                          <div className="absolute left-[30%] right-[30%] h-full bg-primary/5 border-x border-primary/10" />
                          <motion.div
                            initial={{ left: "50%" }}
                            animate={{ left: `${result.technical.rsi}%` }}
                            transition={{
                              duration: 1,
                              delay: 0.5,
                              ease: "backOut",
                            }}
                            className="absolute h-full w-2.5 bg-primary rounded-full shadow-[0_0_15px_rgba(0,0,0,0.1)] border border-background"
                            style={{ transform: "translateX(-50%)" }}
                          />
                        </div>
                        {/* ... */}
                      </div>

                      <div className="flex justify-between items-center py-4 border-t border-border/40">
                        <span className="text-xs font-black uppercase tracking-widest text-muted-foreground">
                          MACD
                        </span>
                        <Badge
                          variant="secondary"
                          className="text-sm px-3 py-1 font-bold"
                        >
                          {result.technical.macd}
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="border-border/40 shadow-xl shadow-black/[0.02] bg-card/80 backdrop-blur-sm">
                    <CardHeader className="border-b border-border/30 pb-4">
                      <CardTitle className="text-base flex items-center gap-2 font-bold uppercase tracking-wider">
                        <Activity className="w-4 h-4 text-primary" />
                        Trend & Volatility
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      <div className="p-4 bg-muted/30 rounded-lg space-y-1">
                        <span className="text-xs font-bold text-muted-foreground uppercase">
                          Current Trend
                        </span>
                        <p className="text-xl font-bold">
                          {result.technical.trend}
                        </p>
                      </div>
                      <div className="p-4 bg-muted/30 rounded-lg space-y-1">
                        <span className="text-xs font-bold text-muted-foreground uppercase">
                          Bollinger Bands
                        </span>
                        <p className="text-lg font-medium">
                          {result.technical.bollinger}
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              <TabsContent
                value="sentiment"
                className="focus-visible:outline-none"
              >
                <Card className="border-border/60 shadow-sm">
                  <CardHeader>
                    <CardTitle className="text-lg">
                      Market Sentiment Analysis
                    </CardTitle>
                    <CardDescription>
                      Aggregate psychology from social media and order books
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-10 pt-4">
                    <div className="flex flex-col items-center space-y-4">
                      <div className="relative w-full max-w-md h-6 bg-gradient-to-r from-sell via-hold to-buy rounded-full shadow-inner">
                        <div
                          className="absolute -top-1 h-8 w-2 bg-foreground rounded-full transition-all duration-1000 shadow-lg border-2 border-background"
                          style={{
                            left: `${result.sentiment.fear_greed_index}%`,
                            transform: "translateX(-50%)",
                          }}
                        />
                      </div>
                      <div className="flex justify-between w-full max-w-md text-[10px] uppercase font-black text-muted-foreground px-1">
                        <span>Extreme Fear</span>
                        <span>Neutral</span>
                        <span>Extreme Greed</span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-8 pt-6 border-t border-border/40">
                      <div className="text-center space-y-1">
                        <p className="text-4xl font-black">
                          {result.sentiment.fear_greed_index}
                        </p>
                        <p className="text-xs font-bold uppercase text-muted-foreground">
                          Index Value
                        </p>
                      </div>
                      <div className="text-center space-y-1">
                        <p
                          className={`text-2xl font-black uppercase ${
                            result.sentiment.label.includes("Greed")
                              ? "text-buy"
                              : result.sentiment.label.includes("Fear")
                              ? "text-sell"
                              : "text-hold"
                          }`}
                        >
                          {result.sentiment.label}
                        </p>
                        <p className="text-xs font-bold uppercase text-muted-foreground">
                          Market Label
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="news" className="focus-visible:outline-none">
                <Card className="border-border/60 shadow-sm">
                  <CardContent className="pt-8">
                    <div className="flex gap-4 items-start">
                      <div className="mt-1 p-2 bg-primary/5 rounded-lg">
                        <Newspaper className="w-6 h-6 text-primary" />
                      </div>
                      <div className="space-y-4">
                        <h3 className="text-xl font-bold tracking-tight">
                          Agent News Feed Analysis
                        </h3>
                        <p className="text-lg leading-relaxed text-muted-foreground">
                          {result.news}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent
                value="fundamentals"
                className="focus-visible:outline-none"
              >
                <Card className="border-border/60 shadow-sm">
                  <CardContent className="pt-8">
                    <div className="flex gap-4 items-start">
                      <div className="mt-1 p-2 bg-primary/5 rounded-lg">
                        <ShieldCheck className="w-6 h-6 text-primary" />
                      </div>
                      <div className="space-y-4">
                        <h3 className="text-xl font-bold tracking-tight">
                          On-Chain & Macro Fundamentals
                        </h3>
                        <p className="text-lg leading-relaxed text-muted-foreground">
                          {result.fundamentals}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Footer */}
      {!loading && !result && (
        <section className="mt-12 text-center p-12 border-2 border-dashed border-border rounded-2xl bg-muted/20">
          <div className="max-w-md mx-auto space-y-4">
            <Activity className="w-12 h-12 text-muted-foreground/40 mx-auto" />
            <h2 className="text-2xl font-bold">Ready for Analysis</h2>
            <p className="text-muted-foreground">
              Select an asset and your investment profile to receive a deep-dive
              AI verdict powered by 4 specialized sub-agents.
            </p>
          </div>
        </section>
      )}

      <footer className="mt-20 pt-8 border-t border-border flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-muted-foreground font-medium">
        <p>© 2026 CryptoOracle AI. Data-driven decision support.</p>
        <div className="flex gap-6">
          <span className="hover:text-primary cursor-pointer transition-colors">
            API Docs
          </span>
          <span className="hover:text-primary cursor-pointer transition-colors">
            Methodology
          </span>
          <span className="hover:text-primary cursor-pointer transition-colors">
            Risk Disclosure
          </span>
        </div>
      </footer>
    </motion.div>
  );
}
