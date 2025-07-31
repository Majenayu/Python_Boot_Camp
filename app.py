from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
import os
import requests
import json
import datetime
import random

# Set template_folder to current directory
app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)))
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')  # Use environment variable

# MongoDB connection
client = MongoClient('mongodb+srv://apt:apt@apt.ydfi6pf.mongodb.net/?retryWrites=true&w=majority&appName=apt')
db = client['school']
users = db['users']

# OpenTDB API configuration
OPENTDB_API_URL = 'https://opentdb.com/api.php'

def generate_questions(num_questions, difficulty, question_types, selection_mode):
    # Map difficulty to OpenTDB format
    opentdb_difficulty = difficulty.lower() if difficulty.lower() in ['easy', 'medium', 'hard'] else ''
    # Map question types to OpenTDB categories
    category_map = {
        'arithmetic': 19,  # Science: Mathematics
        'algebra': 19,
        'geometry': 19,
        'logical reasoning': 23,  # History (proxy, as OpenTDB lacks logical reasoning)
        'verbal reasoning': 10,  # General Knowledge
    }
    category_ids = [category_map.get(qt.lower(), 10) for qt in question_types]
    category_id = random.choice(category_ids) if category_ids else 10  # Default to General Knowledge
    
    params = {
        'amount': min(num_questions, 50),  # OpenTDB max is 50
        'type': 'multiple',  # Only multiple-choice
        'category': category_id,
    }
    if opentdb_difficulty:
        params['difficulty'] = opentdb_difficulty
    
    try:
        response = requests.get(OPENTDB_API_URL, params=params)
        print(f"OpenTDB Response Status: {response.status_code}")
        print(f"OpenTDB Response Text: {response.text}")
        response.raise_for_status()
        response_data = response.json()
        
        if response_data.get('response_code') != 0:
            error_codes = {
                1: "Not enough questions available for the specified criteria",
                2: "Invalid parameter in request",
                3: "Session token not found",
                4: "Session token has returned all possible questions",
                5: "Rate limit exceeded (1 request per 5 seconds)"
            }
            return [], f"OpenTDB error: {error_codes.get(response_data['response_code'], 'Unknown error')}"
        
        questions = []
        for q in response_data.get('results', []):
            options = q['incorrect_answers'] + [q['correct_answer']]
            random.shuffle(options)
            questions.append({
                'question': q['question'],
                'options': options,
                'correct_answer': q['correct_answer'],
                'explanation': f"This question is from the {q['category']} category with {q['difficulty']} difficulty.",
                'type': q['type'],
                'difficulty': q['difficulty']
            })
        if not questions:
            return [], "No questions returned from OpenTDB"
        return questions, None
    except requests.exceptions.HTTPError as e:
        return [], f"HTTP error: {str(e)} (Status: {response.status_code})"
    except requests.exceptions.RequestException as e:
        return [], f"API request failed: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password'].encode('utf-8')
        role = request.form['role']
        
        user = users.find_one({'name': name, 'role': role})
        if user and bcrypt.checkpw(password, user['password']):
            session['user_id'] = str(user['_id'])
            session['role'] = role
            session['name'] = name
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid name, password, or role')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password'].encode('utf-8')
        role = request.form['role']
        
        if users.find_one({'name': name, 'role': role}):
            return render_template('register.html', error='User with this name and role already exists')
        
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        users.insert_one({'name': name, 'password': hashed, 'role': role})
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = users.find_one({'_id': ObjectId(session['user_id'])})
        return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))

@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        quiz_name = request.form['quiz_name']
        num_questions = int(request.form['num_questions'])
        total_time = int(request.form['total_time'])
        per_question_time = int(request.form['per_question_time'])
        difficulty = request.form['difficulty']
        question_types = request.form.getlist('question_types')
        selection_mode = request.form['selection_mode']
        
        # Generate questions
        questions, error = generate_questions(num_questions, difficulty, question_types, selection_mode)
        
        if error or not questions:
            print(f"Quiz generation error: {error}")
            return render_template('create_quiz.html', error=f'Failed to generate questions: {error or "Unknown error"}')
        
        # Store quiz configuration in MongoDB
        user_name = session['name']
        user_collection = db[user_name]
        quiz_data = {
            'quiz_name': quiz_name,
            'num_questions': num_questions,
            'total_time': total_time,
            'per_question_time': per_question_time,
            'difficulty': difficulty,
            'question_types': question_types,
            'selection_mode': selection_mode,
            'questions': questions,
            'created_at': datetime.datetime.now()
        }
        quiz_id = user_collection.insert_one(quiz_data).inserted_id
        
        return redirect(url_for('take_quiz', quiz_id=str(quiz_id)))
    
    return render_template('create_quiz.html')

@app.route('/take_quiz/<quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_name = session['name']
    user_collection = db[user_name]
    quiz = user_collection.find_one({'_id': ObjectId(quiz_id)})
    
    if not quiz:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        answers = request.form.to_dict()
        score = 0
        results = []
        
        for i, question in enumerate(quiz['questions']):
            user_answer = answers.get(f'question_{i}')
            correct = user_answer == question['correct_answer']
            if correct:
                score += 1
            results.append({
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': question['correct_answer'],
                'correct': correct,
                'explanation': question['explanation']
            })
        
        # Store results in MongoDB
        user_collection.update_one(
            {'_id': ObjectId(quiz_id)},
            {'$set': {
                'results': results,
                'score': score,
                'completed_at': datetime.datetime.now()
            }}
        )
        
        return render_template('take_quiz.html', quiz=quiz, results=results, score=score)
    
    return render_template('take_quiz.html', quiz=quiz)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('name', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)