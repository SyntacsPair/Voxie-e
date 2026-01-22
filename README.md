# Voxie-e 🎙️

```
♪ ～ ♪ ～ ♪ ～ ♪ ～ ♪
   ╔══════════════╗
   ║   📝 → 🔊   ║
   ╚══════════════╝
♪ ～ ♪ ～ ♪ ～ ♪ ～ ♪
```

---

**"텍스트에 목소리를 입혀, 세상과 소통하세요!"**
Voxie-e는 텍스트를 자연스러운 음성으로 변환해주는 TTS(Text-to-Speech) 웹 서비스입니다.
6가지 개성 있는 목소리로 당신의 콘텐츠에 생명을 불어넣어 보세요.

---

## 🎤 주요 기능

- **TTS 변환**: 텍스트를 고품질 MP3 음성 파일로 변환
- **다양한 목소리**: 6가지 개성 있는 목소리 중 선택 가능
- **속도 조절**: 0.5x ~ 2.0x 재생 속도 조절
- **히스토리 관리**: 생성한 음성 기록 저장, 조회, 다운로드
- **사용자 인증**: 안전한 JWT 기반 회원 시스템

---

## 🔊 지원 목소리

| ID      | 이름    | 설명                | 추천 용도             |
| ------- | ------- | ------------------- | --------------------- |
| alloy   | Alloy   | 중성적, 균형잡힌 톤 | 비즈니스, 범용        |
| echo    | Echo    | 남성적, 부드러운 톤 | 내레이션, 팟캐스트    |
| fable   | Fable   | 영국식, 따뜻한 톤   | 스토리텔링, 동화      |
| onyx    | Onyx    | 남성적, 깊은 톤     | 다큐멘터리, 공식 발표 |
| nova    | Nova    | 여성적, 밝은 톤     | 광고, 안내 방송       |
| shimmer | Shimmer | 여성적, 부드러운 톤 | 명상, ASMR            |

---

## ✨ 팀 소개

| 역할           | 팀원           |
| -------------- | -------------- |
| **기획**       | 이재혁, 채가을 |
| **디자인**     | 채가을         |
| **프론트엔드** | 채가을         |
| **백엔드**     | 이재혁         |

---

## 💻 기술 스택

| 구분                | 사용 기술                    |
| ------------------- | ---------------------------- |
| **Frontend**        | React, Vite                  |
| **Backend**         | Django                       |
| **Auth**            | JWT (Access / Refresh Token) |
| **Database**        | (추가 예정)                  |
| **Version Control** | Git                          |

---

## 🚀 시작하기

### Frontend

```bash
cd Frontend/voxie-e
npm install
npm run dev
```

### Backend

```bash
cd Backend
pip install -r ../requirements.txt
python manage.py runserver
```

---

## 📡 API 개요

### TTS

| 기능        | Method | Endpoint               |
| ----------- | ------ | ---------------------- |
| 음성 생성   | `POST` | `/api/v1/tts/generate` |
| 목소리 목록 | `GET`  | `/api/v1/tts/voices`   |

### History

| 기능      | Method   | Endpoint                         |
| --------- | -------- | -------------------------------- |
| 목록 조회 | `GET`    | `/api/v1/tts/history`            |
| 상세 조회 | `GET`    | `/api/v1/tts/history/{id}`       |
| 삭제      | `DELETE` | `/api/v1/tts/history/{id}`       |
| 다운로드  | `GET`    | `/api/v1/tts/history/{id}/audio` |

### User

| 기능             | Method    | Endpoint                |
| ---------------- | --------- | ----------------------- |
| 회원가입         | `POST`    | `/api/v1/users/signup`  |
| 로그인           | `POST`    | `/api/v1/users/login`   |
| 로그아웃         | `POST`    | `/api/v1/users/logout`  |
| 토큰 재발급      | `POST`    | `/api/v1/users/reissue` |
| 프로필 조회/수정 | `GET/PUT` | `/api/v1/users/me`      |

---

## 📁 프로젝트 구조

```
Voxie-e/
├── 📂 Frontend/
│   └── voxie-e/        # React 앱
├── 📂 Backend/         # Django 서버
├── 📄 requirements.txt
└── 📄 README.md
```

---

## 📜 라이선스

(추가 예정)
