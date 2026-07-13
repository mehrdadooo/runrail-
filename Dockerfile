FROM python:3.11-slim

WORKDIR /app

# 🚨 کلمه nodejs اضافه شد تا yt-dlp بتواند قفل‌های یوتیوب را بشکند 🚨
RUN apt-get update && apt-get install -y ffmpeg curl unzip netcat-openbsd nodejs && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "worker.py"]
