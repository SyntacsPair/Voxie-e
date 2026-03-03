import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { generateTTS, fetchVoices, fetchHistory, deleteHistory } from '../api'
import '../styles/Home.css'

function Home() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const audioRef = useRef(null)

  // TTS 입력/출력
  const [inputText, setInputText] = useState('')
  const [outputText, setOutputText] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [audioUrl, setAudioUrl] = useState(null)

  // 음성 목록
  const [voices, setVoices] = useState([])
  const [selectedVoice, setSelectedVoice] = useState(null)

  // 히스토리
  const [history, setHistory] = useState([])
  const [showHistory, setShowHistory] = useState(false)

  // 에러
  const [error, setError] = useState('')

  // 음성 목록 로드
  useEffect(() => {
    fetchVoices()
      .then((data) => {
        setVoices(data)
        if (data.length > 0) setSelectedVoice(data[0])
      })
      .catch(() => {})
  }, [])

  // 히스토리 로드 (로그인 상태일 때)
  useEffect(() => {
    if (user) {
      fetchHistory()
        .then(setHistory)
        .catch(() => {})
    }
  }, [user])

  // 오디오 종료 이벤트
  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleEnded = () => setIsPlaying(false)
    audio.addEventListener('ended', handleEnded)
    return () => audio.removeEventListener('ended', handleEnded)
  }, [audioUrl])

  // TTS 생성
  const handleGenerate = async () => {
    if (!inputText.trim()) {
      setError('텍스트를 입력해주세요.')
      return
    }

    setError('')
    setIsGenerating(true)
    setOutputText(inputText)

    try {
      const blob = await generateTTS(inputText)
      const url = URL.createObjectURL(blob)

      // 이전 URL 해제
      if (audioUrl) URL.revokeObjectURL(audioUrl)

      setAudioUrl(url)
      setIsPlaying(false)

      // 로그인 상태면 히스토리 새로고침
      if (user) {
        fetchHistory().then(setHistory).catch(() => {})
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setIsGenerating(false)
    }
  }

  // 재생
  const handlePlay = () => {
    if (!audioUrl || !audioRef.current) return
    audioRef.current.play()
    setIsPlaying(true)
  }

  // 일시정지
  const handlePause = () => {
    if (!audioRef.current) return
    audioRef.current.pause()
    setIsPlaying(false)
  }

  // 히스토리 삭제
  const handleDeleteHistory = async (id) => {
    try {
      await deleteHistory(id)
      setHistory((prev) => prev.filter((item) => item.id !== id))
    } catch {
      setError('히스토리 삭제에 실패했습니다.')
    }
  }

  // 히스토리 항목 재생
  const handlePlayHistory = (item) => {
    if (item.audio_url) {
      if (audioUrl) URL.revokeObjectURL(audioUrl)
      setAudioUrl(item.audio_url)
      setOutputText(item.text)
      setIsPlaying(false)
      setTimeout(() => {
        if (audioRef.current) {
          audioRef.current.play()
          setIsPlaying(true)
        }
      }, 100)
    }
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
            <button
              className={`nav-btn ${showHistory ? 'nav-btn-active' : ''}`}
              onClick={() => setShowHistory(!showHistory)}
            >
              히스토리
            </button>
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

      {/* 히스토리 패널 */}
      {showHistory && user && (
        <div className="history-panel">
          <h3 className="history-title">생성 히스토리</h3>
          {history.length === 0 ? (
            <p className="history-empty">아직 생성된 히스토리가 없습니다.</p>
          ) : (
            <ul className="history-list">
              {history.map((item) => (
                <li key={item.id} className="history-item">
                  <div className="history-item-content">
                    <p className="history-text">{item.text}</p>
                    <div className="history-meta">
                      <span className="history-voice">{item.voice_name}</span>
                      <span className={`history-status history-status-${item.status.toLowerCase()}`}>
                        {item.status === 'COMPLETED' ? '완료' : '처리중'}
                      </span>
                    </div>
                  </div>
                  <div className="history-actions">
                    {item.status === 'COMPLETED' && item.audio_url && (
                      <button
                        className="history-action-btn"
                        onClick={() => handlePlayHistory(item)}
                        title="재생"
                      >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M8 5v14l11-7z"/>
                        </svg>
                      </button>
                    )}
                    <button
                      className="history-action-btn history-delete-btn"
                      onClick={() => handleDeleteHistory(item.id)}
                      title="삭제"
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                      </svg>
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* 숨겨진 오디오 엘리먼트 */}
      {audioUrl && <audio ref={audioRef} src={audioUrl} />}

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
              <button
                className={`control-btn ${isPlaying ? '' : 'control-btn-active'}`}
                onClick={handlePlay}
                disabled={!audioUrl}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </button>
              <button
                className={`control-btn ${isPlaying ? 'control-btn-active' : ''}`}
                onClick={handlePause}
                disabled={!audioUrl}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
                </svg>
              </button>
            </div>
          </div>

          <div className="card voice-card">
            <p className="voice-card-label">Voice</p>
            <div className="voice-grid">
              {voices.map((voice) => (
                <button
                  key={voice.id}
                  className={`voice-btn ${selectedVoice?.id === voice.id ? 'voice-btn-active' : ''}`}
                  onClick={() => setSelectedVoice(voice)}
                >
                  <span className="voice-btn-name">{voice.name}</span>
                  <span className={`voice-btn-gender voice-gender-${voice.gender.toLowerCase()}`}>
                    {voice.gender}
                  </span>
                  <span className="voice-btn-desc">{voice.desc}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="bottom-row">
          <div className="card input-card">
            <div className="input-area">
              <textarea
                placeholder="음성으로 변환할 텍스트를 입력하세요..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
            </div>
            {error && <p className="tts-error">{error}</p>}
            <button
              className="generate-btn"
              onClick={handleGenerate}
              disabled={isGenerating}
            >
              {isGenerating ? '생성 중...' : 'Generate Speech'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
