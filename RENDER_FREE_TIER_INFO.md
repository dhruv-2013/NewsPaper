# Render Free Tier - Important Information

## ⚠️ Free Tier Limitations

### Cold Start / Spin Down

**Render free tier services automatically spin down after 15 minutes of inactivity.**

This means:
- ✅ First request after inactivity: **30-60 second delay** (backend waking up)
- ✅ Subsequent requests: Fast (backend is awake)
- ✅ After 15 min of no requests: Backend goes to sleep again

### This is Normal!

**502/503 errors on first request are expected** when:
- Backend just woke up from sleep
- Service is starting for the first time
- No requests for 15+ minutes

## 🔧 How to Handle

### Option 1: Wait and Retry (Free)

1. Get a 502/503 error? **Wait 30-60 seconds**
2. **Try again** - backend should be awake now
3. Subsequent requests will be fast

### Option 2: Keep Backend Awake (Pro)

Upgrade to paid plan ($7/month) to:
- ✅ No spin downs
- ✅ Always-on service
- ✅ Faster response times

### Option 3: Use Keep-Alive Service

Use a service like [UptimeRobot](https://uptimerobot.com) (free) to ping your backend every 5 minutes to keep it awake.

## 🎯 Best Practices

1. **First Request**: Expect 30-60 second delay
2. **Show Loading State**: Let users know it's processing
3. **Retry Logic**: Automatically retry after timeout
4. **Error Messages**: Inform users about cold start

## 📊 Typical Timeline

```
Request 1 (after sleep): 0s → [50s wake up] → [10s process] → Response (60s total)
Request 2 (awake):      0s → [2s process] → Response (2s total)
Request 3 (awake):      0s → [2s process] → Response (2s total)
... (15 min of inactivity)
Request N (after sleep): 0s → [50s wake up] → Response
```

## ✅ Solutions Implemented

- Increased timeout to 3 minutes for news extraction
- Better error handling for 502/503 errors
- Graceful fallbacks when backend is unavailable
- User-friendly error messages

## 💡 Pro Tip

For production use, consider:
- Paid Render plan ($7/month) for always-on
- Or use Railway ($5/month) - better free tier
- Or use UptimeRobot to ping backend every 5 min (free)

