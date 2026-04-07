import asyncio
import os
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete
from dotenv import load_dotenv

# Import our updated services
import sys
sys.path.append(os.path.join(os.getcwd(), 'app'))
from app.services.auth_service import register_user, login_user
from app.models import User
from app.db.database import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def test_auth():
    async with AsyncSessionLocal() as db:
        print("--- Testing Authentication Flow ---")
        
        test_user = "TestUser_" + str(uuid.uuid4())[:8]
        test_email = test_user + "@example.com"
        test_password = "MySecurePassword123"
        
        print(f"1. Registering: {test_user} / {test_email}")
        reg_result = await register_user(db, "  " + test_user + "  ", "  " + test_email.upper() + "  ", test_password)
        await db.commit()
        print("   Success!")
        
        print(f"2. Login with Lowercase Username: {test_user.lower()}")
        login_result1 = await login_user(db, test_user.lower(), test_password)
        print("   Success!")
        
        print(f"3. Login with Email (mixed case, spaces): '  {test_email.upper()}  '")
        login_result2 = await login_user(db, "  " + test_email.upper() + "  ", test_password)
        print("   Success!")
        
        print("4. Verify hashing format in DB")
        result = await db.execute(select(User).where(User.username == test_user.lower()))
        user = result.scalar_one()
        print(f"   Stored Hash: {user.password_hash[:40]}...")
        assert user.password_hash.startswith("pbkdf2_sha256$")
        
        print("\n--- All Tests Passed! ---")
        
        # Cleanup
        await db.execute(delete(User).where(User.username == test_user.lower()))
        await db.commit()

if __name__ == "__main__":
    asyncio.run(test_auth())
