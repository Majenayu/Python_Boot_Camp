# Python Boot Camp

Python Boot Camp is a Flask/MongoDB learning platform with student and teacher
flows for individual quizzes and room-based quizzes. The server renders HTML
templates, keeps login and quiz state in Flask sessions, and exports quiz
results as CSV.

## User workflows

- Register and log in with a selected role.
- Select English, Hindi, or Kannada for supported content.
- Students create or take quizzes and review analytics.
- Teachers create rooms, admit students with room codes, start/stop quizzes,
  and view room scores.
- Results and room results can be downloaded from dedicated CSV endpoints.

The route implementation in `app.py` is the authoritative behavior; the
repository does not contain a separate REST service or frontend build.

## Requirements and local setup

`requirements.txt` pins Flask 2.3.3, PyMongo 4.8.0, bcrypt 4.0.1, requests
2.32.3, and Gunicorn 21.2.0.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
export FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python app.py
```

Set the MongoDB connection and secret through deployment configuration. The
checked-in application currently contains a database connection fallback, so
do not reuse that value or commit credentials.

Open `http://127.0.0.1:5000/` unless the application configuration changes the
port. Production deployments can use Gunicorn:

```bash
gunicorn app:app
```

## Important routes

```text
/                         landing page
/login, /register         authentication
/dashboard, /analytics    student views
/teacher_dashboard        teacher view
/create_quiz              individual quiz creation
/create_room, /join_room  live room setup/joining
/room/<room_id>            room view and status
/take_quiz/<quiz_id>      individual quiz attempt
/take_room_quiz/<room_id> room quiz attempt
/score/<room_id>           leaderboard and distribution
/download_results/...      CSV exports
/logout                   session logout
```

## Data and security notes

MongoDB stores users, quizzes, rooms, attempts, and related progress. Passwords
are hashed with bcrypt. Sessions carry role, language, and quiz context.
Before production use, rotate any connection fallback, set a strong
`FLASK_SECRET_KEY`, validate authorization on every teacher/student action, and
serve behind HTTPS. The repository does not include a formal schema migration,
CI pipeline, or automated test suite.

## Layout

```text
app.py              # Flask app, persistence, routes, quiz logic
*.html              # server-rendered templates
static/             # browser assets
requirements.txt    # Python dependencies
CHANGELOG.md        # historical notes
```
