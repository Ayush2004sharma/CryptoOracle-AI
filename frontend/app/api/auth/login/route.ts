import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();

    const res = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/login`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );

    const data = await res.json();

    // 🔒 Normalize FastAPI errors → STRING
    if (!res.ok) {
      const message =
        Array.isArray(data?.detail)
          ? data.detail[0]?.msg
          : typeof data?.detail === "string"
          ? data.detail
          : "Login failed";

      return NextResponse.json(
        { error: message },
        { status: res.status }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
