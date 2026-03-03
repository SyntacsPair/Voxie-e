const API_BASE = ''

// ===========================================
// TTS 관련 API
// ===========================================

/** TTS 음성 생성 (POST /api/v1/tts/generate) */
export async function generateTTS(text, voice = '') {
  const response = await fetch(`${API_BASE}/api/v1/tts/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ text, voice }),
  })

  if (!response.ok) {
    const data = await response.json()
    throw new Error(data.error || 'TTS 생성에 실패했습니다.')
  }

  // 오디오 blob 반환
  return await response.blob()
}

/** 음성 목록 조회 (GET /api/v1/tts/voices) */
export async function fetchVoices() {
  const response = await fetch(`${API_BASE}/api/v1/tts/voices`, {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error('음성 목록을 불러오지 못했습니다.')
  }

  const data = await response.json()
  return data.results
}

// ===========================================
// 히스토리 관련 API
// ===========================================

/** 히스토리 목록 조회 (GET /api/v1/tts/history) */
export async function fetchHistory() {
  const response = await fetch(`${API_BASE}/api/v1/tts/history`, {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error('히스토리를 불러오지 못했습니다.')
  }

  const data = await response.json()
  return data.results
}

/** 히스토리 상세 조회 (GET /api/v1/tts/history/:id) */
export async function fetchHistoryDetail(id) {
  const response = await fetch(`${API_BASE}/api/v1/tts/history/${id}`, {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error('히스토리 상세 정보를 불러오지 못했습니다.')
  }

  return await response.json()
}

/** 히스토리 삭제 (DELETE /api/v1/tts/history/:id) */
export async function deleteHistory(id) {
  const response = await fetch(`${API_BASE}/api/v1/tts/history/${id}`, {
    method: 'DELETE',
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error('히스토리 삭제에 실패했습니다.')
  }

  return true
}

/** 오디오 다운로드 (GET /api/v1/tts/history/:id/audio) */
export async function downloadAudio(id) {
  const response = await fetch(`${API_BASE}/api/v1/tts/history/${id}/audio`, {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error('오디오 다운로드에 실패했습니다.')
  }

  return await response.json()
}

// ===========================================
// 중복 검사 API
// ===========================================

/** 이메일 중복 검사 (GET /api/v1/users/email-availability) */
export async function checkEmailAvailability(email) {
  const response = await fetch(
    `${API_BASE}/api/v1/users/email-availability?email=${encodeURIComponent(email)}`,
    { credentials: 'include' }
  )

  if (!response.ok) {
    throw new Error('이메일 확인에 실패했습니다.')
  }

  return await response.json()
}

/** 닉네임 중복 검사 (GET /api/v1/users/nickname-availability) */
export async function checkNicknameAvailability(nickname) {
  const response = await fetch(
    `${API_BASE}/api/v1/users/nickname-availability?nickname=${encodeURIComponent(nickname)}`,
    { credentials: 'include' }
  )

  if (!response.ok) {
    throw new Error('닉네임 확인에 실패했습니다.')
  }

  return await response.json()
}
