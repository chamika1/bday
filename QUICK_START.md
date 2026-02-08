# 🚀 Quick Start Guide - Firebase Authentication

## සියලු Updates Done! ✅

### මොනවද වෙනස් වුණේ:

1. ✅ **Firebase Authentication** - Email/Password authentication using Firebase Auth
2. ✅ **Firestore Database** - Persistent cloud storage
3. ✅ **No More Data Loss** - Container restarts won't affect data
4. ✅ **Better Security** - Firebase handles all authentication

---

## 🔥 Local Testing කරන්න කොහොමද:

### Step 1: Environment Variables Set කරන්න

PowerShell එකේ මේ commands run කරන්න:

```powershell
# ඔයාගේ service account key file එක point කරන්න
$env:GOOGLE_APPLICATION_CREDENTIALS="c:\Users\USER\Desktop\birthday\bdays-28160-firebase-adminsdk-fbsvc-14b400936e.json"

# ImgBB API key එක set කරන්න (if you have one)
$env:IMGBB_API_KEY="your-imgbb-api-key-here"

# Secret key එක set කරන්න
$env:SECRET_KEY="super-secret-key-change-this"
```

### Step 2: Dependencies Install කරන්න

```powershell
cd c:\Users\USER\Desktop\birthday
pip install -r requirements.txt
```

### Step 3: App එක Run කරන්න

```powershell
python app.py
```

### Step 4: Browser එකේ Test කරන්න

1. Browser එකේ `http://localhost:5000` යන්න
2. **Sign Up** එකේ:
   - Email address එකක් enter කරන්න
   - Password එකක් create කරන්න (min 6 characters)
   - Confirm password
   - Click "Create Account"

3. **Dashboard එකේ**:
   - Birthday එකක් add කරන්න
   - Photo එකක් upload කරන්න
   - Save කරන්න

4. **Data Persistence Test කරන්න**:
   - App එක stop කරන්න (`Ctrl+C`)
   - පස්සේ ආයේ run කරන්න
   - Login වෙන්න
   - ඔයාගේ birthdays තවමත් තියෙනවා! ✨

---

## 🌐 Cloud Run එකට Deploy කරන්න:

### Step 1: Secret Manager එකේ Service Account Key දාන්න

```powershell
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create secret from file
gcloud secrets create firebase-credentials `
  --data-file="c:\Users\USER\Desktop\birthday\bdays-28160-firebase-adminsdk-fbsvc-14b400936e.json"
```

### Step 2: Deploy කරන්න

```powershell
cd c:\Users\USER\Desktop\birthday

gcloud run deploy birthday-app `
  --source . `
  --region asia-south1 `
  --allow-unauthenticated `
  --set-env-vars="SECRET_KEY=your-random-secret-key,IMGBB_API_KEY=your-imgbb-key" `
  --set-secrets="GOOGLE_APPLICATION_CREDENTIALS=/secrets/firebase-creds:firebase-credentials:latest"
```

**හෝ Simple Method (Default Credentials):**

```powershell
gcloud run deploy birthday-app `
  --source . `
  --region asia-south1 `
  --allow-unauthenticated `
  --set-env-vars="SECRET_KEY=your-random-secret-key,IMGBB_API_KEY=your-imgbb-key"
```

---

## 🔐 How Firebase Authentication Works:

### Frontend (Browser):
1. User email සහ password enter කරනවා
2. Firebase Authentication SDK handle කරනවා login/signup
3. Firebase issues a **ID Token** (JWT)
4. ID token backend එකට send කරනවා

### Backend (Flask):
1. ID token එක verify කරනවා using Firebase Admin SDK
2. Token valid නම්, user session create කරනවා
3. Firestore එකේ user data save කරනවා

### Benefits:
- ✅ Firebase handles password hashing
- ✅ Built-in email verification
- ✅ Password reset functionality
- ✅ Can add Google, Facebook login later
- ✅ Very secure (industry standard)

---

## 📊 Data Structure (Firestore):

### Users Collection:
```
users/
  └── {firebase_uid}
      ├── uid: "firebase_user_id"
      ├── email: "user@example.com"
      └── created_at: timestamp
```

### Birthdays Collection:
```
birthdays/
  └── {auto_generated_id}
      ├── user_id: "firebase_user_id"
      ├── name: "John Doe"
      ├── relationship: "Friend"
      ├── bdate: "1990-05-15"
      ├── image: "https://i.ibb.co/..."
      ├── memo: "Loves pizza"
      └── created_at: timestamp
```

---

## ⚠️ Important Notes:

### Security:
1. **NEVER commit** `bdays-28160-firebase-adminsdk-fbsvc-14b400936e.json` to Git
2. `.gitignore` already configured to exclude this
3. Change `SECRET_KEY` in production

### Firebase Authentication Settings:
1. Go to Firebase Console: https://console.firebase.google.com/
2. Select your project: `bdays-28160`
3. **Authentication** > **Sign-in method**
4. Make sure **Email/Password** is **enabled** ✅

### Firestore Rules (For Development):
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

**🔴 Warning**: මේ rules development එකට විතරයි! Production එකට proper rules දාන්න:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    match /birthdays/{birthdayId} {
      allow read, write: if request.auth != null && 
                           resource.data.user_id == request.auth.uid;
    }
  }
}
```

---

## 🎯 Features:

| Feature | Status |
|---------|--------|
| Email/Password Auth | ✅ |
| Persistent Storage | ✅ |
| Data Loss Prevention | ✅ |
| Password Security | ✅ (Firebase handles it) |
| Image Upload | ✅ (ImgBB) |
| Responsive Design | ✅ |
| Cloud Deployment | ✅ |
| Auto-scaling | ✅ |

---

## 🐛 Troubleshooting:

### Error: "Could not determine credentials"
**Solution**: Make sure `GOOGLE_APPLICATION_CREDENTIALS` environment variable correctly set කරලා තියෙනවා.

### Error: "Firebase Auth not initialized"
**Solution**: Check Firebase config එක `index.html` එකේ correct කරලා තියෙනවද.

### Error: "Permission denied" in Firestore
**Solution**: 
1. Firestore Rules check කරන්න
2. Development mode එකේ `allow read, write: if true;` තියෙනවද කියලා verify කරන්න

### Data reset වෙනවා නම්:
**This should NOT happen anymore!** If it does:
1. Check Firestore එක properly connected කරලා තියෙනවද
2. App logs check කරන්න Firestore errors තියෙනවද කියලා

---

## 🎊 Summary:

### Before:
- ❌ Username-only authentication (insecure)
- ❌ Local JSON storage (data loss on restart)
- ❌ Manual password hashing

### After:
- ✅ Firebase Authentication (email/password)
- ✅ Cloud Firestore (persistent storage)
- ✅ No more data loss
- ✅ Production-ready security
- ✅ Scalable architecture

---

**මචං, දැන් app එක complete! Local එකේ test කරලා බලන්න, පස්සේ Cloud Run එකට deploy කරන්න! 🚀🎉**
