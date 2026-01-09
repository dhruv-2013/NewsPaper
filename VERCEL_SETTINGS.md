# Vercel Deployment Settings - Exact Configuration

## ✅ Correct Settings for Your Project

### Step 1: Project Settings

1. Go to your Vercel project dashboard
2. Click **Settings** → **General**

**Configure these settings:**

| Setting | Value | Notes |
|---------|-------|-------|
| **Framework Preset** | `Next.js` | Auto-detected, but verify |
| **Root Directory** | `frontend` | ⚠️ **CRITICAL - Must be set!** |
| **Build Command** | `npm run build` | Auto-detected |
| **Output Directory** | `.next` | Auto-detected |
| **Install Command** | `npm install` | Auto-detected |
| **Node.js Version** | `18.x` or `20.x` | Recommended |

### Step 2: Environment Variables

Go to **Settings** → **Environment Variables**

Add this variable:
```
NEXT_PUBLIC_API_URL = https://your-backend-url.railway.app/api
```

Replace `your-backend-url.railway.app` with your actual Railway backend URL.

### Step 3: Redeploy

1. Go to **Deployments** tab
2. Find your latest deployment
3. Click the **⋯** (three dots) menu
4. Select **Redeploy**
5. Wait for deployment to complete

## 🎯 Framework Preset: Next.js

**Answer: Framework should be `Next.js`**

Vercel will auto-detect this, but if you need to set it manually:
- Framework: **Next.js**
- Version: **14.x** (matches your package.json)

## 📋 Complete Checklist

Before redeploying, verify:

- [ ] **Root Directory** = `frontend` ✅
- [ ] **Framework Preset** = `Next.js` ✅
- [ ] **Build Command** = `npm run build` ✅
- [ ] **Output Directory** = `.next` ✅
- [ ] **NEXT_PUBLIC_API_URL** environment variable is set ✅
- [ ] Code is pushed to GitHub main branch ✅

## 🚀 Quick Redeploy Steps

1. **Update Settings** (if needed):
   - Settings → General → Root Directory = `frontend`

2. **Add Environment Variable** (if missing):
   - Settings → Environment Variables
   - Add `NEXT_PUBLIC_API_URL`

3. **Redeploy**:
   - Deployments → Latest deployment → ⋯ → Redeploy

4. **Wait** for build to complete (usually 1-2 minutes)

5. **Test** your deployed site!

## ⚠️ Common Mistakes

❌ **Wrong**: Root Directory = `.` or empty
✅ **Correct**: Root Directory = `frontend`

❌ **Wrong**: Framework = Other
✅ **Correct**: Framework = Next.js

❌ **Wrong**: Missing `NEXT_PUBLIC_API_URL`
✅ **Correct**: Environment variable set with backend URL

## 🔍 How to Verify Settings

After redeploying, check:
1. Build logs show "Build Completed"
2. No 404 errors
3. Site loads at your Vercel URL
4. API calls work (check browser console)

## Still Getting 404?

1. **Double-check Root Directory** = `frontend`
2. **Check build logs** for errors
3. **Verify** `app/page.tsx` exists in frontend folder
4. **Try manual deploy**:
   ```bash
   cd frontend
   npm install -g vercel
   vercel --prod
   ```

