import os
import json
import base64
import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# ImgBB API Configuration
IMGBB_API_KEY = os.environ.get('IMGBB_API_KEY', '')  # Read from environment variable
IMGBB_UPLOAD_URL = 'https://api.imgbb.com/1/upload'

# Data files
USERS_FILE = 'data/users.json'
BIRTHDAYS_FILE = 'data/birthdays.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize data files if they don't exist
def init_data_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    if not os.path.exists(BIRTHDAYS_FILE):
        with open(BIRTHDAYS_FILE, 'w') as f:
            json.dump({}, f)

init_data_files()

# Helper functions
def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
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
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    users = load_json(USERS_FILE)
    
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400
    
    users[username] = {
        'created_at': datetime.now().isoformat()
    }
    save_json(USERS_FILE, users)
    
    session['username'] = username
    return jsonify({'success': True, 'message': 'Account created successfully'})

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    users = load_json(USERS_FILE)
    
    if username not in users:
        return jsonify({'error': 'Username not found'}), 404
    
    session['username'] = username
    return jsonify({'success': True, 'message': 'Signed in successfully'})

@app.route('/signout', methods=['POST'])
def signout():
    session.pop('username', None)
    return jsonify({'success': True, 'message': 'Signed out successfully'})

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/api/birthdays', methods=['GET'])
@login_required
def get_birthdays():
    username = session['username']
    all_birthdays = load_json(BIRTHDAYS_FILE)
    user_birthdays = all_birthdays.get(username, [])
    
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
    username = session['username']
    all_birthdays = load_json(BIRTHDAYS_FILE)
    user_birthdays = all_birthdays.get(username, [])
    
    today = datetime.now()
    today_birthdays = []
    
    for bday in user_birthdays:
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
    username = session['username']
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
    
    all_birthdays = load_json(BIRTHDAYS_FILE)
    if username not in all_birthdays:
        all_birthdays[username] = []
    
    birthday_entry = {
        'id': len(all_birthdays[username]) + 1,
        'name': name,
        'relationship': relationship,
        'bdate': bdate,
        'image': image_url,
        'memo': memo,
        'created_at': datetime.now().isoformat()
    }
    
    all_birthdays[username].append(birthday_entry)
    save_json(BIRTHDAYS_FILE, all_birthdays)
    
    return jsonify({'success': True, 'message': 'Birthday added successfully', 'data': birthday_entry})

@app.route('/api/birthdays/<int:birthday_id>', methods=['PUT'])
@login_required
def update_birthday(birthday_id):
    username = session['username']
    data = request.get_json()
    
    all_birthdays = load_json(BIRTHDAYS_FILE)
    user_birthdays = all_birthdays.get(username, [])
    
    birthday_index = None
    for i, bday in enumerate(user_birthdays):
        if bday['id'] == birthday_id:
            birthday_index = i
            break
    
    if birthday_index is None:
        return jsonify({'error': 'Birthday not found'}), 404
    
    # Update fields
    if 'name' in data:
        user_birthdays[birthday_index]['name'] = data['name'].strip()
    if 'relationship' in data:
        user_birthdays[birthday_index]['relationship'] = data['relationship'].strip()
    if 'bdate' in data:
        user_birthdays[birthday_index]['bdate'] = data['bdate'].strip()
    if 'memo' in data:
        user_birthdays[birthday_index]['memo'] = data['memo'].strip()
    
    # Handle image update
    if 'image' in data and data['image']:
        image_url = upload_to_imgbb(data['image'])
        if image_url:
            user_birthdays[birthday_index]['image'] = image_url
        else:
            return jsonify({'error': 'Failed to upload image'}), 500
    
    user_birthdays[birthday_index]['updated_at'] = datetime.now().isoformat()
    
    all_birthdays[username] = user_birthdays
    save_json(BIRTHDAYS_FILE, all_birthdays)
    
    return jsonify({'success': True, 'message': 'Birthday updated successfully', 'data': user_birthdays[birthday_index]})

@app.route('/api/birthdays/<int:birthday_id>', methods=['DELETE'])
@login_required
def delete_birthday(birthday_id):
    username = session['username']
    
    all_birthdays = load_json(BIRTHDAYS_FILE)
    user_birthdays = all_birthdays.get(username, [])
    
    user_birthdays = [bday for bday in user_birthdays if bday['id'] != birthday_id]
    
    all_birthdays[username] = user_birthdays
    save_json(BIRTHDAYS_FILE, all_birthdays)
    
    return jsonify({'success': True, 'message': 'Birthday deleted successfully'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
