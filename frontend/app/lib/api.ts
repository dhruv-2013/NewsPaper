import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Article {
  id: number
  title: string
  content: string
  summary: string
  author: string
  source: string
  source_url: string
  category: string
  published_date: string
  extracted_date: string
  is_duplicate: boolean
  cluster_id: number | null
}

export interface Highlight {
  id: number
  article_id: number
  title: string
  summary: string
  category: string
  frequency: number
  priority_score: number
  sources: string[]
  authors: string[]
  is_breaking: boolean
  created_date: string
}

export interface ChatRequest {
  question: string
  category?: string
}

export interface ChatResponse {
  answer: string
  sources: string[]
  related_articles: number[]
}

export const extractNews = async (categories: string[] = ['sports', 'lifestyle', 'music', 'finance']) => {
  const response = await api.post('/news/extract', {
    categories,
    force_refresh: false,
  })
  return response.data
}

export const getHighlights = async (category?: string | null, limit: number = 50): Promise<Highlight[]> => {
  const params: any = { limit }
  if (category) {
    params.category = category
  }
  const response = await api.get('/highlights/', { params })
  return response.data
}

export const getCategories = async (): Promise<Record<string, number>> => {
  const response = await api.get('/highlights/categories')
  return response.data
}

export const getBreakingNews = async (): Promise<Highlight[]> => {
  const response = await api.get('/highlights/breaking')
  return response.data
}

export const askQuestion = async (question: string, category?: string | null): Promise<ChatResponse> => {
  const response = await api.post('/chat/ask', {
    question,
    category: category || undefined,
  })
  return response.data
}

export const getChatHistory = async (limit: number = 20) => {
  const response = await api.get('/chat/history', { params: { limit } })
  return response.data
}

