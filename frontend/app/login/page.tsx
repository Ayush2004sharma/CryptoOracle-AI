"use client"

import * as React from "react"
import Link from "next/link"
import { ShieldCheck, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useRouter } from "next/navigation"

export default function LoginPage() {
  const [isLoading, setIsLoading] = React.useState(false)
  const [error, setError] = React.useState("")
  const router = useRouter()

async function onSubmit(event: React.SyntheticEvent) {
  event.preventDefault()
  setIsLoading(true)
  setError("")

  const target = event.target as typeof event.target & {
    email: { value: string }
    password: { value: string }
  }

  try {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: target.email.value,
        password: target.password.value,
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      setError(data.error || "Login failed")
      setIsLoading(false)
      return
    }

    // ✅ STORE TOKEN
    localStorage.setItem("token", data.access_token)

    router.push("/")
  } catch (err) {
    setError("An error occurred. Please try again.")
  } finally {
    setIsLoading(false)
  }
}



  return (
    <div className="container flex h-screen w-screen flex-col items-center justify-center">
      <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
        <div className="flex flex-col space-y-2 text-center">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center text-primary-foreground">
              <ShieldCheck className="w-8 h-8" />
            </div>
          </div>
          <h1 className="text-2xl font-semibold tracking-tight">Welcome back</h1>
          <p className="text-sm text-muted-foreground">Enter your email to sign in to your account</p>
        </div>
        <Card>
          <form onSubmit={onSubmit}>
            <CardHeader className="space-y-1">
              <CardTitle className="text-xl">Sign in</CardTitle>
              <CardDescription>Use your credentials to access the terminal</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-4">
              {error && (
                <div className="p-3 text-sm text-destructive bg-destructive/10 border border-destructive/20 rounded-md">
                  {error}
                </div>
              )}
              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" name="email" type="email" placeholder="m@example.com" required />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="password">Password</Label>
                <Input id="password" name="password" type="password" required />
              </div>
            </CardContent>
            <CardFooter>
              <Button className="w-full" disabled={isLoading}>
                {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Sign In
              </Button>
            </CardFooter>
          </form>
        </Card>
        <p className="px-8 text-center text-sm text-muted-foreground">
          <Link href="/signup" className="hover:text-brand underline underline-offset-4">
            Don&apos;t have an account? Sign Up
          </Link>
        </p>
      </div>
    </div>
  )
}
