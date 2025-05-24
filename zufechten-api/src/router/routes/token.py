from database.database import SessionDep
from database.util.users import get_user_by_username
from fastapi import APIRouter, HTTPException, status
from helpers.security import validate_password, LoginDep, create_token, get_user_scopes
from models.security import Token


router = APIRouter(prefix="/token", tags=["token"])


@router.post("/")
async def get_token(login_info: LoginDep, session: SessionDep) -> Token:
    user = get_user_by_username(session, login_info.username)
    if not user or not validate_password(login_info.password, user.auth_hash):
        # If there is no auth hash associated with the user, it means setup was not completed successfully for the account.
        if not user.auth_hash:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred in authentication. Contact the administrator",
                headers={"WWW-Authenticate": "Bearer"}
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    scopes = get_user_scopes(user.id, session, login_info.scopes)

    token = create_token(data={"sub": user.username, "scopes": scopes})

    return Token(access_token=token, token_type="bearer")
