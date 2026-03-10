# 1. 파이썬 3.10.11 베이스 (RVC 호환성 완벽 보장!)
FROM python:3.10.11-slim

# 2. 작업 폴더 설정
WORKDIR /app

# 3. [네트워크 설정] 카카오 미러 + HTTPS 
# (주의: python 3.10.11-slim은 'bullseye' 버전을 사용하므로 trixie 대신 bullseye로 맞춰야 에러가 안 납니다!)
RUN rm -f /etc/apt/sources.list.d/debian.sources && \
    echo "deb https://mirror.kakao.com/debian bullseye main" > /etc/apt/sources.list && \
    echo "deb https://mirror.kakao.com/debian bullseye-updates main" >> /etc/apt/sources.list

# 4. 필수 프로그램 및 🚨 RVC 생명줄 'ffmpeg' 설치
RUN apt-get -o "Acquire::https::Verify-Peer=false" update && \
    apt-get -o "Acquire::https::Verify-Peer=false" install -y --allow-unauthenticated \
    ca-certificates \
    curl \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ★ 5. Piper "복사" (다운로드 X, 압축풀기 X) ★
COPY piper /app/piper

# 6. Piper 경로 등록
ENV PATH="/app/piper:$PATH"

# 7. 파이썬 라이브러리 설치
# (requirements.txt 안에 rvc-python, edge-tts, django, djangorestframework 등이 있는지 꼭 확인하세요!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 8. 소스 코드 및 Voice 모델 파일들 복사
COPY . .

# 9. 서버 실행 (로컬 테스트용이면 8000 포트 개방)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]