# Fix Vercel Deployment - 405 Error

## 🔴 The Problem

Your frontend on Vercel is trying to call:
```
https://news-paper-bice.vercel.app/api/news/extract
```

But Vercel only hosts your **frontend**, not your **backend**!

## ✅ The Solution

You need to:
1. **Deploy the backend** separately (Render, Railway, etc.)
2. **Point frontend to backend URL** via environment variable

---

## 🚀 Step-by-Step Fix

### Step 1: Deploy Backend (Choose One)

#### Option A: Render (Easiest)

1. Go to [render.com](https://render.com) → Sign up
2. **New +** → **Web Service**
3. Connect GitHub → Select `NewsPaper` repo
4. Settings:
   ```
   Name: news-backend
   Root Directory: backend
   Runtime: Python 3
   Build: pip install -r requirements.txt
   Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
5. Environment Variables:
   ```
   OPENAI_API_KEY=your_key_here
   SECRET_KEY=any_random_string
   CORS_ORIGINS=https://news-paper-bice.vercel.app
   ```
6. Deploy → Copy URL: `https://news-backend.onrender.com`

#### Option B: Railway

1. Go to [railway.app](https://railway.app) → Sign up
2. **New Project** → **Deploy from GitHub**
3. Select repo → Add service → Select `backend` folder
4. Add environment variables (same as above)
5. Deploy → Copy URL

---

### Step 2: Update Vercel Environment Variable

1. Go to **Vercel Dashboard**
2. Select your project: `news-paper-bice`
3. Go to **Settings** → **Environment Variables**
4. **Add/Edit**:
   ```
   Key: NEXT_PUBLIC_API_URL
   Value: https://news-backend.onrender.com/api
   ```
   (Use your actual backend URL from Step 1)

5. **Important**: Select **Production**, **Preview**, and **Development**
6. **Save**

---

### Step 3: Redeploy Frontend

1. In Vercel Dashboard → **Deployments**
2. Click **⋯** on latest deployment
3. Select **Redeploy**
4. Wait for deployment to complete

---

### Step 4: Update Backend CORS

1. Go to your **Backend** (Render/Railway)
2. **Environment Variables**
3. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://news-paper-bice.vercel.app
   ```
4. Backend will auto-redeploy

---

## ✅ Verify It Works

1. Open your Vercel site: `https://news-paper-bice.vercel.app`
2. Open browser console (F12)
3. Type:
   ```javascript
   console.log(process.env.NEXT_PUBLIC_API_URL)
   ```
4. Should show: `https://news-backend.onrender.com/api` (your backend URL)
5. Try extracting news - should work now!

---

## 🎯 Quick Checklist

- [ ] Backend deployed (Render/Railway)
- [ ] Backend URL copied (e.g., `https://news-backend.onrender.com`)
- [ ] `NEXT_PUBLIC_API_URL` set in Vercel = `https://your-backend.com/api`
- [ ] Frontend redeployed on Vercel
- [ ] `CORS_ORIGINS` in backend includes Vercel URL
- [ ] Backend redeployed

---

## 🔍 How to Check Backend URL

Your backend URL should:
- ✅ Start with `https://`
- ✅ End with `/api` (for NEXT_PUBLIC_API_URL)
- ✅ Be accessible (try opening in browser)
- ✅ Show `{"status":"healthy"}` at `/health` endpoint

Example:
- Backend: `https://news-backend.onrender.com`
- API URL: `https://news-backend.onrender.com/api`
- Health: `https://news-backend.onrender.com/health`

---

## 💡 Why This Happened

Vercel is a **frontend hosting platform**. It can't run Python/FastAPI backends.

Your setup needs:
- **Frontend** → Vercel (Next.js)
- **Backend** → Render/Railway (FastAPI)

The frontend calls the backend via `NEXT_PUBLIC_API_URL`.

---

## 🆘 Still Not Working?

1. **Check browser console** - What URL is it trying to call?
2. **Check Vercel environment variables** - Is `NEXT_PUBLIC_API_URL` set?
3. **Check backend logs** - Is backend receiving requests?
4. **Test backend directly** - Can you access `https://your-backend.com/health`?

The most common issue is **forgetting to set `NEXT_PUBLIC_API_URL` in Vercel**!

