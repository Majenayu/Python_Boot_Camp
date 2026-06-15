# 📚 Aptitude Test & Learning Platform (Python Boot Camp)

<div align="center">

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-97.9%25-blue?style=flat-square)
![HTML](https://img.shields.io/badge/HTML-0.6%25-red?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen)

**A comprehensive quiz and learning platform for government schools featuring NCERT-based math questions, aptitude tests, and multilingual support**

[Live Demo](https://python-boot-camp.onrender.com/) • [Report Bug](https://github.com/Majenayu/Python_Boot_Camp/issues) • [Request Feature](https://github.com/Majenayu/Python_Boot_Camp/issues)

</div>

---

## 📋 Project Information

**Project Name:** Aptitude Test & Learning Platform (Python Boot Camp)  
**Developers:**  
- P G AYUSH RAI (majen) - [@Majenayu](https://github.com/Majenayu)  
- Shreyas - [@Shreyas140472](https://github.com/Shreyas140472)  

**Build Date:** 2023  
**Project Type:** Educational Web Application  
**Version:** 1.0.0  
**Live URL:** [python-boot-camp.onrender.com](https://python-boot-camp.onrender.com/)  
**Target Audience:** Government School Students (Grades 8-10)

---

## 🎯 About The Project

The Aptitude Test & Learning Platform is a comprehensive educational web application designed specifically for government school students. It provides an interactive learning environment with NCERT-based mathematics questions, aptitude tests, and multilingual support (English, Hindi, Kannada). The platform features both individual quiz creation and real-time classroom quizzes with teacher-student interaction.

### Key Features

✨ **NCERT Question Bank** - 60+ mathematics questions for grades 8th, 9th, and 10th  
🌐 **Multilingual Support** - English, Hindi (हिंदी), and Kannada (ಕನ್ನಡ)  
👨‍🏫 **Teacher Dashboard** - Create and manage live quiz rooms  
👨‍🎓 **Student Dashboard** - Join rooms, take quizzes, and track performance  
📊 **Real-Time Analytics** - Performance tracking and leaderboards  
🏆 **Leaderboard System** - Score ranking for competitive learning  
🔢 **Multiple Question Types** - Math, aptitude, mixture & alligation, profit & loss, etc.  
⏱️ **Live Quiz Rooms** - Real-time classroom quizzes with room codes  
📈 **Progress Tracking** - Individual analytics and quiz history  
💾 **Result Export** - Download quiz results in CSV format  
🎨 **Modern UI** - Responsive design with animated backgrounds  
🔐 **Secure Authentication** - Role-based access (Teacher/Student)  

---

## 🛠️ Technologies Used

### Backend
- **Python 3** - Core programming language
- **Flask 2.3.3** - Web application framework
- **MongoDB Atlas** - Cloud database solution
- **PyMongo 4.8.0** - MongoDB driver for Python
- **bcrypt 4.0.1** - Password hashing and security
- **Gunicorn 21.2.0** - WSGI HTTP Server for production

### Frontend
- **HTML5** - Structure and markup
- **CSS3** - Styling, animations, and responsive design
- **JavaScript (Vanilla)** - Client-side interactivity
- **SVG Animations** - Animated wave backgrounds

### External APIs
- **Aptitude API** (https://aptitude-api.vercel.app) - Additional aptitude questions

---

## 📂 Project Structure

```
Python_Boot_Camp/
│
├── app.py                          # Main Flask application (93,771 lines)
├── requirements.txt                # Python dependencies
│
├── templates/                      # HTML templates
│   ├── index.html                  # Landing page with animations
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── dashboard.html              # Student dashboard
│   ├── dashboard1.html             # Teacher dashboard
│   ├── create_quiz.html            # Quiz creation interface
│   ├── create_room.html            # Room creation for teachers
│   ├── join_room.html              # Room joining for students
│   ├── wait_room.html              # Waiting room before quiz starts
│   ├── room.html                   # Active quiz room
│   ├── take_quiz.html              # Quiz taking interface
│   ├── result.html                 # Quiz results display
│   ├── score.html                  # Leaderboard and scoring
│   └── analytics.html              # Performance analytics
│
├── static/                         # Static assets
│   ├── css/                        # Stylesheets
│   ├── js/                         # JavaScript files
│   └── images/                     # Images and icons
│
├── venv/                           # Virtual environment
│
└── README.md                       # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **MongoDB Atlas Account** (or local MongoDB instance)
- **pip** (Python package manager)
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Majenayu/Python_Boot_Camp.git
   cd Python_Boot_Camp
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB**
   - Update MongoDB connection string in `app.py`:
     ```python
     client = MongoClient('your-mongodb-connection-string')
     ```

5. **Set Flask secret key**
   ```bash
   export FLASK_SECRET_KEY='your-secret-key-here'
   # Or on Windows
   set FLASK_SECRET_KEY=your-secret-key-here
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser and navigate to:
     ```
     http://localhost:5000
     ```

---

## 📱 Platform Overview

### Landing Page
- Animated background with wave effects
- Clean, modern UI with gradient colors
- Quick access to Login/Register

### User Roles

#### 👨‍🎓 Student
- Create personal quizzes
- Join teacher-created quiz rooms
- Track performance with analytics
- Download quiz results
- View quiz history
- Access leaderboards

#### 👨‍🏫 Teacher
- Create live quiz rooms
- Generate unique room codes
- Monitor student participation
- Start/stop quizzes in real-time
- View class leaderboards
- Track student performance
- Download class results

---

## 🎓 NCERT Question Bank

### Grade 8th (20 Questions)
- **Triangles** - Angle properties, types of triangles
- **Basic Arithmetic** - BODMAS, multiplication
- **Squares & Square Roots** - Calculations and properties
- **Mensuration** - Area, perimeter, volume

### Grade 9th (20 Questions)
- **Polynomials** - Degree, factorization, operations
- **Triangles** - Types, angle calculations
- **Number Systems** - Rational, irrational, HCF, LCM

### Grade 10th (20 Questions)
- **Trigonometry** - sin, cos, tan values
- **Linear Equations** - Two variables, solutions
- **Polynomials** - Zeros, discriminant
- **Real Numbers** - Properties, operations
- **Triangles** - Theorems (Pythagoras, Sine Rule)

---

## 🌐 Multilingual Support

### Supported Languages

**English** - Default language  
**हिंदी (Hindi)** - Complete translation of questions, options, and explanations  
**ಕನ್ನಡ (Kannada)** - Full Kannada language support  

### Language Selection
- Users can select their preferred language
- Questions automatically display in chosen language
- Options and explanations also translated
- Language preference saved in session

---

## 💡 How It Works

### Individual Quiz Flow

1. **Create Quiz**
   - Select number of questions (1-50)
   - Choose difficulty level (Easy/Medium/Hard)
   - Select question types (Math, Aptitude, etc.)
   - Choose language preference

2. **Take Quiz**
   - Questions displayed one at a time
   - Navigate with "Next" button
   - Submit when complete

3. **View Results**
   - Instant feedback on answers
   - Detailed explanations
   - Score calculation
   - Download results as CSV

### Live Room Flow

1. **Teacher Creates Room**
   - Configure quiz settings
   - Receive unique 4-digit room code
   - Share code with students

2. **Students Join Room**
   - Enter room code
   - Wait in waiting room
   - Auto-redirect when quiz starts

3. **Live Quiz**
   - Teacher starts quiz
   - All students take quiz simultaneously
   - Real-time participation tracking

4. **Results & Leaderboard**
   - Instant score calculation
   - Class leaderboard display
   - Individual and class analytics
   - Export functionality

---

## 📊 Features Breakdown

### Completed Features ✅
- User authentication (bcrypt encryption)
- Role-based access (Teacher/Student)
- NCERT question bank (60 questions)
- Multilingual support (3 languages)
- Live quiz rooms with unique codes
- Real-time quiz monitoring
- Performance analytics
- Leaderboard system
- CSV result export
- Question randomization
- API integration for aptitude questions
- Responsive design
- Animated UI elements
- Session management
- MongoDB Atlas integration

### Future Enhancements 🚧
- [ ] Video tutorials
- [ ] Interactive study materials
- [ ] Practice mode with hints
- [ ] Timed quizzes
- [ ] Mobile app version
- [ ] Gamification (badges, achievements)
- [ ] Parent dashboard
- [ ] Homework assignments
- [ ] Discussion forums
- [ ] AI-powered question recommendations
- [ ] Offline mode
- [ ] Voice-based quizzes

---

## 🔧 API Integration

### Aptitude API
**Base URL:** `https://aptitude-api.vercel.app`

**Supported Topics:**
- Mixture and Alligation
- Profit and Loss
- Pipes and Cisterns
- Age Problems
- Permutation & Combination
- Speed, Time & Distance
- Simple Interest
- Calendars

**Usage:**
```python
response = requests.get(f"{APTITUDE_API_BASE_URL}/{topic}", params={'amount': num_questions})
```

---

## 💾 Database Schema

### Collections

#### users
```javascript
{
  name: String (unique per role),
  password: String (bcrypt hashed),
  role: String ('teacher' | 'student')
}
```

#### rooms
```javascript
{
  quiz_name: String,
  num_questions: Number,
  difficulty: String,
  question_types: Array,
  questions: Array,
  room_code: String (4 digits),
  teacher_id: ObjectId,
  students: Array<String>,
  student_results: Array,
  status: String ('active' | 'started' | 'stopped'),
  created_at: Date,
  start_time: Date,
  stop_time: Date
}
```

#### {username} Collections
```javascript
{
  quiz_name: String,
  num_questions: Number,
  difficulty: String,
  question_types: Array,
  questions: Array,
  results: Array,
  score: Number,
  room_id: ObjectId (optional),
  created_at: Date,
  completed_at: Date
}
```

---

## 🌐 Deployment

### Deploy to Render

1. **Create Render account** and link GitHub

2. **Configure Build Settings**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

3. **Set Environment Variables**
   ```
   FLASK_SECRET_KEY=your-secret-key
   MONGODB_URI=your-mongodb-connection-string
   ```

4. **Deploy**
   - Auto-deploys on push to master
   - Access via: https://python-boot-camp.onrender.com/

---

## 🔒 Security Features

- **Password Hashing** - bcrypt with salt rounds
- **Session Management** - Secure Flask sessions
- **Role-Based Access** - Separate teacher/student permissions
- **Input Validation** - Server-side validation
- **MongoDB Security** - Sanitized queries with PyMongo
- **HTTPS** - Secure connections in production

---

## 🐛 Known Issues

- Room codes limited to 4 digits (max 10,000 rooms)
- No password reset functionality
- Limited to 3 languages currently
- No email verification

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add some NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📄 License

This project is part of an educational initiative for government schools.  
For licensing inquiries, please contact the developers.

---

## 👥 Development Team

**P G AYUSH RAI (majen)**
- GitHub: [@Majenayu](https://github.com/Majenayu)
- Role: Lead Developer

**Shreyas**
- GitHub: [@Shreyas140472](https://github.com/Shreyas140472)
- Role: Contributor

---

## 🙏 Acknowledgments

- **Government Schools** - For providing requirements and feedback
- **NCERT** - For curriculum-aligned questions
- **MongoDB** - For cloud database services
- **Aptitude API** - For additional question resources
- **Render** - For hosting platform
- **Flask Community** - For excellent documentation

---

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/Majenayu/Python_Boot_Camp/issues)
- Contact: P G AYUSH RAI (majen) [@Majenayu](https://github.com/Majenayu)

---

## 📈 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

<div align="center">

**Made with ❤️ for Government School Students by P G AYUSH RAI (majen) & Shreyas**

⭐ Star this repository if you find it helpful!

**Learn** | **Practice** | **Excel**

</div>
