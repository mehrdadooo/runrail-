FROM python:3.11

# نصب ابزارهای اصلی + aria2 + کتابخانه‌های امنیتی libnss3 و libnspr4 که برای اجرای curl_cffi کاملاً الزامی هستند
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg aria2 ca-certificates unzip wget curl nodejs npm libnss3 libnspr4 && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deno.land/x/install/install.sh | sh && \
    mv /root/.deno/bin/deno /usr/local/bin/deno && \
    chmod +x /usr/local/bin/deno

RUN mkdir -p /app/xray_bin && \
    wget https://github.com/XTLS/Xray-core/releases/download/v1.8.9/Xray-linux-64.zip && \
    unzip Xray-linux-64.zip -d /app/xray_bin && \
    rm Xray-linux-64.zip

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "worker.py"]
