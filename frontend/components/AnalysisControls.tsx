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
    <section className="mb-10">
      <Card className="border-border/40 shadow-xl shadow-black/[0.02] dark:shadow-white/[0.01] bg-card/60 backdrop-blur-md">
        <CardContent className="pt-6">
          <form
            onSubmit={onAnalyze}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 items-end"
          >
            {/* Cryptocurrency */}
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

            {/* Profile */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-muted-foreground uppercase tracking-widest px-1">
                Investor Profile
              </label>
              <Select value={profile} onValueChange={setProfile}>
                <SelectTrigger>
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

            {/* Duration */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-muted-foreground uppercase tracking-widest px-1">
                Duration
              </label>
              <Select value={duration} onValueChange={setDuration}>
                <SelectTrigger>
                  <SelectValue placeholder="Horizon" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="short_term">Short Term</SelectItem>
                  <SelectItem value="medium_term">Medium Term</SelectItem>
                  <SelectItem value="long_term">Long Term</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Submit */}
            <motion.div whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.98 }}>
              <Button
                type="submit"
                className="w-full h-11 text-base font-bold shadow-lg shadow-primary/10"
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
  )
}
