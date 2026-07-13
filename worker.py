import os
import sys
import Path
frochcybtnxgyping import Optional

from pyrogram import Client
from pyrogram.errors import FloodWait, AuthKeyDuplicated, AuthKeyInvalid

def print_log(msg: str) -> None:
    print(msg, flush=True)
    sys.stdout.flush()

API_ID = int(os.environ.get("API_ID", "                    if resp.status in (200, 202):
                        data = await resp.json()
                        media_url = data.get("url")
                        if media_url: break
            except Exception: continue

        if not media_url: raise Exception("❌ All Cobalt APIs failed.")

        ext = "mp3" if quality == "audio" else "mp4"
        file_path = job_dir / f"video.{ext}"

        async with session.get(media_url) as video_resp:
            if video_resp.status != 200: raise Exception("Download failed from Cobalt URL.")
            with open(file_path, "wb") as f:
                while True:
                    chunk = await video_resp.content.read(2 * 1024 * 1024)
                    if not chunk: break
                    f.write(chunk)

    print_log("✅ Successfully downloaded via Cobalt!")
    return str(file_path.resolve())

async def download_video_via_ytdlp(url: str, job_dir: Path, quality: str = "max") -> str:
    quality = normalize_quality(quality)
    print_log(f"🚜 Running yt-dlp... Quality requested: {quality}")

    is_youtube = "youtube.com" in url.lower() or "youtu.be" in url.lower()
    absolute_job_dir = str(job_dir.resolve())

    if quality == "1080": format_str, sort_args = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best", ["-S", "height:1080"]
    elif quality == "720": format_str, sort_args = "bestvideo[height<=720]+bestaudio/best[height<=720]/best", ["-S", "height:720"]
    elif quality == "480": format_str, sort_args = "bestvideo[height<=480]+bestaudio/best[height<=480]/best", ["-S", "height:480"]
    elif quality == "audio": format_str, sort_args = "bestaudio/best", []
    else: format_str, sort_args = "bv*+ba/best", []

    cmd = [
        "yt-dlp", "-v",
        "-f", format_str, *sort_args, "--no-playlist",
        "--impersonate", "chrome", "--no-check-certificate", "--force-ipv4",
        "--retries", "5", "--fragment-retries", "infinite",
        "--write-info-json", "--write-thumbnail", "--convert-thumbnails", "jpg",
        "--print", "after_move:filepath", "-o", f"{absolute_job_dir}/video.%(ext)s",
    ]

    if COOKIE_FILE_PATH.exists():
        cmd.extend(["--cookies", str(COOKIE_FILE_PATH.resolve())])

    if YTDLP_PROXY:
        cmd.extend(["--proxy", YTDLP_PROXY])

    if quality == "audio": cmd.extend(["--extract-audio", "--audio-format", "mp3"])
    else: cmd.extend(["--merge-output-format", "mp4", "--postprocessor-args", "ffmpeg:-movflags +faststart"])

    if is_youtube and YTDLP_YOUTUBE_ARGS:
        cmd.extend(shlex.split(YTDLP_YOUTUBE_ARGS))

    cmd.append(url)
    print_log(f"Executing: {' '.join(cmd)}")

    returncode, stdout, stderr = await run_subprocess(cmd)

    if stdout: print_log(f"📝 --- yt-dlp stdout ---\n{stdout.strip()}")
    if stderr: print_log(f"⚠️ --- yt-dlp stderr ---\n{stderr.strip()}")

    if returncode != 0: raise Exception(f"yt-dlp Exit code {returncode}")

    printed_candidates = []
    for line in stdout.splitlines():
        line = line.strip().strip('"').strip("'")
        if not line or line.startswith("http://") or line.startswith("https://"): continue
        if "/" in line or "\\" in line: printed_candidates.append(line)

    for candidate in reversed(printed_candidates):
        p = Path(candidate)
        if p.exists() and p.is_file(): return str(p.resolve())

    media_file = find_best_media_file(job_dir)
    if not media_file: raise FileNotFoundError("Video/Audio file not found on disk!")
    return str(media_file)

async def main():
    print_log("✅ Railway Worker Ready! Polling Hugging Face for jobs...\n")
    ensure_cookie_file_from_env()

    # 🚨 روشن کردن موتور VLESS برای تونل زدن ترافیک 🚨
    if YTDLP_PROXY:
        await ensure_xray()

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

                    url, chat_id, message_id, status_msg_id = data["url"], int(data["chat_id"]), int(data["message_id"]), int(data["status_msg_id"])
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

                        if not download_success or not media_path: raise FileNotFoundError("Video/Audio file not found on disk!")
                        file_path = str(Path(media_path).resolve())
                        print_log(f"[{job_id}] 📦 Media file resolved: {file_path}")

                        thumb_path = None
                        thumb_matches = list(job_dir.glob("*.jpg"))
                        if thumb_matches:
                            thumb_matches.sort(key=lambda p: (p.stat().st_mtime, p.stat().st_size), reverse=True)
                            thumb_path = str(thumb_matches[0].resolve())

                        width, height, duration = 0, 0, 0
                        info_matches = list(job_dir.glob("*.info.json"))
                        if info_matches:
                            try:
                                info_matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                                with open(info_matches[0], "r", encoding="utf-8") as f:
                                    info = json.load(f)
                                    width, height, duration = int(info.get("width") or 0), int(info.get("height") or 0), int(float(info.get("duration") or 0))
                            except Exception as e: print_log(f"⚠️ Metadata parse failed: {e}")

                        def progress_callback(current, total):
                            if total and total > 0:
                                percent = int((current * 100) / total)
                                if percent % 10 == 0: print_log(f"[{job_id}] 🚀 Uploading Progress: {percent}%")

                    VHF o+:۵۸.(؟۶۸٫   is_audio = quality == "audio"
                        upload_kwargs = {"chat_id": chat_id, "reply_to_message_id": message_id, "progress": progress_callback}

                        if is_audio:
                            upload_kwargs.update({"audio": file_path, "caption": f"🎵 **دانلود موفق**\n⚡ کیفیت: {quality}"})
                            if thumb_path: upload_kwargs["thumb"] = thumb_path
                            if duration: upload_kwargs["duration"] = duration
                        else:
                            upload_kwargs.update({"video": file_path, "supports_streaming": True, "caption": f"🎬 **دانلود موفق**\n⚡ کیفیت: {quality}"})
                            if thumb_path: upload_kwargs["thumb"] = thumb_path
                            if width: upload_kwargs["width"] = width
                            if height: upload_kwargs["height"] = height
                            if duration: upload_kwargs["duration"] = duration

                        upload_success = False
                        for attempt in range(3):
                            chosen_session = random.choice(BOT_SESSIONS)
                            upload_app = Client(f"railway_{job_id}_{attempt}", api_id=API_ID, api_hash=API_HASH, session_string=chosen_session, in_memory=True)
                            try:
                                async with upload_app:
                                    print_log(f"[{job_id}] 🚀 Attempt {attempt + 1}: Uploading to Telegram...")
                                    if is_audio: await upload_app.send_audio(**upload_kwargs)
                                    else: await upload_app.send_video(**upload_kwargs)
                                    try: await upload_app.delete_messages(chat_id, status_msg_id)
                                    except Exception: pass
                                print_log(f"[{job_id}] 🎉 Job Completed!")
                                upload_success = True
                                break
                            except (AuthKeyDuplicated, AuthKeyInvalid): continue
                            except FloodWait as e: await asyncio.sleep(e.value + 2)
                            except Exception as e: print_log(f"[{job_id}] ❌ Upload attempt {attempt + 1} failed: {e}")

                        if not upload_success: print_log(f"[{job_id}] ❌ Upload failed after all retries.")

                    except Exception as e: print_log(f"[{job_id}] ❌ Error during processing: {e}")
                    finally: shutil.rmtree(job_dir, ignore_errors=True)
                        
            except Exception as e: await asyncio.sleep(5)

if __name__ == "__mai(main())
