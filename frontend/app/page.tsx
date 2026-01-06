"use client"

import { useState } from "react"
import { CryptoDashboard } from "@/components/crypto-dashboard"
import TradingViewChart from "@/components/TradingViewChart"
import { COIN_CONFIG, SupportedCoin } from "@/lib/coins"

export default function Page() {
  // ✅ coin state properly typed
  const [coin, setCoin] = useState<SupportedCoin>("bitcoin")

  return (
    <main className="min-h-screen bg-background space-y-8">
      {/* Dashboard controls the coin */}
      <CryptoDashboard coin={coin} setCoin={setCoin} />

      {/* Chart reacts to coin safely */}
      <TradingViewChart
        symbol={COIN_CONFIG[coin].tv}
        height={600}
      />
    </main>
  )
}
