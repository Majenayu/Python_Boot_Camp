from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
import os
import requests
import json
import datetime

# Set template_folder to current directory
app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)))
app.secret_key = 'your-secret-key'  # Replace with a secure key

# MongoDB connection
client = MongoClient('mongodb+srv://apt:apt@apt.ydfi6pf.mongodb.net/?retryWrites=true&w=majority&appName=apt')
db = client['school']
users = db['users']

# OpenRouter API configuration
OPENROUTER_API_KEY = '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'
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

def generate_questions(num_questions, difficulty, question_types, selection_mode):
    prompt = f"""
    Generate {num_questions} aptitude quiz questions with the following specifications:
    - Difficulty: {difficulty} (if 'mix', include a balanced mix of easy, medium, and hard)
    - Question Types: {', '.join(question_types)} (if multiple, distribute evenly)
    - Format: Each question must have exactly 4 multiple-choice options, one correct answer, and an explanation.
    - Output as JSON with the structure: 
      [
        {{
          "question": "string",
          "options": ["string", "string", "string", "string"],
          "correct_answer": "string",
          "explanation": "string",
          "type": "string",
          "difficulty": "string"
        }}
      ]
    """
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': prompt}]
    }
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes
        response_data = response.json()
        if not response_data.get('choices') or not response_data['choices'][0].get('message') or not response_data['choices'][0]['message'].get('content'):
            return [], "API returned empty or invalid response"
        
        content = response_data['choices'][0]['message']['content']
        try:
            questions = json.loads(content)
            if not isinstance(questions, list):
                return [], "API response is not a valid JSON list"
            for q in questions:
                if not all(key in q for key in ['question', 'options', 'correct_answer', 'explanation', 'type', 'difficulty']) or len(q['options']) != 4:
                    return [], "Invalid question format in API response"
            return questions, None
        except json.JSONDecodeError as e:
            return [], f"JSON parsing error: {str(e)}"
    except requests.exceptions.RequestException as e:
        return [], f"API request failed: {str(e)}"

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
            session['email'] = email
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
            return render_template('create_quiz.html', error=f'Failed to generate questions: {error or "Unknown error"}')
        
        # Store quiz configuration in MongoDB
        user_email = session['email']
        user_collection = db[user_email]
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
    
    user_email = session['email']
    user_collection = db[user_email]
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
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)