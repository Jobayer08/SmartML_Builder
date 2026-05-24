# SmartML Frontend - Quick Start Guide

## 🚀 Get Running in 2 Minutes

### Prerequisites
- Backend running on `http://localhost:8000` (with CORS enabled ✅)
- Node.js 16+ installed
- npm installed

### Start Frontend
```bash
cd frontend
npm install          # First time only
npm run dev          # Starts at http://localhost:5173
```

### Access the App
- Open browser to **http://localhost:5173**
- Register new account or login
- Start training models!

---

## 📁 Frontend Files Guide

### Pages (in `src/pages/`)
| Page | Purpose | Key Features |
|------|---------|--------------|
| **Login.jsx** | User authentication | Email/password, error handling, token storage |
| **Register.jsx** | New user signup | Email/password validation, auto-redirect to login |
| **Dashboard.jsx** | Main hub | Stats, quick navigation cards |
| **Datasets.jsx** | Manage datasets | Upload, list, delete datasets |
| **Models.jsx** | View models | List user's trained models with accuracy |
| **Train.jsx** | Train new model | CSV upload, target selection, auto FE |
| **Predict.jsx** | Make predictions | Model selection, input features, results |
| **History.jsx** | View predictions | All past predictions with timestamps |

### Components (in `src/components/`)
| Component | Used In | Purpose |
|-----------|---------|---------|
| **Navbar.jsx** | All pages | Top navigation, logout button |
| **Sidebar.jsx** | All pages | Left navigation, quick links |
| **ProtectedRoute.jsx** | App.jsx | Guards authenticated routes |
| **DatasetCard.jsx** | Datasets page | Display dataset info |
| **ModelCard.jsx** | Models page | Display model with action buttons |
| **PredictionCard.jsx** | History page | Display prediction result |

### Core Files
| File | Purpose |
|------|---------|
| **App.jsx** | Main app router, handles routing logic |
| **main.jsx** | Vite entry point |
| **context/AuthContext.jsx** | User auth state, login/logout |
| **api/api.js** | Axios config with token interceptor |

---

## 🔑 Key Workflows

### Registration & Login
```
1. Click "Register"
2. Enter email, password
3. Click "Sign Up"
4. System redirects to login
5. Enter credentials
6. Click "Login"
7. Redirected to dashboard (token saved)
```

### Training a Model
```
1. Dashboard → "Train Model"
2. Upload CSV file
3. Select target column (what to predict)
4. Enter model name
5. Click "Train Model"
6. System runs auto feature engineering + training
7. Success! Model ready for predictions
```

### Making a Prediction
```
1. Dashboard → "Predict"
2. Select trained model
3. Enter features (comma-separated)
4. Click "Predict"
5. View prediction result + confidence
6. Automatically saved to history
```

### Viewing History
```
1. Dashboard → "History"
2. See all past predictions
3. View model name, result, timestamp
4. Can filter by date/model
```

---

## 🧠 Understanding the Flow

### Authentication Flow
```
User Input → AuthContext.login() 
  ↓
API call to /login
  ↓
Token received from backend
  ↓
Token stored in localStorage
  ↓
User redirected to /dashboard
  ↓
Token auto-added to all future requests via Axios interceptor
```

### Training Flow
```
User uploads CSV → Train.jsx form
  ↓
FormData sent to /train-model/
  ↓
Backend: auto_feature_engineering() processes CSV
  ↓
Backend: Trains model with preprocessor
  ↓
Backend: Saves model to user_specific_directory
  ↓
Frontend: Shows success message
```

### Prediction Flow
```
User selects model + features → Predict.jsx form
  ↓
CSV sent to /predict-csv/
  ↓
Backend: Loads saved model + preprocessor
  ↓
Backend: Applies preprocessor to input
  ↓
Backend: Gets prediction
  ↓
Frontend: Displays result + confidence
  ↓
Prediction saved to history automatically
```

---

## 🎨 Styling Notes

- **Primary Color:** Blue (#3b82f6)
- **Success Color:** Green (#16a34a)
- **Error Color:** Red (#dc2626)
- **Cards:** White background with shadows
- **Gradients:** Used on Dashboard
- **Responsive:** Mobile-first approach

---

## 🐛 Troubleshooting

### "Connection refused" error?
- Ensure backend is running: `uvicorn app.main:app --reload`
- Check backend port: Should be `8000`
- Check CORS is enabled (✅ We added it)

### Token not persisting after refresh?
- Check browser allows localStorage
- Verify token is in DevTools → Application → localStorage
- Check for localStorage errors in console

### File upload not working?
- Ensure file is CSV format
- Check file size (shouldn't be huge)
- Verify FormData is being sent correctly

### Predictions failing?
- Select model from dropdown (required)
- Enter features in correct order (from training CSV)
- Check backend `/docs` for expected format

---

## 📊 API Endpoints Reference

```
POST   /login                      # Login user
POST   /register                   # Register new user
GET    /my-datasets                # List user's datasets
POST   /upload-dataset/            # Upload CSV dataset
GET    /my-models                  # List user's models
POST   /train-model/               # Train new model
POST   /predict-csv/               # Make CSV prediction
GET    /predictions/               # Get prediction history
```

---

## 💡 Pro Tips

1. **Use same feature order** - Train with CSV columns in order A,B,C then predict with same order
2. **Clear cache** - If pages look wrong, hard refresh (Ctrl+Shift+R)
3. **Check console** - F12 → Console tab for helpful error messages
4. **Test with sample data** - Start with simple datasets
5. **Monitor network** - F12 → Network tab to see API calls

---

## 🚀 Development Commands

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Check for issues
npm run lint        # If linter configured
```

---

## 📱 Device Support

✅ Desktop (1920px+)
✅ Laptop (1440px)
✅ Tablet (768px)
✅ Mobile (375px+)

All pages are fully responsive!

---

## 🎯 Next Steps After Deploy

1. **Test all workflows** - Registration → Training → Prediction → History
2. **Check responsive** - Test on phone/tablet
3. **Monitor errors** - Check browser console
4. **Verify token** - DevTools → localStorage
5. **Test file uploads** - Try different CSV files
6. **Check predictions** - Ensure models train and predict correctly

---

## 📞 Support

### For errors:
1. Check browser console (F12)
2. Check network tab for API responses
3. Verify backend is running
4. Check localStorage in DevTools
5. Review FRONTEND_COMPLETE.md for detailed docs

### Common Issues:
- **CORS Error** → Check backend CORS middleware
- **404 Not Found** → Check backend endpoint exists
- **Token Error** → Clear localStorage, login again
- **Build Error** → `rm -rf node_modules` then `npm install`

---

## ✨ Remember

This is a **production-ready** frontend for a **production-ready** backend. It includes:
- ✅ Automatic feature engineering (handled by backend)
- ✅ Multi-user isolation
- ✅ Secure JWT authentication
- ✅ Complete prediction workflows
- ✅ Professional UI/UX
- ✅ Mobile responsive design
- ✅ Error handling throughout

**Everything is ready to go!** 🚀

---

*SmartML Frontend - Ready for Production*
