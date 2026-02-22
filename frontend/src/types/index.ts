/** Column metadata from schema */
export interface ColumnMeta {
  type: string
  primary_key: boolean | null
  foreign_key: string | null
}

/** Table name -> column name -> ColumnMeta */
export type SchemaMap = Record<string, Record<string, ColumnMeta>>

/** Single history entry */
export interface PromptHistoryItem {
  prompt: string
  sql: string
  timestamp: string
  username: string
}

/** Language option for explanations */
export interface LanguageOption {
  label: string
  code: string
}

/** API: check-auth */
export interface CheckAuthResponse {
  authenticated: boolean
}

/** API: login */
export interface LoginResponse {
  ok?: boolean
}

/** API: schema */
export interface SchemaResponse {
  schema: SchemaMap
  tables: string[]
}

/** API: generate-sql, fix-sql */
export interface SqlResponse {
  sql: string
}

/** API: execute */
export interface ExecuteResponse {
  success: boolean
  results?: Record<string, unknown>[]
  error?: string
}

/** API: explanation */
export interface ExplanationResponse {
  explanation: string
}
