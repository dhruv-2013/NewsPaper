# Deploy to Render - Step by Step Guide

## 🚀 Quick Deploy (5 minutes)

### Method 1: Using render.yaml (Easiest!)

1. **Sign up**: [render.com](https://render.com) → Sign up with GitHub

2. **Create Blueprint**:
   - Click "New +" → "Blueprint"
   - Connect your GitHub repo
   - Select `NewsPaper` repository
   - Render will detect `render.yaml` automatically!

3. **Add Environment Variable**:
   - In the backend service, add:
     ```
     OPENAI_API_KEY=your_openai_key_here
     ```

4. **Click "Apply"** → Render deploys both services automatically!

5. **Done!** Your app will be live in ~5 minutes.

---

### Method 2: Manual Setup (More Control)

#### Step 1: Deploy Backend

1. Go to [render.com](https://render.com) → Sign up

2. **New Web Service**:
   - Click "New +" → "Web Service"
   - Connect GitHub → Select `NewsPaper` repo

3. **Settings**:
   ```
   Name: news-aggregation-backend
   Region: Oregon (or closest to you)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Environment Variables**:
   ```
   OPENAI_API_KEY=sk-proj-... (your key)
   SECRET_KEY=any_random_string_here
   CORS_ORIGINS=https://news-aggregation-frontend.onrender.com
   ```
   (We'll update CORS_ORIGINS after frontend is deployed)

5. **Click "Create Web Service"**
   - Wait ~3-5 minutes for deployment
   - Copy the URL: `https://news-aggregation-backend.onrender.com`

#### Step 2: Deploy Frontend

1. **New Static Site**:
   - Click "New +" → "Static Site"
   - Connect same GitHub repo

2. **Settings**:
   ```
   Name: news-aggregation-frontend
   Branch: main
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: .next
   ```

3. **Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL=https://news-aggregation-backend.onrender.com/api
   ```
   (Use your backend URL from Step 1)

4. **Click "Create Static Site"**
   - Wait ~2-3 minutes
   - Copy frontend URL: `https://news-aggregation-frontend.onrender.com`

#### Step 3: Update CORS

1. Go back to **Backend Service** → **Environment**
2. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://news-aggregation-frontend.onrender.com
   ```
3. Render will auto-redeploy

#### ✅ Done!

Your app is live:
- Frontend: `https://news-aggregation-frontend.onrender.com`
- Backend: `https://news-aggregation-backend.onrender.com`

---

## 🔧 Troubleshooting

### Build Fails?

1. Check build logs in Render dashboard
2. Verify Root Directory is correct (`backend` or `frontend`)
3. Ensure all dependencies are in requirements.txt / package.json

### 404 Errors?

1. Verify Root Directory is set correctly
2. Check that build completed successfully
3. Ensure `app/page.tsx` exists in frontend

### API Not Working?

1. Verify `NEXT_PUBLIC_API_URL` is set correctly
2. Check backend is running (visit backend URL)
3. Update CORS_ORIGINS with frontend URL

---

## 💰 Pricing

**Free Tier Includes:**
- 750 hours/month (enough for 24/7)
- 100GB bandwidth
- Automatic SSL
- Custom domains

**Paid Plans Start at:** $7/month (if you exceed free tier)

---

## 🎯 Why Render?

- ✅ **Easiest deployment** - No complex config
- ✅ **Free tier** - Perfect for personal projects
- ✅ **Auto-deploy** - Deploys on every git push
- ✅ **Built-in SSL** - HTTPS automatically
- ✅ **One platform** - Frontend + Backend together
- ✅ **Great docs** - Excellent documentation

---

## 📝 Next Steps

1. Sign up at render.com
2. Follow Method 1 (Blueprint) for easiest setup
3. Add your OpenAI API key
4. Wait 5 minutes
5. Your app is live! 🎉

