# YouTube Downloader

Simple Windows GUI app for downloading YouTube audio (MP3) or video using yt-dlp.

## Setup (Windows)

1. Install Python
2. Install dependencies:
   pip install -r requirements.txt

3. Put required binaries into /bin:
   - yt-dlp.exe
   - ffmpeg.exe
   - ffprobe.exe

4. Build app:
   build.bat

5. Run from:
   dist/YouTubeDownloader/YoutubeToMp3.exe

## Notes

- Uses yt-dlp + ffmpeg internally
- No installation needed for end user (portable)
