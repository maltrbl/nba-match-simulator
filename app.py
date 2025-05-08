from flask import Flask, request, render_template, jsonify
import random

app = Flask(__name__)

teams = {
    "Lakers": {
        "players": ["LeBron James", "Anthony Davis", "D'Angelo Russell"],
        "avg_score": 110
    },
    "Celtics": {
        "players": ["Jayson Tatum", "Jaylen Brown", "Derrick White"],
        "avg_score": 108
    },
    "Warriors": {
        "players": ["Stephen Curry", "Klay Thompson", "Draymond Green"],
        "avg_score": 112
    },
    "Bucks": {
        "players": ["Giannis Antetokounmpo", "Khris Middleton", "Damian Lillard"],
        "avg_score": 109
    },
    "Suns": {
        "players": ["Kevin Durant", "Devin Booker", "Bradley Beal"],
        "avg_score": 107
    },
    "Nuggets": {
        "players": ["Nikola Jokic", "Jamal Murray", "Aaron Gordon"],
        "avg_score": 111
    }
}

highlight_plays = [
    "💥 {player} hits a deep three!",
    "🚫 {player} swats the shot away!",
    "🔥 {player} goes coast-to-coast for the slam!",
    "🎯 {player} hits a step-back jumper!",
    "🧊 {player} drains a clutch free throw!"
]

def simulate_game(team1, team2):
    score1 = random.randint(teams[team1]["avg_score"] - 5, teams[team1]["avg_score"] + 10)
    score2 = random.randint(teams[team2]["avg_score"] - 5, teams[team2]["avg_score"] + 10)
    winner = team1 if score1 > score2 else team2
    top_scorer = random.choice(teams[winner]["players"])
    points = random.randint(25, 45)
    highlight_msgs = [
        random.choice(highlight_plays).format(player=random.choice(teams[team1]["players"] + teams[team2]["players"]))
        for _ in range(5)
    ]
    return {
        "score1": score1,
        "score2": score2,
        "winner": winner,
        "top_scorer": f"{top_scorer} ({points} pts)",
        "highlights": highlight_msgs
    }

@app.route("/")
def index():
    return render_template("index.html", teams=teams.keys())

@app.route("/simulate", methods=["POST"])
def simulate():
    team1 = request.form.get("team1")
    team2 = request.form.get("team2")
    mode = request.form.get("mode")

    if team1 not in teams or team2 not in teams:
        return render_template("index.html", teams=teams.keys(), error="Invalid teams selected.")

    if mode == "series":
        results = []
        wins = {team1: 0, team2: 0}
        while wins[team1] < 4 and wins[team2] < 4:
            game_result = simulate_game(team1, team2)
            wins[game_result["winner"]] += 1
            results.append(game_result)
        return render_template("index.html", teams=teams.keys(), series_results=results, series_wins=wins)
    else:
        result = simulate_game(team1, team2)
        return render_template("index.html", teams=teams.keys(), result=result, team1=team1, team2=team2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
