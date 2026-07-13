FROM python:3.11

# نصب ابزارهای اصلی و گواهینامه‌های لینوکس بدون لایه اسلیم جهت سازگاری ۱۰۰٪ با پکیج‌های پیش‌کامپایل شده
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg ca-certificates unzip wget curl && \
    rm -rf /var/lib/apt/lists/*

# نصب موتور جاوااسکریپت Deno برای حل کدهای یوتیوب
RUN curl -fsSL https://deno.land/x/install/install.sh | sh
ENV PATH="/root/.deno/bin:$PATH"

# دانلود و نصب xray در مسیر دقیق پوشه xray_bin کدهای شما
RUN mkdir -p /app/xray_bin && \
    wget https://github.com/XTLS/Xray-core/releases/download/v1.8.9/Xray-linux-64.zip && \
    unzip Xray-linux-64.zip -d /app/xray_bin && \
    rm Xray-linux-64.zip

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
