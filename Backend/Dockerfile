# 1. 파이썬 3.10.11 베이스 (RVC와의 완벽한 궁합!)
FROM python:3.10.11-slim

# 2. 작업 폴더 설정
WORKDIR /app

# 3. [네트워크 설정] 원래 잘 되던 https + kakao 형식 유지 (버전만 bullseye로 변경)
RUN rm -f /etc/apt/sources.list.d/debian.sources && \
    echo "deb https://mirror.kakao.com/debian bullseye main" > /etc/apt/sources.list && \
    echo "deb https://mirror.kakao.com/debian bullseye-updates main" >> /etc/apt/sources.list

# 4. 필수 프로그램 및 라이브러리 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    ffmpeg \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 5. 파이썬 라이브러리 설치 (CPU 전용 강조)
COPY requirements.txt .
RUN pip install --no-cache-dir "pip<24.1" && \
    pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# 6. 소스 코드 복사
COPY . .

# 7. 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]