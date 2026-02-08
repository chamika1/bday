# Firestore Setup Guide for Google Cloud Run

## මේ Setup කරන්න Steps

### 1. Firebase Project එකක් Create කරන්න

1. **Firebase Console** එකට යන්න: https://console.firebase.google.com/
2. **"Add project"** click කරන්න
3. Project name එකක් දෙන්න (උදා: `birthday-app`)
4. Google Analytics disable කරන්න (optional)
5. **"Create project"** click කරන්න

### 2. Firestore Database එක Enable කරන්න

1. Firebase project එකේ **"Build"** section එකට යන්න
2. **"Firestore Database"** select කරන්න
3. **"Create database"** click කරන්න
4. **"Start in production mode"** select කරන්න
5. Location එක select කරන්න (Asia South1 - Mumbai recommended)
6. **"Enable"** click කරන්න

### 3. Security Rules සකසන්න (Optional - For Development)

Firestore Rules tab එකේ මේ rules දාන්න:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users collection - authenticated users can read/write their own data
    match /users/{userId} {
      allow read, write: if true;
    }
    
    // Birthdays collection - users can only access their own birthdays
    match /birthdays/{birthdayId} {
      allow read, write: if true;
    }
  }
}
```

**🔴 Note**: මේ rules තියෙන්නේ development එකට විතරයි. Production එකට වෙන rules දාන්න.

### 4. Service Account Key Generate කරන්න

#### Method 1: Firebase Console (Recommended)

1. Firebase Console එකේ **Settings (⚙️)** > **Project settings** යන්න
2. **"Service accounts"** tab එකට යන්න
3. **"Generate new private key"** click කරන්න
4. **"Generate key"** confirm කරන්න
5. JSON file එක download වෙනවා (මේක safe place එකක save කරන්න!)

#### Method 2: Google Cloud Console

1. https://console.cloud.google.com/ යන්න
2. ඔයාගේ project එක select කරන්න
3. **"IAM & Admin"** > **"Service Accounts"** යන්න
4. **"Create Service Account"** click කරන්න
5. Name එකක් දෙන්න (උදා: `birthday-app-service`)
6. **"Create and Continue"** click කරන්න
7. Role එකක් select කරන්න: **"Cloud Datastore User"** හෝ **"Firebase Admin"**
8. **"Done"** click කරන්න
9. Service account එකේ **Actions** menu එකේ **"Manage keys"** click කරන්න
10. **"Add Key"** > **"Create new key"** > **"JSON"** select කරන්න
11. JSON file එක download වෙනවා

### 5. Local Testing (Optional)

#### Service Account Key Use කරලා Test කරන්න:

1. Download කරපු JSON file එක project folder එකට copy කරන්න
2. File name එක rename කරන්න: `serviceAccountKey.json`
3. `.gitignore` file එකේ add කරන්න (security එකට):

```
serviceAccountKey.json
```

4. Environment variable එක set කරන්න PowerShell එකේ:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="c:\Users\USER\Desktop\birthday\serviceAccountKey.json"
```

5. App එක run කරන්න:

```powershell
python app.py
```

### 6. Google Cloud Run එකට Deploy කරන්න

#### Secret Manager එකේ Service Account Key දාන්න:

1. Google Cloud Console එකට යන්න: https://console.cloud.google.com/
2. **"Security"** > **"Secret Manager"** යන්න
3. **"Create Secret"** click කරන්න
4. Name: `firebase-credentials`
5. Secret value: serviceAccountKey.json file එකේ **සම්පූර්ණ content** එක paste කරන්න
6. **"Create Secret"** click කරන්න

#### Deploy කරන විට:

**Option A: Secret Manager Use කරලා (Recommended)**

```powershell
gcloud run deploy birthday-app `
  --source . `
  --region asia-south1 `
  --allow-unauthenticated `
  --set-secrets="GOOGLE_APPLICATION_CREDENTIALS=/secrets/firebase-creds:firebase-credentials:latest"
```

**Option B: Default Credentials Use කරලා (Simpler)**

Cloud Run automatically use කරයි default service account එක. මේකට විශේෂ config එකක් අවශ්‍ය නෑ.

```powershell
gcloud run deploy birthday-app `
  --source . `
  --region asia-south1 `
  --allow-unauthenticated
```

මේ විදිහට කරොත්:
- Cloud Run automatically use කරයි default compute service account එක
- Firestore permissions automatically තියෙනවා same project එකේ නම්

### 7. Verify Deployment

1. Cloud Run URL එකට යන්න
2. Account එකක් create කරන්න username සහ password සමග
3. Birthday එකක් add කරන්න
4. Browser එක refresh කරන්න - data තවමත් තියෙනවා නම් success! 🎉

## Firestore Data Structure

### Collections:

#### `users` collection:
```
users/
  ├── {username}/
      ├── username: "john_doe"
      ├── password: "hashed_password"
      └── created_at: timestamp
```

#### `birthdays` collection:
```
birthdays/
  ├── {auto_generated_id}/
      ├── username: "john_doe"
      ├── name: "Sarah"
      ├── relationship: "Sister"
      ├── bdate: "1995-05-15"
      ├── image: "https://imgbb.com/..."
      ├── memo: "Loves chocolate cake"
      └── created_at: timestamp
```

## Important Environment Variables

App එකට අවශ්‍ය environment variables:

1. **`GOOGLE_APPLICATION_CREDENTIALS`** (Optional for Cloud Run)
   - Local testing එකට පමණයි
   - Service account JSON file එකේ path එක

2. **`IMGBB_API_KEY`** (Required)
   - ImgBB API key එක image uploads එකට

3. **`SECRET_KEY`** (Optional but Recommended)
   - Flask session encryption එකට

Cloud Run එකේ set කරන්න:

```powershell
gcloud run services update birthday-app `
  --region asia-south1 `
  --set-env-vars="SECRET_KEY=your-super-secret-key-here,IMGBB_API_KEY=your-imgbb-api-key"
```

## Troubleshooting

### Error: "Could not automatically determine credentials"

**Solution**: 
1. Service account key එක correctly setup කරලා තියෙනවද check කරන්න
2. `GOOGLE_APPLICATION_CREDENTIALS` environment variable එක correctly set කරලා තියෙනවද check කරන්න

### Error: "Permission denied"

**Solution**:
1. Firestore database එක enabled කරලා තියෙනවද check කරන්න
2. Service account එකට correct permissions තියෙනවද check කරන්න (Cloud Datastore User role)

### Data Reset වෙනවා නම්

**Solution**:
- මේ guide එක follow කරලා Firestore correctly setup කරලා තියෙනවද verify කරන්න
- App එකේ logs check කරන්න Firestore connection errors තියෙනවද කියලා

## මොනවද වෙන Updates?

✅ **JSON files වෙනුවට Firestore** - persistent storage
✅ **Password authentication** - secure login
✅ **Hashed passwords** - security
✅ **No more data loss** - cloud database

## Data නැති වෙන්නේ නෑ කියලා Test කරන්නේ කොහොමද?

1. Account එකක් create කරන්න
2. Birthday එකක් add කරන්න  
3. Browser එක close කරන්න
4. පස්සේ ආයේ login වෙන්න
5. දැන් birthdays තවමත් තියෙනවා! ✨
