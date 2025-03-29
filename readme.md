# FinPal: AI-Powered Student Financial Manager

FinPal is a mobile application designed to help students manage their finances effectively. The app allows users to track expenses, manage accounts, set budgeting goals, and receive AI-powered financial insights tailored specifically for students.

## Features
- 🔐 JWT Authentication
- 💰 Financial Data Management
- 🤖 AI-Powered Budget Analysis
- 📊 Financial Reporting
- 🔄 Real-time Data Processing
- 📱 Mobile-First API Design

## Tech Stack
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT with OAuth2
- **Data Analysis**: Pandas, NumPy
- **ML/AI**: Scikit-learn
- **API Documentation**: OpenAPI/Swagger

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Installation
1. Clone the repository:
```bash
git clone 
cd finpal/backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
python -m app.database
```

6. Run the development server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database configuration
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── services.py       # Business logic
│   ├── ml/               # Machine learning modules
│   │   └── budget_analyzer.py  # AI-powered budget analysis
│   └── routes/           # API routes
│       ├── auth.py       # Authentication endpoints
│       ├── finances.py   # Financial data endpoints
│       ├── reports.py    # Reporting endpoints
│       └── users.py      # User management endpoints
├── .env                  # Environment variables
├── finpal.db             # SQLite database
└── requirements.txt      # Python dependencies

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token

### Financial Management
- `GET /api/finances/summary` - Get financial summary
- `POST /api/finances/expenses` - Add new expense
- `GET /api/finances/expenses` - List expenses
- `POST /api/finances/incomes` - Add new income
- `GET /api/finances/incomes` - List incomes

### Reports
- `GET /api/reports/financial` - Generate financial report
- `GET /api/reports/insights` - Get AI-powered insights


## Contributing

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/new-feature
   ```
3. Commit your changes
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch
   ```bash
   git push origin feature/new-feature
   ```
5. Create a pull request

## License

This project is for educational purposes as part of the COM668 Computing Project at Ulster University.

## Acknowledgements

- Mentor: Bi Yaxin
- Project Support Group: F01

Created by: Nathan Baxter (B00787893)