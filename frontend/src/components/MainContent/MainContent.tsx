import { useState, useEffect, useCallback } from 'react'
import type { MainContentProps, VoiceButtonProps } from '@/types/components'
import type { PromptHistoryItem } from '@/types'
import { styles } from './MainContent.styles'

declare global {
  interface Window {
    SpeechRecognition?: new () => SpeechRecognition
    webkitSpeechRecognition?: new () => SpeechRecognition
  }
}

interface MessageState {
  type: 'warning' | 'error'
  text: string
}

export default function MainContent({
  schema: _schema,
  tables,
  selectedTable,
  selectedLang,
  promptHistory,
  setPromptHistory,
  loading,
  setLoading,
  generateSql,
  executeSql,
  fixSql,
  getExplanation,
}: MainContentProps) {
  const [userInput, setUserInput] = useState('')
  const [generatedSql, setGeneratedSql] = useState('')
  const [lastError, setLastError] = useState<string | null>(null)
  const [apiError, setApiError] = useState<string | null>(null)
  const [queryResults, setQueryResults] = useState<Record<string, unknown>[] | null>(null)
  const [explanation, setExplanation] = useState('')
  const [explanationOpen, setExplanationOpen] = useState(false)
  const [message, setMessage] = useState<MessageState | null>(null)
  const [hasFixedSinceLastExecute, setHasFixedSinceLastExecute] = useState(false)

  const hasError = !!lastError || !!apiError

  const runExecute = useCallback(
    async (sql: string) => {
      setLoading(true)
      setMessage(null)
      setApiError(null)
      try {
        const data = await executeSql(sql)
        console.log('[Query Wizard] Execute response:', data)
        if (data.success) {
          setQueryResults(data.results ?? null)
          setLastError(null)
        } else {
          const errMsg = data.error || 'Execution failed'
          setLastError(errMsg)
          setQueryResults(null)
          console.error('[Query Wizard] Execute error:', errMsg)
        }
      } catch (err) {
        const errMsg = err instanceof Error ? err.message : 'Execution failed'
        setLastError(errMsg)
        setQueryResults(null)
        console.error('[Query Wizard] Execute error:', errMsg)
      } finally {
        setLoading(false)
      }
    },
    [executeSql, setLoading]
  )

  // Clear displayed table when user changes the selected table
  useEffect(() => {
    setQueryResults(null)
    setLastError(null)
  }, [selectedTable])

  useEffect(() => {
    const handler = (e: Event) => {
      const table = (e as CustomEvent<string>).detail
      if (table && tables.includes(table)) {
        const sql = `SELECT * FROM ${table} LIMIT 100;`
        setGeneratedSql(sql)
        setLastError(null)
        runExecute(sql)
      }
    }
    window.addEventListener('display-all-records', handler)
    return () => window.removeEventListener('display-all-records', handler)
  }, [tables, runExecute])

  const handleGenerate = async () => {
    if (!userInput.trim()) {
      setMessage({ type: 'warning', text: 'Please enter a query first.' })
      return
    }
    setMessage(null)
    setLoading(true)
    setLastError(null)
    setApiError(null)
    try {
      const defaultTable =
        selectedTable && selectedTable !== 'None' ? selectedTable : null
      const data = await generateSql(userInput, defaultTable)
      const sql = data.sql || ''
      if (sql.startsWith('AI Error:')) {
        setApiError(sql)
        console.error('[Query Wizard] Generate SQL error:', sql)
      } else {
        setGeneratedSql(sql)
        setApiError(null)
        if (sql) {
          setPromptHistory((prev: PromptHistoryItem[]) => [
            ...prev,
            {
              prompt: userInput,
              sql,
              timestamp: new Date().toISOString().slice(0, 19).replace('T', ' '),
              username: 'User',
            },
          ])
        }
      }
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : 'Generate SQL failed'
      setApiError(errMsg)
      console.error('[Query Wizard] Generate SQL error:', errMsg)
    } finally {
      setLoading(false)
    }
  }

  const handleExecute = () => {
    if (!generatedSql?.trim()) return
    setHasFixedSinceLastExecute(false)
    runExecute(generatedSql)
  }

  const handleDisplayTable = () => {
    if (!selectedTable || selectedTable === 'None') return
    const sql = `SELECT * FROM ${selectedTable} LIMIT 100;`
    runExecute(sql)
  }

  const handleFix = async () => {
    if (!hasError) return
    setLoading(true)
    setMessage(null)
    setApiError(null)
    try {
      const failedSql = generatedSql || ''
      const errorMsg = apiError || lastError || 'Unknown error'
      const defaultTable =
        selectedTable && selectedTable !== 'None' ? selectedTable : null
      const data = await fixSql(
        failedSql,
        errorMsg,
        userInput || undefined,
        defaultTable
      )
      const sql = data.sql || ''
      if (sql.startsWith('AI Error:')) {
        setApiError(sql)
        console.error('[Query Wizard] Fix SQL error:', sql)
      } else {
        setGeneratedSql(sql)
        setApiError(null)
        setLastError(null)
        setHasFixedSinceLastExecute(true)
      }
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : 'Fix SQL failed'
      setApiError(errMsg)
      console.error('[Query Wizard] Fix SQL error:', errMsg)
    } finally {
      setLoading(false)
    }
  }

  const loadExplanation = async () => {
    if (!generatedSql?.trim()) return
    try {
      const data = await getExplanation(generatedSql, selectedLang.code)
      setExplanation(data.explanation || '')
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : 'Failed to load explanation.'
      console.error('[Query Wizard] Explanation error:', errMsg)
      setExplanation('Failed to load explanation. See console for details.')
    }
  }

  const downloadCsv = () => {
    if (!queryResults || queryResults.length === 0) return
    const headers = Object.keys(queryResults[0])
    const csv = [
      headers.join(','),
      ...queryResults.map((row) =>
        headers.map((h) => JSON.stringify(row[h] ?? '')).join(',')
      ),
    ].join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'query_results.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <styles.Main>
      <styles.TitleWrap>
        <styles.TitleLogo src="/assets/logo.png" alt="" aria-hidden />
      </styles.TitleWrap>

      <styles.Section>
        <styles.Heading>Enter Your Query</styles.Heading>
        <styles.Textarea
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Type your natural language query here..."
          rows={6}
        />
        <styles.Buttons>
          <VoiceButton onResult={setUserInput} />
          <styles.BtnPrimary
            type="button"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Generate SQL'}
          </styles.BtnPrimary>
          {selectedTable && selectedTable !== 'None' && (
            <styles.BtnSecondary
              type="button"
              onClick={handleDisplayTable}
              disabled={loading}
            >
              Display Table
            </styles.BtnSecondary>
          )}
        </styles.Buttons>
        {message && (
          <styles.Message $variant={message.type}>{message.text}</styles.Message>
        )}
      </styles.Section>

      {(apiError || lastError) && (
        <styles.SectionError>
          <styles.ErrorBanner>
            <strong>Error (see browser console for details):</strong>
            <p>{apiError || lastError}</p>
          </styles.ErrorBanner>
        </styles.SectionError>
      )}

      {generatedSql && (
        <>
          <styles.Section>
            <styles.Heading>Generated SQL Query</styles.Heading>
            <styles.SqlBlock>{generatedSql}</styles.SqlBlock>
          </styles.Section>

          <styles.Section>
            <styles.Expander
              type="button"
              onClick={() => {
                setExplanationOpen((o) => !o)
                if (!explanationOpen && !explanation) loadExplanation()
              }}
              aria-expanded={explanationOpen}
            >
              {explanationOpen ? '▼' : '▶'} Query Explanation
            </styles.Expander>
            {explanationOpen && (
              <styles.ExplanationBox>
                <strong>{selectedLang.label}:</strong>
                <p>{explanation || 'Loading...'}</p>
              </styles.ExplanationBox>
            )}
          </styles.Section>

          <styles.Buttons>
            <styles.BtnPrimary type="button" onClick={handleExecute} disabled={loading}>
              Execute SQL
            </styles.BtnPrimary>
            {hasError && (
              <styles.BtnSecondary
                type="button"
                onClick={handleFix}
                disabled={loading || hasFixedSinceLastExecute}
                title={hasFixedSinceLastExecute ? 'Run Execute SQL first, then Fix again if it still fails' : undefined}
              >
                Fix Query
              </styles.BtnSecondary>
            )}
          </styles.Buttons>
        </>
      )}

      {queryResults && (
        <styles.Section>
          <styles.Heading>Query Results</styles.Heading>
          <styles.TableWrap>
            <styles.ResultsTable>
              <thead>
                <tr>
                  {queryResults.length > 0 &&
                    Object.keys(queryResults[0]).map((k) => (
                      <th key={k}>{k}</th>
                    ))}
                </tr>
              </thead>
              <tbody>
                {queryResults.map((row, i) => (
                  <tr key={i}>
                    {Object.values(row).map((v, j) => (
                      <td key={j}>{String(v)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </styles.ResultsTable>
          </styles.TableWrap>
        </styles.Section>
      )}

      {queryResults && queryResults.length > 0 && (
        <styles.Section>
          <styles.Heading>📥 Download Results</styles.Heading>
          <styles.BtnLink type="button" onClick={downloadCsv}>
            📥 Download CSV
          </styles.BtnLink>
        </styles.Section>
      )}
    </styles.Main>
  )
}

function VoiceButton({ onResult }: VoiceButtonProps) {
  const [listening, setListening] = useState(false)
  const [supported, setSupported] = useState(false)

  useEffect(() => {
    if (typeof window === 'undefined') return
    const Rec = window.SpeechRecognition || window.webkitSpeechRecognition
    setSupported(!!Rec)
  }, [])

  const startListening = () => {
    if (!supported) {
      alert('Speech recognition is not supported in this browser.')
      return
    }
    try {
      const Rec = window.SpeechRecognition || window.webkitSpeechRecognition
      if (!Rec) throw new Error('Speech recognition not available')
      const rec = new Rec()
      rec.continuous = false
      rec.interimResults = false
      rec.lang = 'en-US'
      setListening(true)
      rec.onresult = (e: SpeechRecognitionEvent) => {
        const text = e.results[0][0].transcript
        onResult(text)
        setListening(false)
      }
      rec.onerror = () => setListening(false)
      rec.onend = () => setListening(false)
      rec.start()
    } catch (err) {
      setListening(false)
      alert(
        'Could not start voice input: ' +
          (err instanceof Error ? err.message : 'Not supported')
      )
    }
  }

  return (
    <styles.BtnSecondary type="button" onClick={startListening} disabled={listening}>
      {listening ? '🎙️ Listening...' : 'Voice Input'}
    </styles.BtnSecondary>
  )
}
