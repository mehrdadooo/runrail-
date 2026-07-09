import os
import asyncio
import aiohttp
import shutil
import uuid
import random
from pathlib import Path
from pyrogram import Client
from pyrogram.errors import FloodWait, AuthKeyDuplicated, AuthKeyInvalid

# متغیرهایی که از پنل Railway خوانده می‌شوند
API_ID = int(os.environ.get("API_ID", "39884025"))
API_HASH = os.environ.get("API_HASH", "24ce21160fcabd7e7c0de00a77b45ef3")
HF_URL = os.environ.get("HF_URL", "https://downloads89oouu-downloader.hf.space") 
WORKER_SECRET = os.environ.get("WORKER_SECRET", "ali_vip_worker_2026")

BOT_SESSIONS = [
    "BAJglPkAO0RCs_NW3uELJV95CRa17odKleHTrosLpwhRpmfX3N1K7SqQobP1kJvc6czR6E1z5j9TChl_X5_hHlAtx5RZH-xdFiOfJ_CrTMrTRKY2wzpe9dC2E9CitkBqwgZQDyHbiLZC-mrJPoXgDZ2tGeNwMMbWd3kHal3me4N8HloJcvwbR93nopWSZaO1VE9OGol8iczRSPovbqMcexgkquu7yb8EO2U6aeHZOqiExD8Vdibnj8W4QUQLA60bdhNhZGSC4EmdKXKCq32DfZHFtNNxC3RMmh3h1xJdS6Jf4W9IJaR32E5mS8pM-COP9N9pCoLWlw-2XjQiSu5KM9AQjGcs5wAAAAINTZ2uAQ",
    "BAJglPkAEIHq7qQmQFqUMINW5U6OolhKB8sxXd5mn0pLpwl6mB5fRnvM8UFmd2wf-7N0oDZ0-Rms2QlSr9JMkRoXAAGxKTp0tj0kK_mUobjFlOtS8hctWZgSwNjcsEDXprLU4f7CMQLvRskRzpPkShd1TxsEuzjtjg2sq9_Ed1hBQan1-BFBdAJ2wVNGSfg6zOAUBgV1XUU1_SAl7LywJJQUmSeQEB8dBX_-tmUqJVzpJI6iorwqPxYu8n5k2bPnXdtRB-vbZf-Oi2Cv-1wl-cvG_0vTVPcVUnTiIJjigDpXRz_Eu0lmVIiRhSNtxJvtSj_4u1z-Ze9qnQOCfTNQ3dRQQHYO1wAAAAINTZ2uAQ",
    "BAJglPkAq5Ab9cqjvp2qvWWxpgmw7wOq2W6wlOC6EUCD9QOu5mAtsAyr7CaY9eOTUCpjB1yuYvE9UyQy6EpZdh-AupsQ6wwQPGjxe6b6wkv7gVm8z0vdO5f54I_dh8erfAY1Lz-186zlCumDcV63EZwm2MO27qKdzbjOocILR4SKECgrvxk1bEqfLHlp5D8nFyTBZeAko4iPWhh8O6d9WMdLQDodXMG-dJCNwQzqE6Vyui1BRNxFIXKoz1XGnZ6iPPuf3eKJH-ayZ3FHJJUei0kYO4MKl_gy3Uv1WFzvTEuvTZtbjyKFKMSp4YH39_OdTdUwXbHca-lQhGwukSztM10quL9_xAAAAAINTZ2uAQ",
    "BAJglPkAag83pxlJ7YpaNRtvcskvrUSiHrWl0HfkNboMFQuljSaFf6rieC84VjbF5aq9Pxrqrplls6jlfm7f4HC9D7JWa7bKqH9WjSplofQTsSbRYmkvQbUk2lmC7obeze9Unblo0VFc9kXXYG5No0hojvU4DCWTH3ZsY8uveLe8hVTSvlHCQiPcU0cJfnTZT9E2yK__EnlPojvEyavyi1h0pFzGWAybMlegSoHnLcX9VGU08qiRgkKOYdF3i5CV3heSijJiFlwI35wu-XYnqKm60zK2lMTJr2lfid6ssTcdy90brCa9C1BzAcnSGPQMy-GaoZo0ESsHEgGR4R7Z9smYtDFSTgAAAAINTZ2uAQ",
    "BAJglPkAnFvYFhSl3hlS4GIGt1SE-9C07UeeF0iteez4skX9hDjV3v_MpG7XN50rodIXGUghdjN_s_ePRYiY2_0d7cOROP1EvEhbcNp1c7FaJzYzRNbC4ejWuqdVF88yRh7Y1_1frOzsrEKlFF8UWq2bl6jeOPcTyl0OZGkosKhuXXIVbnM9h_-X96MLqvRCPlvW9IrBjby-HXHlE_RFAw-68JViTuVNZz6zEFsDWV0M-D5-L8nRfedqEFP0Y1pg_7JZQnCggHKYUJ7lvhCa9-XCo1PJQZjbj9ukDM53B7WoZgpfKGjtnuRfp0kHEuZYrZGtXUHs_N7wmLdrZfeolKQ6RNa1nAAAAAINTZ2uAQ"
]

async def download_via_cobalt(url, job_dir):
    """دانلود شبکه‌های اجتماعی با کبالت (دور زدن فایروال اینستاگرام/تیک‌تاک)"""
    print(f"🌟 Using Cobalt API for: {url}")
    api_urls = ["https://api.cobalt.tools/api/json", "https://cobalt.q0.pm/api/json", "https://co.wuk.sh/api/json"]
    headers = {
        "Accept": "application/json", "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Origin": "https://cobalt.tools", "Referer": "https://cobalt.tools/"
    }
    payload = {"url": url, "vQuality": "max"}

    async with aiohttp.ClientSession() as session:
        video_url = None
        for api in api_urls:
            try:
                async with session.post(api, headers=headers, json=payload, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        video_url = data.get("url")
                        if video_url: break
            except: continue

        if not video_url: raise Exception("❌ Cobalt API Failed.")

        file_path = f"{job_dir}/video.mp4"
        async with session.get(video_url) as video_resp:
            if video_resp.status != 200: raise Exception("Download failed.")
            with open(file_path, 'wb') as f:
                while True:
                    chunk = await video_resp.content.read(2 * 1024 * 1024)
                    if not chunk: break
                    f.write(chunk)
        return True

async def download_youtube(url, job_dir):
    """دانلود یوتیوب با استفاده از تونل سایفون روی پورت 8086"""
    print(f"🚜 Using yt-dlp + WARP Tunnel for: {url}")
    cmd = [
        "yt-dlp", "--rm-cache-dir", "-f", "bv*+ba/b", "--merge-output-format", "mp4",
        "--proxy", "socks5h://127.0.0.1:8086",  # استفاده از تونل داکر
        "--impersonate", "chrome",
        "--extractor-args", "youtube:player_client=tv_downgraded,android_vr",
        "--no-check-certificate", "--force-ipv4", "--retries", "3",
        "-o", f"{job_dir}/video.%(ext)s", url
    ]
    process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise Exception(stderr.decode().strip()[:200])
    return True

async def main():
    print("✅ Railway Worker Ready! Polling Hugging Face...")
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
                        print(f"[{job_id}] 📥 Job Acquired: {url}")

                        try:
                            # تفکیک دانلود
                            if "youtube.com" in url or "youtu.be" in url:
                                await download_youtube(url, job_dir)
                            else:
                                await download_via_cobalt(url, job_dir)
                            
                            matches = list(job_dir.glob("video.mp4")) or list(job_dir.glob("*.*"))
                            file_path = str(matches[0].resolve())

                            # آپلود با استخر سشن‌ها
                            upload_success = False
                            for attempt in range(3):
                                upload_app = Client(f"railway_{job_id}_{attempt}", api_id=API_ID, api_hash=API_HASH, session_string=random.choice(BOT_SESSIONS), in_memory=True)
                                try:
                                    async with upload_app:
                                        print(f"[{job_id}] 🚀 Uploading...")
                                        await upload_app.send_video(chat_id=chat_id, video=file_path, caption=f"🎬 دانلود سریع توسط **Railway VIP**", reply_to_message_id=message_id, supports_streaming=True)
                                        try: await upload_app.delete_messages(chat_id, status_msg_id)
                                        except: pass
                                    print(f"[{job_id}] 🎉 Completed!")
                                    upload_success = True
                                    break
                                except (AuthKeyDuplicated, AuthKeyInvalid): continue
                                except FloodWait as e: await asyncio.sleep(e.value + 2)
                                    
                            if not upload_success: print(f"[{job_id}] ❌ Upload failed.")

                        except Exception as e: print(f"[{job_id}] ❌ Error: {e}")
                        finally: shutil.rmtree(job_dir, ignore_errors=True)
                    else: await asyncio.sleep(5)
            except Exception: await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
