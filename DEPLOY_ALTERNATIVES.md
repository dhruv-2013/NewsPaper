# Alternative Deployment Options

## 🎯 Option 1: Render (Easiest - Recommended) ⭐

Render is simpler than Vercel and supports both frontend and backend on one platform.

### Deploy Backend on Render

1. **Sign up**: Go to [render.com](https://render.com) → Sign up with GitHub

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your `NewsPaper` repo

3. **Configure Backend**:
   - **Name**: `news-aggregation-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**:
   ```
   OPENAI_API_KEY=your_openai_key_here
   SECRET_KEY=generate_random_secret_here
   CORS_ORIGINS=https://your-frontend.onrender.com
   ```

5. **Click "Create Web Service"** → Wait for deployment (~5 minutes)

6. **Copy the URL**: `https://your-backend.onrender.com`

### Deploy Frontend on Render

1. **Create Static Site**:
   - Click "New +" → "Static Site"
   - Connect same GitHub repo

2. **Configure Frontend**:
   - **Name**: `news-aggregation-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `.next`

3. **Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api
   ```
   (Use the backend URL from step 6 above)

4. **Click "Create Static Site"** → Wait for deployment

5. **Update Backend CORS**:
   - Go back to backend service
   - Update `CORS_ORIGINS` with your frontend URL: `https://your-frontend.onrender.com`
   - Redeploy backend

✅ **Done!** Your app is live at: `https://your-frontend.onrender.com`

---

## 🚀 Option 2: Railway (Full Stack on One Platform)

Railway can host both frontend and backend.

### Deploy Backend

1. Go to [railway.app](https://railway.app) → Sign up with GitHub
2. "New Project" → "Deploy from GitHub repo"
3. Select your repo
4. Add service → Select `backend` folder
5. Add environment variables:
   ```
   OPENAI_API_KEY=your_key
   SECRET_KEY=your_secret
   ```
6. Railway auto-deploys! Copy the URL

### Deploy Frontend

1. In same Railway project, "Add Service"
2. Select `frontend` folder
3. Railway auto-detects Next.js
4. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api
   ```
5. Deploy!

---

## 🌐 Option 3: Netlify (Frontend) + Railway (Backend)

### Frontend on Netlify

1. Go to [netlify.com](https://netlify.com) → Sign up
2. "Add new site" → "Import an existing project"
3. Connect GitHub → Select repo
4. Settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `.next`
5. Environment variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api
   ```
6. Deploy!

Backend: Use Railway (same as Option 2)

---

## 🐳 Option 4: Fly.io (Full Stack)

1. Install Fly CLI:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Login:
   ```bash
   fly auth login
   ```

3. Deploy Backend:
   ```bash
   cd backend
   fly launch
   ```

4. Deploy Frontend:
   ```bash
   cd frontend
   fly launch
   ```

---

## 📊 Comparison

| Platform | Ease | Cost | Best For |
|----------|------|------|----------|
| **Render** | ⭐⭐⭐⭐⭐ | Free tier | Easiest, all-in-one |
| **Railway** | ⭐⭐⭐⭐ | $5/month | Full stack, simple |
| **Netlify** | ⭐⭐⭐⭐ | Free tier | Frontend only |
| **Fly.io** | ⭐⭐⭐ | Free tier | More control |

---

## 🎯 My Recommendation: **Render**

**Why Render?**
- ✅ Easiest setup
- ✅ Free tier available
- ✅ Supports both frontend and backend
- ✅ No complex configuration
- ✅ Auto-deploys on git push
- ✅ Built-in PostgreSQL available

**Quick Start with Render:**
1. Sign up at render.com
2. Follow "Option 1" above
3. Done in ~10 minutes!

---

## 🔧 Need Help?

If you choose Render, I can guide you through each step in detail!

