import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        # Simple query to public 'channels' table
        response = supabase.table("channels").select("count", count=True).execute()
        print("✅ Connection successful!")
        print("Tables accessible:", bool(response.data))
    except Exception as e:
        print("❌ Connection failed:", str(e))

if __name__ == "__main__":
    test_connection()