from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_game():

    data = request.get_json()

    try:
        min_number = int(data["min"])
        max_number = int(data["max"])
    except (TypeError, ValueError, KeyError):
        return jsonify({
            "success": False,
            "message": "請輸入有效的整數。"
        }), 400

    if min_number < 1:
        return jsonify({
            "success": False,
            "message": "最小值必須至少為 1。"
        }), 400

    if max_number > 10000:
        return jsonify({
            "success": False,
            "message": "最大值最高只能設定為 10,000。"
        }), 400

    if min_number >= max_number:
        return jsonify({
            "success": False,
            "message": "最大值必須大於最小值。"
        }), 400

    session["game"] = {
        "original_min": min_number,
        "original_max": max_number,
        "current_min": min_number,
        "current_max": max_number,
        "answer": random.randint(min_number, max_number),
        "attempts": 0,
        "finished": False
    }

    return jsonify({
        "success": True,
        "min": min_number,
        "max": max_number
    })


@app.route("/guess", methods=["POST"])
def guess():

    game = session.get("game")

    if not game:
        return jsonify({
            "success": False,
            "message": "請先開始遊戲。"
        }), 400

    if game["finished"]:
        return jsonify({
            "success": False,
            "message": "這一局已經結束。"
        }), 400

    data = request.get_json()

    try:
        guess_number = int(data["guess"])
    except (TypeError, ValueError, KeyError):
        return jsonify({
            "success": False,
            "message": "請輸入有效的整數。"
        }), 400

    if not (
        game["current_min"]
        <= guess_number
        <= game["current_max"]
    ):
        return jsonify({
            "success": False,
            "message":
                f"請輸入目前範圍："
                f"{game['current_min']} ～ "
                f"{game['current_max']}"
        }), 400

    game["attempts"] += 1

    # 猜中
    if guess_number == game["answer"]:

        game["finished"] = True
        session["game"] = game

        return jsonify({
            "success": True,
            "correct": True,
            "answer": game["answer"],
            "attempts": game["attempts"],
            "message": "🎉 你中獎了！"
        })

    # 太小
    if guess_number < game["answer"]:

        game["current_min"] = max(
            game["current_min"],
            guess_number
        )

        session["game"] = game

        return jsonify({
            "success": True,
            "correct": False,
            "result": "small",
            "message": "太小了",
            "current_min": game["current_min"],
            "current_max": game["current_max"],
            "attempts": game["attempts"]
        })

    # 太大
    game["current_max"] = min(
        game["current_max"],
        guess_number
    )

    session["game"] = game

    return jsonify({
        "success": True,
        "correct": False,
        "result": "large",
        "message": "太大了",
        "current_min": game["current_min"],
        "current_max": game["current_max"],
        "attempts": game["attempts"]
    })


@app.route("/renew", methods=["POST"])
def renew():

    game = session.get("game")

    if not game or not game["finished"]:
        return jsonify({
            "success": False,
            "message": "只有猜中後才能 Renew。"
        }), 400

    min_number = game["original_min"]
    max_number = game["original_max"]

    session["game"] = {
        "original_min": min_number,
        "original_max": max_number,
        "current_min": min_number,
        "current_max": max_number,
        "answer": random.randint(
            min_number,
            max_number
        ),
        "attempts": 0,
        "finished": False
    }

    return jsonify({
        "success": True,
        "min": min_number,
        "max": max_number
    })


if __name__ == "__main__":
    app.run(debug=True)