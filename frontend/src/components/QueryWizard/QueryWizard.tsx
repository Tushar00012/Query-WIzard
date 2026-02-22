import { useState, useEffect, useCallback } from 'react'
import {
  getSchema,
  generateSql,
  executeSql,
  fixSql,
  getExplanation,
} from '@/api'
import type { SchemaMap, PromptHistoryItem, LanguageOption } from '@/types'
import Sidebar from '../Sidebar/Sidebar'
import MainContent from '../MainContent/MainContent'
import { styles } from './QueryWizard.styles'

export const LANGUAGES: LanguageOption[] = [
  { label: '🇺🇸 English', code: 'en' },
  { label: '🇪🇸 Spanish', code: 'es' },
  { label: '🇫🇷 French', code: 'fr' },
  { label: '🇩🇪 German', code: 'de' },
  { label: '🇮🇳 Hindi', code: 'hi' },
  { label: '🇨🇳 Chinese', code: 'zh' },
  { label: '🇯🇵 Japanese', code: 'ja' },
  { label: '🇷🇺 Russian', code: 'ru' },
]

export default function QueryWizard() {
  const [schema, setSchema] = useState<SchemaMap>({})
  const [tables, setTables] = useState<string[]>([])
  const [selectedTable, setSelectedTable] = useState('None')
  const [selectedLang, setSelectedLang] = useState<LanguageOption>(LANGUAGES[0])
  const [promptHistory, setPromptHistory] = useState<PromptHistoryItem[]>([])
  const [loading, setLoading] = useState(false)
  const [schemaLoading, setSchemaLoading] = useState(true)

  const loadSchema = useCallback(async () => {
    setSchemaLoading(true)
    try {
      const data = await getSchema()
      setSchema(data.schema || {})
      setTables(data.tables || [])
    } catch {
      setSchema({})
      setTables([])
    } finally {
      setSchemaLoading(false)
    }
  }, [])

  useEffect(() => {
    loadSchema()
  }, [loadSchema])

  return (
    <styles.Layout>
      <Sidebar
        schema={schema}
        tables={tables}
        selectedTable={selectedTable}
        onSelectTable={setSelectedTable}
        selectedLang={selectedLang}
        onSelectLang={setSelectedLang}
        languages={LANGUAGES}
        promptHistory={promptHistory}
        schemaLoading={schemaLoading}
      />
      <styles.MainArea>
        <MainContent
          schema={schema}
          tables={tables}
          selectedTable={selectedTable}
          selectedLang={selectedLang}
          promptHistory={promptHistory}
          setPromptHistory={setPromptHistory}
          loading={loading}
          setLoading={setLoading}
          generateSql={generateSql}
          executeSql={executeSql}
          fixSql={fixSql}
          getExplanation={getExplanation}
        />
      </styles.MainArea>
    </styles.Layout>
  )
}
