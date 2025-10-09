"""
Run database migration to add verification_code column
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def run_migration():
    """Run the verification_code migration"""
    
    # Get Supabase credentials
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
        return False
    
    print("🔧 Connecting to Supabase...")
    print(f"   URL: {supabase_url}")
    
    try:
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        print("\n📋 Running migration: Add verification_code column")
        
        # Read migration file
        migration_path = "../supabase/migrations/20241008_add_verification_code.sql"
        with open(migration_path, 'r') as f:
            migration_sql = f.read()
        
        print(f"\n📄 Migration SQL:")
        print("=" * 60)
        print(migration_sql)
        print("=" * 60)
        
        # Execute migration using RPC
        # Note: Supabase Python client doesn't have direct SQL execution
        # We'll use the REST API to execute SQL
        
        print("\n⚠️  Note: Supabase Python client doesn't support direct SQL execution.")
        print("Please run this migration manually in the Supabase SQL Editor:")
        print("\n1. Go to: https://supabase.com/dashboard/project/eaqwlsnstnobjwfsqrxa/sql")
        print("2. Copy and paste the SQL from: supabase/migrations/20241008_add_verification_code.sql")
        print("3. Click 'Run'")
        
        print("\n📝 Migration SQL to run:")
        print("-" * 60)
        print(migration_sql)
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    run_migration()

