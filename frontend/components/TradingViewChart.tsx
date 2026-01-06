"use client"

import { useEffect, useRef } from "react"

type Props = {
  symbol?: string
  height?: number
}

export default function TradingViewChart({
  symbol = "BINANCE:BTCUSDT",
  height = 500,
}: Props) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!ref.current) return

    ref.current.innerHTML = ""

    const script = document.createElement("script")
    script.src = "https://s3.tradingview.com/tv.js"
    script.async = true
    script.onload = () => {
      // @ts-ignore
      new TradingView.widget({
        autosize: true,
        symbol,
        interval: "5",
        timezone: "Asia/Kolkata",
        theme: "dark",
        style: "1",
        locale: "en",
        enable_publishing: false,
        hide_side_toolbar: false,
        container_id: ref.current!.id,
      })
    }

    ref.current.appendChild(script)
  }, [symbol])

  return (
    <div
      id="tradingview_container"
      ref={ref}
      style={{ height }}
      className="w-full rounded-xl overflow-hidden border"
    />
  )
}
