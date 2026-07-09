FROM python:3.11-slim

WORKDIR /app

# نصب پیش‌نیازها و دانلود ابزار مخفی warp-plus
RUN apt-get update && apt-get install -y ffmpeg curl unzip && \
    curl -L -o warp-plus.zip https://github.com/bepass-org/warp-plus/releases/download/v1.2.4/warp-plus_linux-amd64.zip && \
    unzip -o warp-plus.zip && \
    chmod +x warp-plus && \
    rm warp-plus.zip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# استارت کردن تونل سایفون روی پورت 8086 و سپس اجرای پایتون
CMD ["bash", "-c", "nohup ./warp-plus -b 127.0.0.1:8086 --cfon > /dev/null 2>&1 & sleep 5 && python worker.py"]
