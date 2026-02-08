import os
import json
import base64
import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore, auth

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# ImgBB API Configuration
IMGBB_API_KEY = os.environ.get('IMGBB_API_KEY', '')
IMGBB_UPLOAD_URL = 'https://api.imgbb.com/1/upload'

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        # For Cloud Run: Use Application Default Credentials
        # This automatically uses the service account assigned to Cloud Run
        cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        
        if cred_path and os.path.exists(cred_path):
            # Local development: use service account file
            print(f"Using service account from file: {cred_path}")
            cred = credentials.Certificate(cred_path)
        else:
            # Cloud Run: use default application credentials
            print("Using Application Default Credentials (Cloud Run)")
            cred = credentials.ApplicationDefault()
        
        # Initialize with project ID explicitly
        firebase_admin.initialize_app(cred, {
            'projectId': 'bdays-28160'
        })
        print("✅ Firebase Admin SDK initialized successfully")
        
    except Exception as e:
        print(f"❌ Firebase initialization error: {e}")
        raise

# Initialize Firestore
db = firestore.client()

# Collections
users_collection = db.collection('users')
birthdays_collection = db.collection('birthdays')

# Helper functions
def verify_firebase_token(id_token):
    """Verify Firebase ID token and return user info"""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Token verification error: {e}")
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def upload_to_imgbb(image_base64):
    """Upload image to ImgBB and return the URL"""
    try:
        # Remove data URL prefix if present
        if ',' in image_base64:
            image_base64 = image_base64.split(',')[1]
        
        payload = {
            'key': IMGBB_API_KEY,
            'image': image_base64
        }
        
        response = requests.post(IMGBB_UPLOAD_URL, data=payload)
        result = response.json()
        
        if result.get('success'):
            return result['data']['url']
        else:
            return None
    except Exception as e:
        print(f"Error uploading to ImgBB: {e}")
        return None

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/test')
def test_firebase():
    """Test page for Firebase Authentication debugging"""
    return render_template('test_firebase.html')

@app.route('/signup', methods=['POST'])
def signup():
    # Get Firebase ID token from Authorization header
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Invalid authorization header'}), 401
    
    id_token = auth_header.split('Bearer ')[1]
    
    # Verify the token
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    data = request.get_json()
    email = data.get('email', '').strip()
    uid = decoded_token.get('uid')
    
    if not email or not uid:
        return jsonify({'error': 'Email and UID are required'}), 400
    
    # Check if user already exists in Firestore
    user_ref = users_collection.document(uid)
    user_doc = user_ref.get()
    
    if not user_doc.exists:
        # Create new user document in Firestore
        user_data = {
            'uid': uid,
            'email': email,
            'created_at': firestore.SERVER_TIMESTAMP
        }
        user_ref.set(user_data)
    
    # Create session
    session['user_id'] = uid
    session['email'] = email
    
    return jsonify({'success': True, 'message': 'Account created successfully'})

@app.route('/signin', methods=['POST'])
def signin():
    # Get Firebase ID token from Authorization header
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Invalid authorization header'}), 401
    
    id_token = auth_header.split('Bearer ')[1]
    
    # Verify the token
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    data = request.get_json()
    email = data.get('email', '').strip()
    uid = decoded_token.get('uid')
    
    if not email or not uid:
        return jsonify({'error': 'Email and UID are required'}), 400
    
    # Create session
    session['user_id'] = uid
    session['email'] = email
    
    return jsonify({'success': True, 'message': 'Signed in successfully'})

@app.route('/signout', methods=['POST'])
def signout():
    session.pop('user_id', None)
    session.pop('email', None)
    return jsonify({'success': True, 'message': 'Signed out successfully'})

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', email=session.get('email', ''))

@app.route('/api/birthdays', methods=['GET'])
@login_required
def get_birthdays():
    user_id = session['user_id']
    
    # Query birthdays for this user
    birthdays_query = birthdays_collection.where('user_id', '==', user_id).stream()
    
    user_birthdays = []
    for doc in birthdays_query:
        birthday_data = doc.to_dict()
        birthday_data['id'] = doc.id
        user_birthdays.append(birthday_data)
    
    # Sort by upcoming birthdays
    today = datetime.now()
    
    def get_next_birthday(bday):
        try:
            birth_date = datetime.strptime(bday['bdate'], '%Y-%m-%d')
            next_birthday = birth_date.replace(year=today.year)
            
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            
            days_until = (next_birthday - today).days
            bday['days_until'] = days_until
            bday['age'] = today.year - birth_date.year
            if next_birthday.month < today.month or (next_birthday.month == today.month and next_birthday.day < today.day):
                bday['age'] += 1
            
            return days_until
        except:
            return 999999
    
    sorted_birthdays = sorted(user_birthdays, key=get_next_birthday)
    
    return jsonify(sorted_birthdays)

@app.route('/api/birthdays/today', methods=['GET'])
@login_required
def get_today_birthdays():
    user_id = session['user_id']
    
    # Query birthdays for this user
    birthdays_query = birthdays_collection.where('user_id', '==', user_id).stream()
    
    today = datetime.now()
    today_birthdays = []
    
    for doc in birthdays_query:
        bday = doc.to_dict()
        bday['id'] = doc.id
        
        try:
            birth_date = datetime.strptime(bday['bdate'], '%Y-%m-%d')
            if birth_date.month == today.month and birth_date.day == today.day:
                bday['age'] = today.year - birth_date.year
                today_birthdays.append(bday)
        except:
            continue
    
    return jsonify(today_birthdays)

@app.route('/api/birthdays', methods=['POST'])
@login_required
def add_birthday():
    user_id = session['user_id']
    data = request.get_json()
    
    name = data.get('name', '').strip()
    relationship = data.get('relationship', '').strip()
    bdate = data.get('bdate', '').strip()
    image_data = data.get('image', '')
    memo = data.get('memo', '').strip()
    
    if not name or not bdate:
        return jsonify({'error': 'Name and birth date are required'}), 400
    
    # Upload image to ImgBB if provided
    image_url = None
    if image_data:
        image_url = upload_to_imgbb(image_data)
        if not image_url:
            return jsonify({'error': 'Failed to upload image'}), 500
    
    birthday_entry = {
        'user_id': user_id,
        'name': name,
        'relationship': relationship,
        'bdate': bdate,
        'image': image_url,
        'memo': memo,
        'created_at': firestore.SERVER_TIMESTAMP
    }
    
    # Add to Firestore
    doc_ref = birthdays_collection.add(birthday_entry)
    
    # Prepare response (replace SERVER_TIMESTAMP with actual datetime for JSON serialization)
    response_data = {
        'id': doc_ref[1].id,
        'user_id': user_id,
        'name': name,
        'relationship': relationship,
        'bdate': bdate,
        'image': image_url,
        'memo': memo,
        'created_at': datetime.now().isoformat()
    }
    
    return jsonify({'success': True, 'message': 'Birthday added successfully', 'data': response_data})

@app.route('/api/birthdays/<birthday_id>', methods=['PUT'])
@login_required
def update_birthday(birthday_id):
    user_id = session['user_id']
    data = request.get_json()
    
    # Get birthday document
    birthday_ref = birthdays_collection.document(birthday_id)
    birthday_doc = birthday_ref.get()
    
    if not birthday_doc.exists:
        return jsonify({'error': 'Birthday not found'}), 404
    
    birthday_data = birthday_doc.to_dict()
    
    # Verify ownership
    if birthday_data.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Update fields
    update_data = {}
    if 'name' in data:
        update_data['name'] = data['name'].strip()
    if 'relationship' in data:
        update_data['relationship'] = data['relationship'].strip()
    if 'bdate' in data:
        update_data['bdate'] = data['bdate'].strip()
    if 'memo' in data:
        update_data['memo'] = data['memo'].strip()
    
    # Handle image update
    if 'image' in data and data['image']:
        image_url = upload_to_imgbb(data['image'])
        if image_url:
            update_data['image'] = image_url
        else:
            return jsonify({'error': 'Failed to upload image'}), 500
    
    update_data['updated_at'] = firestore.SERVER_TIMESTAMP
    
    # Update in Firestore
    birthday_ref.update(update_data)
    
    # Get updated document and prepare response
    updated_doc = birthday_ref.get()
    updated_data = updated_doc.to_dict()
    updated_data['id'] = birthday_id
    
    # Convert any Firestore timestamps to serializable format
    if 'created_at' in updated_data and hasattr(updated_data['created_at'], 'isoformat'):
        updated_data['created_at'] = updated_data['created_at'].isoformat()
    if 'updated_at' in updated_data and hasattr(updated_data['updated_at'], 'isoformat'):
        updated_data['updated_at'] = updated_data['updated_at'].isoformat()
    
    return jsonify({'success': True, 'message': 'Birthday updated successfully', 'data': updated_data})

@app.route('/api/birthdays/<birthday_id>', methods=['DELETE'])
@login_required
def delete_birthday(birthday_id):
    user_id = session['user_id']
    
    # Get birthday document
    birthday_ref = birthdays_collection.document(birthday_id)
    birthday_doc = birthday_ref.get()
    
    if not birthday_doc.exists:
        return jsonify({'error': 'Birthday not found'}), 404
    
    birthday_data = birthday_doc.to_dict()
    
    # Verify ownership
    if birthday_data.get('user_id') != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Delete from Firestore
    birthday_ref.delete()
    
    return jsonify({'success': True, 'message': 'Birthday deleted successfully'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
