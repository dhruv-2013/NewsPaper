# Vercel Deployment Troubleshooting

## Fixing 404 NOT_FOUND Error

### Step 1: Verify Vercel Project Settings

1. Go to your Vercel project dashboard
2. Click **Settings** → **General**
3. Verify these settings:
   - **Root Directory**: `frontend` (IMPORTANT!)
   - **Framework Preset**: Next.js (auto-detected)
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)

### Step 2: Check Environment Variables

1. Go to **Settings** → **Environment Variables**
2. Ensure you have:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app/api
   ```
   (Replace with your actual backend URL)

### Step 3: Redeploy

1. Go to **Deployments** tab
2. Click the **⋯** menu on the latest deployment
3. Select **Redeploy**
4. Or push a new commit to trigger auto-deployment

### Step 4: Check Build Logs

1. Click on the failed deployment
2. Check the **Build Logs** tab
3. Look for errors like:
   - Missing dependencies
   - Build failures
   - TypeScript errors

## Common Issues & Solutions

### Issue: "404 NOT_FOUND" after deployment

**Solution:**
- Verify Root Directory is set to `frontend`
- Ensure `app/page.tsx` exists
- Check that build completed successfully

### Issue: Build fails

**Solution:**
```bash
# Test build locally first
cd frontend
npm install
npm run build
```

If it works locally but fails on Vercel:
- Check Node.js version (should be 18+)
- Verify all dependencies are in package.json
- Check for missing environment variables

### Issue: API calls fail (CORS errors)

**Solution:**
1. Update backend CORS settings:
   ```python
   # In backend/app/main.py
   cors_origins = [
       "https://your-app.vercel.app",
       "http://localhost:3000"
   ]
   ```

2. Redeploy backend after updating CORS

### Issue: Page loads but shows errors

**Solution:**
1. Open browser console (F12)
2. Check for errors
3. Verify `NEXT_PUBLIC_API_URL` is set correctly
4. Ensure backend is accessible

## Quick Fix Checklist

- [ ] Root Directory = `frontend`
- [ ] `NEXT_PUBLIC_API_URL` environment variable set
- [ ] Build completes successfully (check logs)
- [ ] Backend is deployed and accessible
- [ ] CORS allows your Vercel domain

## Manual Redeploy

If auto-deploy isn't working:

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy from frontend directory
cd frontend
vercel --prod
```

## Still Having Issues?

1. **Check Vercel Logs**: Dashboard → Deployments → Click deployment → Logs
2. **Test Locally**: `npm run build` in frontend directory
3. **Verify Structure**: Ensure `app/page.tsx` exists
4. **Check GitHub**: Ensure code is pushed to main branch

## Expected File Structure

```
frontend/
├── app/
│   ├── page.tsx          ← Must exist
│   ├── layout.tsx         ← Must exist
│   └── ...
├── package.json
├── next.config.js
└── vercel.json
```

If your structure is different, Vercel might not detect it correctly.

