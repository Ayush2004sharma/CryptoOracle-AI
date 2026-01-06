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
      <TabsList className="grid grid-cols-5 gap-1.5 p-1.5 bg-secondary/40 rounded-2xl mb-8">
        {["summary", "technical", "sentiment", "news", "fundamentals"].map(tab => (
          <TabsTrigger
            key={tab}
            value={tab}
            className="uppercase text-xs font-bold tracking-wider"
          >
            {tab}
          </TabsTrigger>
        ))}
      </TabsList>

      {/* SUMMARY */}
      <TabsContent value="summary">
        <Card>
          <CardContent className="pt-8 flex gap-4">
            <TrendingUp className="w-6 h-6 text-primary mt-1" />
            <p className="text-lg leading-relaxed">{result.summary}</p>
          </CardContent>
        </Card>
      </TabsContent>

      {/* TECHNICAL */}
      <TabsContent value="technical">
        <Card>
          <CardContent className="pt-8 space-y-3">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-primary" />
              <b>RSI:</b> {result.technical.rsi}
            </div>
            <p><b>MACD:</b> {result.technical.macd}</p>
            <p><b>Trend:</b> {result.technical.trend}</p>
          </CardContent>
        </Card>
      </TabsContent>

      {/* SENTIMENT */}
      <TabsContent value="sentiment">
        <Card>
          <CardContent className="pt-8 space-y-2">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-primary" />
              <b>Fear & Greed Index:</b> {result.sentiment.fear_greed_index}
            </div>
            <p><b>Label:</b> {result.sentiment.label}</p>
          </CardContent>
        </Card>
      </TabsContent>

      {/* NEWS */}
      <TabsContent value="news">
        <Card>
          <CardContent className="pt-8 flex gap-4">
            <Newspaper className="w-6 h-6 text-primary mt-1" />
            <p className="leading-relaxed">{result.news}</p>
          </CardContent>
        </Card>
      </TabsContent>

      {/* FUNDAMENTALS */}
      <TabsContent value="fundamentals">
        <Card>
          <CardContent className="pt-8 flex gap-4">
            <ShieldCheck className="w-6 h-6 text-primary mt-1" />
            <p className="leading-relaxed">{result.fundamentals}</p>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  )
}
