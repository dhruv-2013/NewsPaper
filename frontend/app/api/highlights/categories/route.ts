import { NextResponse } from "next/server";

export async function GET() {
  try {
    // TODO: Query database for category counts
    // Group highlights by category and count
    // For now, return empty object
    
    return NextResponse.json({});
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Failed to fetch categories" },
      { status: 500 }
    );
  }
}

