# Birthday Reminder Web Application

A beautiful and modern birthday reminder web application built with Python Flask and HTML/CSS/JavaScript.

## Features

- ✨ **Beautiful UI** - Modern glassmorphism design with smooth animations
- 🔐 **Secure Authentication** - Username and password-based sign up and sign in
- 🔒 **Password Security** - Passwords are hashed using Werkzeug security
- 📅 **Birthday Management** - Add, edit, and delete birthdays
- 🎂 **Today's Birthdays** - Special section highlighting today's birthdays
- 📆 **Upcoming Birthdays** - View all upcoming birthdays sorted by date
- 📷 **Photo Upload** - Upload photos using ImgBB API integration
- 📝 **Memos** - Add special notes and memories for each birthday
- ☁️ **Cloud Storage** - All data stored in Google Cloud Firestore (persistent and scalable)
- 🚀 **Cloud Run Ready** - Designed for Google Cloud Run deployment

## Birthday Information Tracked

- Name
- Relationship (Friend, Family, etc.)
- Birth Date
- Photo (uploaded to ImgBB)
- Memo/Notes

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Setup Firestore:**
   - Follow the detailed instructions in `FIRESTORE_SETUP.md`
   - Create a Firebase project
   - Enable Firestore Database
   - Download service account key
   - Set environment variable: `GOOGLE_APPLICATION_CREDENTIALS`

3. **Set Environment Variables:**
```bash
# Windows PowerShell
$env:GOOGLE_APPLICATION_CREDENTIALS="path/to/serviceAccountKey.json"
$env:IMGBB_API_KEY="your-imgbb-api-key"
$env:SECRET_KEY="your-secret-key"
```

4. **Run the application:**
```bash
python app.py
```

5. **Open your browser:**
Navigate to `http://localhost:5000`

## Project Structure

```
birthday/
├── app.py                     # Flask backend with Firestore integration
├── requirements.txt           # Python dependencies
├── FIRESTORE_SETUP.md         # Firestore setup guide
├── CLOUD_RUN_DEPLOYMENT.md    # Cloud Run deployment guide
├── Dockerfile                 # Docker configuration for Cloud Run
├── .gitignore                 # Git ignore file (excludes credentials)
├── serviceAccountKey.json     # Firebase credentials (DO NOT COMMIT)
├── templates/                 # HTML templates
│   ├── index.html            # Landing/Auth page
│   └── dashboard.html        # Main dashboard
└── static/                   # Static assets
    ├── css/
    │   └── style.css         # Styles
    └── js/
        ├── auth.js           # Authentication logic
        └── dashboard.js      # Dashboard logic
```

## Usage

### Sign Up / Sign In
1. Open the application in your browser
2. Choose "Sign Up" to create a new account or "Sign In" to access an existing account
3. Enter your username and password
   - Password must be at least 6 characters
   - For Sign Up, confirm your password

### Add Birthday
1. Click the "Add Birthday" button
2. Fill in the details:
   - Name (required)
   - Relationship (optional)
   - Birth Date (required)
   - Photo (optional)
   - Memo (optional)
3. Click "Save Birthday"

### View Birthday Details
- Click on any birthday card to view full details

### Edit Birthday
1. Click on a birthday card
2. Click "Edit" button
3. Update the information
4. Click "Update Birthday"

### Delete Birthday
1. Click on a birthday card
2. Click "Delete" button
3. Confirm deletion

## Features in Detail

### Today's Birthdays
- Special section at the top of the dashboard
- Shows all birthdays occurring today
- Displays the person's age

### Upcoming Birthdays
- Sorted by how soon the birthday is
- Shows countdown in days
- Displays upcoming age

### Image Upload
- Supports all common image formats
- Maximum file size: 5MB
- Images are uploaded to ImgBB for reliable hosting
- Automatic image optimization

## Technologies Used

- **Backend**: Python Flask
- **Database**: Google Cloud Firestore (NoSQL)
- **Authentication**: Werkzeug password hashing
- **Frontend**: HTML, CSS, JavaScript
- **Image Hosting**: ImgBB API
- **Design**: Glassmorphism, CSS animations
- **Deployment**: Google Cloud Run
- **Container**: Docker

## API Endpoints

- `POST /signup` - Create new user account
- `POST /signin` - Sign in to existing account
- `POST /signout` - Sign out
- `GET /api/birthdays` - Get all birthdays for current user
- `GET /api/birthdays/today` - Get today's birthdays
- `POST /api/birthdays` - Add new birthday
- `PUT /api/birthdays/<id>` - Update birthday
- `DELETE /api/birthdays/<id>` - Delete birthday

## Cloud Deployment

See `CLOUD_RUN_DEPLOYMENT.md` and `FIRESTORE_SETUP.md` for detailed deployment instructions.

**Quick Deploy to Google Cloud Run:**

```bash
gcloud run deploy birthday-app \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated
```

## Notes

- All data is stored in Google Cloud Firestore (persistent cloud database)
- Each user's birthdays are private to their account
- Passwords are securely hashed before storage
- The application automatically calculates ages and countdown days
- Images are permanently hosted on ImgBB
- Container automatically scales based on traffic
- Data persists across container restarts (no more data loss!)

## Development

To modify the application:
- Backend logic: Edit `app.py`
- HTML structure: Edit files in `templates/`
- Styling: Edit `static/css/style.css`
- Frontend logic: Edit files in `static/js/`

## License

Free to use and modify for personal projects.

## Support

If you encounter any issues, make sure:
1. All dependencies are installed
2. Python version is 3.7 or higher
3. Port 5000 is not in use by another application

Enjoy managing your birthdays! 🎂🎉
