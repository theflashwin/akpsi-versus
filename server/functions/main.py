import json
import firebase_functions
from firebase_functions import https_fn
from firebase_admin import initialize_app

from middlewares import question_handler, player_handler

initialize_app()

K = 24

@https_fn.on_request()
def fetch_question_and_players(req: https_fn.Request) -> https_fn.Response:

    try:
        # fetch a random question
        question = question_handler.fetch_question()

        # fetch 4 random players
        players = player_handler.fetch_players()

        response = {
            "question": question,
            "players": [player.dict() for player in players]
        }

        json_response = json.dumps(response)

        return https_fn.Response(
            json_response,
            status=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        )
    except Exception as e:
        error_response = json.dumps({"error": str(e)})
        return https_fn.Response(
            error_response,
            status=500,
           headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*", 
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        )
    
@https_fn.on_request()
def post_result(req: https_fn.Request) -> https_fn.Response:

    CORS_HEADERS = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    if req.method == "OPTIONS":
        return https_fn.Response(
            "", status=204, headers=CORS_HEADERS
        )

    try:
        body = req.get_json(silent=True)

        if not body:
            return https_fn.Response(
                json.dumps({"error": "Missing JSON body"}),
                status=400,
                headers={**CORS_HEADERS, "Content-Type": "application/json"}
            )

        category = body.get("category")
        winner_id = body.get("winner_id")
        loser_ids = body.get("loser_ids") 

        if not category or not winner_id or not loser_ids:
            return https_fn.Response(
                json.dumps({"error": "Missing required fields"}),
                status=400,
                headers={**CORS_HEADERS, "Content-Type": "application/json"}
            )

        # 1. Get winner's current rating
        winner_rating = player_handler.fetch_rating(player_id=winner_id, category=category)

        # 2. Get losers' current ratings
        loser_ratings = [(i, player_handler.fetch_rating(player_id=i, category=category)) for i in loser_ids]

        winner_rating_delta = 0

        for loser_id, loser_rating in loser_ratings:

            e_winner = 1 / (1 + 10 ** ((loser_rating - winner_rating) / 400))

            winner_rating_delta += K * (1 - e_winner)
            new_loser_rating = loser_rating + K * (e_winner - 1)

            # Update loser's rating
            player_handler.update_rating(player_id=loser_id, category=category, new_rating=new_loser_rating)

        # Update winner's rating
        player_handler.update_rating(player_id=winner_id, category=category, new_rating=winner_rating + winner_rating_delta)

        return https_fn.Response(
            json.dumps({"message": "Ratings updated successfully"}),
            status=200,
            headers={**CORS_HEADERS, "Content-Type": "application/json"}
        )
    except Exception as e:
        print(f"Unexpected server error: {e}")
        return https_fn.Response(
            json.dumps({"error": "Internal server error"}),
            status=500,
            headers={**CORS_HEADERS, "Content-Type": "application/json"}
        )
    
@https_fn.on_request()
def fetch_questions(req: https_fn.Request) ->https_fn.Response:

    try:

        response = question_handler.fetch_questions()
        json_response = json.dumps(response)

        return https_fn.Response(
            json_response,
            status=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        )
    
    except Exception as e:
        error_response = json.dumps({"error": str(e)})
        return https_fn.Response(
            error_response,
            status=500,
           headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*", 
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        )

@https_fn.on_request()
def fetch_question(req: https_fn.Request) -> https_fn.Response:

    CORS = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    }

    if req.method == "OPTIONS":
        # Preflight
        return https_fn.Response("", status=204, headers=CORS)
    
    try:

        body = req.get_json(silent=True)

        if not body or "id" not in body:
            return https_fn.Response(
            json.dumps({"error": "Missing id"}),
            status=400,
            headers={**CORS, "Content-Type": "application/json"}
            )

        question_id = int(body.get("id"))
        question = question_handler.fetch_question_with_id(question_id=question_id)

        json_response = json.dumps(question)

        return https_fn.Response(
          json.dumps({ "question": question }),
          status=200,
          headers={**CORS, "Content-Type": "application/json"}
        )

    except Exception as e:
        return https_fn.Response(
          json.dumps({"error": str(e)}),
          status=500,
          headers={**CORS, "Content-Type": "application/json"}
        )

@https_fn.on_request()
def fetch_leaderboard(req: https_fn.Request) -> https_fn.Response:

    CORS_HEADERS = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    if req.method == "OPTIONS":
        return https_fn.Response(
            "", status=204, headers=CORS_HEADERS
        )

    try:

        body = req.get_json(silent=True)

        if not body:
            return https_fn.Response(
                json.dumps({"error": "Missing JSON body"}),
                status=400,
                headers={**CORS_HEADERS, "Content-Type": "application/json"}
            )

        category = body.get("category")
        sorted_players = player_handler.get_leaderboard(category=category)

        json_response = json.dumps(
            sorted_players,
            default=lambda o: o.dict(),
            ensure_ascii=False,
            indent=2
        )

        return https_fn.Response(
            json_response,
            status=200,
            headers={**CORS_HEADERS, "Content-Type": "application/json"}
        )

    except Exception as e:
        print(f"Unexpected server error: {e}")
        return https_fn.Response(
            json.dumps({"error": "Internal server error"}),
            status=500,
            headers={**CORS_HEADERS, "Content-Type": "application/json"}
        )
