import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { categories = ["sports", "lifestyle", "music", "finance"], force_refresh = false } = body;

    // Get backend URL from environment or use default
    const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:8000';
    
    // Proxy request to Python backend
    try {
      const response = await fetch(`${backendUrl}/api/news/extract`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ categories, force_refresh }),
      });

      if (!response.ok) {
        throw new Error(`Backend responded with status ${response.status}`);
      }

      const data = await response.json();
      return NextResponse.json(data);
    } catch (backendError: any) {
      // If backend is not available, return helpful error
      if (backendError.message.includes('fetch failed') || backendError.message.includes('ECONNREFUSED')) {
        return NextResponse.json(
          {
            message: "Backend server is not available. Please ensure your backend is deployed and BACKEND_URL is set correctly.",
            articles_extracted: 0,
            duplicates_found: 0,
            highlights_created: 0,
            error: "Backend connection failed. Set BACKEND_URL environment variable to your Python backend URL."
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

