# Fix Network Error - Step by Step

## 🔴 Error You're Seeing

```
Network Error: ERR_BLOCKED_BY_CLIENT
POST http://localhost:8000/api/news/extract
```

## ✅ Solutions

### Solution 1: If Running Locally

**The backend must be running!**

1. **Start Backend**:
   ```bash
   cd backend
   source venv/bin/activate
   python run.py
   ```
   
2. **Verify Backend is Running**:
   - Open: http://localhost:8000/health
   - Should see: `{"status":"healthy"}`

3. **Start Frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

4. **Test**: Open http://localhost:3000

---

### Solution 2: If Deployed (Render/Vercel/etc)

**You MUST set the environment variable!**

#### For Frontend Deployment:

1. **Go to your deployment platform** (Render/Vercel)
2. **Settings** → **Environment Variables**
3. **Add**:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com/api
   ```
   (Replace with your actual backend URL)

4. **Redeploy** the frontend

#### Example URLs:
- Render backend: `https://news-backend.onrender.com/api`
- Railway backend: `https://your-app.railway.app/api`

---

### Solution 3: Check CORS Settings

**Backend must allow your frontend domain!**

1. **Go to Backend** (Railway/Render)
2. **Environment Variables**
3. **Update CORS_ORIGINS**:
   ```
   CORS_ORIGINS=https://your-frontend.onrender.com,http://localhost:3000
   ```
   (Add your frontend URL)

4. **Redeploy backend**

---

### Solution 4: Disable Ad Blockers

**Ad blockers can block localhost requests!**

1. **Disable ad blocker** for localhost
2. Or use a different browser
3. Or add localhost to whitelist

---

## 🔍 How to Check What's Wrong

### Step 1: Check Browser Console

1. Open browser DevTools (F12)
2. Go to **Console** tab
3. Look for error messages
4. Check what URL it's trying to connect to

### Step 2: Check Network Tab

1. DevTools → **Network** tab
2. Try extracting news again
3. Look for the failed request
4. Check:
   - What URL is being called?
   - What's the error code?
   - Is it a CORS error?

### Step 3: Verify Environment Variable

**In browser console, type:**
```javascript
console.log(process.env.NEXT_PUBLIC_API_URL)
```

**Should show your backend URL, not `undefined`!**

---

## 🎯 Quick Checklist

- [ ] Backend is running (if local) or deployed (if production)
- [ ] `NEXT_PUBLIC_API_URL` environment variable is set
- [ ] Backend URL is correct (ends with `/api`)
- [ ] CORS is configured to allow frontend domain
- [ ] No ad blockers blocking requests
- [ ] Backend is accessible (try opening backend URL in browser)

---

## 🚀 For Render Deployment

### Backend:
1. Deploy backend first
2. Copy backend URL: `https://news-backend.onrender.com`

### Frontend:
1. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://news-backend.onrender.com/api
   ```
2. Deploy frontend
3. Update backend CORS:
   ```
   CORS_ORIGINS=https://news-frontend.onrender.com
   ```

---

## 💡 Still Not Working?

1. **Check backend logs** in deployment platform
2. **Check frontend build logs**
3. **Verify backend URL** is accessible (open in browser)
4. **Test backend directly**: `https://your-backend.com/health`

The most common issue is **missing `NEXT_PUBLIC_API_URL` environment variable**!

