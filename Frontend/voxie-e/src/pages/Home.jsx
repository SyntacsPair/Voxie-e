import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import '../styles/Home.css'

function Home() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [inputText, setInputText] = useState('')
  const [outputText, setOutputText] = useState('')
  const [isPlaying, setIsPlaying] = useState(false)

  const handlePlay = () => {
    setIsPlaying(true)
    // TTS play logic here
  }

  const handlePause = () => {
    setIsPlaying(false)
    // TTS pause logic here
  }

  const handleGenerate = () => {
    // TTS generation logic here
    setOutputText(inputText)
  }

  const handleLogout = async () => {
    await logout()
    navigate('/')
  }

  return (
    <div className="container">
      <nav className="nav-links">
        {user ? (
          <>
            <div className="nav-user-badge">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
              </svg>
              {user.username}
            </div>
            <button className="nav-btn" onClick={handleLogout}>로그아웃</button>
          </>
        ) : (
          <>
            <Link to="/login" className="nav-btn">로그인</Link>
            <Link to="/signup" className="nav-btn nav-btn-primary">회원가입</Link>
          </>
        )}
      </nav>

      <div className="left-section">
        <img src="/mike.png" alt="Microphone" className="microphone-image" />
      </div>

      <div className="right-section">
        <div className="top-row">
          <div className="card player-card">
            <div className="text-display">
              <p>{outputText || 'Generated text will appear here...'}</p>
            </div>
            <div className="controls">
              <button className="control-btn" onClick={handlePlay}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </button>
              <button className="control-btn" onClick={handlePause}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
                </svg>
              </button>
            </div>
          </div>

          <div className="card info-card">
            <div className="info-content">
              <p className="info-title">Voice Settings</p>
              <p className="info-subtitle">Custom TTS</p>
            </div>
          </div>
        </div>

        <div className="bottom-row">
          <div className="card input-card">
            <div className="input-area">
              <textarea
                placeholder="Enter text to convert to speech..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
            </div>
            <button className="generate-btn" onClick={handleGenerate}>
              Generate Speech
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
