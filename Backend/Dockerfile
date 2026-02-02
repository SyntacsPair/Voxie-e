# 1. 파이썬 3.12 베이스
FROM python:3.12-slim

# 2. 작업 폴더 설정 (컨테이너 내부)
WORKDIR /app

# 3. 필수 프로그램 설치 (curl, tar는 Piper 다운로드용)
RUN apt-get update && \
    apt-get install -y curl tar && \
    rm -rf /var/lib/apt/lists/*

# 4. Piper TTS 엔진 설치 (리눅스용)
# 자동으로 다운받아서 /usr/local/bin에 설치함 -> 어디서든 'piper' 명령어가 먹힘
RUN curl -L https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz | tar -xz -C /usr/local/bin --strip-components=1

# 5. 파이썬 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 소스 코드 복사 (이때 voice 폴더도 같이 복사됨!)
COPY . .

# 7. 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
