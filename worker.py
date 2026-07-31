import os
import sys
import asyncio
import aiohttp
import shutil
import uuid
import random
import json
import urllib.parse
from pathlib import Path
from pyrogram import Client
from pyrogram.errors import FloodWait, AuthKeyDuplicated, AuthKeyInvalid

def print_log(msg):
    print(msg, flush=True)
    sys.stdout.flush()

# ─── تنظیمات اختصاصی ───
API_ID = 39884025
API_HASH = "24ce21160fcabd7e7c0de00a77b45ef3"

# 🚨 توکن جدید رباتت را حتماً جایگزین متن زیر کن! 🚨
BOT_TOKEN = "8813125038:AAHTqUJKP-i8zp1gktfC7i54N7ngC7BHOdU"

HF_URL = "https://downloads89oouu-downloader.hf.space" 
WORKER_SECRET = "ali_vip_worker_2026"

# سشن‌های جدید و تازه‌نفس گیت‌هاب
bot_sessions_env = os.getenv("BOT_SESSIONS")
if bot_sessions_env:
    try:
        BOT_SESSIONS = json.loads(bot_sessions_env)
    except Exception:
        BOT_SESSIONS = [s.strip() for s in bot_sessions_env.split(",") if s.strip()]
else:
    BOT_SESSIONS = [
        "BAJglPkAC_SKECo8kmycaRgH9ENQVFmG2iJd3ZLQM78j--fsiXEPjZ-xfRr54zzJuVMvK6lU0pBXqzImWKgO2_bjvexr0KEAoCx8Og47Z0Nwi5aNuCDl4Lhh2uOYkFBaoCXIm2swNNVQ1KboP_d1g6OCbXCrg-6GdaAhKEUcJpTMseWUkwleRF5lT71vxxTpAs395gsWQh3x532Y-roAvSh5eyazksRNlxC8hO4TzUEbSRx6I1K1pNjFWL4GRsho8LILS81oaHeg1g3dllmDjZJxRgjOwT1EhdY5ldYrrWy5kpPere3a0HTd_IHUi4AMSVfzmaY_4FYh3ZlnXoXyJbGs15XS5AAAAAINTZ2uAQ",
        "BAJglPkAkVAkoGtHOx1cbzVQlXR6NUpxygWj7i0g7U_g2DaqnrKHh5SJvvm5f5M_ZowkNQxGEMN_qYPTpUqUvbuUzuP-pZH9eEDKHlvbnFka3wzUEk5tFKphPn37VH7z1nUQSJvfoJbTa2lwwiw8BS5ZN8a4aTL7z6pI9CBEuq-s-H2e9BboYiE8ZhcXlvKn_1i7VMMnTZq1dr9uhpo-I1H82j3hY9XhEvzMycoihavZDwrStbqVjBw9myQDCLMJ7i-IV-mJzy0FvRAua5NusHa1o8-44Efn9Xmh-VyqLZRZo7WD3RIh6deLP3WcsTZAokptuYkF98izN_Cz9Wi1Il7PTs869gAAAAINTZ2uAQ",
        "BAJglPkAVtz7FKDcBjXi5XJj0ZA8bEvx_Gb9MO2sfnVvQwqSpWllWooa9gmJdcZm8kuKzbSgdWjC1ugkQ_yng-ERFgHgte0M--TT4HCaWU_i8Pj45m3Wgmjug0QvkOm-v6_wplz8e-1KlCXjTggw-f6eFpxK9Bo1WdDny9r9uylG-tIM9togZzfdtVMwYWgjCfo2yo7FR5XIY0ms7WEH-d00unrzJv6QuhWYnWjX5-Krd1w-PDRQ_nr9YJiruWoY-rCZrR_r6WJ36xI5GebAz2zk76-suybSxypKaXhDX1XQ6jCWQVAjh5S8pm6R7ArZ0ULko--CDbXWq6gOWg7BZe_2MRRMDwAAAAINTZ2uAQ",
        "BAJglPkAc1OzMtwFUpXVo4sC7EZNBL7cDZvv2-a8ZwPLbzPrCF5rQ8D6vxyRxaROpsvojreGiJaHe0wBuz90HAkkZOTsu9zxRP0gVHcIAvPcLHBg1WtpUThWjfIzx93U5vv2QjeYZ__el0C_u00ZizIU6ullp1BW1LR2NJXZ9Vvi0-p__2p7cdyYsaxMzI4Iisk1ntFFxqr_N6lcl9FTZ3GeveZ7ElRo3H-zjocyDwpXaUlqnsB1-1ykKH90kcddjoHIB_WxvqaDOpU3CCOjObPAALsaoIYAjP-VO-dwXfSgNXDXVneRHVisAvEiPffeQbql20XesJRYIOWAaSc3qXTvhqT-zAAAAAINTZ2uAQ",
        "BAJglPkATX4SkUzK71SnjztYffdZeCp40IJ2g5gUXQfia0zaHxkFvaKfljZFTrBCgJK8GtVXOD9QO9yMxVjtKXJ0N0pzuachiA9WpzgHrUTvE8o7puJzRfCV9F4F-8AYEJtfzrAuz6NtrH-98bGYAboA0ctv2YRb-5XuKalfdLlrpWJ6GaqOXRoVaf993tq-W8PDsb8rEsVo9MTb-46VfLEBuZ8E33LnMwB5rpc16wLBUQ6xX72iFJICdVpK_lbJKVRreM9Vj7fVzhZHLcqZzPIDNjqjlXqPBsnJGtcA-TV5QQoKD9C052Q-YwI8sCVBVeN0cAYWEzSrWXkXfedXo8I68YI49gAAAAINTZ2uAQ"
    ]

app = Client("vip_worker", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

COOKIE_FILE_PATH = Path(__file__).parent / "cookies.txt"

def _setup_cookies():
    cookie_data = os.getenv("YT_COOKIES")
    if cookie_data and len(cookie_data.strip()) > 0:
        with open(COOKIE_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(cookie_data)
        print_log("🍪 YT_COOKIES detected! cookies.txt written successfully.")
        return True
    return False

async def start_xray_proxy():
    vless_link = os.getenv("VLESS_LINK")
    if not vless_link: return
    try:
        print_log("⚙️ Configuring Xray VLESS Client...")
        vless_url = vless_link.split("#")[0]
        parsed = urllib.parse.urlparse(vless_url)
        qs = urllib.parse.parse_qs(parsed.query)
        config = {
            "log": {"loglevel": "warning"},
            "inbounds": [{"port": 10808, "listen": "127.0.0.1", "protocol": "socks"}],
            "outbounds": [{
                "protocol": "vless",
                "settings": {"vnext": [{"address": parsed.hostname, "port": int(parsed.port or 443), "users": [{"id": parsed.username, "encryption": "none"}]}]},
                "streamSettings": {
                    "network": qs.get("type", ["tcp"])[0], "security": qs.get("security", ["none"])[0],
                    "wsSettings": {"path": qs.get("path", ["/"])[0], "headers": {"Host": qs.get("host", [""])[0]}},
                    "tlsSettings": {"serverName": qs.get("sni", [""])[0], "fingerprint": qs.get("fp", ["chrome"])[0], "alpn": qs.get("alpn", ["http/1.1"])[0].split(",")}
                }
            }]
        }
        with open("config.json", "w") as f: json.dump(config, f)
        import subprocess
        subprocess.Popen(["/app/xray_bin/xray", "run", "-c", "config.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        await asyncio.sleep(3)
        print_log("✅ Xray Proxy is running on SOCKS5 127.0.0.1:10808")
    except Exception as e: print_log(f"❌ Failed to start Xray: {e}")

async def download_video_via_ytdlp(url, job_dir, quality="max"):
    is_youtube = "youtube.com" in url.lower() or "youtu.be" in url.lower()
    absolute_job_dir = str(job_dir.resolve()) 
    
    # 🚨 تله‌ی هوشمند کیفیت: حذف بخش /b تا در صورت نبودن کیفیت بالا، دانلود یواشکی متوقف شود 🚨
    if is_youtube:
        if quality == "1080": format_str = "bv*[height>=1080]+ba" 
        elif quality == "720": format_str = "bv*[height>=720]+ba"
        elif quality == "480": format_str = "bv*[height>=480]+ba"
        elif quality == "audio": format_str = "ba/b"
        else: format_str = "bv*+ba/b"
    else:
        format_str = "b"
        if quality == "1080": format_str = "best[height<=1080]/best"
        elif quality == "720": format_str = "best[height<=720]/best"
        elif quality == "480": format_str = "best[height<=480]/best"
        elif quality == "audio": format_str = "ba/b"
    
    cmd = [
        "yt-dlp", "--rm-cache-dir", "-f", format_str, 
        "--write-info-json", "--write-thumbnail", "--convert-thumbnails", "jpg",
        "--no-check-certificate", "--retries", "5", "--fragment-retries", "infinite",
        "-o", f"{absolute_job_dir}/video.%(ext)s"
    ]
    
    if quality == "audio":
        cmd.extend(["--extract-audio", "--audio-format", "mp3"])
    else:
        cmd.extend(["--merge-output-format", "mp4", "--postprocessor-args", "ffmpeg:-movflags +faststart"])

    print_log("🥷 Trying Ninja Mode (Direct Connection + iOS Client)...")
    ninja_cmd = list(cmd)
    if is_youtube:
        ninja_cmd.extend(["--extractor-args", "youtube:player_client=ios,android", "--remote-components", "ejs:github", "--impersonate", "chrome"])
    ninja_cmd.append(url)
    
    process = await asyncio.create_subprocess_exec(*ninja_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    
    if process.returncode == 0:
        print_log("✅ Ninja Mode Success!")
        return True
        
    print_log(f"⚠️ Ninja Mode failed (Exit code {process.returncode}). Initiating Tank Mode fallback...")

    print_log("🛡️ Trying Tank Mode (VLESS Proxy + Cookies + TV/VR Client)...")
    _setup_cookies()
    
    tank_cmd = list(cmd)
    if os.getenv("VLESS_LINK"):
        tank_cmd.extend(["--proxy", "socks5h://127.0.0.1:10808"])
    if COOKIE_FILE_PATH.exists():
        tank_cmd.extend(["--cookies", str(COOKIE_FILE_PATH.resolve())])
        
    if is_youtube:
        tank_cmd.extend(["--extractor-args", "youtube:player_client=tv,android_vr", "--remote-components", "ejs:github", "--impersonate", "chrome", "--force-ipv4"])
    tank_cmd.append(url)
    
    process = await asyncio.create_subprocess_exec(*tank_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    
    if process.returncode == 0:
        print_log("✅ Tank Mode Success!")
        return True
        
    error_msg = stderr.decode('utf-8', errors='ignore').strip()
    raise Exception(f"yt-dlp failed completely. Last error: {error_msg}")

async def download_via_cobalt(url, job_dir, quality="max"):
    print_log(f"🌟 Starting Cobalt API fallback for: {url} | Quality: {quality}")
    
    api_urls = ["https://api.cobalt.tools/api/json", "https://cobalt.q0.pm/api/json", "https://co.wuk.sh/api/json"]
    headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    q_val = "1080" if quality == "max" else quality
    payload = {"url": url}
    
    if quality == "audio": 
        payload["isAudioOnly"] = True
    else:
        payload["videoQuality"] = q_val if q_val in ["1080", "720", "480", "360", "240", "144"] else "1080"
        payload["isAudioMuted"] = False

    async with aiohttp.ClientSession() as session:
        video_url = None
        for api in api_urls:
            try:
                async with session.post(api, headers=headers, json=payload, timeout=15) as resp:
                    if resp.status in [200, 202]:
                        data = await resp.json()
                        if data.get("status") in ["redirect", "stream", "success", "picker"]:
                            video_url = data.get("url")
                            if video_url: break
            except Exception as e: 
                continue

        if not video_url: raise Exception("❌ All Cobalt APIs failed or blocked.")

        ext = "mp3" if quality == "audio" else "mp4"
        file_path = f"{job_dir.resolve()}/video.{ext}"
        print_log(f"📥 Downloading raw media from Cobalt to: {file_path}")
        async with session.get(video_url) as video_resp:
            if video_resp.status != 200: raise Exception("Download from Cobalt stream failed.")
            with open(file_path, 'wb') as f:
                while True:
                    chunk = await video_resp.content.read(2 * 1024 * 1024)
                    if not chunk: break
                    f.write(chunk)
        print_log("✅ Successfully downloaded via Cobalt!")
        return True

async def main():
    await start_xray_proxy()
    _setup_cookies()

    print_log("\n" + "="*50)
    print_log("🚀 Starting Persistent Telegram Client...")
    await app.start()
    print_log("✅ SUPER WORKER Ready! Polling Hugging Face for jobs...\n")

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
                                print_log(f"⚠️ yt-dlp failed: {e}")
                            
                            if not download_success:
                                print_log("🔄 Falling back to Cobalt API for high quality extraction...")
                                try:
                                    await download_via_cobalt(url, job_dir, quality)
                                    download_success = True
                                except Exception as cobalt_err:
                                    print_log(f"❌ Cobalt API also failed: {cobalt_err}")
                                    raise Exception("All download methods (yt-dlp & Cobalt) failed.")

                            matches = list(job_dir.glob("video.mp4")) or list(job_dir.glob("video.mp3")) or [m for m in job_dir.glob("video.*") if m.suffix.lower() not in ['.jpg', '.json']]
                            if not matches or not download_success: raise FileNotFoundError("Video/Audio file not found on disk!")
                            file_path = str(matches[0].resolve())

                            thumb_path = None
                            thumb_matches = list(job_dir.glob("*.jpg"))
                            if thumb_matches: thumb_path = str(thumb_matches[0].resolve())

                            width, height, duration, title = 0, 0, 0, "Video"
                            info_matches = list(job_dir.glob("*.info.json"))
                            if info_matches:
                                try:
                                    with open(info_matches[0], 'r', encoding='utf-8') as f:
                                        info = json.load(f)
                                        width, height, duration, title = info.get('width', 0), info.get('height', 0), info.get('duration', 0), info.get('title', 'Video')
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
                            quality_text = "صدا (MP3)" if is_audio else f"{quality}p" if quality != "max" else "بهترین کیفیت"
                            upload_kwargs = {
                                "chat_id": chat_id, 
                                "caption": f"🎬 **{title}**\n\n⚙️ کیفیت: `{quality_text}`\n⚡ دریافت سریع", 
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
