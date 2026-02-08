# 🎉 Birthday App - Firestore Integration සහ Password Authentication

## 🔥 මොනවද වෙනස් වුණේ?

### ✅ 1. **Firestore Database Integration**
- **Before**: JSON files use කරලා local storage එකේ data save කරපු
- **After**: Google Cloud Firestore use කරලා cloud එකේ permanent storage
- **Result**: Container restart වුණත්, scale down වුණත් data නැති වෙන්නේ **නෑ**! 🎊

### ✅ 2. **Password Authentication Added**
- **Before**: Username පමණක් use කරලා login වුණා (insecure)
- **After**: Username **සහ** Password දෙකම use කරන්න ඕන
- **Security**: Passwords hashed කරලා save වෙනවා (Werkzeug security)

### ✅ 3. **Updated Files**

#### නව Files:
1. **`FIRESTORE_SETUP.md`** - Firestore setup කරන්න complete guide (Sinhala + English)
2. **`.gitignore`** (updated) - Service account keys commit වෙන්නේ නෑ

#### Modified Files:
1. **`app.py`** - Firebase Admin SDK integration + password hashing
2. **`requirements.txt`** - `firebase-admin==6.4.0` added
3. **`templates/index.html`** - Password input fields added (signin + signup)
4. **`static/js/auth.js`** - Password validation logic added
5. **`README.md`** - Updated documentation

---

## 🚀 දැන් කරන්න ඕන දේවල්

### Step 1: Firestore Setup
**`FIRESTORE_SETUP.md`** file එක open කරලා කියවන්න. එතන තියෙන්නේ:
1. Firebase project එකක් හදන්න කියලා
2. Firestore database එක enable කරන්න කියලා
3. Service account key එකක් download කරන්න කියලා
4. Local සහ Cloud Run testing කරන්න කියලා

### Step 2: Local Testing (Optional)
```powershell
# Service account key file එක download කරලා project folder එකට දාන්න
# සහ environment variable එක set කරන්න:
$env:GOOGLE_APPLICATION_CREDENTIALS="c:\Users\USER\Desktop\birthday\serviceAccountKey.json"
$env:IMGBB_API_KEY="your-imgbb-api-key"

# Dependencies install කරන්න
pip install -r requirements.txt

# App එක run කරන්න
python app.py
```

### Step 3: Cloud Run Deploy
```powershell
# Simplest method - Default credentials use කරන්න
gcloud run deploy birthday-app `
  --source . `
  --region asia-south1 `
  --allow-unauthenticated `
  --set-env-vars="IMGBB_API_KEY=your-imgbb-api-key,SECRET_KEY=your-secret-key-here"
```

---

## 🎯 Key Benefits

### 1. **No More Data Loss** 🛡️
- Containers ephemeral වෙද්දීත් data cloud එකේ safe
- Automatic backups Firestore එකේන්
- Multi-region replication

### 2. **Better Security** 🔐
- Password-based authentication
- Hashed passwords (not plain text)
- Secure session management

### 3. **Scalability** 📈
- Firestore automatically scales
- No storage limits
- Fast global access

### 4. **Production Ready** 🏭
- Cloud-native architecture
- Automatic container restarts won't affect data
- Easy to manage and monitor

---

## 📝 How Authentication Works Now

### Sign Up:
1. User enters username + password (+ confirm password)
2. Password validated (min 6 characters)
3. Password hashed using Werkzeug
4. User document created in Firestore `users` collection
5. Session created

### Sign In:
1. User enters username + password
2. Firestore query for username
3. Password hash verified
4. Session created on success

---

## 🗄️ Firestore Data Structure

### Collections:

```
users/
  └── {username}
      ├── username: "john_doe"
      ├── password: "hashed_password_string"
      └── created_at: timestamp

birthdays/
  └── {auto_generated_id}
      ├── username: "john_doe"
      ├── name: "Sarah"
      ├── relationship: "Sister"
      ├── bdate: "1995-05-15"
      ├── image: "https://i.ibb.co/..."
      ├── memo: "Loves chocolate"
      └── created_at: timestamp
```

---

## ⚠️ Important Notes

### Security:
- **NEVER** commit `serviceAccountKey.json` to Git
- `.gitignore` already configured to exclude this
- Use environment variables for sensitive data

### Testing Data Persistence:
1. Deploy to Cloud Run
2. Create account + add birthdays
3. Wait a few minutes (or force container restart)
4. Login again
5. All data should still be there! ✨

### Cost:
- Firestore Free Tier:
  - 1 GB storage
  - 50,000 reads/day
  - 20,000 writes/day
  - 20,000 deletes/day
- ImgBB: Free (images stored externally)
- Cloud Run: Pay per request (free tier available)

---

## 🎊 Summary

| Feature | Before | After |
|---------|--------|-------|
| Storage | Local JSON files | Cloud Firestore |
| Data Persistence | ❌ Lost on restart | ✅ Permanent |
| Authentication | Username only | Username + Password |
| Password Security | N/A | ✅ Hashed |
| Scalability | Limited | ✅ Auto-scaling |
| Production Ready | ❌ No | ✅ Yes |

---

## 📞 Next Steps

1. **Read**: `FIRESTORE_SETUP.md` for detailed setup
2. **Setup**: Firebase project සහ Firestore database
3. **Test**: Local environment එකේ
4. **Deploy**: Cloud Run එකට
5. **Verify**: Data persistence working කියලා

මචං, දැන් ඔයාගේ app එක **production-ready**! Data නැති වෙන්නේ නෑ, secure authentication තියෙනවා, සහ cloud එකේ scale වෙනවා! 🚀🎉
