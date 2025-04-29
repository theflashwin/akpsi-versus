import os
from dotenv import load_dotenv
from supabase import create_client, Client
import random

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def fetch_question() -> str:

    response = (
        supabase.table("questions")
        .select("*")
        .execute()
    )

    if not response.data:
        return "NONE"
    
    return random.choice(response.data)

def fetch_questions() -> list[str]:

    response = (
        supabase.table("questions")
        .select("*")
        .execute()
    )

    return response.data

def fetch_question_with_id(question_id: int) -> str:

    response = supabase\
        .table("questions")\
        .select("value")\
        .eq("id", question_id)\
        .single()\
        .execute()
    
    data = response.data
    if not data:
        raise ValueError(f"No question found with id {question_id}")
    
    return data["value"]