import logging
import os
import asyncio
import re
from functools import partial
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable

logger = logging.getLogger(__name__)
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "vi")
TRANSCRIPT_TIMEOUT = int(os.getenv("TRANSCRIPT_TIMEOUT", 5))
PROXIES = {
    "http": os.getenv("PROXY")
}

def extract_video_id(video_url: str) -> str | None:
    match = re.search(r"(?:v=|\/shorts\/|youtu\.be\/)([a-zA-Z0-9_-]{11})", video_url)
    
    return match.group(1) if match else None

async def get_youtube_transcript(video_url: str, language: str = DEFAULT_LANGUAGE, retries: int = 2) -> str | None:
    for attempt in range(retries):
        try:
            video_id = extract_video_id(video_url)
            if not video_id:
                logger.error(f"Could not extract video ID from URL: {video_url}")
                return None

            loop = asyncio.get_event_loop()
            get_transcript_func = partial(YouTubeTranscriptApi.get_transcript, video_id, languages=[language], proxies=PROXIES)
            transcript = await asyncio.wait_for(loop.run_in_executor(None, get_transcript_func), timeout=TRANSCRIPT_TIMEOUT)

            return " ".join([entry['text'] for entry in transcript])

        except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable) as e:
            logger.warning(f"{type(e).__name__} for video: {video_url}. Attempt {attempt+1}/{retries}")
            return None
        except Exception as e:
            logger.warning(f"Attempt {attempt+1}/{retries} failed: {e}")
            await asyncio.sleep(0.5)
    return None
