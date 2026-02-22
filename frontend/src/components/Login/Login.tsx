import { useState, FormEvent } from 'react'
import { login } from '@/api'
import type { LoginProps } from '@/types/components'
import { styles } from './Login.styles'

export default function Login({ onSuccess }: LoginProps) {
  const [dbName, setDbName] = useState('')
  const [dbPassword, setDbPassword] = useState('')
  const [googleApiKey, setGoogleApiKey] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError('')
    if (!dbName.trim() || !dbPassword) {
      setError('Please enter database name and password.')
      return
    }
    setLoading(true)
    try {
      await login(dbName.trim(), dbPassword)
      onSuccess()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not save credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <styles.Page>
      <styles.LogoWrap>
          <styles.Logo src="/assets/logo.png" alt="Query Wizard" />
        </styles.LogoWrap>
      <styles.Box>

        <styles.Title>🔐 Login Credentials</styles.Title>
        <styles.Sub>
          Enter your DB credentials and API key.
        </styles.Sub>
        <styles.Form onSubmit={handleSubmit}>
          <label>
            Database name
            <input
              type="text"
              value={dbName}
              onChange={(e) => setDbName(e.target.value)}
              placeholder="Your Database Name"
              autoComplete="off"
            />
          </label>
          <label>
            Database password
            <input
              type="password"
              value={dbPassword}
              onChange={(e) => setDbPassword(e.target.value)}
              placeholder="Your Database Password"
            />
          </label>
          {/* <label>
            Google API key
            <input
              type="password"
              value={googleApiKey}
              onChange={(e) => setGoogleApiKey(e.target.value)}
              placeholder="AIza..."
              autoComplete="off"
            />
          </label> */}
          {error && <styles.Error>{error}</styles.Error>}
          <styles.Submit type="submit" disabled={loading}>
            {loading ? 'Saving...' : 'Save & continue'}
          </styles.Submit>
        </styles.Form>
      </styles.Box>
    </styles.Page>
  )
}
