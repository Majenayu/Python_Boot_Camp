from flask import Flask, request, render_template, redirect, url_for, session, jsonify, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
import os
import requests
import json
import datetime
import random
import math
import string
import logging

app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)))
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = MongoClient('mongodb+srv://apt:apt@apt.ydfi6pf.mongodb.net/?retryWrites=true&w=majority&appName=apt')
db = client['school']
users = db['users']
rooms = db['rooms']

APTITUDE_API_BASE_URL = 'https://aptitude-api.vercel.app'

def generate_questions(num_questions, difficulty, question_types, selection_mode):
    topic_map = {
        'mixture_alligation': 'MixtureAndAlligation',
        'profit_loss': 'ProfitAndLoss',
        'pipes_cisterns': 'PipesAndCistern',
        'age': 'Age',
        'permutation_combination': 'PermutationAndCombination',
        'speed_time_distance': 'SpeedTimeDistance',
        'simple_interest': 'SimpleInterest',
        'calendars': 'Calendar'
    }
    selected_topics = [topic_map.get(qt.lower(), 'Age') for qt in question_types] if question_types else ['Age']
    all_questions = []
    max_attempts = num_questions * 3
    attempts = 0

    while len(all_questions) < num_questions and attempts < max_attempts:
        topic = random.choice(selected_topics)
        params = {'amount': 1}
        try:
            response = requests.get(f"{APTITUDE_API_BASE_URL}/{topic}", params=params)
            response.raise_for_status()
            response_data = response.json()
            question_items = response_data if isinstance(response_data, list) else [response_data]
            for item in question_items:
                if 'question' in item and item['question'] not in [q['question'] for q in all_questions]:
                    all_questions.append({
                        'question': item.get('question', 'No question available'),
                        'options': item.get('options', ['A', 'B', 'C', 'D']),
                        'correct_answer': item.get('answer', 'N/A'),
                        'explanation': item.get('explanation', 'No explanation available'),
                        'type': topic,
                        'difficulty': difficulty if difficulty else 'Any'
                    })
                    break
        except requests.exceptions.RequestException:
            pass
        attempts += 1
    random.shuffle(all_questions)
    return all_questions[:num_questions], None

def generate_room_code():
    return ''.join(random.choices(string.digits, k=4))

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
            logger.debug(f"User {name} ({role}) logged in with session: {session}")
            if role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = users.find_one({'_id': ObjectId(session['user_id'])})
    return render_template('dashboard.html', user=user)

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'user_id' not in session or session['role'] != 'teacher':
        logger.debug(f"Unauthorized access to teacher_dashboard: {session}")
        return redirect(url_for('login'))
    user = users.find_one({'_id': ObjectId(session['user_id'])})
    active_rooms = list(rooms.find({'teacher_id': session['user_id'], 'status': {'$in': ['active', 'started', 'stopped']}}))
    for room in active_rooms:
        room['_id'] = str(room['_id'])
        room['num_students'] = len(room.get('students', []))
    return render_template('dashboard1.html', user=user, active_rooms=active_rooms)

@app.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_name = session['name']
    user_collection = db[user_name]
    quizzes = list(user_collection.find({'results': {'$exists': True}}))
    for quiz in quizzes:
        correct = quiz.get('score', 0)
        total = quiz.get('num_questions', 0)
        incorrect = total - correct
        quiz['_id'] = str(quiz['_id'])
        quiz['correct'] = correct
        quiz['incorrect'] = incorrect
        quiz['date'] = quiz.get('completed_at').strftime('%Y-%m-%d') if quiz.get('completed_at') else 'N/A'
    return render_template('analytics.html', quizzes=quizzes)

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
        questions, error = generate_questions(num_questions, difficulty, question_types, selection_mode)
        if error or not questions:
            return render_template('create_quiz.html', error=f'Failed to generate questions: {error or "Unknown error"}')
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

@app.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if 'user_id' not in session or session['role'] != 'teacher':
        logger.debug(f"Unauthorized access to create_room: {session}")
        return redirect(url_for('login'))
    if request.method == 'POST':
        quiz_name = request.form['quiz_name']
        num_questions = int(request.form['num_questions'])
        total_time = int(request.form['total_time'])
        per_question_time = int(request.form['per_question_time'])
        difficulty = request.form['difficulty']
        question_types = request.form.getlist('question_types')
        selection_mode = request.form['selection_mode']
        questions, error = generate_questions(num_questions, difficulty, question_types, selection_mode)
        if error or not questions:
            return render_template('create_quiz.html', error=f'Failed to generate questions: {error or "Unknown error"}')
        room_code = generate_room_code()
        while rooms.find_one({'room_code': room_code}):
            room_code = generate_room_code()
        room_data = {
            'room_code': room_code,
            'teacher_id': session['user_id'],
            'quiz_name': quiz_name,
            'num_questions': num_questions,
            'total_time': total_time,
            'per_question_time': per_question_time,
            'difficulty': difficulty,
            'question_types': question_types,
            'selection_mode': selection_mode,
            'questions': questions,
            'students': [],
            'status': 'active',
            'created_at': datetime.datetime.now()
        }
        room_id = rooms.insert_one(room_data).inserted_id
        return redirect(url_for('room', room_id=str(room_id)))
    return render_template('create_quiz.html')

@app.route('/room/<room_id>')
def room(room_id):
    if 'user_id' not in session or session['role'] != 'teacher':
        logger.debug(f"Unauthorized access to room {room_id}: {session}")
        return redirect(url_for('login'))
    room = rooms.find_one({'_id': ObjectId(room_id), 'teacher_id': session['user_id']})
    if not room:
        return redirect(url_for('teacher_dashboard'))
    room['_id'] = str(room['_id'])
    room['num_students'] = len(room.get('students', []))
    return render_template('room.html', room=room)

@app.route('/join_room', methods=['GET', 'POST'])
def join_room():
    if 'user_id' not in session or session['role'] != 'student':
        logger.debug(f"Unauthorized access to join_room: {session}")
        return redirect(url_for('login'))
    if request.method == 'POST':
        room_code = request.form['room_code']
        room = rooms.find_one({'room_code': room_code, 'status': 'active'})
        if not room:
            return render_template('join_room.html', error='Invalid or inactive room code')
        user_name = session['name']
        if user_name not in room.get('students', []):
            rooms.update_one(
                {'_id': ObjectId(room['_id'])},
                {'$addToSet': {'students': user_name}}
            )
        return redirect(url_for('wait_room', room_id=str(room['_id'])))
    return render_template('join_room.html')

@app.route('/wait_room/<room_id>')
def wait_room(room_id):
    if 'user_id' not in session or session['role'] != 'student':
        logger.debug(f"Unauthorized access to wait_room {room_id}: {session}")
        return redirect(url_for('login'))
    room = rooms.find_one({'_id': ObjectId(room_id), 'status': {'$in': ['active', 'started', 'stopped']}})
    if not room or session['name'] not in room.get('students', []):
        return redirect(url_for('dashboard'))
    if room['status'] == 'started':
        return redirect(url_for('take_room_quiz', room_id=room_id))
    error = 'The quiz has been stopped by the teacher.' if room['status'] == 'stopped' else None
    return render_template('wait_room.html', room_id=room_id, error=error)

@app.route('/start_quiz/<room_id>')
def start_quiz(room_id):
    if 'user_id' not in session or session['role'] != 'teacher':
        logger.debug(f"Unauthorized access to start_quiz {room_id}: {session}")
        return redirect(url_for('login'))
    room = rooms.find_one({'_id': ObjectId(room_id), 'teacher_id': session['user_id']})
    if not room:
        return redirect(url_for('teacher_dashboard'))
    rooms.update_one(
        {'_id': ObjectId(room_id)},
        {'$set': {'status': 'started', 'start_time': datetime.datetime.now()}}
    )
    return redirect(url_for('room', room_id=room_id))

@app.route('/stop_quiz/<room_id>')
def stop_quiz(room_id):
    if 'user_id' not in session or session['role'] != 'teacher':
        logger.debug(f"Unauthorized access to stop_quiz {room_id}: {session}")
        return redirect(url_for('login'))
    room = rooms.find_one({'_id': ObjectId(room_id), 'teacher_id': session['user_id']})
    if not room:
        return redirect(url_for('teacher_dashboard'))
    rooms.update_one(
        {'_id': ObjectId(room_id)},
        {'$set': {'status': 'stopped', 'stop_time': datetime.datetime.now()}}
    )
    return redirect(url_for('room', room_id=room_id))

@app.route('/take_room_quiz/<room_id>', methods=['GET', 'POST'])
def take_room_quiz(room_id):
    if 'user_id' not in session or session['role'] != 'student':
        logger.debug(f"Unauthorized access to take_room_quiz {room_id}: {session}")
        return redirect(url_for('login'))
    room = rooms.find_one({'_id': ObjectId(room_id)})
    if not room or session['name'] not in room.get('students', []):
        return redirect(url_for('dashboard'))
    if room['status'] != 'started':
        error = 'The quiz is not active or has been stopped by the teacher.'
        return render_template('wait_room.html', room_id=room_id, error=error)
    if 'current_question' not in session or 'room_id' not in session or session['room_id'] != room_id:
        session['current_question'] = 0
        session['room_id'] = room_id
        session['answers'] = {}
        questions = room['questions']
        random.shuffle(questions)
        session['questions'] = questions
    current_question = session['current_question']
    questions = session['questions']
    if request.method == 'POST':
        user_answer = request.form.get(f'question_{current_question}')
        if user_answer:
            session['answers'][str(current_question)] = user_answer
        if 'next' in request.form and current_question < len(questions) - 1:
            session['current_question'] = current_question + 1
            return redirect(url_for('take_room_quiz', room_id=room_id))
        elif 'submit_quiz' in request.form or current_question >= len(questions) - 1:
            # Recheck room status to ensure quiz hasn't been stopped during submission
            room = rooms.find_one({'_id': ObjectId(room_id)})
            if room['status'] != 'started':
                error = 'The quiz has been stopped by the teacher.'
                return render_template('wait_room.html', room_id=room_id, error=error)
            answers = session.get('answers', {})
            score = 0
            results = []
            for i, question in enumerate(questions):
                user_answer = answers.get(str(i))
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
            user_name = session['name']
            user_collection = db[user_name]
            quiz_data = {
                'quiz_name': room['quiz_name'],
                'num_questions': room['num_questions'],
                'total_time': room['total_time'],
                'per_question_time': room['per_question_time'],
                'difficulty': room['difficulty'],
                'question_types': room['question_types'],
                'selection_mode': room['selection_mode'],
                'questions': questions,
                'results': results,
                'score': score,
                'room_id': room_id,
                'completed_at': datetime.datetime.now()
            }
            quiz_id = user_collection.insert_one(quiz_data).inserted_id
            rooms.update_one(
                {'_id': ObjectId(room_id)},
                {'$push': {'student_results': {'name': user_name, 'score': score, 'results': results, 'quiz_id': str(quiz_id)}}}
            )
            session.pop('current_question', None)
            session.pop('answers', None)
            session.pop('room_id', None)
            session.pop('questions', None)
            return render_template('take_quiz.html', quiz=room, results=results, score=score, show_results=True, room_id=room_id, quiz_id=str(quiz_id))
    return render_template('take_quiz.html', quiz=room, current_question=current_question, room_id=room_id)

@app.route('/room_status/<room_id>')
def room_status(room_id):
    logger.debug(f"Accessing room_status for {room_id} with session: {session}")
    room = rooms.find_one({'_id': ObjectId(room_id)})
    if not room:
        logger.debug(f"Room {room_id} not found")
        return jsonify({'error': 'Room not found'}), 404
    # Allow students to check status, but only teachers get detailed info
    response = {'status': room.get('status', 'active')}
    if 'user_id' in session and session['role'] == 'teacher' and room['teacher_id'] == session['user_id']:
        response.update({
            'num_students': len(room.get('students', [])),
            'students': room.get('students', [])
        })
    return jsonify(response)

@app.route('/score/<room_id>')
def score(room_id):
    if 'user_id' not in session or session['role'] != 'teacher':
        logger.debug(f"Unauthorized access to score {room_id}: {session}")
        return redirect(url_for('login'))
    room = rooms.find_one({'_id': ObjectId(room_id), 'teacher_id': session['user_id']})
    if not room:
        return redirect(url_for('teacher_dashboard'))
    student_results = room.get('student_results', [])
    leaderboard = sorted(student_results, key=lambda x: x['score'], reverse=True)
    scores = [result['score'] for result in student_results]
    num_questions = room['num_questions']
    score_distribution = [0] * (num_questions + 1)
    for score in scores:
        score_distribution[score] += 1
    return render_template('score.html', room=room, leaderboard=leaderboard, score_distribution=score_distribution)

@app.route('/take_quiz/<quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    if 'user_id' not in session:
        logger.debug(f"Unauthorized access to take_quiz {quiz_id}: {session}")
        return redirect(url_for('login'))
    user_name = session['name']
    user_collection = db[user_name]
    quiz = user_collection.find_one({'_id': ObjectId(quiz_id)})
    if not quiz:
        return redirect(url_for('dashboard'))
    if 'current_question' not in session or 'quiz_id' not in session or session['quiz_id'] != quiz_id:
        session['current_question'] = 0
        session['quiz_id'] = quiz_id
        session['answers'] = {}
    current_question = session['current_question']
    if request.method == 'POST':
        user_answer = request.form.get(f'question_{current_question}')
        if user_answer:
            session['answers'][str(current_question)] = user_answer
        if 'next' in request.form and current_question < len(quiz['questions']) - 1:
            session['current_question'] = current_question + 1
            return redirect(url_for('take_quiz', quiz_id=quiz_id))
        elif 'submit_quiz' in request.form or current_question >= len(quiz['questions']) - 1:
            answers = session.get('answers', {})
            score = 0
            results = []
            for i, question in enumerate(quiz['questions']):
                user_answer = answers.get(str(i))
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
            user_collection.update_one(
                {'_id': ObjectId(quiz_id)},
                {'$set': {'results': results, 'score': score, 'completed_at': datetime.datetime.now()}}
            )
            session.pop('current_question', None)
            session.pop('answers', None)
            session.pop('quiz_id', None)
            return render_template('take_quiz.html', quiz=quiz, results=results, score=score, show_results=True, quiz_id=quiz_id)
    return render_template('take_quiz.html', quiz=quiz, current_question=current_question, quiz_id=quiz_id)

@app.route('/download_results/<quiz_id>')
def download_results(quiz_id):
    if 'user_id' not in session:
        logger.debug(f"Unauthorized access to download_results {quiz_id}: {session}")
        return redirect(url_for('login'))
    user_name = session['name']
    user_collection = db[user_name]
    quiz = user_collection.find_one({'_id': ObjectId(quiz_id)})
    if not quiz or 'results' not in quiz:
        return "No results found", 404
    lines = [
        f"Quiz: {quiz.get('quiz_name', 'Unknown')}",
        f"Score: {quiz.get('score', 0)}/{quiz.get('num_questions', 0)}",
        "Results:\n"
    ]
    for i, result in enumerate(quiz['results'], 1):
        lines.append(f"{i}. {result['question']}")
        lines.append(f"   Your Answer: {result['user_answer'] or 'Not answered'}")
        lines.append(f"   Correct Answer: {result['correct_answer']}")
        lines.append(f"   Result: {'✅ Correct' if result['correct'] else '❌ Incorrect'}")
        lines.append(f"   Explanation: {result['explanation']}")
        lines.append("")
    content = "\n".join(lines)
    response = make_response(content)
    response.headers["Content-Disposition"] = f"attachment; filename=quiz_{quiz_id}_results.txt"
    response.headers["Content-Type"] = "text/plain"
    return response

@app.route('/download_room_results/<room_id>')
def download_room_results(room_id):
    if 'user_id' not in session or session['role'] != 'student':
        logger.debug(f"Unauthorized access to download_room_results {room_id}: {session}")
        return redirect(url_for('login'))
    user_name = session['name']
    room = rooms.find_one({'_id': ObjectId(room_id)})
    if not room or user_name not in room.get('students', []):
        return "Room not found or user not authorized", 404
    student_result = next((result for result in room.get('student_results', []) if result['name'] == user_name), None)
    if not student_result or 'results' not in student_result:
        return "No results found for this user in the room", 404
    lines = [
        f"Quiz: {room.get('quiz_name', 'Unknown')}",
        f"Score: {student_result.get('score', 0)}/{room.get('num_questions', 0)}",
        "Results:\n"
    ]
    for i, result in enumerate(student_result['results'], 1):
        lines.append(f"{i}. {result['question']}")
        lines.append(f"   Your Answer: {result['user_answer'] or 'Not answered'}")
        lines.append(f"   Correct Answer: {result['correct_answer']}")
        lines.append(f"   Result: {'✅ Correct' if result['correct'] else '❌ Incorrect'}")
        lines.append(f"   Explanation: {result['explanation']}")
        lines.append("")
    content = "\n".join(lines)
    response = make_response(content)
    response.headers["Content-Disposition"] = f"attachment; filename=room_quiz_{room_id}_results.txt"
    response.headers["Content-Type"] = "text/plain"
    return response

@app.route('/logout')
def logout():
    logger.debug(f"Logging out with session: {session}")
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('name', None)
    session.pop('current_question', None)
    session.pop('answers', None)
    session.pop('quiz_id', None)
    session.pop('room_id', None)
    session.pop('questions', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)