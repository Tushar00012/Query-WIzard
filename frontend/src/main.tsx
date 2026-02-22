import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { GlobalStyles } from './styles/GlobalStyles'

function AppWithBackground() {
  return (
    <>
      <GlobalStyles />
      <ErrorBoundary>
        <App />
      </ErrorBoundary>
    </>
  )
}

interface FallbackProps {
  error: Error | null
}

function Fallback({ error }: FallbackProps) {
  return (
    <div
      style={{
        padding: '2rem',
        fontFamily: 'sans-serif',
        textAlign: 'center',
      }}
    >
      <h1>Something went wrong</h1>
      <p style={{ color: '#666' }}>{error?.message || 'Unknown error'}</p>
    </div>
  )
}

interface ErrorBoundaryState {
  error: Error | null
}

interface ErrorBoundaryProps {
  children: React.ReactNode
}

class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = { error: null }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error }
  }

  render() {
    if (this.state.error) {
      return <Fallback error={this.state.error} />
    }
    return this.props.children
  }
}

const root = document.getElementById('root')
if (!root) {
  document.body.innerHTML = '<p>Root element not found.</p>'
} else {
  ReactDOM.createRoot(root).render(
    <React.StrictMode>
      <AppWithBackground />
    </React.StrictMode>
  )
}
