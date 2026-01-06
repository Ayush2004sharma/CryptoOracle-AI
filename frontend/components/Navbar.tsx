"use client"

import { ShieldCheck, Moon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/theme-toggle"
import { useRouter } from "next/navigation"

export default function Navbar() {
  const router = useRouter()

  const handleLogout = () => {
    localStorage.removeItem("token")
    localStorage.removeItem("user_name")
    localStorage.removeItem("user_email")
    router.push("/login")
  }

  return (
    <header className="w-full px-6 py-4 flex items-center justify-between border-b border-border bg-background/80 backdrop-blur-md">
      {/* LEFT BRAND */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-primary-foreground">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div className="leading-tight">
          <h1 className="text-xl font-extrabold tracking-tight">
            CryptoOracle
          </h1>
          <p className="text-xs text-muted-foreground">
            Professional AI Analysis Terminal
          </p>
        </div>
      </div>

      {/* RIGHT ACTIONS */}
      <div className="flex items-center gap-3">
        <ThemeToggle />
        <Button
          variant="ghost"
          size="sm"
          onClick={handleLogout}
          className="rounded-full px-5 py-2 bg-muted/40 hover:bg-muted transition"
        >
          Logout
        </Button>
      </div>
    </header>
  )
}
