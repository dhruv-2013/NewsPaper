# Simple Deployment Guide

## Backend (Render)

Your backend is already deployed on Render. No changes needed.

## Frontend (Vercel) - Simple Setup

### Quick Steps

1. **Go to [vercel.com](https://vercel.com)** and sign in with GitHub

2. **Import Project**:
   - Click "Add New Project"
   - Select repository: `dhruv-2013/NewsPaper`
   - Set **Root Directory** to: `frontend`

3. **Add Environment Variable**:
   - Go to Project Settings → Environment Variables
   - Add: `BACKEND_URL` = `https://your-render-backend-url.onrender.com`
   - Replace with your actual Render backend URL

4. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete
   - Your app will be live automatically!

### That's it!

Vercel will auto-detect Next.js and build automatically. No extra configuration needed.

## Notes

- Vercel auto-deploys on every Git push
- Backend URL should be your Render service URL (e.g., `https://newspaper-7e3o.onrender.com`)
- No build commands needed - Vercel handles everything

