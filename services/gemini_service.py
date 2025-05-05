import logging
import os
import aiohttp
import re
from exceptions.gemini import GeminiAPIError
from services.prompt_service import get_prompt_by_video_type

logger = logging.getLogger(__name__)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_TIMEOUT = int(os.getenv("GEMINI_TIMEOUT", 15))

async def call_gemini_api(transcript: str, video_type: str = None, custom_prompt: str = None) -> str:
    if custom_prompt:
        prompt = f"{custom_prompt.strip()}\n\n{transcript}"
    else:
        prompt_template = get_prompt_by_video_type(video_type or "cooking")
        prompt = prompt_template.replace("{{transcript}}", transcript)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    timeout = aiohttp.ClientTimeout(total=GEMINI_TIMEOUT)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, headers=headers, json=payload, ssl=False) as response:
                response.raise_for_status()
                result = await response.json()
                result = result.get("candidates", [])[0].get("content", {}).get("parts", [])[0].get("text", "")
                result = result.replace("\\n", "").replace("\n", "")
                return re.sub(r"^```html\s*|```$", "", result.strip())
    
    except aiohttp.ClientResponseError as e:
        logger.error(f"Gemini API returned an error: {e.status} - {e.message}")
        raise GeminiAPIError(f"Gemini API error: {e.status} - {e.message}", status_code=e.status)
    except aiohttp.ClientConnectionError as e:
        logger.error(f"Error connecting to Gemini API: {e}")
        raise GeminiAPIError(f"Could not connect to Gemini API: {e}")
    except asyncio.TimeoutError:
        logger.error(f"Timeout while calling Gemini API after {GEMINI_TIMEOUT} seconds.")
        raise GeminiAPIError(f"Timeout while calling Gemini API.")
    except Exception as e:
        logger.error(f"Unexpected error calling Gemini API: {e}")
        raise GeminiAPIError(f"Unexpected error while calling Gemini API: {e}")
