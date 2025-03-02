from flask import Blueprint, request, jsonify

leaderboard_bp = Blueprint('leaderboard_bp', __name__)

# Temporary leaderboard data (Later, store in a database)
LEADERBOARD = []

@leaderboard_bp.route('/get_leaderboard', methods=['GET'])
def get_leaderboard():
    sorted_leaderboard = sorted(LEADERBOARD, key=lambda x: x["score"], reverse=True)
    return jsonify({"leaderboard": sorted_leaderboard})

@leaderboard_bp.route('/update_leaderboard', methods=['POST'])
def update_leaderboard():
    data = request.json
    name = data.get("name")
    score = data.get("score")
    
    if name and score is not None:
        LEADERBOARD.append({"name": name, "score": score})
        return jsonify({"message": "Leaderboard updated!"}), 200
    else:
        return jsonify({"error": "Missing name or score"}), 400
