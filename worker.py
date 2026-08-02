import os
import sys
import time
import asyncio
import aiohttp
import shutil
import uuid
import json
import urllib.parse
import subprocess
from pathlib import Path

from pyrogram import Client
from pyrogram.errors import FloodWait, AuthKeyDuplicated, AuthKeyInvalid

# ---------- 🚀 uvloop: ایونت‌لوپ سریع‌تر (در صورت نصب) ----------
try:
    import uvloop
    uvloop.install()
except ImportError:
    pass

def print_log(msg):
    print(msg, flush=True)
    sys.stdout.flush()

API_ID = 39884025
API_HASH = "24ce21160fcabd7e7c0de00a77b45ef3"
HF_URL = "https://downloads89oouu-downloader.hf.space"
WORKER_SECRET = "ali_vip_worker_2026"

# ---------- ⚙️ تنظیمات سرعت (قابل تغییر از Env) ----------
MAX_JOBS = int(os.getenv("MAX_JOBS", "3"))                 # تعداد Job همزمان
UPLOAD_WORKERS = int(os.getenv("UPLOAD_WORKERS", "16"))    # ورکرهای Pyrogram
MAX_TRANSMISSIONS = int(os.getenv("MAX_TRANSMISSIONS", "8"))  # آپلود موازی چانک (pyrofork)
ARIA2 = shutil.which("aria2c")                             # دانلودر چندکاناله

bot_sessions_env = os.getenv("BOT_SESSIONS")
if bot_sessions_env:
    try:
        BOT_SESSIONS = json.loads(bot_sessions_env)
    except Exception:
        BOT_SESSIONS = [s.strip() for s in bot_sessions_env.split(",") if s.strip()]
else:
    BOT_SESSIONS = [
         "BAJglPkAO0RCs_NW3uELJV95CRa17odKleHTrosLpwhRpmfX3N1K7SqQobP1kJvc6czR6E1z5j9TChl_X5_hHlAtx5RZH-xdFiOfJ_CrTMrTRKY2wzpe9dC2E9CitkBqwgZQDyHbiLZC-mrJPoXgDZ2tGeNwMMbWd3kHal3me4N8HloJcvwbR93nopWSZaO1VE9OGol8iczRSPovbqMcexgkquu7yb8EO2U6aeHZOqiExD8Vdibnj8W4QUQLA60bdhNhZGSC4EmdKXKCq32DfZHFtNNxC3RMmh3h1xJdS6Jf4W9IJaR32E5mS8pM-COP9N9pCoLWlw-2XjQiSu5KM9AQjGcs5wAAAAINTZ2uAQ",
        "BAJglPkAEIHq7qQmQFqUMINW5U6OolhKB8sxXd5mn0pLpwl6mB5fRnvM8UFmd2wf-7N0oDZ0-Rms2QlSr9JMkRoXAAGxKTp0tj0kK_mUobjFlOtS8hctWZgSwNjcsEDXprLU4f7CMQLvRskRzpPkShd1TxsEuzjtjg2sq9_Ed1hBQan1-BFBdAJ2wVNGSfg6zOAUBgV1XUU1_SAl7LywJJQUmSeQEB8dBX_-tmUqJVzpJI6iorwqPxYu8n5k2bPnXdtRB-vbZf-Oi2Cv-1wl-cvG_0vTVPcVUnTiIJjigDpXRz_Eu0lmVIiRhSNtxJvtSj_4u1z-Ze9qnQOCfTNQ3dRQQHYO1wAAAAINTZ2uAQ",
        "BAJglPkAq5Ab9cqjvp2qvWWxpgmw7wOq2W6wlOC6EUCD9QOu5mAtsAyr7CaY9eOTUCpjB1yuYvE9UyQy6EpZdh-AupsQ6wwQPGjxe6b6wkv7gVm8z0vdO5f54I_dh8erfAY1Lz-186zlCumDcV63EZwm2MO27qKdzbjOocILR4SKECgrvxk1bEqfLHlp5D8nFyTBZeAko4iPWhh8O6d9WMdLQDodXMG-dJCNwQzqE6Vyui1BRNxFIXKoz1XGnZ6iPPuf3eKJH-ayZ3FHJJUei0kYO4MKl_gy3Uv1WFzvTEuvTZtbjyKFKMSp4YH39_OdTdUwXbHca-lQhGwukSztM10quL9_xAAAAAINTZ2uAQ"
    ]

COOKIE_FILE_PATH = Path(__file__).parent / "cookies.txt"

def _setup_cookies():
    cookie_data = os.getenv("YT_COOKIES")
    if cookie_data and len(cookie_data.strip()) > 0:
        with open(COOKIE_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(cookie_data)
        print_log("🍪 YT_COOKIES detected! cookies.txt written successfully.")
        return True
    return False

# ============================================================
# 🚀 Upload Client Pool — اتصال یکباره، استفاده مکرر
# ============================================================
def make_client(name, session_string):
    kwargs = dict(
        api_id=API_ID, api_hash=API_HASH,
        session_string=session_string, in_memory=True,
        no_updates=True, workers=UPLOAD_WORKERS,
    )
    try:
        # pyrofork: آپلود موازی چند چانک = جهش بزرگ سرعت آپلود
        return Client(name, max_concurrent_transmissions=MAX_TRANSMISSIONS, **kwargs)
    except TypeError:
        return Client(name, **kwargs)  # pyrogram معمولی

async def start_upload_pool():
    """همه سشن‌ها به‌صورت همزمان وصل می‌شن؛ دیگه هزینه connect در هر Job نیست."""
    async def _start(i, s):
        c = make_client(f"pool_{i}", s)
        try:
            await c.start()
            print_log(f"🔌 Upload client #{i+1} connected.")
            return c
        except (AuthKeyDuplicated, AuthKeyInvalid) as e:
            print_log(f"⚠️ Session #{i+1} dropped: {type(e).__name__}")
            return None
        except Exception as e:
            print_log(f"⚠️ Session #{i+1} connect error: {e}")
            return None

    clients = [c for c in await asyncio.gather(*[_start(i, s) for i, s in enumerate(BOT_SESSIONS)]) if c]
    q = asyncio.Queue()
    for c in clients:
        q.put_nowait(c)
    print_log(f"✅ Upload pool ready: {q.qsize()}/{len(BOT_SESSIONS)} clients.")
    return q

async def upload_with_pool(upload_queue, job_id, is_audio, upload_kwargs, chat_id, status_msg_id):
    attempts = max(3, upload_queue.qsize() + 1)
    for attempt in range(attempts):
        client = await upload_queue.get()
        try:
            print_log(f"[{job_id}] 🚀 Upload attempt {attempt+1} (Direct Mode)...")
            if is_audio:
                await client.send_audio(**upload_kwargs)
            else:
                await client.send_video(**upload_kwargs)
            try:
                await client.delete_messages(chat_id, status_msg_id)
            except Exception:
                pass
            upload_queue.put_nowait(client)
            return True
        except FloodWait as e:
            upload_queue.put_nowait(client)
            wait = min(e.value + 2, 60)
            print_log(f"[{job_id}] ⏳ FloodWait {e.value}s")
            await asyncio.sleep(wait)
        except (AuthKeyDuplicated, AuthKeyInvalid) as e:
            # سشن خراب به صف برنمی‌گرده
            print_log(f"[{job_id}] ⚠️ Bad session removed from pool: {type(e).__name__}")
        except Exception as e:
            upload_queue.put_nowait(client)
            print_log(f"[{job_id}] ❌ Upload error: {e}")
            await asyncio.sleep(2)
    return False

# ============================================================
# 🌐 Xray Proxy
# ============================================================
async def start_xray_proxy():
    vless_link = os.getenv("VLESS_LINK")
    if not vless_link:
        print_log("⚠️ VLESS_LINK is not set. Xray will not start.")
        return
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
                "settings": {"vnext": [{
                    "address": parsed.hostname,
                    "port": int(parsed.port or 443),
                    "users": [{"id": parsed.username, "encryption": "none"}]
                }]},
                "streamSettings": {
                    "network": qs.get("type", ["tcp"])[0],
                    "security": qs.get("security", ["none"])[0],
                    "wsSettings": {"path": qs.get("path", ["/"])[0], "headers": {"Host": qs.get("host", [""])[0]}},
                    "tlsSettings": {
                        "serverName": qs.get("sni", [""])[0],
                        "fingerprint": qs.get("fp", ["chrome"])[0],
                        "alpn": qs.get("alpn", ["http/1.1"])[0].split(",")
                    }
                }
            }]
        }
        with open("config.json", "w") as f:
            json.dump(config, f)
        print_log("🚀 Starting Xray Process in background...")
        subprocess.Popen(["/app/xray_bin/xray", "run", "-c", "config.json"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        await asyncio.sleep(3)
        print_log("✅ Xray Proxy is running on SOCKS5 127.0.0.1:10808")
    except Exception as e:
        print_log(f"❌ Failed to start Xray: {e}")

# ============================================================
# ⬇️ دانلود
# ============================================================
def _format_selector(is_youtube, quality):
    """ترجیح mp4/m4a → مرج سریع‌تر، بدون نیاز به ری‌انکد، سازگار با تلگرام"""
    if quality == "audio":
        return "ba/b"
    if is_youtube:
        if quality == "1080": return "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/bv*[height<=1080]+ba/b"
        if quality == "720":  return "bv*[height<=720][ext=mp4]+ba[ext=m4a]/bv*[height<=720]+ba/b"
        if quality == "480":  return "bv*[height<=480][ext=mp4]+ba[ext=m4a]/bv*[height<=480]+ba/b"
        return "bv*[ext=mp4]+ba[ext=m4a]/bv*+ba/b"
    return "b"

def _base_ytdlp_cmd(job_dir, quality):
    is_youtube = True  # فرمت فقط برای یوتیوب متفاوته، ولی فلگهای سرعت عمومی‌ان
    cmd = [
        "yt-dlp", "--rm-cache-dir", "--no-playlist", "--no-progress",
        "-f", _format_selector(False, quality),  # placeholder، پایین بازنویسی می‌شه
        "--write-info-json", "--write-thumbnail", "--convert-thumbnails", "jpg",
        "--no-check-certificate",
        "--retries", "5", "--fragment-retries", "infinite",
        "--file-access-retries", "3", "--socket-timeout", "20",
        "--throttled-rate", "100K",          # اگه یوتیوب تارتل کرد، ریکانکت و ادامه
        "--concurrent-fragments", "8",       # دانلود موازی فرگمنت‌های HLS/DASH
        "-o", f"{str(job_dir.resolve())}/video.%(ext)s",
    ]
    if ARIA2:
        # 🚀 دانلود چندکاناله — معمولاً ۲ تا ۵ برابر سریع‌تر
        cmd += ["--downloader", "aria2c",
                "--downloader-args",
                "aria2c:-x 16 -s 16 -k 2M --file-allocation=none --summary-interval=0 --console-log-level=warn"]
    if quality == "audio":
        cmd += ["--extract-audio", "--audio-format", "mp3"]
    else:
        # ⚠️ faststart حذف شد — یه پاس کامل بازنویسی فایل بود و تلگرام بهش نیاز نداره
        cmd += ["--merge-output-format", "mp4"]
    return cmd

async def download_video_via_ytdlp(url, job_dir, quality="max"):
    is_youtube = "youtube.com" in url.lower() or "youtu.be" in url.lower()
    base_cmd = _base_ytdlp_cmd(job_dir, quality)
    # اصلاح سلکتور فرمت بر اساس یوتیوب بودن
    base_cmd[base_cmd.index("-f") + 1] = _format_selector(is_youtube, quality)

    # 🥷 فاز اول: Ninja Mode
    print_log("🥷 Trying Ninja Mode (Direct + Modern Clients)...")
    ninja_cmd = list(base_cmd)
    if is_youtube:
        ninja_cmd += [
            "--extractor-args", "youtube:player_client=web,android_vr,tv_downgraded;player_skip=webpage",
            "--remote-components", "ejs:github",
            "--impersonate", "chrome", "--force-ipv4"
        ]
    ninja_cmd.append(url)
    process = await asyncio.create_subprocess_exec(*ninja_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    _, stderr = await process.communicate()
    if process.returncode == 0:
        print_log("✅ Ninja Mode Success!")
        return True
    print_log(f"⚠️ Ninja failed (code {process.returncode}). Tank Mode fallback...")

    # 🛡️ فاز دوم: Tank Mode
    print_log("🛡️ Trying Tank Mode (VLESS + Cookies + Web Creator)...")
    _setup_cookies()
    tank_cmd = list(base_cmd)
    if os.getenv("VLESS_LINK"):
        tank_cmd += ["--proxy", "socks5h://127.0.0.1:10808"]
    if COOKIE_FILE_PATH.exists():
        tank_cmd += ["--cookies", str(COOKIE_FILE_PATH.resolve())]
    if is_youtube:
        tank_cmd += [
            "--extractor-args", "youtube:player_client=web_creator,tv_downgraded,android_vr;player_skip=webpage",
            "--remote-components", "ejs:github",
            "--impersonate", "chrome", "--force-ipv4"
        ]
    tank_cmd.append(url)
    process = await asyncio.create_subprocess_exec(*tank_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    _, stderr = await process.communicate()
    if process.returncode == 0:
        print_log("✅ Tank Mode Success!")
        return True
    raise Exception(f"Both modes failed. Last error: {stderr.decode('utf-8', errors='ignore').strip()[-500:]}")

COBALT_APIS = ["https://api.cobalt.tools/api/json", "https://cobalt.q0.pm/api/json", "https://api.cobalt.tools/"]

async def download_via_cobalt(session, url, job_dir, quality="max"):
    """همه APIهای Cobalt همزمان صدا زده می‌شن؛ اولین موفق برنده‌ست."""
    print_log(f"🌟 Cobalt fallback: {url} | {quality}")
    headers = {
        "Accept": "application/json", "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    payload = {"url": url, "vQuality": quality if quality != "audio" else "max"}
    if quality == "audio":
        payload["isAudioOnly"] = True

    async def _try(api):
        try:
            async with session.post(api, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=12)) as r:
                if r.status in (200, 202):
                    return (await r.json()).get("url")
        except Exception:
            return None

    results = await asyncio.gather(*[_try(a) for a in COBALT_APIS])
    video_url = next((u for u in results if u), None)
    if not video_url:
        raise Exception("❌ All Cobalt APIs failed.")

    ext = "mp3" if quality == "audio" else "mp4"
    file_path = f"{job_dir.resolve()}/video.{ext}"
    async with session.get(video_url, timeout=aiohttp.ClientTimeout(total=900)) as r:
        if r.status != 200:
            raise Exception(f"Cobalt file download failed: HTTP {r.status}")
        with open(file_path, "wb") as f:
            async for chunk in r.content.iter_chunked(4 * 1024 * 1024):
                f.write(chunk)
    print_log("✅ Cobalt download done.")
    return True

# ============================================================
# 📦 پردازش هر Job
# ============================================================
async def process_job(session, upload_queue, data):
    url = data["url"]
    chat_id, message_id, status_msg_id = int(data["chat_id"]), int(data["message_id"]), int(data["status_msg_id"])
    quality = data.get("quality", "max")
    job_id = str(uuid.uuid4())[:8]
    job_dir = Path(f"jobs/{job_id}")
    job_dir.mkdir(parents=True, exist_ok=True)
    t_start = time.monotonic()
    print_log(f"[{job_id}] 📥 Job Acquired: {url} | Quality: {quality}")

    try:
        # ---------- دانلود ----------
        t0 = time.monotonic()
        is_yt = "youtube.com" in url or "youtu.be" in url
        try:
            await download_video_via_ytdlp(url, job_dir, quality)
        except Exception as e:
            print_log(f"[{job_id}] ⚠️ yt-dlp failed: {e}")
            if is_yt:
                raise
            await download_via_cobalt(session, url, job_dir, quality)
        dl_time = time.monotonic() - t0

        matches = list(job_dir.glob("video.mp4")) or list(job_dir.glob("video.mp3")) or \
                  [m for m in job_dir.glob("video.*") if m.suffix.lower() not in (".jpg", ".json")]
        if not matches:
            raise FileNotFoundError("Media file not found on disk!")
        file_path = str(matches[0].resolve())
        size_mb = os.path.getsize(file_path) / 1e6
        print_log(f"[{job_id}] ⬇️ {size_mb:.1f}MB in {dl_time:.1f}s ({size_mb / max(dl_time, 0.1):.1f} MB/s)")

        thumb = next(iter(job_dir.glob("*.jpg")), None)
        thumb_path = str(thumb.resolve()) if thumb else None

        width = height = duration = 0
        info_file = next(iter(job_dir.glob("*.info.json")), None)
        if info_file:
            try:
                info = json.loads(info_file.read_text(encoding="utf-8"))
                width, height, duration = info.get("width", 0), info.get("height", 0), info.get("duration", 0)
            except Exception:
                pass

        # قطع پروکسی سطح سیستم برای آپلود مستقیم پرسرعت
        for k in ("http_proxy", "https_proxy", "ALL_PROXY", "HTTP_PROXY", "HTTPS_PROXY"):
            os.environ.pop(k, None)

        # پراگرس سبک: حداکثر هر ۵ ثانیه یک لاگ
        last = {"t": 0.0, "p": -1}
        async def progress_callback(current, total):
            if total <= 0:
                return
            p = int(current * 100 / total)
            now = time.monotonic()
            if (p == 100 or now - last["t"] >= 5) and p != last["p"]:
                last["t"], last["p"] = now, p
                print_log(f"[{job_id}] 🚀 Uploading: {p}%")

        is_audio = quality == "audio"
        upload_kwargs = {
            "chat_id": chat_id,
            "caption": "🎬 **دانلود موفق**\n⚡ دریافت سریع از دیتاسنتر",
            "reply_to_message_id": message_id,
            "progress": progress_callback,
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

        # ---------- آپلود ----------
        t1 = time.monotonic()
        ok = await upload_with_pool(upload_queue, job_id, is_audio, upload_kwargs, chat_id, status_msg_id)
        up_time = time.monotonic() - t1
        if ok:
            print_log(f"[{job_id}] 🎉 Done | ⬇️ {dl_time:.1f}s + ⬆️ {up_time:.1f}s = total {time.monotonic() - t_start:.1f}s")
        else:
            print_log(f"[{job_id}] ❌ Upload failed after all retries.")
    except Exception as e:
        print_log(f"[{job_id}] ❌ Error: {e}")
    finally:
        shutil.rmtree(job_dir, ignore_errors=True)

# ============================================================
# 🏁 Main
# ============================================================
async def main():
    await start_xray_proxy()

    print_log("🔍 DIAGNOSTIC SYSTEM STARTING:")
    print_log(f"📁 Cookies path: {COOKIE_FILE_PATH.resolve()}")
    print_log("✅ cookies.txt FOUND!" if COOKIE_FILE_PATH.exists() else "⚠️ cookies.txt NOT found!")
    print_log(f"🧩 aria2c: {'FOUND → multi-connection downloads ON 🚀' if ARIA2 else 'NOT found → install aria2 for 2-5x faster downloads'}")
    print_log("=" * 50)

    # 🚀 اتصال همزمان همه سشن‌ها قبل از شروع کار
    upload_queue = await start_upload_pool()
    if upload_queue.empty():
        print_log("🚨 WARNING: No valid upload sessions in pool!")

    sem = asyncio.Semaphore(MAX_JOBS)
    connector = aiohttp.TCPConnector(limit=64, ttl_dns_cache=600, enable_cleanup_closed=True)

    async with aiohttp.ClientSession(connector=connector) as http_session:
        async def run_job(data):
            try:
                await process_job(http_session, upload_queue, data)
            finally:
                sem.release()

        print_log("✅ VIP Worker Ready! Polling Hugging Face for jobs...\n")
        while True:
            try:
                headers = {"Authorization": f"Bearer {WORKER_SECRET}"}
                async with http_session.get(f"{HF_URL}/poll", headers=headers,
                                            timeout=aiohttp.ClientTimeout(total=20)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "no_job":
                            await asyncio.sleep(1.5)
                            continue
                        # 🚀 Job رو بسپار به تسک جدا و فوراً برگرد به polling → پردازش موازی
                        await sem.acquire()
                        asyncio.create_task(run_job(data))
                        await asyncio.sleep(0.3)
                    else:
                        await asyncio.sleep(4)
            except Exception as e:
                print_log(f"⚠️ Poll error: {e}")
                await asyncio.sleep(4)

if __name__ == "__main__":
    asyncio.run(main())
