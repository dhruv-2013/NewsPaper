import { NextResponse } from "next/server";

// Force dynamic rendering
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const category = searchParams.get("category");
  const limit = parseInt(searchParams.get("limit") || "50");

  try {
    // Get backend URL
    const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:8000';
    
    // Build query string
    const params = new URLSearchParams({ limit: limit.toString() });
    if (category) params.append('category', category);
    
    // Proxy to backend
    const response = await fetch(`${backendUrl}/api/highlights/?${params.toString()}`);
    
    if (!response.ok) {
      throw new Error(`Backend responded with status ${response.status}`);
    }
    
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    // If backend unavailable, return empty array
    if (error.message.includes('fetch failed') || error.message.includes('ECONNREFUSED')) {
      return NextResponse.json([]);
    }
    return NextResponse.json(
      { error: error.message || "Failed to fetch highlights" },
      { status: 500 }
    );
  }
}

