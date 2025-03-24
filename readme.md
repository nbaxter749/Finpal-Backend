# FinPal: AI-Powered Student Financial Manager

FinPal is a mobile application designed to help students manage their finances effectively. The app allows users to track expenses, manage accounts, set budgeting goals, and receive AI-powered financial insights tailored specifically for students.

## Features

- **Account Management**: Track multiple financial accounts in one place
- **Expense Tracking**: Log and categorize expenses
- **Income Management**: Record and monitor various income sources
- **Debt Management**: Track student loans and other debts
- **Budget Insights**: Receive AI-powered recommendations to improve financial health
- **Financial Reports**: Generate printable reports summarizing financial status
- **Goal Setting**: Set financial goals and track progress

## Technology Stack

### Frontend
- React Native / Expo (SDK 52)
- React Navigation for routing
- Context API for state management
- Axios for API communication
- React Native Chart Kit for data visualization

### Backend
- FastAPI (Python)
- SQLAlchemy for ORM
- JWT Authentication
- Pandas and NumPy for data analysis
- Scikit-learn for AI recommendations

## Getting Started

### Prerequisites
-Node.js (v16 or later)
-npm or yarn
-Python 3.11+ (for backend)
-Expo Go app installed on your mobile device (or Android Studio for emulator)

### Frontend Setup
1. Clone the repository
2. Navigate to the frontend directory
   
   cd finpal/frontent

3. Install dependencies
   
   npm install --legacy-peer-deps

4. Update the API URL in src/config.js to match your local IP address export const API_URL = 'http://YOUR_LOCAL_IP:8000';
5. Start the application
   
   npm expo start

6. Choose one of the following options:
   Use the Expo Go app on your phone to scan the QR code
   Press 'a' to open in an Android emulator (requires Android Studio setup)
   Press 'w' to open in a web browser
   Press 't' to use tunnel mode if on a restricted network

### Backend Setup
1. Navigate to the backend directory
   
   cd finpal/backend

2. Create a virtual environment
   
   python -m venv venv
   
   venv\Scripts\activate

3. Install dependencies

   pip install -r requirements.txt
   
4. Create a `.env` file with the following content:

   DATABASE_URL=sqlite:///./finpal.db
   SECRET_KEY=your-secret-key-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

5. Start the backend server
   
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   

## Project Structure

### Frontend

frontend/
├── App.js                # Main application component
├── package.json          # Project dependencies
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── Button.js
│   │   ├── Card.js
│   │   ├── EmptyState.js
│   │   ├── InputField.js
│   │   └── LoadingScreen.js
│   ├── context/          # React Context for state management
│   │   ├── AuthContext.js
│   │   └── FinanceContext.js
│   ├── navigation/       # Navigation configuration
│   │   └── AppNavigator.js
│   ├── screens/          # Application screens
│   │   ├── auth/         # Authentication screens
│   │   │   ├── LoginScreen.js
│   │   │   └── RegisterScreen.js
│   │   └── main/         # Main application screens
│   │       ├── AccountDetailScreen.js
│   │       ├── AccountsScreen.js
│   │       ├── AddAccountScreen.js
│   │       ├── AddDebtScreen.js
│   │       ├── AddExpenseScreen.js
│   │       ├── AddGoalScreen.js
│   │       ├── AddIncomeScreen.js
│   │       ├── DashboardScreen.js
│   │       ├── DebtsScreen.js
│   │       ├── EditGoalScreen.js
│   │       ├── ExpensesScreen.js
│   │       ├── GoalsScreen.js
│   │       ├── IncomesScreen.js
│   │       └── ReportsScreen.js
│   ├── services/         # API services
│   │   ├── authService.js
│   │   └── financeService.js
│   ├── utils/            # Utility functions
│   │   ├── dateUtils.js
│   │   ├── formatCurrency.js
│   │   └── validators.js
│   └── config.js         # Configuration variables

### Backend
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