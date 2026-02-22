import type { Dispatch, SetStateAction } from 'react'
import type { SchemaMap, PromptHistoryItem, LanguageOption } from './index'

export interface LoginProps {
  onSuccess: () => void
}

export interface SidebarProps {
  schema: SchemaMap
  tables: string[]
  selectedTable: string
  onSelectTable: (table: string) => void
  selectedLang: LanguageOption
  onSelectLang: (lang: LanguageOption) => void
  languages: LanguageOption[]
  promptHistory: PromptHistoryItem[]
  schemaLoading: boolean
  onLogout?: () => void
}

export interface MainContentProps {
  schema: SchemaMap
  tables: string[]
  selectedTable: string
  selectedLang: LanguageOption
  promptHistory: PromptHistoryItem[]
  setPromptHistory: Dispatch<SetStateAction<PromptHistoryItem[]>>
  loading: boolean
  setLoading: (v: boolean) => void
  generateSql: (prompt: string, defaultTable: string | null) => Promise<{ sql: string }>
  executeSql: (sql: string) => Promise<{ success: boolean; results?: Record<string, unknown>[]; error?: string }>
  fixSql: (
    failedSql: string,
    errorMessage: string,
    originalPrompt?: string,
    defaultTable?: string | null
  ) => Promise<{ sql: string }>
  getExplanation: (sql: string, language: string) => Promise<{ explanation: string }>
}

export interface VoiceButtonProps {
  onResult: (text: string) => void
}
