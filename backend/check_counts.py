import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('DATABASE_URL_SYNC')
if not url:
    print("DATABASE_URL_SYNC not found")
    exit(1)

engine = create_engine(url)
tables = ['users', 'skills', 'challenges', 'rewards', 'quests', 'user_skills', 'user_challenges', 'user_rewards']

with engine.connect() as conn:
    print("--- Database Counts ---")
    for table in tables:
        try:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"{table}: {count}")
        except Exception as e:
            print(f"{table}: Error - {e}")
