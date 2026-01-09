# Quick Deployment Guide

## 🚀 Fastest Way: Vercel + Railway

### Step 1: Deploy Backend (Railway) - 5 minutes

1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `NewsPaper` repository
4. Click "Add Service" → Select the `backend` folder
5. Go to "Variables" tab and add:
   ```
   OPENAI_API_KEY=your_openai_key_here
   SECRET_KEY=generate_a_random_secret
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```
6. Railway will auto-deploy! Copy the URL (e.g., `https://your-app.railway.app`)

### Step 2: Deploy Frontend (Vercel) - 3 minutes

1. Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. Click "Add New Project" → Import your `NewsPaper` repository
3. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js (auto-detected)
4. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-app.railway.app/api
   ```
   (Use the Railway URL from Step 1)
5. Click "Deploy"

### Step 3: Update CORS

1. Go back to Railway
2. Update `CORS_ORIGINS` variable with your Vercel URL:
   ```
   CORS_ORIGINS=https://your-app.vercel.app
   ```
3. Railway will auto-redeploy

### ✅ Done!

Your app is live at: `https://your-app.vercel.app`

---

## Alternative: Render (All-in-One)

### Backend on Render

1. Go to [render.com](https://render.com) → Sign up
2. "New +" → "Web Service"
3. Connect GitHub → Select repo
4. Settings:
   - **Name**: `news-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   ```
   OPENAI_API_KEY=your_key
   SECRET_KEY=your_secret
   ```
6. Deploy!

### Frontend on Render

1. "New +" → "Static Site"
2. Connect GitHub → Select repo
3. Settings:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `out`
4. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api
   ```
5. Deploy!

---

## 🐳 Docker Deployment

If you have a server with Docker:

```bash
# Clone repo
git clone https://github.com/dhruv-2013/NewsPaper.git
cd NewsPaper

# Create .env file
echo "OPENAI_API_KEY=your_key" > .env
echo "SECRET_KEY=your_secret" >> .env

# Deploy
docker-compose up -d
```

App will be at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

## 📝 Environment Variables Checklist

### Backend
- ✅ `OPENAI_API_KEY` - Required for AI features
- ✅ `SECRET_KEY` - Random string for security
- ✅ `DATABASE_URL` - Auto-provided by Railway/Render
- ✅ `CORS_ORIGINS` - Your frontend URL

### Frontend
- ✅ `NEXT_PUBLIC_API_URL` - Your backend URL

---

## 🔧 Troubleshooting

**Backend won't start?**
- Check logs in Railway/Render dashboard
- Verify all environment variables are set
- Ensure `PORT` variable is used (platform provides this)

**Frontend can't connect?**
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings in backend
- Look at browser console for errors

**Database errors?**
- Railway/Render provide PostgreSQL automatically
- Check `DATABASE_URL` is set correctly

---

## 💰 Cost Estimates

- **Railway**: $5/month (free tier available)
- **Vercel**: Free for personal projects
- **Render**: Free tier available
- **OpenAI API**: Pay-as-you-go (~$0.002 per request)

---

## 🎉 Success!

Once deployed, your app will be accessible worldwide!

- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-app.railway.app`
- API Docs: `https://your-app.railway.app/docs`

