FROM python:3.11

# نصب ابزارهای اصلی، ffmpeg و لود سراسری nodejs برای حل کدهای امنیتی یوتیوب
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg ca-certificates unzip wget curl nodejs && \
    rm -rf /var/lib/apt/lists/*

# دانلود و نصب دائم هسته Xray در مسیر دقیق xray_bin کدهای شما
RUN mkdir -p /app/xray_bin && \
    wget https://github.com/XTLS/Xray-core/releases/download/v1.8.9/Xray-linux-64.zip && \
    unzip Xray-linux-64.zip -d /app/xray_bin && \
    rm Xray-linux-64.zip

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# اجرای مستقیم ورکر (تمام کارهای راه‌اندازی پروکسی و کوکی توسط خود پایتون انجام می‌شود)
CMD ["python", "worker.py"]
