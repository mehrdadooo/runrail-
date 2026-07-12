FROM python:3.11-slim

WORKDIR /app

# نصب پیش‌نیازها، Netcat برای مانیتورینگ پورت و ابزار سایفون
RUN apt-get update && apt-get install -y ffmpeg curl unzip netcat-openbsd && \
    curl -L -o warp-plus.zip https://github.com/bepass-org/warp-plus/releases/download/v1.2.4/warp-plus_linux-amd64.zip && \
    unzip -o warp-plus.zip && \
    chmod +x warp-plus && \
    rm warp-plus.zip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 🚨 تضمین 100% اجرای پروکسی قبل از پایتون با netcat 🚨
CMD ["bash", "-lc", "nohup ./warp-plus -b 127.0.0.1:8086 --cfon >/tmp/warp.log 2>&1 & for i in $(seq 1 30); do nc -z 127.0.0.1 8086 && break; sleep 1; done; python worker.py"]
