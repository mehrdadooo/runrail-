FROM python:3.11-slim

WORKDIR /app

# 🚨 اضافه شدن nodejs برای حل کردن قفل‌های جاوااسکریپت یوتیوب 🚨
RUN apt-get update && apt-get install -y ffmpeg curl unzip nodejs && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "worker.py"]
