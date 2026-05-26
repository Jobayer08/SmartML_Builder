import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'

// Optional: Error Boundary component
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('App Error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-lg p-8 max-w-md text-center border border-red-200">
            <div className="text-6xl mb-4">😰</div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Something went wrong</h1>
            <p className="text-gray-600 mb-4">The application encountered an unexpected error.</p>
            <pre className="bg-red-50 p-3 rounded-lg text-xs text-red-700 mb-4 overflow-auto">
              {this.state.error?.message || 'Unknown error'}
            </pre>
            <button
              onClick={() => window.location.reload()}
              className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-2 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all"
            >
              🔄 Refresh Page
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

// Get the root element
const rootElement = document.getElementById('root')

// Check if root element exists
if (!rootElement) {
  throw new Error('Failed to find the root element. Make sure there is a <div id="root"></div> in your HTML.')
}

// Create root and render app with error boundary
const root = createRoot(rootElement)

root.render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>
)

// Log successful mount in development
if (process.env.NODE_ENV === 'development') {
  console.log('%c🚀 SmartML App Mounted Successfully', 'color: #3b82f6; font-size: 14px; font-weight: bold;')
  console.log('%cTheme: Light Blue ML Dashboard', 'color: #60a5fa; font-size: 12px;')
}