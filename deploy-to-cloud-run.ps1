# Google Cloud Run Deployment Script
# Run this in PowerShell

Write-Host "🚀 Deploying Birthday App to Google Cloud Run..." -ForegroundColor Cyan
Write-Host ""

# Configuration
$PROJECT_ID = "bdays-28160"
$SERVICE_NAME = "birthday-app"
$REGION = "asia-south1"
$IMGBB_API_KEY = "61e3d87e49e4158a72f7254e5159b4d0"
$SECRET_KEY = "production-secret-key-$(Get-Random -Maximum 99999)"

Write-Host "📋 Configuration:" -ForegroundColor Yellow
Write-Host "  Project ID: $PROJECT_ID"
Write-Host "  Service Name: $SERVICE_NAME"
Write-Host "  Region: $REGION"
Write-Host ""

# Set the project
Write-Host "🔧 Setting GCloud project..." -ForegroundColor Cyan
gcloud config set project $PROJECT_ID

# Deploy to Cloud Run
Write-Host ""
Write-Host "🚢 Deploying to Cloud Run..." -ForegroundColor Cyan
Write-Host "  This will take a few minutes..." -ForegroundColor Yellow
Write-Host ""

gcloud run deploy $SERVICE_NAME `
  --source . `
  --region $REGION `
  --allow-unauthenticated `
  --platform managed `
  --memory 512Mi `
  --set-env-vars="SECRET_KEY=$SECRET_KEY,IMGBB_API_KEY=$IMGBB_API_KEY" `
  --timeout=300

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Your app is now live at:" -ForegroundColor Cyan
    gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"
    Write-Host ""
    Write-Host "📝 Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Open the URL above in your browser"
    Write-Host "  2. Create an account with email/password"
    Write-Host "  3. Add birthdays with photos"
    Write-Host "  4. Data persists in Firestore - no more data loss!"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    Write-Host "  Check the error messages above" -ForegroundColor Yellow
    Write-Host ""
}
