from pydantic import UUID4
from main import main
from uuid import uuid4
from datetime import datetime, timedelta
from main.models.database import query_execute, hash_password
from fastapi.responses import FileResponse
from fastapi import Depends, UploadFile, File, HTTPException, Response
from main import config
from main.schemas.response import DefaultResponse
from main.schemas.user import UserRegular, UserLogin, UserSignUp
from main.utils.user import get_user_by_username, get_user_by_email, get_current_user, get_user_by_token_with_type


# , response_model=DefaultResponse
@main.post('/api/upload_file')
def api_upload_file(
        file: UploadFile = File(...),
        user: UserRegular = Depends(get_current_user)
):
    return {"filename": file.filename, "content_type": file.content_type, "size": file.size}
