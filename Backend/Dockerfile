# 1. 파이썬 3.12 베이스
FROM python:3.12-slim

# 2. 작업 폴더 설정
WORKDIR /app

# 3. [네트워크 설정] 카카오 미러 + HTTPS (pip install을 위해 인터넷은 뚫어둬야 함)
RUN rm -f /etc/apt/sources.list.d/debian.sources && \
    echo "deb https://mirror.kakao.com/debian trixie main" > /etc/apt/sources.list && \
    echo "deb https://mirror.kakao.com/debian trixie-updates main" >> /etc/apt/sources.list

# 4. 필수 프로그램 설치
RUN apt-get -o "Acquire::https::Verify-Peer=false" update && \
    apt-get -o "Acquire::https::Verify-Peer=false" install -y --allow-unauthenticated \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ★ 5. Piper "복사" (다운로드 X, 압축풀기 X) ★
COPY piper /app/piper

# 6. Piper 경로 등록
ENV PATH="/app/piper:$PATH"

# 7. 파이썬 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 8. 소스 코드 복사
COPY . .

# 9. 서버 실행 (HTTPS)
CMD ["python", "manage.py", "runsslserver", "0.0.0.0:8000"]