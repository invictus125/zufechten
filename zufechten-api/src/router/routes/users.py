from database.database import SessionDep
from database.util.users import get_user_by_email, get_user_by_username
from fastapi import APIRouter, HTTPException
from models.models import Zufechtenuser


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=Zufechtenuser)
async def get_user(user_id: str, session: SessionDep):
    user = session.get(Zufechtenuser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/register", response_model=Zufechtenuser)
async def add_user(user: Zufechtenuser, session: SessionDep):
    if get_user_by_email(session, user.email) is not None:
        raise HTTPException(status_code=400, detail="A user with that email is already registered.")
    elif get_user_by_username(session, user.username) is not None:
        raise HTTPException(status_code=400, detail="A user with that username is already registered.")

    session.add(user)
    session.commit()
    session.refresh(user)
    return user