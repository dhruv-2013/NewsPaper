import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { question, category } = body;

    if (!question) {
      return NextResponse.json(
        { error: "Question is required" },
        { status: 400 }
      );
    }

    // TODO: Implement RAG chatbot logic
    // This needs:
    // 1. Query database for relevant articles
    // 2. Use OpenAI API for RAG
    // 3. Return response with sources
    
    return NextResponse.json({
      answer: "Chatbot endpoint - implementation needed. Please connect to your backend service.",
      sources: [],
      related_articles: []
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Failed to process question" },
      { status: 500 }
    );
  }
}

