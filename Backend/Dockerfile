# 1. 베이스 이미지 (파이썬 3.12가 깔린 리눅스를 가져와라)
FROM python:3.12-slim

# 2. 작업 폴더 설정 (리눅스 내부의 /app 폴더에서 작업하겠다)
WORKDIR /app

# 3. 필수 패키지 설치 (DB 관련 라이브러리 등)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. 명세서 복사 및 설치 (내 컴퓨터의 requirements.txt를 컨테이너로 복사)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 소스코드 복사 (나머지 코드 몽땅 복사)
COPY . .

# 6. 실행 명령어 (서버 켜라! 0.0.0.0은 외부 접속 허용 의미)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]