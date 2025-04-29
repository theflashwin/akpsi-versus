import os
from dotenv import load_dotenv
from supabase import create_client, Client
import random
from typing import List

from schemas import player

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

DEFAULT_RATING = 1200.0

# fetches four random players
def fetch_players(count: int = 4) -> list:

    response = supabase.table("players").select("*").execute()

    if len(response.data) < count:
        raise ValueError(f"Not enough players to select {count} unique ones.")
    
    selected_players = random.sample(response.data, count)
    players = [player.Player(**row) for row in selected_players]

    return players

def fetch_rating(player_id: int, category: str) -> int:

    response = (
        supabase.table("players")
        .select("*")
        .eq("id", player_id)    # WHERE id = player_id
        .single()               # Expect exactly one result
        .execute()
    )

    if category in response.data.get("ratings"):
        return response.data.get("ratings")[category]
    else:
        return DEFAULT_RATING
    
def update_rating(player_id: int, category: str, new_rating: int):
    # Step 1: Fetch existing ratings
    response = (
        supabase.table("players")
        .select("ratings")
        .eq("id", player_id)
        .single()
        .execute()
    )

    current_ratings = response.data.get("ratings") or {}

    # Step 2: Update the specific category
    current_ratings[category] = new_rating

    # Step 3: Push the updated ratings back to the database
    update_response = (
        supabase.table("players")
        .update({"ratings": current_ratings})
        .eq("id", player_id)
        .execute()
    )

    return update_response.data

def get_leaderboard(category: str) -> List[player.Player]:

    # fetch all players
    response = supabase.table("players").select("*").execute()
    raw_players = response.data

    players = [player.Player(**p) for p in raw_players]

    print(category)
    print(players[-1].ratings.get("Most Likely to Bring a Briefcase to Class", 1200))

    sorted_players = sorted(
        players,
        key=lambda p: p.ratings.get(category, DEFAULT_RATING),
        reverse=True
    )

    return sorted_players