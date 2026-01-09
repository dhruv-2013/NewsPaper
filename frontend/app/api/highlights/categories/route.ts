import { NextResponse } from "next/server";

// Force dynamic rendering
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

export async function GET() {
  try {
    const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:8000';
    
    const response = await fetch(`${backendUrl}/api/highlights/categories`);
    
    if (!response.ok) {
      throw new Error(`Backend responded with status ${response.status}`);
    }
    
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    if (error.message.includes('fetch failed') || error.message.includes('ECONNREFUSED')) {
      return NextResponse.json({});
    }
    return NextResponse.json(
      { error: error.message || "Failed to fetch categories" },
      { status: 500 }
    );
  }
}

