from flask import Blueprint, request, jsonify
from controllers.summarize_controller import summarize

summarize_bp = Blueprint('summarize', __name__)

@summarize_bp.route("/summarize", methods=["POST"])
async def summarize_route():
    try:
        return await summarize(request)
    except Exception as e:
        return jsonify({"error": str(e)}), 500