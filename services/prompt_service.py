from pathlib import Path

PROMPT_DIR = Path(__file__).parent.parent / "prompts"

def get_prompt_by_video_type(video_type: str) -> str:
    prompt_file = PROMPT_DIR / f"{video_type}_prompt.txt"

    if not prompt_file.exists():
        prompt_file = PROMPT_DIR / "cooking_prompt.txt"
    
    return prompt_file.read_text()
