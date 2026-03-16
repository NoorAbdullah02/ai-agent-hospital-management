# Hospital Appointment Management System

A complete web-based appointment scheduling system for hospitals using FastAPI backend and Streamlit frontend with PostgreSQL database.

## 🏥 Features

### Backend (FastAPI)
- **Schedule Appointments** - Create new patient appointments
- **Cancel Appointments** - Mark appointments as canceled
- **List Appointments** - View all active appointments
- PostgreSQL database with SQLAlchemy ORM
- RESTful API with automatic documentation

### Frontend (Streamlit)
- **User-friendly interface** with 3 main tabs
- **Schedule Appointments** - Easy form to book new appointments
- **Cancel Appointments** - Cancel existing appointments
- **View All Appointments** - Display appointments in a table with statistics
- Real-time connection status and error handling
- Configurable backend URL

## 📋 Project Structure

```
Voice-agent/
├── backend.py              # FastAPI application with endpoints
├── database.py             # SQLAlchemy models and database configuration
├── dummy_frontend.py       # Streamlit web interface
├── .env                    # Environment variables (PostgreSQL URL)
├── .env.example            # Template for environment variables
├── .gitignore              # Git ignore rules
└── requirements.txt        # Python dependencies
```

## 🔧 Tech Stack

- **Backend**: FastAPI 0.135.1
- **Frontend**: Streamlit
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLAlchemy 2.0.48
- **Server**: Uvicorn
- **Driver**: psycopg2-binary

## 📦 Installation

### Prerequisites
- Python 3.13+
- Virtual environment (venv)
- PostgreSQL database (Neon recommended)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/NoorAbdullah02/ai-agent-hospital-management.git
cd Voice-agent
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv streamlit requests pandas
```

4. **Configure database**
- Copy `.env.example` to `.env`
- Update `DATABASE_URL` with your PostgreSQL connection string:
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

## 🚀 Running the Application

### Start Backend Server (Terminal 1)
```bash
source .venv/bin/activate
uvicorn backend:app --reload
```
- Backend API will run at: `http://localhost:8000`
- API documentation at: `http://localhost:8000/docs`

### Start Frontend (Terminal 2)
```bash
source .venv/bin/activate
streamlit run dummy_frontend.py
```
- Frontend will run at: `http://localhost:8501`

## 📊 Database Models

### Appointment Table
- `id` - Primary key
- `patient_name` - Patient's full name
- `reason` - Reason for appointment
- `start_time` - Appointment date and time
- `canceled` - Boolean flag for cancellation status
- `created_at` - Timestamp of creation

## 🔌 API Endpoints

### Schedule Appointment
```
POST /schedule_appointments/
Content-Type: application/json

{
  "patient_name": "John Doe",
  "reason": "General checkup",
  "start_time": "2026-03-20T10:00:00"
}
```

### Cancel Appointment
```
POST /cancel_appointment/
Content-Type: application/json

{
  "patient_name": "John Doe",
  "date": "2026-03-20T10:00:00"
}
```

### List Appointments
```
GET /list_appointments/
```

## 🌐 Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://neondb_owner:password@host/database?sslmode=require&channel_binding=require
```

## 📝 Notes

- `.gitignore` includes Python, virtual environment, IDE, and environment variable files
- `.env` file is protected by `.gitignore` for security
- Use `.env.example` as a template for other developers
- Database tables are auto-created when the app starts

## 🤝 Contributing

1. Create a new branch for features
2. Commit changes with clear messages
3. Push to the repository
4. Create a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Noor Abdullah

## 🐛 Troubleshooting

### Connection Error
- Check if backend is running: `uvicorn backend:app --reload`
- Verify database URL in `.env`
- Ensure PostgreSQL is accessible

### Module Not Found
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use
- Backend (change port): `uvicorn backend:app --port 8001`
- Frontend (Streamlit handles automatically)

---

Happy coding! 🎉
