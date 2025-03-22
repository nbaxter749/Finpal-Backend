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
- React Native / Expo
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
- Node.js (v14 or later)
- npm or yarn
- Python 3.11+ (for backend)
- Expo CLI

### Frontend Setup
1. Clone the repository
2. Navigate to the frontend directory
   cd finpal/frontent
3. Install dependencies
   ```bash
   npm install
   ```
4. Start the application
   ```bash
   npm start
   ```
5. Use the Expo Go app on your phone to scan the QR code, or press 'a' to open in an Android emulator

### Backend Setup
1. Navigate to the backend directory
   ```bash
   cd finpal/backend
   ```
2. Create a virtual environment
   ```bash
    venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with the following content:
   ```
   DATABASE_URL=sqlite:///./finpal.db
   SECRET_KEY=your-secret-key-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
5. Start the backend server
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

### Frontend
```
frontend/
├── App.js                # Main application component
├── package.json          # Project dependencies
├── src/
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
│   │       ├── AddExpenseScreen.js
│   │       ├── DashboardScreen.js
│   │       ├── ExpensesScreen.js
│   │       └── ReportsScreen.js
│   ├── services/         # API services
│   │   ├── authService.js
│   │   └── financeService.js
│   └── config.js         # Configuration variables
```

### Backend
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database configuration
│   ├── models/           # Database models
│   ├── routes/           # API routes
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── ml/               # Machine learning modules
├── tests/                # Backend tests
├── .env                  # Environment variables
└── requirements.txt      # Python dependencies
```

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