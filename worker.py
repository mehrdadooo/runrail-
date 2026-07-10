import os
import sys
import asyncio
import aiohttp
import shutil
import uuid
import random
from pathlib import Path
from pyrogram import Client
from pyrogram.errors import FloodWait, AuthKeyDuplicated, AuthKeyInvalid

# 🚨 تخلیه فوری خروجی برای نمایش زنده و ثانیه‌ای لاگ‌ها در Railway 🚨
def print_log(msg):
    print(msg, flush=True)
    sys.stdout.flush()

# ─── تنظیمات اختصاصی شما ───
API_ID = 39884025
API_HASH = "24ce21160fcabd7e7c0de00a77b45ef3"
HF_URL = "https://downloads89oouu-downloader.hf.space" 
WORKER_SECRET = "ali_vip_worker_2026"

BOT_SESSIONS = [
    "BAJglPkAO0RCs_NW3uELJV95CRa17odKleHTrosLpwhRpmfX3N1K7SqQobP1kJvc6czR6E1z5j9TChl_X5_hHlAtx5RZH-xdFiOfJ_CrTMrTRKY2wzpe9dC2E9CitkBqwgZQDyHbiLZC-mrJPoXgDZ2tGeNwMMbWd3kHal3me4N8HloJcvwbR93nopWSZaO1VE9OGol8iczRSPovbqMcexgkquu7yb8EO2U6aeHZOqiExD8Vdibnj8W4QUQLA60bdhNhZGSC4EmdKXKCq32DfZHFtNNxC3RMmh3h1xJdS6Jf4W9IJaR32E5mS8pM-COP9N9pCoLWlw-2XjQiSu5KM9AQjGcs5wAAAAINTZ2uAQ",
    "BAJglPkAEIHq7qQmQFqUMINW5U6OolhKB8sxXd5mn0pLpwl6mB5fRnvM8UFmd2wf-7N0oDZ0-Rms2QlSr9JMkRoXAAGxKTp0tj0kK_mUobjFlOtS8hctWZgSwNjcsEDXprLU4f7CMQLvRskRzpPkShd1TxsEuzjtjg2sq9_Ed1hBQan1-BFBdAJ2wVNGSfg6zOAUBgV1XUU1_SAl7LywJJQUmSeQEB8dBX_-tmUqJVzpJI6iorwqPxYu8n5k2bPnXdtRB-vbZf-Oi2Cv-1wl-cvG_0vTVPcVUnTiIJjigDpXRz_Eu0lmVIiRhSNtxJvtSj_4u1z-Ze9qnQOCfTNQ3dRQQHYO1wAAAAINTZ2uAQ",
    "BAJglPkAq5Ab9cqjvp2qvWWxpgmw7wOq2W6wlOC6EUCD9QOu5mAtsAyr7CaY9eOTUCpjB1yuYvE9UyQy6EpZdh-AupsQ6wwQPGjxe6b6wkv7gVm8z0vdO5f54I_dh8erfAY1Lz-186zlCumDcV63EZwm2MO27qKdzbjOocILR4SKECgrvxk1bEqfLHlp5D8nFyTBZeAko4iPWhh8O6d9WMdLQDodXMG-dJCNwQzqE6Vyui1BRNxFIXKoz1XGnZ6iPPuf3eKJH-ayZ3FHJJUei0kYO4MKl_gy3Uv1WFzvTEuvTZtbjyKFKMSp4YH39_OdTdUwXbHca-lQhGwukSztM10quL9_xAAAAAINTZ2uAQ",
    "BAJglPkAag83pxlJ7YpaNRtvcskvrUSiHrWl0HfkNboMFQuljSaFf6rieC84VjbF5aq9Pxrqrplls6jlfm7f4HC9D7JWa7bKqH9WjSplofQTsSbRYmkvQbUk2lmC7obeze9Unblo0VFc9kXXYG5No0hojvU4DCWTH3ZsY8uveLe8hVTSvlHCQiPcU0cJfnTZT9E2yK__EnlPojvEyavyi1h0pFzGWAybMlegSoHnLcX9VGU08qiRgkKOYdF3i5CV3heSijJiFlwI35wu-XYnqKm60zK2lMTJr2lfid6ssTcdy90brCa9C1BzAcnSGPQMy-GaoZo0ESsHEgGR4R7Z9smYtDFSTgAAAAINTZ2uAQ",
    "BAJglPkAnFvYFhSl3hlS4GIGt1SE-9C07UeeF0iteez4skX9hDjV3v_MpG7XN50rodIXGUghdjN_s_ePRYiY2_0d7cOROP1EvEhbcNp1c7FaJzYzRNbC4ejWuqdVF88yRh7Y1_1frOzsrEKlFF8UWq2bl6jeOPcTyl0OZGkosKhuXXIVbnM9h_-X96MLqvRCPlvW9IrBjby-HXHlE_RFAw-68JViTuVNZz6zEFsDWV0M-D5-L8nRfedqEFP0Y1pg_7JZQnCggHKYUJ7lvhCa9-XCo1PJQZjbj9ukDM53B7WoZgpfKGjtnuRfp0kHEuZYrZGtXUHs_N7wmLdrZfeolKQ6RNa1nAAAAAINTZ2uAQ"
]

async def download_via_cobalt(url, job_dir):
    """دانلود با کبالت - آپدیت شده برای API نسخه جدید (v11)"""
    print_log(f"🌟 Starting Cobalt API fallback for: {url}")
    api_urls = [
        "https://api.cobalt.tools/api/json", 
        "https://cobalt.q0.pm/api/json", 
        "https://api.cobalt.tools/"
    ]
    
    headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    
    # ساختار جدید کبالت
    payload = {"url": url, "videoQuality": "max"}

    async with aiohttp.ClientSession() as session:
        video_url = None
        for api in api_urls:
            try:
                async with session.post(api, headers=headers, json=payload, timeout=15) as resp:
                    if resp.status in [200, 202]:
                        data = await resp.json()
                        # در نسخه جدید، لینک داخل متغیر url قرار می‌گیرد
                        video_url = data.get("url")
                        if video_url: 
                            print_log(f"✅ Extracted link from Cobalt API: {api}")
                            break
            except Exception as e:
                print_log(f"⚠️ Cobalt API {api} failed: {e}")
                continue

        if not video_url: raise Exception("❌ All Cobalt APIs failed.")

        # ذخیره با آدرس مطلق
        file_path = f"{job_dir.resolve()}/video.mp4"
        async with session.get(video_url) as video_resp:
            if video_resp.status != 200: raise Exception("Download failed from extracted URL.")
            with open(file_path, 'wb') as f:
                while True:
                    chunk = await video_resp.content.read(2 * 1024 * 1024)
                    if not chunk: break
                    f.write(chunk)
        print_log("✅ Successfully downloaded via Cobalt!")
        return True

async def download_video_via_ytdlp(url, job_dir):
    """دانلود با yt-dlp - رفع باگ پورت 8086 و بهینه‌سازی برای اینستاگرام"""
    print_log(f"🚜 Running yt-dlp...")
    
    is_youtube = "youtube.com" in url.lower() or "youtu.be" in url.lower()
    absolute_job_dir = str(job_dir.resolve()) 
    
    cmd = [
        "yt-dlp", "--rm-cache-dir", 
        "-f", "bv*+ba/b" if is_youtube else "b", 
        "--merge-output-format", "mp4",
        # 🚨 پروکسی حذف شد تا مستقیم روی شبکه Railway دانلود کند 🚨
        "--impersonate", "chrome",
        "--no-check-certificate", "--force-ipv4", "--retries", "5",
        "--fragment-retries", "infinite",
        "-o", f"{absolute_job_dir}/video.%(ext)s", url
    ]
    
    if is_youtube:
        cmd.extend([
            "--extractor-args", "youtube:player_client=android", # کلاینت اندروید مثل گیت‌هاب
            "--remote-components", "ejs:github"
        ])
        
    process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    
    yt_out = stdout.decode('utf-8', errors='ignore').strip()
    yt_err = stderr.decode('utf-8', errors='ignore').strip()
    if yt_out: print_log(f"📝 --- yt-dlp stdout ---\n{yt_out}")
    if yt_err: print_log(f"⚠️ --- yt-dlp stderr ---\n{yt_err}")
        
    if process.returncode != 0:
        raise Exception(f"yt-dlp Exit code {process.returncode}")
    return True

async def main():
    print_log("✅ Railway Worker Ready! Polling Hugging Face for jobs...\n")

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                headers = {"Authorization": f"Bearer {WORKER_SECRET}"}
                async with session.get(f"{HF_URL}/poll", headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "no_job":
                            await asyncio.sleep(2)
                            continue

                        url, chat_id, message_id, status_msg_id = data["url"], int(data["chat_id"]), int(data["message_id"]), int(data["status_msg_id"])
                        job_id = str(uuid.uuid4())[:8]
                        job_dir = Path(f"jobs/{job_id}")
                        job_dir.mkdir(parents=True, exist_ok=True)
                        print_log(f"[{job_id}] 📥 Job Acquired: {url}")

                        try:
                            download_success = False
                            
                            # ۱. تلاش برای دانلود با yt-dlp (بدون پروکسی لوکال)
                            try:
                                await download_video_via_ytdlp(url, job_dir)
                                download_success = True
                            except Exception as e:
                                print_log(f"⚠️ yt-dlp download failed: {e}")
                            
                            # ۲. فال‌بک به کبالت در صورت شکست
                            if not download_success and not ("youtube.com" in url or "youtu.be" in url):
                                print_log("🔄 Falling back to Cobalt API...")
                                await download_via_cobalt(url, job_dir)
                                download_success = True

                            # چک کردن فیزیکی فایل روی هارد داکر
                            matches = list(job_dir.glob("video.mp4")) or list(job_dir.glob("video.*")) or list(job_dir.glob("*.*"))
                            if not matches or not download_success:
                                raise FileNotFoundError("Video file not found on disk!")
                                
                            file_path = str(matches[0].resolve())

                            # سیستم درصدگیر آپلود زنده
                            last_percent = -1
                            async def progress_callback(current, total):
                                nonlocal last_percent
                                if total > 0:
                                    percent = int((current * 100) / total)
                                    if percent % 10 == 0 and percent != last_percent:
                                        last_percent = percent
                                        print_log(f"[{job_id}] 🚀 Uploading Progress: {percent}%")

                            # ۳. آپلود با استخر سشن (دقیقاً مشابه کد GitHub Actions شما)
                            upload_success = False
                            for attempt in range(3):
                                chosen_session = random.choice(BOT_SESSIONS)
                                upload_app = Client(f"railway_{job_id}_{attempt}", api_id=API_ID, api_hash=API_HASH, session_string=chosen_session, in_memory=True)
                                try:
                                    async with upload_app:
                                        print_log(f"[{job_id}] 🚀 Attempt {attempt+1}: Uploading to Telegram...")
                                        await upload_app.send_video(
                                            chat_id=chat_id, 
                                            video=file_path, 
                                            caption=f"🎬 **دانلود موفق**\n⚡ توسط سرور پرسرعت", 
                                            reply_to_message_id=message_id, 
                                            supports_streaming=True, 
                                            progress=progress_callback
                                        )
                                        try: await upload_app.delete_messages(chat_id, status_msg_id)
                                        except: pass
                                    print_log(f"[{job_id}] 🎉 Job Completed!")
                                    upload_success = True
                                    break
                                except (AuthKeyDuplicated, AuthKeyInvalid): 
                                    print_log(f"[{job_id}] ⚠️ Session collision detected. Retrying...")
                                    continue
                                except FloodWait as e: 
                                    print_log(f"[{job_id}] 🛑 Telegram Rate Limit: Must wait {e.value} seconds.")
                                    await asyncio.sleep(e.value + 2)
                                    
                            if not upload_success: print_log(f"[{job_id}] ❌ Upload failed after all retries.")

                        except Exception as e: print_log(f"[{job_id}] ❌ Error during processing: {e}")
                        finally: shutil.rmtree(job_dir, ignore_errors=True)
                    else: await asyncio.sleep(5)
            except Exception: await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
