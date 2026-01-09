# Vercel Setup - Connect Your Backend

## ✅ Your Backend is Deployed!

**Backend URL**: `https://newspaper-7e3o.onrender.com`

## 🔧 Step 1: Set Environment Variable in Vercel

1. Go to **[Vercel Dashboard](https://vercel.com/dashboard)**
2. Select your project: **news-paper-bice** (or your project name)
3. Click **Settings** → **Environment Variables**
4. Click **Add New**
5. Add this variable:

   ```
   Key: BACKEND_URL
   Value: https://newspaper-7e3o.onrender.com
   ```

6. **Important**: Select all three checkboxes:
   - ✅ Production
   - ✅ Preview  
   - ✅ Development

7. Click **Save**

## 🔄 Step 2: Redeploy Frontend

1. Go to **Deployments** tab
2. Find the latest deployment
3. Click the **⋯** (three dots) menu
4. Select **Redeploy**
5. Wait for deployment to complete (~1-2 minutes)

## ✅ Step 3: Verify It Works

1. **Test Backend**: Open `https://newspaper-7e3o.onrender.com/health`
   - Should show: `{"status":"healthy"}`

2. **Test Frontend**: Go to your Vercel site
   - Click **"Extract News"**
   - Should work now! 🎉

## 🔍 Troubleshooting

### Still getting 503 error?

1. **Check BACKEND_URL is set**:
   - Vercel → Settings → Environment Variables
   - Verify `BACKEND_URL` = `https://newspaper-7e3o.onrender.com`

2. **Verify backend is running**:
   - Open: `https://newspaper-7e3o.onrender.com/health`
   - Should return: `{"status":"healthy"}`

3. **Check backend logs**:
   - Go to Render dashboard
   - Check logs for any errors

4. **Redeploy frontend**:
   - After setting environment variable, you MUST redeploy

### Backend is slow?

- First request after sleep takes ~30 seconds (free tier)
- This is normal for Render free tier
- Subsequent requests are faster

## 🎯 Your Setup

- **Frontend**: `https://news-paper-bice.vercel.app` (Vercel)
- **Backend**: `https://newspaper-7e3o.onrender.com` (Render)
- **Status**: ✅ Backend deployed, needs Vercel configuration

## 📝 Quick Checklist

- [ ] `BACKEND_URL` set in Vercel = `https://newspaper-7e3o.onrender.com`
- [ ] Environment variable selected for Production, Preview, Development
- [ ] Frontend redeployed after setting variable
- [ ] Backend health check works: `/health` endpoint
- [ ] Test news extraction on frontend

## 🎉 Once Complete

Your app will be fully functional:
- ✅ News extraction
- ✅ Highlights display
- ✅ Chatbot
- ✅ All features working!

