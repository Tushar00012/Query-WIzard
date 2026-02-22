import styled from 'styled-components'
import bgImage from '@/assets/image.png'

const Layout = styled.div`
  display: flex;
  min-height: 100vh;
  background: #f0f2f6;
`

const MainArea = styled.div`
  flex: 1;
  padding: 2rem;
  overflow: auto;
  margin-left: 21rem;
  background: #f0f2f6 url(${bgImage}) no-repeat center center fixed;
  background-size: cover;

  @media (max-width: 768px) {
    margin-left: 0;
  }
`

export const styles = {
  Layout,
  MainArea,
}
