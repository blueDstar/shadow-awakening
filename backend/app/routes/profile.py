import os
import uuid
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User, Character
from app.schemas.character import CharacterResponse

router = APIRouter(prefix="/api/profile", tags=["profile"])

UPLOAD_DIR = "static/uploads"

@router.post("/upload/{img_type}")
async def upload_profile_image(
    img_type: str,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if img_type not in ["avatar", "cover", "background"]:
        raise HTTPException(status_code=400, detail="Invalid image type")

    # Ensure upload dir exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    if not file_ext:
        file_ext = ".png" # default
    
    filename = f"{img_type}_{user.id}_{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    # Update database
    result = await db.execute(select(Character).where(Character.user_id == user.id))
    character = result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    url = f"/static/uploads/{filename}"
    if img_type == "avatar":
        character.avatar_url = url
    elif img_type == "cover":
        character.cover_url = url
    elif img_type == "background":
        character.background_url = url

    await db.commit()
    return {"url": url}

@router.get("/me", response_model=CharacterResponse)
async def get_my_profile(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Character).where(Character.user_id == user.id))
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character
