"use client"

import { useState } from "react"
import { CryptoDashboard } from "@/components/crypto-dashboard"
import TradingViewChart from "@/components/TradingViewChart"
import { COIN_CONFIG, SupportedCoin } from "@/lib/coins"
import Navbar from "@/components/Navbar"

export default function Page() {
  // ✅ coin state properly typed
  const [coin, setCoin] = useState<SupportedCoin>("bitcoin")

  return (
 <main className="min-h-screen bg-background">
  <Navbar />

  <CryptoDashboard coin={coin} setCoin={setCoin} />

  <TradingViewChart
    symbol={COIN_CONFIG[coin].tv}
    height={600}
  />
</main>


  )
}
