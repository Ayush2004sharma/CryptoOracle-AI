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

/* ===== helpers ===== */
function formatText(text: string) {
  return text
    .replace(/---/g, "")
    .replace(/•/g, "\n•")
    .replace(/:/g, ":\n")
    .trim()
}

function renderBlocks(text: string) {
  return formatText(text)
    .split("\n\n")
    .map((block, i) => {
      if (block.startsWith("•")) {
        return (
          <ul
            key={i}
            className="list-disc pl-6 space-y-1 text-muted-foreground"
          >
            {block.split("\n").map((item, j) => (
              <li key={j}>{item.replace("•", "").trim()}</li>
            ))}
          </ul>
        )
      }

      return (
        <p key={i} className="text-foreground/90 leading-relaxed">
          {block}
        </p>
      )
    })
}

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

      {/* ===== TAB HEADER (FULL WIDTH LIKE PEHLE) ===== */}
      <TabsList className="flex w-full gap-2 p-2 bg-secondary/40 rounded-2xl mb-8 border border-border/40">
        {["summary", "technical", "sentiment", "news", "fundamentals"].map(tab => (
          <TabsTrigger
            key={tab}
            value={tab}
            className="
              flex-1
              py-3
              uppercase
              text-xs
              font-bold
              tracking-wider
              rounded-xl
              data-[state=active]:bg-background
              data-[state=active]:shadow-lg
            "
          >
            {tab}
          </TabsTrigger>
        ))}
      </TabsList>

      {/* ================= SUMMARY ================= */}
      <TabsContent value="summary">
        <Card className="border-border/60 shadow-sm bg-card">
          <CardContent className="pt-8 space-y-6">
            <div className="flex gap-4 items-start">
              <TrendingUp className="w-6 h-6 text-primary mt-1" />
              <div className="space-y-4">
                {renderBlocks(result.summary)}
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      {/* ================= TECHNICAL ================= */}
      <TabsContent value="technical">
        <Card className="border-border/60 shadow-sm">
          <CardContent className="pt-8 space-y-4">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-primary" />
              <b>RSI:</b> {result.technical.rsi}
            </div>
            <p><b>MACD:</b> {result.technical.macd}</p>
            <p><b>Trend:</b> {result.technical.trend}</p>
          </CardContent>
        </Card>
      </TabsContent>

      {/* ================= SENTIMENT ================= */}
      <TabsContent value="sentiment">
        <Card className="border-border/60 shadow-sm">
          <CardContent className="pt-8 space-y-3">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-primary" />
              <b>Fear & Greed Index:</b>
              {result.sentiment.fear_greed_index}
            </div>
            <p><b>Market Label:</b> {result.sentiment.label}</p>
          </CardContent>
        </Card>
      </TabsContent>

      {/* ================= NEWS (SYSTEMATIC) ================= */}
      <TabsContent value="news">
        <Card className="border-border/60 shadow-sm">
          <CardContent className="pt-8">
            <div className="flex gap-4 items-start">
              <Newspaper className="w-6 h-6 text-primary mt-1" />
              <div className="space-y-4">
                {renderBlocks(result.news)}
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      {/* ================= FUNDAMENTALS (SYSTEMATIC) ================= */}
      <TabsContent value="fundamentals">
        <Card className="border-border/60 shadow-sm">
          <CardContent className="pt-8">
            <div className="flex gap-4 items-start">
              <ShieldCheck className="w-6 h-6 text-primary mt-1" />
              <div className="space-y-4">
                {renderBlocks(result.fundamentals)}
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

    </Tabs>
  )
}
