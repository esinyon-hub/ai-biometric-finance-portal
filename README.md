# AI Biometric Finance Portal

A secure fintech system using **AI-powered biometric authentication** (face recognition) for user login and financial transactions.

## Features
- Face Recognition Login
- Secure Transactions
- Fraud Detection (AI)
- User Dashboard

## Tech Stack
- Django (Python)
- OpenCV (for face recognition)
- HTML / CSS / JavaScript
- SQLite / MySQL

## Project Structure
- `finance_portal/` → Main Django project  
- `portal/` → App for user authentication and finance management  
- `media/faces/` → Biometric images  
- `manage.py` → Django entry point  

## Usage
1. Clone the repo  
2. Create a virtual environment  
3. Install dependencies: `pip install -r requirements.txt`  
4. Run the server: `python manage.py runserver`  

---

## 🔒 Note
- `db.sqlite3` and `.env` are excluded for security  
- Add your own database and environment variables to run
