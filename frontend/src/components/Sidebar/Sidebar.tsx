import { useState, useRef, useEffect } from 'react'
import { createPortal } from 'react-dom'
import { logout } from '@/api'
import type { SidebarProps } from '@/types/components'
import type { ColumnMeta } from '@/types'
import { styles } from './Sidebar.styles'

interface SelectOption {
  value: string
  label: string
}

function CustomSelect({
  value,
  options,
  onChange,
  disabled,
  placeholder = 'Select...',
}: {
  value: string
  options: SelectOption[]
  onChange: (value: string) => void
  disabled?: boolean
  placeholder?: string
}) {
  const [open, setOpen] = useState(false)
  const [position, setPosition] = useState({ top: 0, left: 0, width: 0 })
  const triggerRef = useRef<HTMLButtonElement>(null)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const label = (options.find((o) => o.value === value)?.label ?? value) || placeholder

  useEffect(() => {
    if (!open || !triggerRef.current) return
    const rect = triggerRef.current.getBoundingClientRect()
    setPosition({
      top: rect.bottom + 2,
      left: rect.left,
      width: rect.width,
    })
  }, [open])

  useEffect(() => {
    if (!open) return
    const onDocClick = (e: MouseEvent) => {
      const target = e.target as Node
      if (triggerRef.current?.contains(target)) return
      if (dropdownRef.current?.contains(target)) return
      setOpen(false)
    }
    document.addEventListener('click', onDocClick, true)
    return () => document.removeEventListener('click', onDocClick, true)
  }, [open])

  return (
    <styles.SelectWrap>
      <styles.SelectTrigger
        ref={triggerRef}
        type="button"
        onClick={() => !disabled && setOpen((o) => !o)}
        disabled={disabled}
        aria-expanded={open}
        aria-haspopup="listbox"
      >
        <span>{label}</span>
        <styles.SelectArrow aria-hidden $open={open} />
      </styles.SelectTrigger>
      {open &&
        createPortal(
          <styles.SelectDropdown
            ref={dropdownRef}
            $top={position.top}
            $left={position.left}
            $width={position.width}
          >
            {options.map((opt) => (
              <styles.SelectOption
                key={opt.value}
                type="button"
                role="option"
                aria-selected={opt.value === value}
                $selected={opt.value === value}
                onClick={() => {
                  onChange(opt.value)
                  setOpen(false)
                }}
              >
                {opt.label}
              </styles.SelectOption>
            ))}
          </styles.SelectDropdown>,
          document.body
        )}
    </styles.SelectWrap>
  )
}

export default function Sidebar({
  schema,
  tables,
  selectedTable,
  onSelectTable,
  selectedLang,
  onSelectLang,
  languages,
  promptHistory,
  schemaLoading,
  onLogout,
}: SidebarProps) {
  const [schemaExpanded, setSchemaExpanded] = useState(false)
  const [loggingOut, setLoggingOut] = useState(false)
  const tableColumns: Record<string, ColumnMeta> =
    selectedTable && selectedTable !== 'None' ? schema[selectedTable] || {} : {}

  const handleLogout = async () => {
    if (!onLogout || loggingOut) return
    setLoggingOut(true)
    try {
      await logout()
      onLogout()
      window.location.reload()
    } catch {
      setLoggingOut(false)
    }
  }

  return (
    <styles.SidebarAside>
      <styles.Header>
        <styles.Logo
          src="/assets/logo.png"
          alt="Query Wizard"
          onError={(e) => {
            ;(e.target as HTMLImageElement).style.display = 'none'
          }}
        />
        {onLogout && (
          <styles.LogoutBtn
            type="button"
            onClick={handleLogout}
            disabled={loggingOut}
            title="Log out and clear cached schema"
            aria-label={loggingOut ? 'Logging out...' : 'Log out'}
          >
            <styles.LogoutIcon
              src="/assets/logout.png"
              alt=""
              aria-hidden
            />
          </styles.LogoutBtn>
        )}
      </styles.Header>

      <styles.Section>
        <styles.Heading>Database Tables</styles.Heading>
        <styles.Label>Select a Table</styles.Label>
        <CustomSelect
          value={selectedTable}
          options={[{ value: 'None', label: 'None' }, ...tables.map((t) => ({ value: t, label: t }))]}
          onChange={onSelectTable}
          disabled={schemaLoading}
          placeholder="Select a table"
        />

        {selectedTable && selectedTable !== 'None' && (
          <>
            <styles.Expander
              type="button"
              onClick={() => setSchemaExpanded((s) => !s)}
              aria-expanded={schemaExpanded}
            >
              {schemaExpanded ? '▼' : '▶'} {selectedTable} Schema
            </styles.Expander>
            {schemaExpanded && (
              <styles.SchemaDetail>
                {Object.entries(tableColumns).map(([col, details]) => (
                  <styles.SchemaRow key={col}>
                    <styles.SchemaDiamond>🔹</styles.SchemaDiamond>
                    <strong>{col}</strong>
                    <styles.SchemaType>: {details.type}</styles.SchemaType>
                  </styles.SchemaRow>
                ))}
                {/* <styles.DisplayAllBtn
                  type="button"
                  onClick={() => {
                    const event = new CustomEvent('display-all-records', {
                      detail: selectedTable,
                    })
                    window.dispatchEvent(event)
                  }}
                >
                  📋 Display All Records
                </styles.DisplayAllBtn> */}
              </styles.SchemaDetail>
            )}
          </>
        )}
      </styles.Section>

      <styles.Hr />

      <styles.Section>
        <styles.Heading>📝 Explanation Language</styles.Heading>
        <styles.Label>Select language for explanation</styles.Label>
        <CustomSelect
          value={selectedLang.code}
          options={languages.map((l) => ({ value: l.code, label: l.label }))}
          onChange={(code) => {
            const lang = languages.find((l) => l.code === code)
            if (lang) onSelectLang(lang)
          }}
          placeholder="Select language"
        />
      </styles.Section>

      <styles.Hr />

      <styles.Section>
        <styles.Heading>Query History</styles.Heading>
        {promptHistory.length === 0 ? (
          <styles.Info>No query history yet</styles.Info>
        ) : (
          <styles.HistoryList>
            {[...promptHistory].reverse().map((item, i) => (
              <styles.HistoryItem key={i}>
                <summary>Query {promptHistory.length - i}</summary>
                <styles.HistoryMeta>Time: {item.timestamp}</styles.HistoryMeta>
                <styles.HistoryMeta>User: {item.username}</styles.HistoryMeta>
                <hr />
                <p>
                  <strong>Original Prompt:</strong>
                </p>
                <styles.HistoryPrompt>{item.prompt}</styles.HistoryPrompt>
                <p>
                  <strong>Generated SQL:</strong>
                </p>
                <styles.HistorySql>{item.sql}</styles.HistorySql>
              </styles.HistoryItem>
            ))}
          </styles.HistoryList>
        )}
      </styles.Section>
    </styles.SidebarAside>
  )
}
