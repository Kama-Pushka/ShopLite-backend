import os
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.config import settings
from app.services.auth_service import AuthService

router = APIRouter(prefix="/media", tags=["Media"])


@router.post("/upload")
async def upload_image(
    file: Annotated[UploadFile, File(...)],
    current_user=Depends(AuthService.get_current_user),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are allowed")

    suffix = Path(file.filename or "").suffix or ".jpg"
    filename = f"{uuid.uuid4().hex}{suffix}"
    upload_dir = Path(settings.MEDIA_ROOT)
    upload_dir.mkdir(parents=True, exist_ok=True)
    dest_path = upload_dir / filename

    contents = await file.read()
    with open(dest_path, "wb") as out:
        out.write(contents)

    url = f"{settings.MEDIA_URL.rstrip('/')}/{filename}"
    return {"url": url, "filename": filename}
