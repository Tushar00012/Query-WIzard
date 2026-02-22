import styled from 'styled-components'
import sidebarBg from '@/assets/sidebarBg.png'

const SidebarAside = styled.aside`
  width: 21rem;
  min-width: 21rem;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  padding: 1.5rem 1rem;
  overflow-y: auto;
  border-right: 1px solid #e0e0e0;
  isolation: isolate;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: -1;
    background: #f0f2f6 url(${sidebarBg}) no-repeat center center;
    background-size: 300% 100%;
    filter: blur(10px);
    transform: scale(1.05);
  }
`

const Header = styled.div`
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  background: transparent;
`

const Logo = styled.img`
  width: 10rem;
  height: auto;
  object-fit: contain;
  flex-shrink: 0;
  background: transparent;
  display: block;
`

const Title = styled.span`
  font-weight: 600;
  font-size: 1.1rem;
  color: #31333f;
`

const LogoutBtn = styled.button`
  margin-left: auto;
  padding: 0.35rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;

  &:hover:not(:disabled) {
    opacity: 0.9;
    transform: scale(1.05);
  }
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`

const LogoutIcon = styled.img`
  display: block;
  width: 2rem;
  height: 2rem;
  object-fit: contain;
`

const Section = styled.section`
  margin-bottom: 1rem;
`

const Heading = styled.h3`
  font-size: 1rem;
  margin: 0 0 0.5rem 0;
  color: #31333f;
  font-weight: 600;
`

const Label = styled.label`
  display: block;
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0.35rem;
`

const SelectWrap = styled.div`
  position: relative;
  width: 100%;
`

const SelectTrigger = styled.button`
  width: 100%;
  padding: 0.55rem 0.85rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.95);
  font-size: 0.95rem;
  color: #31333f;
  text-align: left;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  transition: border-color 0.2s, box-shadow 0.2s;

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
  &:hover:not(:disabled) {
    border-color: #6366f1;
    box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.2);
  }
`

const SelectArrow = styled.span<{ $open?: boolean }>`
  display: inline-block;
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 6px solid #6b7280;
  transform: ${(p) => (p.$open ? 'rotate(180deg)' : 'none')};
  transition: transform 0.2s;
  flex-shrink: 0;
`

const SelectDropdown = styled.div<{ $width: number; $top: number; $left: number }>`
  position: fixed;
  top: ${(p) => p.$top}px;
  left: ${(p) => p.$left}px;
  width: ${(p) => p.$width}px;
  max-height: 220px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
  z-index: 10000;
`

const SelectOption = styled.button<{ $selected?: boolean }>`
  display: block;
  width: 100%;
  padding: 0.55rem 0.85rem;
  border: none;
  font-size: 0.95rem;
  text-align: left;
  cursor: pointer;
  transition: background 0.15s;
  background: ${(p) => (p.$selected ? '#2563eb' : 'transparent')};
  color: ${(p) => (p.$selected ? '#fff' : '#31333f')};

  &:hover {
    background: ${(p) => (p.$selected ? '#1d4ed8' : 'rgba(37, 99, 235, 0.12)')};
  }
  &:not(:last-child) {
    border-bottom: 1px solid #f3f4f6;
  }
`

const Expander = styled.button`
  width: 100%;
  margin-top: 0.75rem;
  padding: 0.5rem 0;
  background: transparent;
  border: none;
  text-align: left;
  font-size: 0.95rem;
  cursor: pointer;
  color: #31333f;

  &:hover {
    color: #ff4b4b;
  }
`

const SchemaDetail = styled.div`
  padding: 0.75rem 0;
  border-top: 1px solid #e8e8e8;
`

const SchemaRow = styled.div`
  font-size: 0.9rem;
  margin-bottom: 0.35rem;
  color: #31333f;
`

const SchemaDiamond = styled.span`
  margin-right: 0.35rem;
`

const SchemaType = styled.span`
  color: #6c757d;
  font-family: monospace;
`

const Btn = styled.button`
  width: 100%;
  margin-top: 0.75rem;
  padding: 0.65rem 1rem;
  border-radius: 5px;
  border: 1px solid #e0e0e0;
  background: #fff;
  font-size: 0.95rem;
  cursor: pointer;
  color: #31333f;

  &:hover {
    background: #e8e8e8;
    border-color: #ccc;
  }
`

const DisplayAllBtn = styled(Btn)`
  border-color: #ff4b4b;
  color: #ff4b4b;

  &:hover {
    background: #fff5f5;
  }
`

const Hr = styled.hr`
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 1rem 0;
`

const Info = styled.p`
  font-size: 0.9rem;
  color: #6c757d;
  margin: 0;
`

const HistoryList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`

const HistoryItem = styled.details`
  font-size: 0.9rem;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  padding: 0.5rem 0.75rem;
  background: #fff;

  summary {
    cursor: pointer;
    font-weight: 500;
  }
`

const HistoryMeta = styled.p`
  margin: 0.25rem 0;
  color: #6c757d;
  font-size: 0.85rem;
`

const HistoryPrompt = styled.div`
  background: #000;
  color: #fff;
  padding: 0.5rem;
  border-radius: 5px;
  margin: 0.5rem 0;
  font-size: 0.85rem;
`

const HistorySql = styled.pre`
  background: #f8f9fa;
  padding: 0.5rem;
  border-radius: 5px;
  overflow-x: auto;
  font-size: 0.8rem;
  margin: 0.5rem 0 0 0;
`

export const styles = {
  SidebarAside,
  Header,
  Logo,
  LogoutBtn,
  LogoutIcon,
  Title,
  Section,
  Heading,
  Label,
  SelectWrap,
  SelectTrigger,
  SelectArrow,
  SelectDropdown,
  SelectOption,
  Expander,
  SchemaDetail,
  SchemaRow,
  SchemaDiamond,
  SchemaType,
  Btn,
  DisplayAllBtn,
  Hr,
  Info,
  HistoryList,
  HistoryItem,
  HistoryMeta,
  HistoryPrompt,
  HistorySql,
}
