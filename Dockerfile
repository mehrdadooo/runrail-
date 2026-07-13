FROM python:3.11-slim

WORKDIR /app

# نصب ابزارهای شبکه، ویدیو و فایل‌های سیستمی لینوکس
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg ca-certificates wget unzip curl && \
    rm -rf /var/lib/apt/lists/*

# نصب موتور جاوااسکریپت Deno برای حل کردن چالش‌های امنیتی یوتیوب (PO Token)
RUN curl -fsSL https://deno.land/x/install/install.sh | sh
ENV PATH="/root/.deno/bin:${PATH}"

# دانلود و نصب فیزیکی هسته Xray Core لینوکس در کانتینر
RUN wget https://github.com/XTLS/Xray-core/releases/download/v1.8.9/Xray-linux-64.zip && \
    unzip Xray-linux-64.zip -d /app/xray_bin && \
    rm Xray-linux-64.zip && \
    chmod +x /app/xray_bin/xray

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "worker.py"]
