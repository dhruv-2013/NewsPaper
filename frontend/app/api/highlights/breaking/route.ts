import { NextResponse } from "next/server";

export async function GET() {
  try {
    // TODO: Query database for breaking news
    // Filter highlights where is_breaking = true
    // For now, return empty array
    
    return NextResponse.json([]);
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Failed to fetch breaking news" },
      { status: 500 }
    );
  }
}

