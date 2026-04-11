import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from pathlib import Path

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User, Character
from app.schemas.character import CharacterResponse

router = APIRouter(prefix="/api/profile", tags=["profile"])

# Use absolute path for uploads relative to the app root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"

class AssetSelection(BaseModel):
    asset_type: str  # avatar, cover, background
    asset_path: str  # e.g. /avatar/avatar_male_1.png

@router.get("/assets")
async def get_available_assets():
    """List available pre-defined assets for profile."""
    # These are relative to frontend's public folder
    avatars = [
        "/avatar/avatar_female_1.png", "/avatar/avatar_female_2.png", "/avatar/avatar_female_3.png", 
        "/avatar/avatar_female_4.png", "/avatar/avatar_female_5.png",
        "/avatar/avatar_male_1.png", "/avatar/avatar_male_2.png", "/avatar/avatar_male_3.png", 
        "/avatar/avatar_male_4.png", "/avatar/avatar_male_5.png"
    ]
    backgrounds = [
        "/background/banner_male_3.png", "/background/banner_male_4.png"
    ]
    return {
        "avatars": avatars,
        "backgrounds": backgrounds,
        "covers": backgrounds # Using backgrounds as covers for now
    }

@router.post("/set-asset")
async def set_profile_asset(
    selection: AssetSelection,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if selection.asset_type not in ["avatar", "cover", "background"]:
        raise HTTPException(status_code=400, detail="Invalid asset type")

    result = await db.execute(select(Character).where(Character.user_id == user.id))
    character = result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    if selection.asset_type == "avatar":
        character.avatar_url = selection.asset_path
    elif selection.asset_type == "cover":
        character.cover_url = selection.asset_path
    elif selection.asset_type == "background":
        character.background_url = selection.asset_path

    await db.commit()
    return {"status": "success", "url": selection.asset_path}

@router.post("/upload/{img_type}")
# ... (existing upload code)
async def upload_profile_image(
    img_type: str,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if img_type not in ["avatar", "cover", "background"]:
        raise HTTPException(status_code=400, detail="Invalid image type")

    # Ensure upload dir exists
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    file_ext = Path(file.filename).suffix
    if not file_ext:
        file_ext = ".png" # default
    
    filename = f"{img_type}_{user.id}_{uuid.uuid4().hex}{file_ext}"
    file_path = UPLOAD_DIR / filename

    try:
        content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        print(f"Error saving file: {e}")
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
