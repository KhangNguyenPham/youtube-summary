import logging
import os
import asyncio
from functools import partial
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable

logger = logging.getLogger(__name__)
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "vi")
TRANSCRIPT_TIMEOUT = int(os.getenv("TRANSCRIPT_TIMEOUT", 5))

async def get_youtube_transcript(video_url: str, language: str = DEFAULT_LANGUAGE) -> str | None:
    try:
        video_id = video_url.split("v=")[-1].split("&")[0]

        loop = asyncio.get_event_loop()
        get_transcript_func = partial(YouTubeTranscriptApi.get_transcript, video_id, languages=[language])
        transcript = await asyncio.wait_for(loop.run_in_executor(None, get_transcript_func), timeout=TRANSCRIPT_TIMEOUT)

        return " ".join([entry['text'] for entry in transcript])

    except NoTranscriptFound:
        logger.warning(f"No transcript found for video: {video_url} in language '{language}'.")
    except TranscriptsDisabled:
        logger.warning(f"Transcripts are disabled for video: {video_url}.")
    except VideoUnavailable:
        logger.error(f"Video unavailable or private: {video_url}.")
    except asyncio.TimeoutError:
        logger.error(f"Timeout while fetching transcript for video: {video_url} after {TRANSCRIPT_TIMEOUT} seconds.")
    except Exception as e:
        logger.error(f"Unexpected error fetching transcript for video {video_url}: {e}")
    
    return None
