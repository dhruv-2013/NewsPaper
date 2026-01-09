# Deploy Backend in 5 Minutes - Quick Guide

## 🚀 Fastest Way: Render (5 minutes)

### Step 1: Sign Up & Create Service

1. Go to **[render.com](https://render.com)** → Sign up with GitHub (free)

2. Click **"New +"** → **"Web Service"**

3. **Connect Repository**:
   - Select **"dhruv-2013/NewsPaper"**
   - Click **"Connect"**

### Step 2: Configure Backend

Fill in these **EXACT** settings:

```
Name: news-backend

Region: Oregon (or closest)

Branch: main

Root Directory: backend          ← IMPORTANT!

Runtime: Python 3

Build Command: pip install -r requirements.txt

Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Step 3: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these **ONE BY ONE**:

```
Key: OPENAI_API_KEY
Value: your_openai_api_key_here
```
(Use your actual OpenAI API key - don't commit it to GitHub!)

```
Key: SECRET_KEY
Value: any-random-string-12345
```

```
Key: CORS_ORIGINS
Value: https://news-paper-bice.vercel.app
```

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. **Copy the URL**: `https://news-backend.onrender.com` (or similar)

### Step 5: Update Vercel

1. Go to **Vercel Dashboard**
2. Your project → **Settings** → **Environment Variables**
3. Add:
   ```
   Key: BACKEND_URL
   Value: https://news-backend.onrender.com
   ```
   (Use your actual Render URL from Step 4)

4. **Select**: Production, Preview, Development
5. **Save**
6. **Redeploy** frontend

---

## ✅ Done!

Your backend is now deployed and connected!

---

## 🔍 Verify It Works

1. **Test Backend**: Open `https://news-backend.onrender.com/health`
   - Should show: `{"status":"healthy"}`

2. **Test Frontend**: Go to your Vercel site
   - Click "Extract News"
   - Should work now!

---

## 🆘 Troubleshooting

### Backend won't build?

- Check Root Directory = `backend` (not empty!)
- Check Build Command = `pip install -r requirements.txt`
- Check Start Command = `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Still getting 503?

1. Verify `BACKEND_URL` is set in Vercel
2. Check backend URL is accessible (open in browser)
3. Redeploy frontend after setting environment variable
4. Check backend logs in Render dashboard

### Backend is slow?

- First request can take 30-60 seconds (cold start)
- Subsequent requests are faster
- This is normal for free tier

---

## 💡 Pro Tips

- **Free tier** on Render includes 750 hours/month
- Backend auto-sleeps after 15 min of inactivity (free tier)
- First request after sleep takes ~30 seconds to wake up
- This is normal and expected!

---

## 🎯 Next Steps

Once backend is deployed:
1. ✅ Set `BACKEND_URL` in Vercel
2. ✅ Redeploy frontend
3. ✅ Test news extraction
4. ✅ Enjoy your working app!

