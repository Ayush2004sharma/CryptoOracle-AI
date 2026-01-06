"use client"

import { motion } from "framer-motion"
import { Loader2, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
} from "@/components/ui/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { COIN_CONFIG, SupportedCoin } from "@/lib/coins"

type Props = {
  coin: SupportedCoin
  setCoin: (coin: SupportedCoin) => void
  profile: string
  setProfile: (v: string) => void
  duration: string
  setDuration: (v: string) => void
  loading: boolean
  onAnalyze: (e?: React.FormEvent) => void
}
export default function AnalysisControls({
  coin,
  setCoin,
  profile,
  setProfile,
  duration,
  setDuration,
  loading,
  onAnalyze,
}: Props) {
  return (
    <aside className="w-full max-w-xs">
      <Card className="border-border/40 shadow-xl bg-card/70 backdrop-blur-md">
        <CardContent className="pt-6 space-y-6">

          {/* ASSET */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-muted-foreground uppercase tracking-widest">
              Asset
            </label>
            <Select
              value={coin}
              onValueChange={(v) => setCoin(v as SupportedCoin)}
            >
              <SelectTrigger className="w-full">
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

          {/* PROFILE */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-muted-foreground uppercase tracking-widest">
              Profile
            </label>
            <Select value={profile} onValueChange={setProfile}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Investor Profile" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="new_buyer">New Investor</SelectItem>
                <SelectItem value="existing_buyer">
                  Existing Holder
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* DURATION */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-muted-foreground uppercase tracking-widest">
              Duration
            </label>
            <Select value={duration} onValueChange={setDuration}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Time Horizon" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="short_term">Short Term</SelectItem>
                <SelectItem value="medium_term">Medium Term</SelectItem>
                <SelectItem value="long_term">Long Term</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* RUN BUTTON */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.97 }}
            className="pt-4"
          >
            <Button
              type="submit"
              onClick={onAnalyze}
              className="w-full h-12 text-base font-bold shadow-lg shadow-primary/20"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Running...
                </>
              ) : (
                <>
                  Run Analysis
                  <ChevronRight className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
          </motion.div>

        </CardContent>
      </Card>
    </aside>
  )
}
