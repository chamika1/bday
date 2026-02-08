# Deploy Birthday Reminder to Google Cloud Run

This guide will help you deploy the Birthday Reminder application to Google Cloud Run **for FREE** (within free tier limits).

## Why Google Cloud Run?

✅ **Generous Free Tier**: 2 million requests per month FREE  
✅ **Pay Only When Used**: Scales to zero when idle (no charges)  
✅ **Easy Deployment**: Simple container deployment  
✅ **Automatic HTTPS**: Free SSL certificates  
✅ **Auto-scaling**: Handles traffic automatically  

## Free Tier Limits (as of 2024)

- 2 million requests per month
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds
- This is MORE than enough for a personal birthday reminder app!

## Prerequisites

1. **Google Cloud Account**
   - Sign up at https://cloud.google.com/
   - New users get $300 free credit for 90 days
   - No charges within free tier limits

2. **Install Google Cloud SDK**
   - Download from: https://cloud.google.com/sdk/docs/install
   - Or use Google Cloud Shell (browser-based, no installation needed)

## Deployment Steps

### Step 1: Set Up Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Create a new project (replace PROJECT_ID with your choice)
gcloud projects create birthday-reminder-app --name="Birthday Reminder"

# Set the project
gcloud config set project birthday-reminder-app

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 2: Deploy to Cloud Run

```bash
# Navigate to your project directory
cd c:\Users\USER\Desktop\birthday

# Deploy the application (choose a region close to you)
# Asia regions: asia-south1 (Mumbai), asia-southeast1 (Singapore)
gcloud run deploy birthday-reminder \
  --source . \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --min-instances 0

# Note: --min-instances 0 means it scales to zero when not used (FREE!)
```

### Step 3: Access Your Application

After deployment completes, you'll get a URL like:
```
https://birthday-reminder-xxxxxxxxx-xx.a.run.app
```

Your app is now live! 🎉

## Cost Optimization Tips

### 1. **Minimize Instance Count**
```bash
# Always use min-instances=0 for free tier
gcloud run services update birthday-reminder \
  --min-instances 0 \
  --region asia-south1
```

### 2. **Reduce Memory Usage**
```bash
# Use minimum memory (saves costs)
gcloud run services update birthday-reminder \
  --memory 512Mi \
  --region asia-south1
```

### 3. **Set Request Timeout**
```bash
# Reduce timeout to avoid long-running requests
gcloud run services update birthday-reminder \
  --timeout 60s \
  --region asia-south1
```

### 4. **Monitor Usage**
```bash
# Check your usage to stay within free tier
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

## Alternative: Deploy via Google Cloud Console (No Command Line)

1. Go to https://console.cloud.google.com/run
2. Click "CREATE SERVICE"
3. Select "Continuously deploy from a repository"
4. Connect your GitHub repository (or upload code)
5. Configure:
   - Region: asia-south1 (Mumbai) or closest to you
   - Authentication: Allow unauthenticated invocations
   - Container: Auto-build from source
   - Memory: 512 MiB
   - CPU: 1
   - Min instances: 0 (important for free tier!)
   - Max instances: 10
6. Click "CREATE"

## Important Notes

### Data Persistence

⚠️ **Cloud Run uses ephemeral storage** - data in JSON files will be lost when the container restarts.

**Solutions:**

1. **Firebase (Recommended for Free Tier)**
   ```bash
   # Free tier: 1GB storage, 50K reads/day, 20K writes/day
   # Perfect for this app!
   ```

2. **Google Cloud Storage** (Alternative)
   ```bash
   # Free tier: 5GB storage
   ```

3. **Keep JSON files** (Simple option)
   - Works fine if you don't mind occasional data resets
   - For personal use with daily backups

### Session Management

The current app uses Flask sessions. For production:
- Sessions will persist as long as the container is alive
- Users may need to re-login if container restarts
- This is acceptable for a personal birthday reminder

## Updating Your Deployment

```bash
# Make changes to your code, then re-deploy:
gcloud run deploy birthday-reminder \
  --source . \
  --region asia-south1
```

## Custom Domain (Optional)

```bash
# Add your own domain (e.g., birthdays.yourdomain.com)
gcloud run domain-mappings create \
  --service birthday-reminder \
  --domain birthdays.yourdomain.com \
  --region asia-south1
```

## Monitoring Costs

### Check Your Usage
```bash
# View service details
gcloud run services describe birthday-reminder --region asia-south1

# Check logs
gcloud run logs read birthday-reminder --region asia-south1
```

### Set Budget Alerts
1. Go to https://console.cloud.google.com/billing/budgets
2. Create a budget alert for $1
3. Get notified if you exceed free tier

## Estimated Costs (if you exceed free tier)

- **Requests**: $0.40 per million requests (after free 2M)
- **Memory**: $0.0000025 per GB-second (after free tier)
- **For typical usage**: $0 - $0.50 per month

## Delete the Service (if needed)

```bash
# Stop all charges
gcloud run services delete birthday-reminder --region asia-south1
```

## Troubleshooting

### Build Fails
```bash
# Check build logs
gcloud builds list
gcloud builds log [BUILD-ID]
```

### Service Not Starting
```bash
# Check service logs
gcloud run logs read birthday-reminder --region asia-south1 --limit 50
```

### Out of Memory
```bash
# Increase memory
gcloud run services update birthday-reminder \
  --memory 1Gi \
  --region asia-south1
```

## Support

- Google Cloud Run Docs: https://cloud.google.com/run/docs
- Pricing Calculator: https://cloud.google.com/products/calculator
- Free Tier Details: https://cloud.google.com/free

---

**🎉 Your birthday reminder app will be FREE to run within the generous Google Cloud Run free tier limits!**
