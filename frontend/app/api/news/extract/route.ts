import { NextResponse } from "next/server";

// Force dynamic rendering - don't pre-render at build time
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { categories = ["sports", "lifestyle", "music", "finance"], force_refresh = false } = body;

    // Get backend URL from environment or use default
    const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:8000';
    
    // Proxy request to Python backend
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 180000); // 3 minutes timeout
      
      const response = await fetch(`${backendUrl}/api/news/extract`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ categories, force_refresh }),
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text().catch(() => 'Unknown error');
        console.error(`Backend error ${response.status}:`, errorText);
        
        if (response.status === 502 || response.status === 503) {
          throw new Error(`Backend is unavailable (${response.status}). Render free tier may be spinning up. Please wait 30-60 seconds and try again.`);
        }
        
        throw new Error(`Backend responded with status ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      return NextResponse.json(data);
    } catch (backendError: any) {
      // Handle different error types
      const errorMsg = backendError.message || '';
      
      if (errorMsg.includes('fetch failed') || errorMsg.includes('ECONNREFUSED') || errorMsg.includes('502') || errorMsg.includes('503')) {
        return NextResponse.json(
          {
            message: "Backend server is unavailable. Render free tier may be spinning up. Please wait 30-60 seconds and try again.",
            articles_extracted: 0,
            duplicates_found: 0,
            highlights_created: 0,
            error: errorMsg.includes('502') || errorMsg.includes('503') 
              ? "Backend is starting up (Render free tier). Wait 30-60 seconds and retry."
              : "Backend connection failed. Check BACKEND_URL and ensure backend is deployed."
          },
          { status: 503 }
        );
      }
      
      throw backendError;
    }
  } catch (error: any) {
    return NextResponse.json(
      { 
        error: error.message || "Failed to extract news",
        message: "News extraction failed",
        articles_extracted: 0,
        duplicates_found: 0,
        highlights_created: 0
      },
      { status: 500 }
    );
  }
}

