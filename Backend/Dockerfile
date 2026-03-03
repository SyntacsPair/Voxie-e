# 1. 베이스 이미지 (파이썬 3.12가 깔린 리눅스를 가져와라)
FROM python:3.12-slim

# 2. 작업 폴더 설정 (리눅스 내부의 /app 폴더에서 작업하겠다)
WORKDIR /app

# 3. 필수 패키지 설치 (DB 관련 라이브러리 등)
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# docker build -t voxie-backend .