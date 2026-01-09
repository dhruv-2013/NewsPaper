import { NextResponse } from "next/server";

// This will be a serverless function on Vercel
// For now, return mock data - you'll need to connect to your database
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const category = searchParams.get("category");
  const limit = parseInt(searchParams.get("limit") || "50");

  try {
    // TODO: Replace with actual database query
    // For now, return empty array
    // You'll need to set up a database (Vercel Postgres, Supabase, etc.)
    
    return NextResponse.json([]);
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Failed to fetch highlights" },
      { status: 500 }
    );
  }
}

