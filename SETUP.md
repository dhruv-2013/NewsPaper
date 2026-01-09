# Quick Setup Guide

## Backend Setup (5 minutes)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

5. **Download NLTK data (if needed):**
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```

6. **Run the server:**
   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:8000`

## Frontend Setup (3 minutes)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## First Use

1. Open `http://localhost:3000` in your browser
2. Click the "Extract News" button in the header
3. Wait for the extraction to complete (may take 1-2 minutes)
4. Browse highlights and try the chatbot!

## Troubleshooting

### Backend won't start
- Check that Python 3.9+ is installed: `python --version`
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify `.env` file exists and has `OPENAI_API_KEY` set

### Frontend won't start
- Check that Node.js 18+ is installed: `node --version`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Ensure backend is running on port 8000

### No articles extracted
- Check your internet connection
- Some RSS feeds may be temporarily unavailable
- Try again after a few minutes

### Chatbot not working
- Verify `OPENAI_API_KEY` is set correctly in backend `.env`
- Check that you have credits in your OpenAI account
- Ensure articles have been extracted first

