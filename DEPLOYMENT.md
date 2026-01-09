# Deployment Guide

This guide covers deploying the AI News Aggregation application to production.

## Architecture

- **Backend**: FastAPI (Python) - needs a Python hosting service
- **Frontend**: Next.js (React) - can deploy to Vercel, Netlify, or similar

## Recommended Deployment Platforms

### Option 1: Vercel (Frontend) + Railway (Backend) ⭐ Recommended

#### Backend Deployment (Railway)

1. **Sign up at [Railway.app](https://railway.app)**

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select the `backend` folder

3. **Configure Environment Variables**:
   - Go to Variables tab
   - Add:
     ```
     DATABASE_URL=postgresql://... (Railway provides this)
     OPENAI_API_KEY=your_openai_api_key
     SECRET_KEY=your_secret_key
     ENVIRONMENT=production
     ```

4. **Configure Build Settings**:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py` or `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. **Get Backend URL**: Railway will provide a URL like `https://your-app.railway.app`

#### Frontend Deployment (Vercel)

1. **Sign up at [Vercel.com](https://vercel.com)**

2. **Import Project**:
   - Click "Add New Project"
   - Import from GitHub
   - Select your repository
   - Root Directory: `frontend`

3. **Configure Environment Variables**:
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://your-app.railway.app/api
     ```

4. **Deploy**: Vercel will automatically deploy

### Option 2: Render (Both Backend & Frontend)

#### Backend on Render

1. **Sign up at [Render.com](https://render.com)**

2. **Create New Web Service**:
   - Connect GitHub repository
   - Settings:
     - Name: `news-aggregation-backend`
     - Root Directory: `backend`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**:
   ```
   DATABASE_URL=postgresql://... (Render provides)
   OPENAI_API_KEY=your_key
   SECRET_KEY=your_secret
   ```

#### Frontend on Render

1. **Create New Static Site**:
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `out`

2. **Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api
   ```

### Option 3: Docker Deployment

See `docker-compose.yml` for containerized deployment.

## Quick Deploy Scripts

### Railway Backend

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
cd backend
railway init

# Deploy
railway up
```

### Vercel Frontend

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel
```

## Environment Variables Checklist

### Backend (.env)
- ✅ `DATABASE_URL` - PostgreSQL connection string
- ✅ `OPENAI_API_KEY` - Your OpenAI API key
- ✅ `SECRET_KEY` - Random secret for sessions
- ✅ `ENVIRONMENT=production`

### Frontend (.env.local)
- ✅ `NEXT_PUBLIC_API_URL` - Your backend API URL

## Post-Deployment Steps

1. **Update CORS** in `backend/app/main.py`:
   ```python
   allow_origins=["https://your-frontend.vercel.app"]
   ```

2. **Test the deployment**:
   - Visit frontend URL
   - Click "Extract News"
   - Test chatbot

3. **Monitor logs**:
   - Check Railway/Render logs for errors
   - Monitor API usage

## Troubleshooting

### Backend Issues
- Check logs for database connection errors
- Verify environment variables are set
- Ensure port is set to `$PORT` (platform-provided)

### Frontend Issues
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check browser console for CORS errors
- Ensure backend is accessible

### Database Issues
- Use PostgreSQL on production (not SQLite)
- Railway/Render provide managed PostgreSQL
- Update `DATABASE_URL` accordingly

## Cost Estimates

- **Railway Backend**: ~$5-20/month (depending on usage)
- **Vercel Frontend**: Free tier available
- **Render**: Free tier available (with limitations)
- **OpenAI API**: Pay-as-you-go

## Security Notes

- ✅ Never commit `.env` files
- ✅ Use strong `SECRET_KEY`
- ✅ Enable HTTPS only
- ✅ Set up rate limiting for production
- ✅ Monitor API usage

