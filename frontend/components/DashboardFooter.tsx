"use client"

import { Activity } from "lucide-react"

type Props = {
  showEmptyState: boolean
}

export default function DashboardFooter({ showEmptyState }: Props) {
  return (
    <>
      {/* Empty / Ready State */}
      {showEmptyState && (
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

      {/* Footer */}
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
    </>
  )
}
