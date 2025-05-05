from flask import jsonify, Response
import re
import json
from services.gemini_service import call_gemini_api
from services.transcript_service import get_youtube_transcript

def validate_input(data):
    if not data.get("url"):
        return "Missing video URL"
    if "youtube.com/watch?v=" not in data.get("url"):
        return "Invalid YouTube URL"
    return None

async def summarize(request):
    data = request.get_json()
    error = validate_input(data)

    if error:
        return jsonify({"error": error}), 400

    video_url = data["url"]
    language = data.get("language", "vi")
    video_type = data.get("video_type", "cooking")
    user_prompt = data.get("prompt")

    try:
        transcript = await get_youtube_transcript(video_url, language=language)

        if not transcript:
            return jsonify({"error": "Transcript not available"}), 400

        data = await call_gemini_api(transcript, video_type, user_prompt)

        """
        cleaned = re.sub(r"^```json|```$", "", data.strip(), flags=re.MULTILINE)

        try:
            parsed_result = json.loads(cleaned)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format from Gemini"}), 500

        #return jsonify({"data": parsed_result})

        html = f"<h1>{parsed_result.get('title', '')}</h1>"
        html += f"<p><strong>Giới thiệu:</strong> {parsed_result.get('introduction', '')}</p>"

        html += "<h2>Nguyên liệu</h2><ul>"
        for item in parsed_result.get("ingredients", []):
            html += f"<li>{item}</li>"
        html += "</ul>"

        html += "<h2>Các bước thực hiện</h2>"
        for section in parsed_result.get("sections", []):
            html += f"<h3>{section.get('title', '')}</h3><ol>"
            for step in section.get("steps", []):
                html += f"<li>{step}</li>"
            html += "</ol>"

        html += f"<h2>Kết luận</h2><p>{parsed_result.get('conclusion', '')}</p>"
        """

        return Response(data, mimetype="text/html")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
