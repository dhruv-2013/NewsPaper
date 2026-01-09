import axios from 'axios'

// Get API URL from environment or use Next.js API routes
const getApiUrl = () => {
  // If NEXT_PUBLIC_API_URL is set, use external backend
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL
  }
  
  // Otherwise, use Next.js API routes (works on Vercel)
  // In browser, use relative path; in server, use full URL
  if (typeof window !== 'undefined') {
    return '/api'
  }
  
  // Server-side: use full URL or localhost for development
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:8000/api'
  }
  
  // Production: use relative path for Next.js API routes
  return '/api'
}

const API_BASE_URL = getApiUrl()

// Create separate axios instances for different endpoints
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 90000, // 90 seconds for news extraction
})

// Separate instance for chat (shorter timeout)
const chatApi = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds for chat
})

// Add request interceptor for better error handling
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
      console.error('Network Error - Backend may not be running or CORS issue')
      console.error('API URL:', API_BASE_URL)
      throw new Error('Cannot connect to backend. Please check if the backend server is running and CORS is configured correctly.')
    }
    console.error('API Error:', error.response?.data || error.message)
    throw error
  }
)

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
  const response = await chatApi.post('/chat/ask', {
    question,
    category: category || undefined,
  })
  return response.data
}

export const getChatHistory = async (limit: number = 20) => {
  const response = await api.get('/chat/history', { params: { limit } })
  return response.data
}

