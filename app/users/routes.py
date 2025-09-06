from fastapi import APIRouter, Path, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List

from sqlalchemy.testing.pickleable import User
from users.schemas import (
    UserLoginSchema, UserRegisterSchema
)
from users.models import UserModel
from sqlalchemy.orm import Session
from core.database import get_db

router = APIRouter(tags=["users"], prefix="/users")


@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=request.username).one_or_none()
    if not user_obj:
        raise HTTPException(status_code=400, detail="User doesnt exists")

    if not user_obj.verify_password(request.password):
        raise HTTPException(status_code=400, detail="Passwords wrong")

    return user_obj



@router.post("/register")
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=request.username).one_or_none()
    if user_obj:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = UserModel(username=request.username)
    new_user.set_password(request.password)
    db.add(new_user)
    db.commit()

    return JSONResponse(status_code=200, content={"detail": "User register successfully"})
