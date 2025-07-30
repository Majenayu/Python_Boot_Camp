from flask import Flask, request, render_template, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key

# MongoDB connection
client = MongoClient('mongodb+srv://apt:apt@apt.ydfi6pf.mongodb.net/?retryWrites=true&w=majority&appName=apt')
db = client['school']
users = db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        role = request.form['role']
        
        user = users.find_one({'email': email, 'role': role})
        if user and bcrypt.checkpw(password, user['password']):
            session['user_id'] = str(user['_id'])
            session['role'] = role
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials or role')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        role = request.form['role']
        
        if users.find_one({'email': email, 'role': role}):
            return render_template('register.html', error='User already exists')
        
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        users.insert_one({'email': email, 'password': hashed, 'role': role})
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = users.find_one({'_id': ObjectId(session['user_id'])})
        return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)