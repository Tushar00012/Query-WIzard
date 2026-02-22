import styled from 'styled-components'

const Main = styled.main`
  padding: 2rem;
  max-width: 900px;
  background: transparent;
`

const TitleWrap = styled.h1`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0 0 1.5rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: #31333f;
  background: transparent;
`

const TitleLogo = styled.img`
  height: 5rem;
  width: auto;
  display: block;
  background: transparent;
`

const Section = styled.section`
  margin-bottom: 1.5rem;
`

const Heading = styled.h2`
  font-size: 1.25rem;
  margin: 0 0 0.75rem 0;
  color: #31333f;
  font-weight: 600;
`

const Textarea = styled.textarea`
  width: 100%;
  min-height: 150px;
  padding: 0.75rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;

  &:focus {
    outline: none;
    border-color: #ff4b4b;
    box-shadow: 0 0 0 1px #ff4b4b;
  }
`

const Buttons = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
`

const BaseBtn = styled.button`
  padding: 0.65rem 1.35rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: box-shadow 0.2s, background 0.2s, border-color 0.2s;

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
`

const BtnPrimary = styled(BaseBtn)`
  background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%);
  color: white;
  border: none;
  box-shadow: 0 2px 4px rgba(37, 99, 235, 0.3);

  &:hover:not(:disabled) {
    background: linear-gradient(180deg, #1d4ed8 0%, #1e40af 100%);
    box-shadow: 0 4px 8px rgba(37, 99, 235, 0.35);
  }
`

const BtnSecondary = styled(BaseBtn)`
  background: rgba(255, 255, 255, 0.95);
  color: #374151;
  border: 1px solid #d1d5db;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);

  &:hover:not(:disabled) {
    background: #fff;
    border-color: #9ca3af;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  }
`

const BtnLink = styled(BaseBtn)`
  background: transparent;
  color: #1f77b4;
  border: none;
  text-decoration: underline;

  &:hover {
    color: #1668a0;
  }
`

const Message = styled.div<{ $variant: 'warning' | 'error' }>`
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 5px;
  font-size: 0.95rem;
  background: ${(p) => (p.$variant === 'warning' ? '#fff3cd' : '#f8d7da')};
  color: ${(p) => (p.$variant === 'warning' ? '#856404' : '#721c24')};
  border: 1px solid ${(p) => (p.$variant === 'warning' ? '#ffc107' : '#f5c6cb')};
`

const SectionError = styled(Section)`
  margin-top: 0.5rem;
`

const ErrorBanner = styled.div`
  background: #fff3cd;
  border: 1px solid #ffc107;
  color: #856404;
  padding: 0.75rem 1rem;
  border-radius: 5px;
  font-size: 0.9rem;

  strong {
    display: block;
    margin-bottom: 0.35rem;
  }
  p {
    margin: 0;
    word-break: break-word;
  }
`

const SqlBlock = styled.pre`
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  padding: 1rem;
  overflow-x: auto;
  font-family: ui-monospace, monospace;
  font-size: 0.95rem;
  color: #31333f;
  margin: 0;
`

const Expander = styled.button`
  width: 100%;
  padding: 0.65rem 0;
  background: transparent;
  border: none;
  text-align: left;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  color: #31333f;

  &:hover {
    color: #ff4b4b;
  }
`

const ExplanationBox = styled.div`
  padding: 1rem;
  background: #000;
  color: #fff;
  border-radius: 5px;
  margin-top: 0.5rem;

  p {
    margin: 0.5rem 0 0 0;
    line-height: 1.5;
  }
`

const TableWrap = styled.div`
  overflow-x: auto;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
`

const ResultsTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;

  th,
  td {
    padding: 0.5rem 0.75rem;
    text-align: left;
    border-bottom: 1px solid #e8e8e8;
  }
  th {
    background: #f8f9fa;
    font-weight: 600;
    color: #31333f;
  }
  tr:hover {
    background: #f8f9fa;
  }
`

export const styles = {
  Main,
  TitleWrap,
  TitleLogo,
  Section,
  Heading,
  Textarea,
  Buttons,
  BtnPrimary,
  BtnSecondary,
  BtnLink,
  Message,
  SectionError,
  ErrorBanner,
  SqlBlock,
  Expander,
  ExplanationBox,
  TableWrap,
  ResultsTable,
}
