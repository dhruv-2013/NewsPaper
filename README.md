# AI-Powered News Aggregation & Chatbot

A comprehensive AI-powered system that extracts news articles from multiple Australian news outlets, categorizes and summarizes them, and presents daily highlights in a beautiful web UI. Features a RAG-based chatbot for interactive news queries.

## Features

- **News Extraction**: Automated extraction from multiple Australian news sources (ABC, The Guardian, SBS, AFR)
- **Smart Categorization**: Automatic classification into sports, lifestyle, music, and finance
- **Duplicate Detection**: Clustering algorithm to identify similar articles across sources
- **AI Summarization**: GPT-powered article summarization
- **Highlights Generation**: Prioritized highlights based on keywords and frequency
- **Beautiful UI**: Modern, responsive web dashboard with animations
- **RAG Chatbot**: Interactive chatbot using Retrieval-Augmented Generation

## Project Structure

```
NewsPaper/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── database.py     # Database configuration
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── routers/        # API routes
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Python dependencies
│   └── run.py             # Application entry point
│
└── frontend/               # Next.js frontend
    ├── app/
    │   ├── page.tsx       # Main page
    │   ├── components/    # React components
    │   └── lib/          # API utilities
    ├── package.json       # Node dependencies
    └── tailwind.config.js # Tailwind CSS config
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL (optional, SQLite used by default)
- OpenAI API key (for summarization and chatbot)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./news.db
```

6. Download NLTK data (if needed):
```python
python -c "import nltk; nltk.download('punkt')"
```

7. Run the backend server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file (optional):
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

### 1. Extract News

- Click the "Extract News" button in the header
- The system will fetch articles from all configured sources
- Articles are automatically categorized and duplicates are detected

### 2. View Highlights

- Browse highlights by category using the filter buttons
- Breaking news is highlighted at the top
- Each highlight shows:
  - Title and summary
  - Source(s) and author(s)
  - Frequency (number of sources)
  - Priority score

### 3. Use the Chatbot

- Switch to the "Chatbot" tab
- Ask questions about the news highlights
- The chatbot uses RAG to provide context-aware answers
- Example questions:
  - "What are the top sports stories?"
  - "Tell me about breaking news"
  - "What happened in finance today?"

## API Endpoints

### News Extraction
- `POST /api/news/extract` - Extract news articles
- `GET /api/news/articles` - Get articles (with optional category filter)

### Highlights
- `GET /api/highlights/` - Get highlights (with optional category filter)
- `GET /api/highlights/categories` - Get category counts
- `GET /api/highlights/breaking` - Get breaking news

### Chatbot
- `POST /api/chat/ask` - Ask a question
- `GET /api/chat/history` - Get chat history

## Technologies Used

### Backend
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database operations
- OpenAI API - AI summarization and chatbot
- Sentence Transformers - Embeddings for semantic search
- BeautifulSoup4 - Web scraping
- Feedparser - RSS feed parsing

### Frontend
- Next.js 14 - React framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Framer Motion - Animations
- Axios - HTTP client

## Configuration

### News Sources

Edit `backend/app/services/news_extractor.py` to add or modify news sources. The system currently supports:
- ABC News (Sports, Business, Lifestyle)
- The Guardian Australia (Sports, Business, Lifestyle, Music)
- SBS News (Sports)
- AFR (Finance)

### Categories

The system supports four categories:
- Sports
- Lifestyle
- Music
- Finance

### Highlight Prioritization

Highlights are prioritized based on:
- **Frequency**: Number of sources reporting the story
- **Breaking Keywords**: "breaking", "urgent", "alert", etc.
- **Important Keywords**: "announcement", "decision", "wins", etc.

## Troubleshooting

### Backend Issues

1. **Import errors**: Ensure all dependencies are installed
2. **Database errors**: Check DATABASE_URL in `.env`
3. **OpenAI errors**: Verify API key is set correctly

### Frontend Issues

1. **API connection errors**: Ensure backend is running on port 8000
2. **Build errors**: Run `npm install` again
3. **Styling issues**: Ensure Tailwind CSS is properly configured

## Future Enhancements

- [ ] Add more news sources
- [ ] Implement user authentication
- [ ] Add email notifications for breaking news
- [ ] Support for more categories
- [ ] Advanced filtering and search
- [ ] Export highlights to PDF
- [ ] Mobile app version

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

