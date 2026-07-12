import os
import sys
import asyncio
import aiohttp
import shutil
import uuid
import random
import json
import shlex
from pathlib import Path
from typing import Optional

from pyrogram import Client
from pyrogram.errors import FloodWait, AuthKeyDuplicated, AuthKeyInvalid


def print_log(msg: str) -> None:
    print(msg, flush=True)
    sys.stdout.flush()


# ─── Configuration ───
API_ID = int(os.environ.get("API_ID", "39884025"))
API_HASH = os.environ.get("API_HASH", "24ce21160fcabd7e7c0de00a77b45ef3")
HF_URL = os.environ.get("HF_URL", "https://downloads89oouu-downloader.hf.space")
WORKER_SECRET = os.environ.get("WORKER_SECRET", "ali_vip_worker_2026")

# Optional: extra yt-dlp args for YouTube only.
YTDLP_YOUTUBE_ARGS = os.environ.get("YTDLP_YOUTUBE_ARGS", "").strip()

# 🚨 سشن‌های ۵ گانه بدون نقص شما 🚨
BOT_SESSIONS = [
    "BAJglPkAO0RCs_NW3uELJV95CRa17odKleHTrosLpwhRpmfX3N1K7SqQobP1kJvc6czR6E1z5j9TChl_X5_hHlAtx5RZH-xdFiOfJ_CrTMrTRKY2wzpe9dC2E9CitkBqwgZQDyHbiLZC-mrJPoXgDZ2tGeNwMMbWd3kHal3me4N8HloJcvwbR93nopWSZaO1VE9OGol8iczRSPovbqMcexgkquu7yb8EO2U6aeHZOqiExD8Vdibnj8W4QUQLA60bdhNhZGSC4EmdKXKCq32DfZHFtNNxC3RMmh3h1xJdS6Jf4W9IJaR32E5mS8pM-COP9N9pCoLWlw-2XjQiSu5KM9AQjGcs5wAAAAINTZ2uAQ",
    "BAJglPkAEIHq7qQmQFqUMINW5U6OolhKB8sxXd5mn0pLpwl6mB5fRnvM8UFmd2wf-7N0oDZ0-Rms2QlSr9JMkRoXAAGxKTp0tj0kK_mUobjFlOtS8hctWZgSwNjcsEDXprLU4f7CMQLvRskRzpPkShd1TxsEuzjtjg2sq9_Ed1hBQan1-BFBdAJ2wVNGSfg6zOAUBgV1XUU1_SAl7LywJJQUmSeQEB8dBX_-tmUqJVzpJI6iorwqPxYu8n5k2bPnXdtRB-vbZf-Oi2Cv-1wl-cvG_0vTVPcVUnTiIJjigDpXRz_Eu0lmVIiRhSNtxJvtSj_4u1z-Ze9qnQOCfTNQ3dRQQHYO1wAAAAINTZ2uAQ",
    "BAJglPkAq5Ab9cqjvp2qvWWxpgmw7wOq2W6wlOC6EUCD9QOu5mAtsAyr7CaY9eOTUCpjB1yuYvE9UyQy6EpZdh-AupsQ6wwQPGjxe6b6wkv7gVm8z0vdO5f54I_dh8erfAY1Lz-186zlCumDcV63EZwm2MO27qKdzbjOocILR4SKECgrvxk1bEqfLHlp5D8nFyTBZeAko4iPWhh8O6d9WMdLQDodXMG-dJCNwQzqE6Vyui1BRNxFIXKoz1XGnZ6iPPuf3eKJH-ayZ3FHJJUei0kYO4MKl_gy3Uv1WFzvTEuvTZtbjyKFKMSp4YH39_OdTdUwXbHca-lQhGwukSztM10quL9_xAAAAAINTZ2uAQ",
    "BAJglPkAag83pxlJ7YpaNRtvcskvrUSiHrWl0HfkNboMFQuljSaFf6rieC84VjbF5aq9Pxrqrplls6jlfm7f4HC9D7JWa7bKqH9WjSplofQTsSbRYmkvQbUk2lmC7obeze9Unblo0VFc9kXXYG5No0hojvU4DCWTH3ZsY8uveLe8hVTSvlHCQiPcU0cJfnTZT9E2yK__EnlPojvEyavyi1h0pFzGWAybMlegSoHnLcX9VGU08qiRgkKOYdF3i5CV3heSijJiFlwI35wu-XYnqKm60zK2lMTJr2lfid6ssTcdy90brCa9C1BzAcnSGPQMy-GaoZo0ESsHEgGR4R7Z9smYtDFSTgAAAAINTZ2uAQ",
    "BAJglPkAnFvYFhSl3hlS4GIGt1SE-9C07UeeF0iteez4skX9hDjV3v_MpG7XN50rodIXGUghdjN_s_ePRYiY2_0d7cOROP1EvEhbcNp1c7FaJzYzRNbC4ejWuqdVF88yRh7Y1_1frOzsrEKlFF8UWq2bl6jeOPcTyl0OZGkosKhuXXIVbnM9h_-X96MLqvRCPlvW9IrBjby-HXHlE_RFAw-68JViTuVNZz6zEFsDWV0M-D5-L8nRfedqEFP0Y1pg_7JZQnCggHKYUJ7lvhCa9-XCo1PJQZjbj9ukDM53B7WoZgpfKGjtnuRfp0kHEuZYrZGtXUHs_N7wmLdrZfeolKQ6RNa1nAAAAAINTZ2uAQ"
]

COOKIE_FILE_PATH = Path("cookies.txt")
ALLOWED_MEDIA_EXTS = {
    ".mp4", ".mkv", ".webm", ".mov", ".m4v",
    ".mp3", ".m4a", ".aac", ".opus", ".ogg",
}


def ensure_cookie_file_from_env() -> None:
    yt_cookies = os.environ.get("YT_COOKIES")
    if yt_cookies and not COOKIE_FILE_PATH.exists():
        COOKIE_FILE_PATH.write_text(yt_cookies, encoding="utf-8")
        print_log("✅ Fresh cookies.txt generated on Railway from YT_COOKIES environment variable.")


def normalize_quality(quality: str) -> str:
    q = (quality or "max").strip().lower()
    aliases = {
        "1080p": "1080",
        "720p": "720",
        "480p": "480",
        "audio_only": "audio",
        "mp3": "audio",
    }
    return aliases.get(q, q)


def find_best_media_file(job_dir: Path) -> Optional[Path]:
    candidates = []
    for p in job_dir.rglob("*"):
        if not p.is_file():
            continue
        suffix = p.suffix.lower()
        if suffix not in ALLOWED_MEDIA_EXTS:
            continue
        if p.name.endswith(".part"):
            continue
        candidates.append(p)

    if not candidates:
        return None

    candidates.sort(key=lambda p: (p.stat().st_mtime, p.stat().st_size), reverse=True)
    return candidates[0].resolve()


async def run_subprocess(cmd: list[str]) -> tuple[int, str, str]:
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    return (
        process.returncode,
        stdout.decode("utf-8", errors="ignore"),
        stderr.decode("utf-8", errors="ignore"),
    )


async def download_via_cobalt(url: str, job_dir: Path, quality: str = "max") -> str:
    print_log(f"🌟 Starting Cobalt API fallback for: {url} | Quality: {quality}")
    api_urls = [
        "https://api.cobalt.tools/api/json",
        "https://cobalt.q0.pm/api/json",
        "https://api.cobalt.tools/",
    ]
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        ),
    }

    payload = {"url": url, "vQuality": quality if quality != "audio" else "max"}
    if quality == "audio":
        payload["isAudioOnly"] = True

    async with aiohttp.ClientSession() as session:
        media_url = None
        for api in api_urls:
            try:
                async with session.post(api, headers=headers, json=payload, timeout=15) as resp:
                    if resp.status in (200, 202):
                        data = await resp.json()
                        media_url = data.get("url")
                        if media_url:
                            break
            except Exception:
                continue

        if not media_url:
            raise Exception("❌ All Cobalt APIs failed.")

        ext = "mp3" if quality == "audio" else "mp4"
        file_path = job_dir / f"video.{ext}"

        async with session.get(media_url) as video_resp:
            if video_resp.status != 200:
                raise Exception("Download failed from Cobalt URL.")
            with open(file_path, "wb") as f:
                while True:
                    chunk = await video_resp.content.read(2 * 1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)

    print_log("✅ Successfully downloaded via Cobalt!")
    return str(file_path.resolve())


async def download_video_via_ytdlp(url: str, job_dir: Path, quality: str = "max") -> str:
    quality = normalize_quality(quality)
    print_log(f"🚜 Running yt-dlp... Quality requested: {quality}")

    is_youtube = "youtube.com" in url.lower() or "youtu.be" in url.lower()
    absolute_job_dir = str(job_dir.resolve())

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

    # 🚨 پروکسی به طور کامل از ریشه حذف شد 🚨
    cmd = [
        "yt-dlp",
        "-f", format_str,
        *sort_args,
        "--no-playlist",
        "--impersonate", "chrome",
        "--no-check-certificate",
        "--force-ipv4",
        "--retries", "5",
        "--fragment-retries", "infinite",
        "--write-info-json",
        "--write-thumbnail",
        "--convert-thumbnails", "jpg",
        "--print", "after_move:filepath",
        "-o", f"{absolute_job_dir}/video.%(ext)s",
    ]

    if COOKIE_FILE_PATH.exists():
        cmd.extend(["--cookies", str(COOKIE_FILE_PATH.resolve())])
        print_log("🍪 cookies.txt injected into yt-dlp.")

    if quality == "audio":
        cmd.extend([
            "--extract-audio",
            "--audio-format", "mp3",
        ])
    else:
        cmd.extend([
            "--merge-output-format", "mp4",
            "--postprocessor-args", "ffmpeg:-movflags +faststart",
        ])

    if is_youtube and YTDLP_YOUTUBE_ARGS:
        cmd.extend(shlex.split(YTDLP_YOUTUBE_ARGS))
        print_log(f"🎛 Extra YouTube yt-dlp args enabled: {YTDLP_YOUTUBE_ARGS}")

    cmd.append(url)
    print_log(f"Executing: {' '.join(cmd)}")

    returncode, stdout, stderr = await run_subprocess(cmd)

    if stdout:
        print_log(f"📝 --- yt-dlp stdout ---\n{stdout.strip()}")
    if stderr:
        print_log(f"⚠️ --- yt-dlp stderr ---\n{stderr.strip()}")

    if returncode != 0:
        raise Exception(f"yt-dlp Exit code {returncode}")

    # First: trust yt-dlp's printed output path, if present.
    printed_candidates = []
    for line in stdout.splitlines():
        line = line.strip().strip('"').strip("'")
        if not line:
            continue
        if line.startswith("http://") or line.startswith("https://"):
            continue
        if "/" in line or "\\" in line:
            printed_candidates.append(line)

    for candidate in reversed(printed_candidates):
        p = Path(candidate)
        if p.exists() and p.is_file():
            return str(p.resolve())

    # Fallback: scan the job directory for the newest valid media file.
    media_file = find_best_media_file(job_dir)
    if not media_file:
        raise FileNotFoundError("Video/Audio file not found on disk!")

    return str(media_file)


async def main():
    print_log("✅ Railway Worker Ready! Polling Hugging Face for jobs...\n")
    ensure_cookie_file_from_env()

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                headers = {"Authorization": f"Bearer {WORKER_SECRET}"}
                async with session.get(f"{HF_URL}/poll", headers=headers) as resp:
                    if resp.status != 200:
                        await asyncio.sleep(5)
                        continue

                    data = await resp.json()
                    if data.get("status") == "no_job":
                        await asyncio.sleep(2)
                        continue

                    url = data["url"]
                    chat_id = int(data["chat_id"])
                    message_id = int(data["message_id"])
                    status_msg_id = int(data["status_msg_id"])
                    quality = normalize_quality(data.get("quality", "max"))

                    job_id = str(uuid.uuid4())[:8]
                    job_dir = Path(f"jobs/{job_id}")
                    job_dir.mkdir(parents=True, exist_ok=True)
                    print_log(f"[{job_id}] 📥 Job Acquired: {url} | Quality: {quality}")

                    try:
                        download_success = False
                        media_path = None

                        try:
                            media_path = await download_video_via_ytdlp(url, job_dir, quality)
                            download_success = True
                        except Exception as e:
                            print_log(f"⚠️ yt-dlp download failed: {e}")

                        if not download_success and "youtube.com" not in url.lower() and "youtu.be" not in url.lower():
                            print_log("🔄 Falling back to Cobalt API...")
                            media_path = await download_via_cobalt(url, job_dir, quality)
                            download_success = True

                        if not download_success or not media_path:
                            raise FileNotFoundError("Video/Audio file not found on disk!")

                        file_path = str(Path(media_path).resolve())
                        print_log(f"[{job_id}] 📦 Media file resolved: {file_path}")

                        # Thumbnail
                        thumb_path = None
                        thumb_matches = list(job_dir.glob("*.jpg"))
                        if thumb_matches:
                            thumb_matches.sort(key=lambda p: (p.stat().st_mtime, p.stat().st_size), reverse=True)
                            thumb_path = str(thumb_matches[0].resolve())

                        # Metadata
                        width, height, duration = 0, 0, 0
                        info_matches = list(job_dir.glob("*.info.json"))
                        if info_matches:
                            try:
                                info_matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                                with open(info_matches[0], "r", encoding="utf-8") as f:
                                    info = json.load(f)
                                    width = int(info.get("width") or 0)
                                    height = int(info.get("height") or 0)
                                    duration = int(float(info.get("duration") or 0))
                            except Exception as e:
                                print_log(f"⚠️ Metadata parse failed: {e}")

                        def progress_callback(current, total):
                            if total and total > 0:
                                percent = int((current * 100) / total)
                                if percent % 10 == 0:
                                    print_log(f"[{job_id}] 🚀 Uploading Progress: {percent}%")

                        is_audio = quality == "audio"
                        upload_kwargs = {
                            "chat_id": chat_id,
                            "reply_to_message_id": message_id,
                            "progress": progress_callback,
                        }

                        if is_audio:
                            upload_kwargs["audio"] = file_path
                            upload_kwargs["caption"] = f"🎵 **دانلود موفق**\n⚡ کیفیت: {quality}"
                            if thumb_path:
                                upload_kwargs["thumb"] = thumb_path
                            if duration:
                                upload_kwargs["duration"] = duration
                        else:
                            upload_kwargs["video"] = file_path
                            upload_kwargs["supports_streaming"] = True
                            upload_kwargs["caption"] = f"🎬 **دانلود موفق**\n⚡ کیفیت: {quality}"
                            if thumb_path:
                                upload_kwargs["thumb"] = thumb_path
                            if width:
                                upload_kwargs["width"] = width
                            if height:
                                upload_kwargs["height"] = height
                            if duration:
                                upload_kwargs["duration"] = duration

                        upload_success = False
                        for attempt in range(3):
                            chosen_session = random.choice(BOT_SESSIONS)
                            upload_app = Client(
                                f"railway_{job_id}_{attempt}",
                                api_id=API_ID,
                                api_hash=API_HASH,
                                session_string=chosen_session,
                                in_memory=True,
                            )
                            try:
                                async with upload_app:
                                    print_log(f"[{job_id}] 🚀 Attempt {attempt + 1}: Uploading to Telegram...")

                                    if is_audio:
                                        await upload_app.send_audio(**upload_kwargs)
                                    else:
                                        await upload_app.send_video(**upload_kwargs)

                                    try:
                                        await upload_app.delete_messages(chat_id, status_msg_id)
                                    except Exception:
                                        pass

                                print_log(f"[{job_id}] 🎉 Job Completed!")
                                upload_success = True
                                break

                            except (AuthKeyDuplicated, AuthKeyInvalid):
                                print_log(f"[{job_id}] ⚠️ Session collision detected. Retrying with another session...")
                                continue
                            except FloodWait as e:
                                print_log(f"[{job_id}] 🛑 Telegram Rate Limit: Must wait {e.value} seconds.")
                                await asyncio.sleep(e.value + 2)
                            except Exception as e:
                                print_log(f"❌ Upload attempt {attempt + 1} failed: {e}")

                        if not upload_success:
                            print_log(f"[{job_id}] ❌ Upload failed after all retries.")

                    except Exception as e:
                        print_log(f"[{job_id}] ❌ Error during processing: {e}")

                    finally:
                        shutil.rmtree(job_dir, ignore_errors=True)
                        print_log(f"[{job_id}] 🧹 Cleanup done. Ready for next job.\n")

            except Exception as e:
                print_log(f"⚠️ Main loop error: {e}")
                await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
