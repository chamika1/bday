# Birthday Reminder Web Application

A beautiful and modern birthday reminder web application built with Python Flask and HTML/CSS/JavaScript.

## Features

- ✨ **Beautiful UI** - Modern glassmorphism design with smooth animations
- 🔐 **Simple Authentication** - Username-based sign up and sign in
- 📅 **Birthday Management** - Add, edit, and delete birthdays
- 🎂 **Today's Birthdays** - Special section highlighting today's birthdays
- 📆 **Upcoming Birthdays** - View all upcoming birthdays sorted by date
- 📷 **Photo Upload** - Upload photos using ImgBB API integration
- 📝 **Memos** - Add special notes and memories for each birthday
- 💾 **JSON Storage** - All data stored locally in JSON files

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

2. **Run the application:**
```bash
python app.py
```

3. **Open your browser:**
Navigate to `http://localhost:5000`

## Project Structure

```
birthday/
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── data/                   # Data storage (auto-created)
│   ├── users.json         # User accounts
│   └── birthdays.json     # Birthday data
├── templates/             # HTML templates
│   ├── index.html        # Landing/Auth page
│   └── dashboard.html    # Main dashboard
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Styles
    └── js/
        ├── auth.js       # Authentication logic
        └── dashboard.js  # Dashboard logic
```

## Usage

### Sign Up / Sign In
1. Open the application in your browser
2. Choose "Sign Up" to create a new account or "Sign In" to access an existing account
3. Enter your username

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
- **Frontend**: HTML, CSS, JavaScript
- **Storage**: JSON files
- **Image Hosting**: ImgBB API
- **Design**: Glassmorphism, CSS animations

## API Endpoints

- `POST /signup` - Create new user account
- `POST /signin` - Sign in to existing account
- `POST /signout` - Sign out
- `GET /api/birthdays` - Get all birthdays for current user
- `GET /api/birthdays/today` - Get today's birthdays
- `POST /api/birthdays` - Add new birthday
- `PUT /api/birthdays/<id>` - Update birthday
- `DELETE /api/birthdays/<id>` - Delete birthday

## Notes

- All data is stored locally in JSON files
- Each user's birthdays are private to their account
- The application automatically calculates ages and countdown days
- Images are permanently hosted on ImgBB

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
