from database.database import SessionDep
from database.util.users import get_user_by_email, get_user_by_username
from fastapi import APIRouter, HTTPException, Security
from database.models import Zufechtenuser
from helpers.security import get_current_user, sanitize_user_info
from typing import Annotated


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=Zufechtenuser)
async def get_user(user_id: str, session: SessionDep, _current_user: Annotated[Zufechtenuser, Security(get_current_user, scopes=['read-user'])]):
    user = session.get(Zufechtenuser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove privileged information
    return sanitize_user_info(user)


@router.post("/register", response_model=Zufechtenuser)
async def add_user(user: Zufechtenuser, session: SessionDep):
    if get_user_by_email(session, user.email) is not None:
        raise HTTPException(status_code=400, detail="A user with that email is already registered.")
    elif get_user_by_username(session, user.username) is not None:
        raise HTTPException(status_code=400, detail="A user with that username is already registered.")

    session.add(user)
    session.commit()
    session.refresh(user)
    return sanitize_user_info(user)