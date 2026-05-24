# SmartML Frontend

A production-ready React + Vite + TailwindCSS SaaS dashboard for ML model training, prediction, and management.

## Features

✅ **User Authentication** - Secure registration and login with JWT tokens  
✅ **Dataset Management** - Upload and manage training datasets  
✅ **Auto Feature Engineering** - Automatic preprocessing during training  
✅ **Model Training** - Train ML models with automatic feature engineering  
✅ **Predictions** - Make predictions using trained models  
✅ **History Tracking** - View all prediction history  
✅ **Multi-User Isolation** - Each user has isolated models and datasets  
✅ **Responsive Design** - Works on desktop and mobile  

## Installation

### Prerequisites
- Node.js 16+
- npm or yarn
- Backend API running on `http://localhost:8000`

### Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open `http://localhost:5173` in your browser

## Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Login.jsx         # User login page
│   │   ├── Register.jsx      # User registration
│   │   ├── Dashboard.jsx     # Main dashboard
│   │   ├── Datasets.jsx      # Dataset management
│   │   ├── Models.jsx        # Model listing
│   │   ├── Train.jsx         # Model training
│   │   ├── Predict.jsx       # Make predictions
│   │   └── History.jsx       # Prediction history
│   ├── components/
│   │   ├── Navbar.jsx        # Top navigation
│   │   ├── Sidebar.jsx       # Left sidebar navigation
│   │   ├── ProtectedRoute.jsx # Route protection
│   │   ├── DatasetCard.jsx   # Dataset display card
│   │   ├── ModelCard.jsx     # Model display card
│   │   └── PredictionCard.jsx # Prediction display card
│   ├── context/
│   │   └── AuthContext.jsx   # Authentication state
│   ├── api/
│   │   └── api.js            # Axios configuration
│   ├── App.jsx               # Main app component
│   └── main.jsx              # Entry point
└── public/                   # Static assets
```

## Key Components

### Authentication
- **AuthContext** - Manages user login state and JWT tokens
- **ProtectedRoute** - Wraps routes that require authentication
- Tokens stored in `localStorage` as `token`

### API Integration
- **api.js** - Axios instance with automatic token injection
- **Token Interceptor** - Adds JWT token to all requests

### Pages

#### Dashboard
Shows user statistics and quick links to main features

#### Datasets
- View uploaded datasets
- Upload new CSV files
- Delete datasets

#### Models
- List trained models
- View model accuracy
- Quick predict button

#### Train
- Upload CSV file
- Select target column
- Enter model name
- Auto feature engineering applied

#### Predict
- Select trained model
- Enter input features
- View prediction results

#### History
- View all past predictions
- Filter by model
- See prediction timestamps

## Available Scripts

### Development
```bash
npm run dev        # Start dev server on :5173
```

### Build
```bash
npm run build      # Build for production
npm run preview    # Preview production build
```

## Backend API Integration

The frontend communicates with the backend API using these endpoints:

```
POST   /login                      # User login
POST   /register                   # User registration
GET    /my-datasets                # List user's datasets
POST   /upload-dataset             # Upload dataset
GET    /my-models                  # List user's models
POST   /train-model                # Train a model
GET    /predictions                # Prediction history
POST   /predict-csv                # Make predictions
```

## Authentication Flow

1. User registers with email/password
2. Backend returns JWT token
3. Token stored in localStorage
4. Axios interceptor adds token to all requests
5. ProtectedRoute checks for token, redirects to login if missing
6. User logout clears token

## Styling

- **TailwindCSS** for utility-first styling
- **Gradient backgrounds** for visual appeal
- **Responsive grid layouts** for cards
- **Hover effects** and transitions
- **Color scheme**: Blue primary, Green success, Red error

## Environment Variables

Create `.env` file (optional):
```
VITE_API_URL=http://localhost:8000
```

Current setup uses `http://localhost:8000` as default API URL.

## Development Tips

1. **Hot Reload** - Changes reflect instantly in browser
2. **React DevTools** - Use browser extension for debugging
3. **Network Tab** - Monitor API calls in DevTools
4. **Console** - Check for errors and warnings

## Production Deployment

```bash
# Build production bundle
npm run build

# Deploy 'dist' folder to your hosting service
# (Vercel, Netlify, GitHub Pages, etc.)
```

## Troubleshooting

### CORS Error
- Ensure backend has CORS middleware configured
- Check backend is running on port 8000

### Token Not Persisting
- Check localStorage isn't disabled
- Verify token is being stored correctly in AuthContext

### API Calls Failing
- Check backend server is running
- Verify endpoints match backend implementation
- Check network tab in DevTools for error responses

### Build Errors
- Clear `node_modules` and `package-lock.json`
- Run `npm install` again
- Check Node version is 16+

## License

This project is part of SmartML Platform.
