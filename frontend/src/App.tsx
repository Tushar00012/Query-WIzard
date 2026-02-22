import { useState, useEffect } from 'react'
import { checkAuth } from '@/api'
import Login from '@/components/Login/Login'
import QueryWizard from '@/components/QueryWizard/QueryWizard'

export default function App() {
  const [authenticated, setAuthenticated] = useState(false)

  useEffect(() => {
    checkAuth()
      .then((ok) => setAuthenticated(ok === true))
      .catch(() => setAuthenticated(false))
  }, [])

  const onLoginSuccess = () => setAuthenticated(true)

  if (!authenticated) {
    return <Login onSuccess={onLoginSuccess} />
  }

  return <QueryWizard />
}
