import styled from 'styled-components'
import bgImage from '@/assets/image.png'

const Page = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #f0f2f6 url(${bgImage}) no-repeat center center fixed;
  background-size: cover;
`

const Box = styled.div`
  max-width: 420px;
  width: 100%;
  padding: 2.5rem 2rem;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  background: #fff;
`

const Title = styled.h1`
  font-size: 1.75rem;
  margin: 0 0 0.25rem 0;
  font-weight: 600;
  color: #31333f;
`

const Sub = styled.p`
  color: #6c757d;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
  line-height: 1.4;

  code {
    background: #f0f2f6;
    padding: 0.1em 0.4em;
    border-radius: 4px;
    font-size: 0.9em;
  }
`

const Form = styled.form`
  label {
    display: block;
    margin-bottom: 1rem;
    font-weight: 500;
    color: #31333f;
  }
  input {
    display: block;
    width: 100%;
    margin-top: 0.35rem;
    padding: 0.5rem 0.75rem;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    font-size: 1rem;
  }
  input:focus {
    outline: none;
    border-color: #ff4b4b;
    box-shadow: 0 0 0 1px #ff4b4b;
  }
`

const Error = styled.div`
  color: #ff4b4b;
  font-size: 0.9rem;
  margin-bottom: 1rem;
`

const Submit = styled.button`
  width: 100%;
  padding: 0.7rem 1rem;
  border-radius: 8px;
  border: none;
  background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(37, 99, 235, 0.3);
  transition: box-shadow 0.2s, background 0.2s;

  &:hover:not(:disabled) {
    background: linear-gradient(180deg, #1d4ed8 0%, #1e40af 100%);
    box-shadow: 0 4px 8px rgba(37, 99, 235, 0.35);
  }
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
`

export const styles = {
  Page,
  Box,
  Title,
  Sub,
  Form,
  Error,
  Submit,
}
