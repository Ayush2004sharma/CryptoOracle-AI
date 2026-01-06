"use client"

import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import { Card, CardContent } from "@/components/ui/card"
import {
  TrendingUp,
  BarChart3,
  Activity,
  Newspaper,
  ShieldCheck,
} from "lucide-react"

type Props = {
  result: {
    summary: string
    news: string
    fundamentals: string
    technical: {
      rsi: number
      macd: string
      trend: string
    }
    sentiment: {
      fear_greed_index: number
      label: string
    }
  }
}

export default function DashboardTabs({ result }: Props) {
  return (
    <Tabs defaultValue="summary" className="w-full">

      {/* ✅ RESTORED TAB BAR */}
      <TabsList
        className="
          flex flex-wrap md:grid md:grid-cols-5
          gap-1.5 h-auto p-1.5
          bg-secondary/40 rounded-2xl
          mb-8 border border-border/40
        "
      >
        {["summary", "technical", "sentiment", "news", "fundamentals"].map(tab => (
          <TabsTrigger
            key={tab}
            value={tab}
            className="
              flex-1 py-3 px-4
              rounded-xl
              font-bold text-xs uppercase tracking-wider
              transition-all
              data-[state=active]:bg-background
              data-[state=active]:shadow-lg
              data-[state=active]:shadow-black/[0.05]
            "
          >
            {tab}
          </TabsTrigger>
        ))}
      </TabsList>

      {/* SUMMARY */}
      <TabsContent value="summary">
        <Card className="border-border/60 shadow-sm bg-card">
          <CardContent className="pt-8 flex gap-4">
            <TrendingUp className="w-6 h-6 text-primary mt-1" />
            <p className="text-lg leading-relaxed font-medium">
              {result.summary}
            </p>
          </CardContent>
        </Card>
      </TabsContent>

      {/* TECHNICAL */}
      <TabsContent value="technical">
        <Card className="border-border/60 shadow-sm bg-card">
          <CardContent className="pt-8 space-y-3">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-primary" />
              <span className="font-bold">RSI:</span> {result.technical.rsi}
            </div>
            <p><b>MACD:</b> {result.technical.macd}</p>
            <p><b>Trend:</b> {result.technical.trend}</p>
          </CardContent>
        </Card>
      </TabsContent>

      {/* SENTIMENT */}
      <TabsContent value="sentiment">
        <Card className="border-border/60 shadow-sm bg-card">
          <CardContent className="pt-8 space-y-2">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-primary" />
              <span className="font-bold">
                Fear & Greed Index:
              </span>
              {result.sentiment.fear_greed_index}
            </div>
            <p><b>Label:</b> {result.sentiment.label}</p>
          </CardContent>
        </Card>
      </TabsContent>

      {/* NEWS */}
      <TabsContent value="news">
        <Card className="border-border/60 shadow-sm bg-card">
          <CardContent className="pt-8 flex gap-4">
            <Newspaper className="w-6 h-6 text-primary mt-1" />
            <p className="leading-relaxed">{result.news}</p>
          </CardContent>
        </Card>
      </TabsContent>

      {/* FUNDAMENTALS */}
      <TabsContent value="fundamentals">
        <Card className="border-border/60 shadow-sm bg-card">
          <CardContent className="pt-8 flex gap-4">
            <ShieldCheck className="w-6 h-6 text-primary mt-1" />
            <p className="leading-relaxed">{result.fundamentals}</p>
          </CardContent>
        </Card>
      </TabsContent>

    </Tabs>
  )
}
