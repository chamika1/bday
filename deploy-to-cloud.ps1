# Quick Deployment Script for Google Cloud Run
# Run this script to deploy your Birthday Reminder app

Write-Host "🎂 Birthday Reminder - Google Cloud Run Deployment" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Generate unique project ID
$randomNum = Get-Random -Maximum 99999
$projectId = "birthday-reminder-$randomNum"

Write-Host "Step 1: Creating Google Cloud Project..." -ForegroundColor Yellow
Write-Host "Project ID: $projectId" -ForegroundColor Green
Write-Host ""

# Create project
gcloud projects create $projectId --name="Birthday Reminder"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Project created successfully!" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Step 2: Setting active project..." -ForegroundColor Yellow
    gcloud config set project $projectId
    
    Write-Host ""
    Write-Host "Step 3: Enabling required APIs..." -ForegroundColor Yellow
    gcloud services enable run.googleapis.com
    gcloud services enable cloudbuild.googleapis.com
    
    Write-Host ""
    Write-Host "Step 4: Deploying to Cloud Run..." -ForegroundColor Yellow
    Write-Host "This will take a few minutes..." -ForegroundColor Gray
    Write-Host ""
    
    gcloud run deploy birthday-reminder `
      --source . `
      --platform managed `
      --region asia-south1 `
      --allow-unauthenticated `
      --memory 512Mi `
      --cpu 1 `
      --max-instances 10 `
      --min-instances 0
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 Deployment Successful!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your app is now live! Check the URL above." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "💡 Tips:" -ForegroundColor Yellow
        Write-Host "- Min instances = 0 means FREE when not in use" -ForegroundColor Gray
        Write-Host "- You get 2 million requests/month FREE" -ForegroundColor Gray
        Write-Host "- App auto-scales when needed" -ForegroundColor Gray
    }
} else {
    Write-Host ""
    Write-Host "❌ Project creation failed. Please try again or use a different project ID." -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Try this command manually:" -ForegroundColor Yellow
    Write-Host "gcloud projects create birthday-reminder-YOUR-NUMBER --name=`"Birthday Reminder`"" -ForegroundColor Gray
}
