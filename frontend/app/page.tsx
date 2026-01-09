'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Newspaper, 
  MessageSquare, 
  RefreshCw, 
  TrendingUp, 
  Clock,
  User,
  ExternalLink,
  Sparkles,
  Filter
} from 'lucide-react'
import HighlightsSection from './components/HighlightsSection'
import ChatbotSection from './components/ChatbotSection'
import { extractNews, getHighlights, getCategories } from './lib/api'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'highlights' | 'chat'>('highlights')
  const [loading, setLoading] = useState(false)
  const [categories, setCategories] = useState<Record<string, number>>({})
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)

  useEffect(() => {
    loadCategories()
  }, [])

  const loadCategories = async () => {
    try {
      const cats = await getCategories()
      setCategories(cats)
    } catch (error) {
      console.error('Error loading categories:', error)
    }
  }

  const handleExtractNews = async () => {
    setLoading(true)
    try {
      const result = await extractNews(['sports', 'lifestyle', 'music', 'finance'])
      alert(`News extraction completed! ${result.articles_extracted} articles extracted, ${result.highlights_created} highlights created.`)
      loadCategories()
    } catch (error: any) {
      console.error('Error extracting news:', error)
      const errorMessage = error?.message || 'Unknown error occurred'
      if (errorMessage.includes('Cannot connect to backend')) {
        alert('Cannot connect to backend server. Please ensure:\n1. Backend is running\n2. NEXT_PUBLIC_API_URL is set correctly\n3. CORS is configured properly')
      } else {
        alert(`Error extracting news: ${errorMessage}\n\nPlease check:\n1. Backend server is running\n2. Network connection is stable\n3. Try again in a moment`)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-lg sticky top-0 z-50 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg">
                <Newspaper className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  AI News Aggregation
                </h1>
                <p className="text-sm text-gray-500">Daily Highlights & Chatbot</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={handleExtractNews}
                disabled={loading}
                className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                <span>{loading ? 'Extracting...' : 'Extract News'}</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Category Filter */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        <div className="flex items-center space-x-4 overflow-x-auto pb-4">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`flex items-center space-x-2 px-4 py-2 rounded-full transition-all ${
              selectedCategory === null
                ? 'bg-blue-500 text-white shadow-md'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            <Filter className="w-4 h-4" />
            <span>All</span>
          </button>
          {Object.entries(categories).map(([category, count]) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-full transition-all capitalize ${
                selectedCategory === category
                  ? 'bg-blue-500 text-white shadow-md'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              <span>{category}</span>
              <span className="text-xs bg-white/20 px-2 py-0.5 rounded-full">
                {count}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        <div className="flex space-x-4 border-b border-gray-200">
          <button
            onClick={() => setActiveTab('highlights')}
            className={`flex items-center space-x-2 px-6 py-3 font-medium transition-all ${
              activeTab === 'highlights'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <TrendingUp className="w-5 h-5" />
            <span>Highlights</span>
          </button>
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex items-center space-x-2 px-6 py-3 font-medium transition-all ${
              activeTab === 'chat'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <MessageSquare className="w-5 h-5" />
            <span>Chatbot</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'highlights' ? (
          <HighlightsSection category={selectedCategory} />
        ) : (
          <ChatbotSection category={selectedCategory} />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white/80 backdrop-blur-md border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            AI-Powered News Aggregation System • Built with Next.js & FastAPI
          </p>
        </div>
      </footer>
    </div>
  )
}

