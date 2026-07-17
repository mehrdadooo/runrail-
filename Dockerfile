FROM python:3.11

# ۱. نصب ابزارهای پایه و گواهینامه‌های SSL
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg ca-certificates unzip wget curl && \
    rm -rf /var/lib/apt/lists/*

# 🚨 فیکسِ جهانی: نصب موتور Deno و انتقال آن به مسیر سراسریِ سیستم‌عامل (برای حل قطعی معمای یوتیوب)
RUN curl -fsSL https://deno.land/x/install/install.sh | sh && \
    mv /root/.deno/bin/deno /usr/local/bin/deno && \
    chmod +x /usr/local/bin/deno

# ۳. نصب موتور Xray در پوشه اختصاصی
RUN mkdir -p /app/xray_bin && \
    wget https://github.com/XTLS/Xray-core/releases/download/v1.8.9/Xray-linux-64.zip && \
    unzip Xray-linux-64.zip -d /app/xray_bin && \
    rm Xray-linux-64.zip

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "worker.py"]
