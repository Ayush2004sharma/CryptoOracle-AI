import { NextResponse } from "next/server"

export async function POST(req: Request) {
  try {
    const body = await req.json()

    const res = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/trade/analyze`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // optional: JWT forward later
        },
        body: JSON.stringify(body),
      }
    )

    const data = await res.json()

    if (!res.ok) {
      return NextResponse.json(
        { error: data.detail || "Analysis failed" },
        { status: res.status }
      )
    }

    return NextResponse.json(data)
  } catch (err) {
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    )
  }
}
