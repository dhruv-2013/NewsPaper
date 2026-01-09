# Vercel Environment Variables Setup

## Required Environment Variables

For the Next.js API routes to work, you need to set the backend URL:

### Option 1: Use External Backend (Recommended)

Set this in Vercel:

```
BACKEND_URL=https://your-backend.onrender.com
```

Or:

```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api
```

The API routes will automatically proxy requests to your Python backend.

### Option 2: Local Development

For local development, the routes will automatically use:
- `http://localhost:8000` if no environment variable is set

## How to Set in Vercel

1. Go to **Vercel Dashboard**
2. Select your project
3. **Settings** → **Environment Variables**
4. Add:
   ```
   Key: BACKEND_URL
   Value: https://your-backend.onrender.com
   ```
5. Select: **Production**, **Preview**, **Development**
6. **Save**
7. **Redeploy** your project

## How It Works

The Next.js API routes (`/api/*`) act as a **proxy** to your Python backend:

- Frontend calls: `https://your-app.vercel.app/api/news/extract`
- Next.js route proxies to: `https://your-backend.onrender.com/api/news/extract`
- Backend processes and returns data
- Next.js route returns data to frontend

This way:
- ✅ No CORS issues (same origin)
- ✅ Backend logic stays in Python
- ✅ Works on Vercel
- ✅ Easy to maintain

## Troubleshooting

### Still getting 0 articles?

1. **Check BACKEND_URL is set** in Vercel
2. **Verify backend is running** - visit `https://your-backend.com/health`
3. **Check backend logs** for errors
4. **Redeploy frontend** after setting environment variable

### Backend connection failed?

- Verify `BACKEND_URL` is correct (no trailing slash)
- Check backend CORS allows Vercel domain
- Ensure backend is accessible from internet

