"use client"

import { motion } from "framer-motion"
import { Loader2, Activity } from "lucide-react"

export default function DashboardLoading() {
  return (
    <motion.div
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
            Performing deep multi-agent synthesis of current market dynamics and sentiment pools.
          </p>
        </div>
      </div>
    </motion.div>
  )
}
