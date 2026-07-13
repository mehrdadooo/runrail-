import os
import sys
import asyncio
import aiohttp
import shutil
import uuid
import random
import json
import urllib.parse
import urllib.request
import zipfile
import socket
import subprocess
from pathlib import Path
from pyrogram import Client
from pyrogram.errors import FloodWait, AuthKeyDuplicated, AuthKeyInvalid

def print_log(msg):
    print(msg, flush=True)
    sys.stdout.flush()

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

COOKIE_FILE_PATH = Path("cookies.txt")

# 🚨 اولین کانفیگ پرسرعت شما به عنوان دیفالت قرار گرفت 🚨
DEFAULT_VLESS = "vless://6522fd56-5f15-4c0b-96cd-b69034d5e8e9@still-mountain-f7fa.yyuuyouuu7.workers.dev:443?encryption=none&host=still-mountain-f7fa.yyuuyouuu7.workers.dev&type=ws&security=tls&path=%2FeyJxZFc1cklqb2llalkxWjNFd1JUSmFRbTlaY3lJc0luQnliM1J2WTI5c0lqb2lkbXdpTENKdGIyUmxJam9pY0hKdmVIbHBjQ0lzSW5CaGJtVnNTVkJ6SWpwYlhYMCUzRCUzRmVkJTNEMjU2MCZzbmk=stilL-mouNtAiN-f7Fa.YyuUyOuuU7.WOrkerS.dEV&fp=chrome&alpn=http%2F1.1#BPB_Worker"
VLESS_LINK = os.environ.get("VLESS_LINK", DEFAULT_VLESS)

def parse_vless_to_xray_json(vless_url):
    """تبدیل جادویی لینک VLESS به فایل کانفیگ استاندارد Xray در صدم ثانیه"""
    if '#' in vless_url:
        vless_url = vless_url.split('#')[0]
        
    parsed = urllib.parse.urlparse(vless_url)
    uuid_str = parsed.username
    address = parsed.hostname
    port = parsed.port or 443
    qs = urllib.parse.parse_qs(parsed.query)
    
    network = qs.get('type', ['tcp'])[0]
    security = qs.get('security', ['none'])[0]
    path = qs.get('path', ['/'])[0]
    host = qs.get('host', [''])[0]
    sni = qs.get('sni', [host])[0]
    fp = qs.get('fp', ['chrome'])[0]
    alpn = qs.get('alpn', ['http/1.1'])[0]
    
    config_json = {
        "inbounds": [{"port": 10808, "listen": "127.0.0.1", "protocol": "socks", "settings": {"udp": True}}],
        "outbounds": [{
            "protocol": "vless",
            "settings": {"vnext": [{"address": address, "port": int(port), "users": [{"id": uuid_str, "encryption": "none"}]}]},
            "streamSettings": {"network": network, "security": security}
        }]
    }
    
    if security == "tls":
        config_json["outbounds"][0]["streamSettings"]["tlsSettings"] = {"serverName": sni, "fingerprint": fp, "alpn": alpn.split(',') if ',' in alpn else [alpn]}
    if network == "ws":
        config_json["outbounds"][0]["streamSettings"]["wsSettings"] = {"path": path, "headers": {"Host": host} if host else {}}
        
    with open("config.json", "w") as f:
        json.dump(config_json, f, indent=2)

async def ensure_xray():
    """دانلود و اجرای موتور Xray در صورت نیاز"""
    if not os.path.exists("xray"):
        print_log("⚙️ Downloading Xray-core...")
        urllib.request.urlretrieve("https://github.com/XTLS/Xray-core/releases/download/v1.8.9/Xray-linux-64.zip", "xray.zip")
        with zipfile.ZipFile("xray.zip", 'r') as zip_ref:
            zip_ref.extract("xray", path=".")
        os.chmod("xray", 0o755)
        os.remove("xray.zip")

    # ساخت فایل کانفیگ از روی لینک شما
    parse_vless_to_xray_json(VLESS_LINK)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', 10808)) == 0:
            return True

    print_log("🚀 Starting Xray VLESS Engine on port 10808...")
    subprocess.Popen(["./xray", "run", "-c", "config.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await asyncio.sleep(2)
    return True

async def download_via_cobalt(url, job_dir, quality="max"):
    """دانلود با کبالت"""
    print_log(f"🌟 Starting Cobalt API fallback for: {url} | Quality: {quality}")
    api_urls = ["https://api.cobalt.tools/api/json", "https://cobalt.q0.pm/api/json", "https://api.cobalt.tools/"]
    headers = {"Accept": "application/json", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    payload = {"url": url, "vQuality": quality if quality != "audio" else "max"}
    if quality == "audio": payload["isAudioOnly"] = True

    async with aiohttp.ClientSession() as session:
        video_url = None
        for api in api_urls:
            try:
                async with session.post(api, headers=headers, json=payload, timeout=15) as resp:
                    if resp.status in [200, 202]:
                        data = await resp.json()
                        video_url = data.get("url")
                        if video_url: break
            except: continue

        if not video_url: raise Exception("❌ All Cobalt APIs failed.")

        ext = "mp3" if quality == "audio" else "mp4"
        file_path = f"{job_dir.resolve()}/video.{ext}"
        async with session.get(video_url) as video_resp:
            if video_resp.status != 200: raise Exception("Download failed.")
            with open(file_path, 'wb') as f:
                while True:
                    chunk = await video_resp.content.read(2 * 1024 * 1024)
                    if not chunk: break
                    f.write(chunk)
        print_log("✅ Successfully downloaded via Cobalt!")
        return True

async def download_video_via_ytdlp(url, job_dir, quality="max"):
    print_log(f"🚜 Running yt-dlp... Quality requested: {quality}")
    is_youtube = "youtube.com" in url.lower() or "youtu.be" in url.lower()
    absolute_job_dir = str(job_dir.resolve())
    quality = (quality or "max").strip().lower()

    if quality == "1080":
        format_str = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
        sort_args = ["-S", "height:1080"]
    elif quality == "720":
        format_str = "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
        sort_args = ["-S", "height:720"]
    elif quality == "480":
        format_str = "bestvideo[height<=480]+bestaudio/best[height<=480]/best"
        sort_args = ["-S", "height:480"]
    elif quality == "audio":
        format_str = "bestaudio/best"
        sort_args = []
    else:
        format_str = "bv*+ba/best"
        sort_args = []

    cmd = [
        "yt-dlp", "-f", format_str, *sort_args, "--no-playlist",
        "--impersonate", "chrome", "--no-check-certificate", "--force-ipv4",
        "--retries", "5", "--fragment-retries", "infinite",
        "--write-info-json", "--write-thumbnail", "--convert-thumbnails", "jpg",
        "--print", "after_move:filepath", "-o", f"{absolute_job_dir}/video.%(ext)s"
    ]

    if COOKIE_FILE_PATH.exists():
        cmd.extend(["--cookies", str(COOKIE_FILE_PATH.resolve())])

    if quality == "audio":
        cmd.extend(["--extract-audio", "--audio-format", "mp3"])
    else:
        cmd.extend(["--merge-output-format", "mp4", "--postprocessor-args", "ffmpeg:-movflags +faststart"])

    if is_youtube:
        await ensure_xray() # 🚨 استارت موتور قدرتمند Xray 🚨
        cmd.extend([
            "--proxy", "socks5h://127.0.0.1:10808", # 🚨 انتقال ترافیک به تونل Xray
            "--extractor-args", "youtube:player_client=android", 
            "--remote-components", "ejs:github"
        ])

    cmd.append(url)
    print_log(f"Executing: {' '.join(cmd)}")

    process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise Exception(f"yt-dlp Exit code {process.returncode}")

    return True

async def main():
    print_log("✅ Railway Worker Ready! Polling Hugging Face for jobs...\n")

    yt_cookies = os.environ.get("YT_COOKIES")
    if yt_cookies:
        with open("cookies.txt", "w", encoding="utf-8") as f: f.write(yt_cookies)

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
                        quality = data.get("quality", "max") 
                        
                        job_id = str(uuid.uuid4())[:8]
                        job_dir = Path(f"jobs/{job_id}")
                        job_dir.mkdir(parents=True, exist_ok=True)
                        print_log(f"[{job_id}] 📥 Job Acquired: {url} | Quality: {quality}")

                        try:
                            download_success = False
                            try:
                                await download_video_via_ytdlp(url, job_dir, quality)
                                download_success = True
                            except Exception as e:
                                print_log(f"⚠️ yt-dlp download failed: {e}")
                            
                            if not download_success and not ("youtube.com" in url or "youtu.be" in url):
                                print_log("🔄 Falling back to Cobalt API...")
                                await download_via_cobalt(url, job_dir, quality)
                                download_success = True

                            matches = list(job_dir.glob("video.mp4")) or list(job_dir.glob("video.mp3")) or [m for m in job_dir.glob("video.*") if m.suffix.lower() not in ['.jpg', '.json']]
                            if not matches or not download_success: raise FileNotFoundError("Video/Audio file not found on disk!")
                            file_path = str(matches[0].resolve())

                            thumb_path = None
                            thumb_matches = list(job_dir.glob("*.jpg"))
                            if thumb_matches: thumb_path = str(thumb_matches[0].resolve())

                            width, height, duration = 0, 0, 0
                            info_matches = list(job_dir.glob("*.info.json"))
                            if info_matches:
                                try:
                                    with open(info_matches[0], 'r', encoding='utf-8') as f:
                                        info = json.load(f)
                                        width, height, duration = info.get('width', 0), info.get('height', 0), info.get('duration', 0)
                                except Exception: pass

                            last_percent = -1
                            async def progress_callback(current, total):
                                nonlocal last_percent
                                if total > 0:
                                    percent = int((current * 100) / total)
                                    if percent % 10 == 0 and percent != last_percent:
                                        last_percent = percent
                                        print_log(f"[{job_id}] 🚀 Uploading Progress: {percent}%")

                            is_audio = quality == "audio"
                            upload_kwargs = {
                                "chat_id": chat_id, 
                                "caption": f"🎬 **دانلود موفق**\n⚡ کیفیت: {quality}", 
                                "reply_to_message_id": message_id, 
                                "progress": progress_callback
                            }
                            
                            if is_audio:
                                upload_kwargs["audio"] = file_path
                                if thumb_path: upload_kwargs["thumb"] = thumb_path
                                if duration: upload_kwargs["duration"] = int(duration)
                            else:
                                upload_kwargs["video"] = file_path
                                upload_kwargs["supports_streaming"] = True
                                if thumb_path: upload_kwargs["thumb"] = thumb_path
                                if width: upload_kwargs["width"] = width
                                if height: upload_kwargs["height"] = height
                                if duration: upload_kwargs["duration"] = int(duration)

                            upload_success = False
                            for attempt in range(3):
                                chosen_session = random.choice(BOT_SESSIONS)
                                upload_app = Client(f"railway_{job_id}_{attempt}", api_id=API_ID, api_hash=API_HASH, session_string=chosen_session, in_memory=True)
                                try:
                                    async with upload_app:
                                        print_log(f"[{job_id}] 🚀 Attempt {attempt+1}: Uploading to Telegram...")
                                        
                                        if is_audio: await upload_app.send_audio(**upload_kwargs)
                                        else: await upload_app.send_video(**upload_kwargs)
                                            
                                        try: await upload_app.delete_messages(chat_id, status_msg_id)
                                        except: pass
                                    print_log(f"[{job_id}] 🎉 Job Completed!")
                                    upload_success = True
                                    break
                                except (AuthKeyDuplicated, AuthKeyInvalid): continue
                                except FloodWait as e: await asyncio.sleep(e.value + 2)
                                    
                            if not upload_success: print_log(f"[{job_id}] ❌ Upload failed after all retries.")

                        except Exception as e: print_log(f"[{job_id}] ❌ Error during processing: {e}")
                        finally: shutil.rmtree(job_dir, ignore_errors=True)
                    else: await asyncio.sleep(5)
            except Exception: await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
