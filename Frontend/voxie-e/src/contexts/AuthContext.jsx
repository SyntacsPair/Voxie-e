import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

const ERROR_MESSAGES = {
  'The password is too similar to the username.': '비밀번호가 닉네임과 너무 비슷합니다.',
  'The password is too similar to the email address.': '비밀번호가 이메일과 너무 비슷합니다.',
  'This password is too short. It must contain at least 8 characters.': '비밀번호는 최소 8자 이상이어야 합니다.',
  'This password is too common.': '너무 흔한 비밀번호입니다.',
  'This password is entirely numeric.': '비밀번호는 숫자로만 이루어질 수 없습니다.',
  'A user with that username already exists.': '이미 사용 중인 닉네임입니다.',
  'A user is already registered with this e-mail address.': '이미 등록된 이메일입니다.',
  'Unable to log in with provided credentials.': '닉네임 또는 비밀번호가 올바르지 않습니다.',
  'This field may not be blank.': '필수 입력 항목입니다.',
  'Enter a valid email address.': '올바른 이메일 형식을 입력해주세요.',
}

function translateError(msg) {
  return ERROR_MESSAGES[msg] || msg
}

const API_BASE = import.meta.env.VITE_API_URL || ''

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 페이지 새로고침 시 localStorage에서 유저 정보 복원
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      setUser(JSON.parse(savedUser))
    }
    setLoading(false)
  }, [])

  const login = async (username, password) => {
    const response = await fetch(`${API_BASE}/api/v1/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ username, password }),
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(translateError(data.non_field_errors?.[0]) || '로그인에 실패했습니다.')
    }

    const data = await response.json()
    const userData = { username: data.user?.username || username }
    setUser(userData)
    localStorage.setItem('user', JSON.stringify(userData))
    return data
  }

  const signup = async ({ email, nickname, password }) => {
    const response = await fetch(`${API_BASE}/api/v1/users/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: nickname,
        email,
        password1: password,
        password2: password,
      }),
    })

    if (!response.ok) {
      const data = await response.json()
      // dj-rest-auth 에러 형식 파싱
      const firstError =
        data.username?.[0] ||
        data.email?.[0] ||
        data.password1?.[0] ||
        data.non_field_errors?.[0] ||
        '회원가입에 실패했습니다.'
      throw new Error(translateError(firstError))
    }

    return await response.json()
  }

  const logout = async () => {
    try {
      await fetch(`${API_BASE}/api/v1/users/logout`, {
        method: 'POST',
        credentials: 'include',
      })
    } catch {
      // 로그아웃 실패해도 로컬 상태는 정리
    }
    setUser(null)
    localStorage.removeItem('user')
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
