# FinPal: AI-Powered Student Financial Manager

FinPal is a mobile application designed to help students manage their finances effectively. The app allows users to track expenses, manage accounts, set budgeting goals, and receive AI-powered financial insights tailored specifically for students.

## Features
- 🔐 JWT Authentication
- 💰 Financial Data Management
- 🤖 AI-Powered Budget Analysis (OpenAI Integration)
- 📊 Financial Reporting
- 🔄 Real-time Data Processing
- 📱 Mobile-First API Design

## Tech Stack
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT with OAuth2
- **Data Analysis**: Pandas, NumPy
- **AI Integration**: OpenAI GPT API
- **API Documentation**: OpenAPI/Swagger

## Quick Start

### Prerequisites
- Python 3.11 https://www.python.org/downloads/release/python-3110/ 
- pip (Python package manager)
- Git
- OpenAI API key (for AI-powered features)

### Installation
1. Clone the repository:
```bash
git clone 
cd finpal/backend
```

2. Create and activate virtual environment:
```bash
# Create a venv
python -m venv venv
# Activate a venv
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
# Edit .env with your configuration including your OpenAI API key
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
│   │   └── openai_budget_analyzer.py  # OpenAI-powered budget analysis
│   └── routes/           # API routes
│       ├── auth.py       # Authentication endpoints
│       ├── finances.py   # Financial data endpoints
│       ├── reports.py    # Reporting endpoints
│       └── users.py      # User management endpoints
├── .env                  # Environment variables
├── finpal.db             # SQLite database
└── requirements.txt      # Python dependencies

## API Endpoints

*(Note: All routes require authentication via JWT Bearer token in the Authorization header, except for `/users/` (POST) and `/token`)*

### Authentication (`/token`)
- `POST /token`: Login with username (email) and password in form data to receive an access token.

### Users (`/users/`)
- `POST /users/`: Register a new user.
- `GET /users/me`: Get the current authenticated user's profile.
- `PUT /users/me`: Update the current authenticated user's profile (email, first name, last name).

### Finances (Accounts, Expenses, Incomes, Debts, Goals)
- **Accounts (`/accounts/`)**
  - `POST /accounts/`: Create a new financial account.
  - `GET /accounts/`: List all financial accounts for the current user.
  - `GET /accounts/{account_id}`: Get details of a specific account.
  - `PUT /accounts/{account_id}`: Update details of a specific account.
  - `DELETE /accounts/{account_id}`: Delete a specific account.
- **Expenses (`/expenses/`)**
  - `POST /expenses/`: Add a new expense record.
  - `GET /expenses/`: List all expense records for the current user.
- **Incomes (`/incomes/`)**
  - `POST /incomes/`: Add a new income record.
  - `GET /incomes/`: List all income records for the current user.
- **Debts (`/debts/`)**
  - `POST /debts/`: Add a new debt record.
  - `GET /debts/`: List all debt records for the current user.
- **Goals (`/goals/`)**
  - `POST /goals/`: Create a new financial goal.
  - `GET /goals/`: List all financial goals for the current user.

### Reports (`/reports/`)
- `GET /reports/financial_summary`: Generate a comprehensive financial summary report for the current user, including AI-powered insights and recommendations.

## OpenAI Integration

FinPal uses OpenAI's GPT models to provide intelligent financial analysis and personalized recommendations. The integration:

1. Analyzes spending patterns across categories
2. Identifies trends in financial behavior
3. Generates tailored budget recommendations
4. Applies financial best practices (50/30/20 rule, etc.)

To use the OpenAI features:
1. Obtain an API key from [OpenAI Platform](https://platform.openai.com/)
2. Add your key to the `.env` file
3. Ensure sufficient expenses, income, and debt data for meaningful analysis

The system is designed to fall back to basic recommendations if the API is unavailable.

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