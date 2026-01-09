# SIMPLE Deployment - Step by Step (No Confusion!)

## 🎯 Let's Deploy on Render (Easiest Platform)

### Why Render?
- ✅ Actually works with monorepos (frontend + backend together)
- ✅ Free tier
- ✅ No confusing settings
- ✅ Step-by-step below

---

## 📋 STEP 1: Prepare Your Repo (Already Done ✅)

Your repo structure is correct:
```
NewsPaper/
├── backend/     ← Python/FastAPI
└── frontend/    ← Next.js
```

---

## 🚀 STEP 2: Deploy Backend First

### Go to Render.com

1. **Sign Up**: [render.com](https://render.com)
   - Click "Get Started for Free"
   - Sign up with **GitHub** (easiest)

2. **Create Web Service**:
   - Click the big **"New +"** button (top right)
   - Select **"Web Service"**

3. **Connect Repository**:
   - Click **"Connect account"** if not connected
   - Select **"dhruv-2013/NewsPaper"** from the list
   - Click **"Connect"**

4. **Configure Backend** - Fill in EXACTLY:

   ```
   Name: news-backend
   
   Region: Oregon (or closest to you)
   
   Branch: main
   
   Root Directory: backend          ← IMPORTANT!
   
   Runtime: Python 3
   
   Build Command: pip install -r requirements.txt
   
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Environment Variables** - Click "Advanced" → "Add Environment Variable":
   
   Add these ONE BY ONE:
   
   ```
   Key: OPENAI_API_KEY
   Value: your_openai_api_key_here
   ```
   (Use your actual OpenAI API key - don't commit it to GitHub!)
   
   ```
   Key: SECRET_KEY
   Value: any-random-string-here-12345
   ```
   
   ```
   Key: CORS_ORIGINS
   Value: https://news-frontend.onrender.com
   ```
   (We'll update this after frontend deploys)

6. **Click "Create Web Service"**
   - Wait 3-5 minutes
   - You'll see build logs
   - When done, copy the URL: `https://news-backend.onrender.com`

---

## 🎨 STEP 3: Deploy Frontend

1. **Still in Render Dashboard**:
   - Click **"New +"** again
   - Select **"Static Site"** (NOT Web Service!)

2. **Connect Same Repository**:
   - Select **"dhruv-2013/NewsPaper"** again

3. **Configure Frontend** - Fill in EXACTLY:

   ```
   Name: news-frontend
   
   Branch: main
   
   Root Directory: frontend         ← IMPORTANT!
   
   Build Command: npm install && npm run build
   
   Publish Directory: .next
   ```

4. **Environment Variables**:
   
   ```
   Key: NEXT_PUBLIC_API_URL
   Value: https://news-backend.onrender.com/api
   ```
   (Use the backend URL from Step 2)

5. **Click "Create Static Site"**
   - Wait 2-3 minutes
   - Copy frontend URL: `https://news-frontend.onrender.com`

---

## 🔧 STEP 4: Update CORS

1. Go back to **Backend Service** (news-backend)
2. Click **"Environment"** tab
3. Find `CORS_ORIGINS`
4. Click **"Edit"**
5. Change value to: `https://news-frontend.onrender.com`
6. Render will auto-redeploy

---

## ✅ DONE!

Your app is live:
- **Frontend**: `https://news-frontend.onrender.com`
- **Backend**: `https://news-backend.onrender.com`

---

## 🆘 If Something Goes Wrong

### Backend won't build?
- Check Root Directory = `backend` (not `.` or empty)
- Check Build Command = `pip install -r requirements.txt`
- Check Start Command = `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend won't build?
- Check Root Directory = `frontend` (not `.` or empty)
- Check Build Command = `npm install && npm run build`
- Check Publish Directory = `.next`

### Can't find repository?
- Make sure you connected GitHub account
- Make sure repo is public (or you gave Render access)
- Try refreshing the page

### Still stuck?
1. Check the build logs in Render dashboard
2. Look for red error messages
3. Copy the error and I can help fix it!

---

## 📸 Visual Guide

When you click "New +" → "Web Service", you'll see:

```
┌─────────────────────────────────┐
│ Repository: [Select: NewsPaper] │
│ Branch: main                    │
│ Root Directory: backend  ← SET! │
│ Runtime: Python 3               │
│ Build: pip install...           │
│ Start: uvicorn app.main...      │
└─────────────────────────────────┘
```

**The key is Root Directory!** Make sure it says `backend` or `frontend`, not empty!

---

## 🎉 That's It!

Follow these steps exactly and it WILL work. Render is much simpler than Vercel for this setup!

