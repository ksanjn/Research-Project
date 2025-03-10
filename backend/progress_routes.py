from flask import Blueprint, request, jsonify

progress_bp = Blueprint('progress_bp', __name__)

# Temporary progress tracking data
USER_PROGRESS = {}

@progress_bp.route('/get_progress', methods=['GET'])
def get_progress():
    return jsonify({"progress": USER_PROGRESS})

@progress_bp.route('/update_progress', methods=['POST'])
def update_progress():
    data = request.json
    user_id = data.get("user_id")
    progress = data.get("progress")

    if user_id and progress is not None:
        USER_PROGRESS[user_id] = progress
        return jsonify({"message": "Progress updated!"}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400
