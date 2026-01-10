'use client'

import { useState, useEffect, useRef } from 'react'
import { 
  Send, 
  Bot, 
  User as UserIcon, 
  Loader2,
  Sparkles,
  MessageSquare
} from 'lucide-react'
import { askQuestion, ChatResponse } from '../lib/api'

interface ChatbotSectionProps {
  category?: string | null
}

interface Message {
  id: string
  type: 'user' | 'bot'
  content: string
  sources?: string[]
  timestamp: Date
}

export default function ChatbotSection({ category }: ChatbotSectionProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'bot',
      content: `Hello! I'm your AI news assistant. Ask me anything about the latest news highlights${category ? ` in ${category}` : ''}!`,
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      // Don't restrict by category - let the chatbot search across all categories
      const response: ChatResponse = await askQuestion(input, undefined)
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: response.answer,
        sources: response.sources,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (error) {
      console.error('Error asking question:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: 'Sorry, I encountered an error. Please try again or rephrase your question.',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
        {/* Chat Header */}
        <div className="bg-gradient-to-r from-blue-500 to-indigo-600 p-6 text-white">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-white/20 rounded-lg">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold">AI News Assistant</h2>
              <p className="text-sm text-blue-100">
                Ask questions about the latest news highlights
              </p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="h-[500px] overflow-y-auto p-6 space-y-4 bg-gray-50">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          
          {loading && (
            <div className="flex items-center space-x-2 text-gray-500 animate-fade-in">
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Thinking...</span>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 bg-white border-t border-gray-200">
          <div className="flex items-end space-x-2">
            <div className="flex-1 relative">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a question about the news..."
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-gray-900 placeholder-gray-400"
                rows={1}
                style={{ minHeight: '48px', maxHeight: '120px' }}
              />
            </div>
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="p-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </div>
          <p className="text-xs text-gray-400 mt-2 text-center">
            Press Enter to send, Shift+Enter for new line
          </p>
        </div>
      </div>

      {/* Example Questions */}
      <div className="mt-6">
        <p className="text-sm text-gray-600 mb-3">Try asking:</p>
        <div className="flex flex-wrap gap-2">
          {[
            'What are the top sports stories?',
            'Tell me about breaking news',
            'What happened in finance today?',
            'Summarize the music news',
          ].map((question) => (
            <button
              key={question}
              onClick={() => setInput(question)}
              className="px-4 py-2 bg-white text-gray-700 rounded-full text-sm border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-all"
            >
              {question}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

function MessageBubble({ message }: { message: Message }) {
  const isBot = message.type === 'bot'

  return (
    <div className={`flex animate-fade-in ${isBot ? 'justify-start' : 'justify-end'}`}>
      <div className={`flex items-start space-x-3 max-w-[80%] ${isBot ? '' : 'flex-row-reverse space-x-reverse'}`}>
        <div
          className={`p-2 rounded-lg ${
            isBot
              ? 'bg-gradient-to-br from-blue-500 to-indigo-600 text-white'
              : 'bg-gray-200 text-gray-800'
          }`}
        >
          {isBot ? (
            <Bot className="w-5 h-5" />
          ) : (
            <UserIcon className="w-5 h-5" />
          )}
        </div>
        <div
          className={`rounded-2xl px-4 py-3 ${
            isBot
              ? 'bg-white border border-gray-200 text-gray-800'
              : 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white'
          }`}
        >
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
          {isBot && message.sources && message.sources.length > 0 && (
            <div className="mt-2 pt-2 border-t border-gray-200">
              <p className="text-xs text-gray-500 mb-1">Sources:</p>
              <div className="flex flex-wrap gap-1">
                {message.sources.map((source, idx) => (
                  <span
                    key={idx}
                    className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded"
                  >
                    {source}
                  </span>
                ))}
              </div>
            </div>
          )}
          <p className="text-xs opacity-60 mt-2">
            {message.timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
        </div>
      </div>
    </div>
  )
}

