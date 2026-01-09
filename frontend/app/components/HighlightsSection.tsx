'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Clock, 
  User, 
  ExternalLink, 
  TrendingUp, 
  AlertCircle,
  Newspaper,
  Users
} from 'lucide-react'
import { format } from 'date-fns'
import { getHighlights, getBreakingNews, Highlight } from '../lib/api'

interface HighlightsSectionProps {
  category?: string | null
}

export default function HighlightsSection({ category }: HighlightsSectionProps) {
  const [highlights, setHighlights] = useState<Highlight[]>([])
  const [breakingNews, setBreakingNews] = useState<Highlight[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadHighlights()
  }, [category])

  const loadHighlights = async () => {
    setLoading(true)
    try {
      const [highlightsData, breakingData] = await Promise.all([
        getHighlights(category || undefined),
        getBreakingNews(),
      ])
      setHighlights(highlightsData)
      setBreakingNews(breakingData)
    } catch (error) {
      console.error('Error loading highlights:', error)
    } finally {
      setLoading(false)
    }
  }

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      sports: 'bg-green-100 text-green-800 border-green-300',
      lifestyle: 'bg-pink-100 text-pink-800 border-pink-300',
      music: 'bg-purple-100 text-purple-800 border-purple-300',
      finance: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    }
    return colors[category] || 'bg-gray-100 text-gray-800 border-gray-300'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Breaking News Section */}
      {breakingNews.length > 0 && (
        <div>
          <div className="flex items-center space-x-2 mb-4">
            <AlertCircle className="w-6 h-6 text-red-500" />
            <h2 className="text-2xl font-bold text-gray-800">Breaking News</h2>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {breakingNews.map((highlight, index) => (
              <BreakingNewsCard key={highlight.id} highlight={highlight} index={index} />
            ))}
          </div>
        </div>
      )}

      {/* All Highlights */}
      <div>
        <div className="flex items-center space-x-2 mb-6">
          <TrendingUp className="w-6 h-6 text-blue-600" />
          <h2 className="text-2xl font-bold text-gray-800">
            {category ? `${category.charAt(0).toUpperCase() + category.slice(1)} Highlights` : 'All Highlights'}
          </h2>
        </div>

        {highlights.length === 0 ? (
          <div className="text-center py-20">
            <Newspaper className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No highlights available. Extract news to get started!</p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {highlights.map((highlight, index) => (
              <HighlightCard
                key={highlight.id}
                highlight={highlight}
                index={index}
                categoryColor={getCategoryColor(highlight.category)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function BreakingNewsCard({ highlight, index }: { highlight: Highlight; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="bg-gradient-to-br from-red-50 to-orange-50 border-2 border-red-300 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-300"
    >
      <div className="flex items-start justify-between mb-3">
        <span className="px-3 py-1 bg-red-500 text-white text-xs font-bold rounded-full flex items-center space-x-1">
          <AlertCircle className="w-3 h-3" />
          <span>BREAKING</span>
        </span>
        <span className="text-xs text-gray-500 capitalize border px-2 py-1 rounded">
          {highlight.category}
        </span>
      </div>
      <h3 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2">
        {highlight.title}
      </h3>
      <p className="text-sm text-gray-600 mb-4 line-clamp-3">
        {highlight.summary}
      </p>
      <div className="flex items-center justify-between text-xs text-gray-500">
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1">
            <Users className="w-3 h-3" />
            <span>{highlight.frequency} sources</span>
          </div>
          {highlight.authors.length > 0 && (
            <div className="flex items-center space-x-1">
              <User className="w-3 h-3" />
              <span>{highlight.authors[0]}</span>
            </div>
          )}
        </div>
        <div className="flex items-center space-x-1">
          <Clock className="w-3 h-3" />
          <span>{format(new Date(highlight.created_date), 'MMM d')}</span>
        </div>
      </div>
    </motion.div>
  )
}

function HighlightCard({ 
  highlight, 
  index, 
  categoryColor 
}: { 
  highlight: Highlight
  index: number
  categoryColor: string
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className="bg-white rounded-xl p-6 shadow-md hover:shadow-xl transition-all duration-300 border border-gray-200 hover:border-blue-300"
    >
      <div className="flex items-start justify-between mb-3">
        <span className={`px-3 py-1 text-xs font-semibold rounded-full border capitalize ${categoryColor}`}>
          {highlight.category}
        </span>
        {highlight.is_breaking && (
          <span className="px-2 py-1 bg-red-500 text-white text-xs font-bold rounded">
            BREAKING
          </span>
        )}
      </div>
      
      <h3 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2 hover:text-blue-600 transition-colors">
        {highlight.title}
      </h3>
      
      <p className="text-sm text-gray-600 mb-4 line-clamp-3">
        {highlight.summary}
      </p>
      
      <div className="space-y-2 mb-4">
        <div className="flex items-center space-x-2 text-xs text-gray-500">
          <Users className="w-4 h-4" />
          <span className="font-medium">{highlight.frequency} source{highlight.frequency > 1 ? 's' : ''}</span>
        </div>
        {highlight.sources.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {highlight.sources.slice(0, 3).map((source, idx) => (
              <span key={idx} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                {source}
              </span>
            ))}
            {highlight.sources.length > 3 && (
              <span className="text-xs text-gray-500">+{highlight.sources.length - 3} more</span>
            )}
          </div>
        )}
        {highlight.authors.length > 0 && (
          <div className="flex items-center space-x-2 text-xs text-gray-500">
            <User className="w-4 h-4" />
            <span>{highlight.authors[0]}{highlight.authors.length > 1 ? ` +${highlight.authors.length - 1} more` : ''}</span>
          </div>
        )}
      </div>
      
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="flex items-center space-x-1 text-xs text-gray-400">
          <Clock className="w-3 h-3" />
          <span>{format(new Date(highlight.created_date), 'MMM d, yyyy')}</span>
        </div>
        <div className="flex items-center space-x-1 text-xs text-blue-600">
          <TrendingUp className="w-3 h-3" />
          <span>Score: {highlight.priority_score.toFixed(0)}</span>
        </div>
      </div>
    </motion.div>
  )
}

