import type {
  CheckAuthResponse,
  LoginResponse,
  SchemaResponse,
  SqlResponse,
  ExecuteResponse,
  ExplanationResponse,
} from '@/types'

const API = '/api'

export async function checkAuth(): Promise<boolean> {
  try {
    const r = await fetch(`${API}/check-auth`)
    const data: CheckAuthResponse = await r.json().catch(() => ({}))
    return data.authenticated === true
  } catch {
    return false
  }
}

export async function logout(): Promise<void> {
  const r = await fetch(`${API}/logout`, { method: 'POST' })
  if (!r.ok) {
    const err = await r.json().catch(() => ({ detail: r.statusText }))
    throw new Error((err as { detail?: string }).detail || 'Logout failed')
  }
}

export async function login(
  dbName: string,
  dbPassword: string,
  googleApiKey: string
): Promise<LoginResponse> {
  const r = await fetch(`${API}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      db_name: dbName,
      db_password: dbPassword,
      google_api_key: googleApiKey,
    }),
  })
  if (!r.ok) {
    const err = await r.json().catch(() => ({ detail: r.statusText }))
    throw new Error((err as { detail?: string }).detail || 'Login failed')
  }
  return r.json()
}

export async function getSchema(): Promise<SchemaResponse> {
  const r = await fetch(`${API}/schema`)
  if (!r.ok) throw new Error('Failed to load schema')
  return r.json()
}

export async function generateSql(
  prompt: string,
  defaultTable: string | null = null
): Promise<SqlResponse> {
  const r = await fetch(`${API}/generate-sql`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt, default_table: defaultTable || undefined }),
  })
  if (!r.ok) throw new Error(((await r.json()) as { detail?: string }).detail || 'Generate failed')
  return r.json()
}

export async function executeSql(sql: string): Promise<ExecuteResponse> {
  const r = await fetch(`${API}/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sql }),
  })
  const data: ExecuteResponse = await r.json()
  if (!r.ok) throw new Error(data.error || (data as { detail?: string }).detail || 'Execute failed')
  return data
}

export async function fixSql(
  failedSql: string,
  errorMessage: string,
  originalPrompt: string | null = null,
  defaultTable: string | null = null
): Promise<SqlResponse> {
  const r = await fetch(`${API}/fix-sql`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      failed_sql: failedSql,
      error_message: errorMessage,
      original_prompt: originalPrompt || undefined,
      default_table: defaultTable || undefined,
    }),
  })
  if (!r.ok) throw new Error(((await r.json()) as { detail?: string }).detail || 'Fix failed')
  return r.json()
}

export async function getExplanation(
  sql: string,
  language: string = 'en'
): Promise<ExplanationResponse> {
  const r = await fetch(`${API}/explanation`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sql, language }),
  })
  if (!r.ok)
    throw new Error(((await r.json()) as { detail?: string }).detail || 'Explanation failed')
  return r.json()
}
