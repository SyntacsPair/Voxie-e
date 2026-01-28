import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import '../styles/Signup.css'

function Signup() {
  const navigate = useNavigate()
  const { signup } = useAuth()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    passwordConfirm: '',
    nickname: ''
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  const validatePassword = (password) => {
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$/
    return passwordRegex.test(password)
  }

  const validateNickname = (nickname) => {
    const nicknameRegex = /^[가-힣a-zA-Z0-9]{1,8}$/
    return nicknameRegex.test(nickname)
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))

    // 실시간 유효성 검사
    const newErrors = { ...errors }

    if (name === 'email') {
      if (value && !validateEmail(value)) {
        newErrors.email = '올바른 이메일 형식을 입력해주세요.'
      } else {
        delete newErrors.email
      }
    }

    if (name === 'password') {
      if (value && !validatePassword(value)) {
        newErrors.password = '8~20자, 영문+숫자+특수문자 조합으로 입력해주세요.'
      } else {
        delete newErrors.password
      }
    }

    if (name === 'passwordConfirm') {
      if (value && value !== formData.password) {
        newErrors.passwordConfirm = '비밀번호가 일치하지 않습니다.'
      } else {
        delete newErrors.passwordConfirm
      }
    }

    if (name === 'nickname') {
      if (value && !validateNickname(value)) {
        newErrors.nickname = '1~8자, 한글/영문/숫자만 가능합니다.'
      } else {
        delete newErrors.nickname
      }
    }

    setErrors(newErrors)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    // 전체 유효성 검사
    const newErrors = {}

    if (!formData.email) {
      newErrors.email = '이메일을 입력해주세요.'
    } else if (!validateEmail(formData.email)) {
      newErrors.email = '올바른 이메일 형식을 입력해주세요.'
    }

    if (!formData.password) {
      newErrors.password = '비밀번호를 입력해주세요.'
    } else if (!validatePassword(formData.password)) {
      newErrors.password = '8~20자, 영문+숫자+특수문자 조합으로 입력해주세요.'
    }

    if (!formData.passwordConfirm) {
      newErrors.passwordConfirm = '비밀번호 확인을 입력해주세요.'
    } else if (formData.password !== formData.passwordConfirm) {
      newErrors.passwordConfirm = '비밀번호가 일치하지 않습니다.'
    }

    if (!formData.nickname) {
      newErrors.nickname = '닉네임을 입력해주세요.'
    } else if (!validateNickname(formData.nickname)) {
      newErrors.nickname = '1~8자, 한글/영문/숫자만 가능합니다.'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    setIsLoading(true)

    try {
      await signup({
        email: formData.email,
        nickname: formData.nickname,
        password: formData.password,
      })
      navigate('/login')
    } catch (err) {
      setErrors({ general: err.message || '회원가입에 실패했습니다. 다시 시도해주세요.' })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card signup-card">
        <div className="auth-header">
          <div className="auth-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
              <path d="M15 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm-9-2V7H4v3H1v2h3v3h2v-3h3v-2H6zm9 4c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
          <h1 className="auth-title">회원가입</h1>
          <p className="auth-subtitle">Voxie-e와 함께 시작하세요</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="email">이메일</label>
            <div className={`input-wrapper ${errors.email ? 'input-error' : ''}`}>
              <input
                type="email"
                id="email"
                name="email"
                placeholder="example@email.com"
                value={formData.email}
                onChange={handleChange}
                autoComplete="email"
              />
            </div>
            {errors.email && <span className="field-error">{errors.email}</span>}
          </div>

          <div className="input-group">
            <label htmlFor="nickname">닉네임</label>
            <div className={`input-wrapper ${errors.nickname ? 'input-error' : ''}`}>
              <input
                type="text"
                id="nickname"
                name="nickname"
                placeholder="1~8자, 한글/영문/숫자"
                value={formData.nickname}
                onChange={handleChange}
                maxLength={8}
              />
            </div>
            {errors.nickname && <span className="field-error">{errors.nickname}</span>}
          </div>

          <div className="input-group">
            <label htmlFor="password">비밀번호</label>
            <div className={`input-wrapper ${errors.password ? 'input-error' : ''}`}>
              <input
                type="password"
                id="password"
                name="password"
                placeholder="8~20자, 영문+숫자+특수문자"
                value={formData.password}
                onChange={handleChange}
                autoComplete="new-password"
              />
            </div>
            {errors.password && <span className="field-error">{errors.password}</span>}
          </div>

          <div className="input-group">
            <label htmlFor="passwordConfirm">비밀번호 확인</label>
            <div className={`input-wrapper ${errors.passwordConfirm ? 'input-error' : ''}`}>
              <input
                type="password"
                id="passwordConfirm"
                name="passwordConfirm"
                placeholder="비밀번호를 다시 입력하세요"
                value={formData.passwordConfirm}
                onChange={handleChange}
                autoComplete="new-password"
              />
            </div>
            {errors.passwordConfirm && <span className="field-error">{errors.passwordConfirm}</span>}
          </div>

          {errors.general && <p className="error-message">{errors.general}</p>}

          <button
            type="submit"
            className="auth-btn"
            disabled={isLoading}
          >
            {isLoading ? '가입 중...' : '회원가입'}
          </button>
        </form>

        <div className="auth-footer">
          <p>이미 계정이 있으신가요? <Link to="/login">로그인</Link></p>
        </div>
      </div>

      <Link to="/" className="back-link">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
        </svg>
        홈으로 돌아가기
      </Link>
    </div>
  )
}

export default Signup
