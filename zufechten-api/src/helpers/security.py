import bcrypt
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from database.models import Zufechtenuser
from database.util.users import get_user_by_username
from database.database import SessionDep


#############################
#       CONFIGURATION       #
#############################

# TODO: Move SECRET_KEY and ACCESS_TOKEN_EXPIRE_MINUTES to env / config file (change secret key)
# openssl rand -hex 32
SECRET_KEY = "edf9b277fac827d8ecd13102440085c661ee1e0100c72cc203d3a90a8dc6c851"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# OAUTH setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
LoginDep = Annotated[OAuth2PasswordRequestForm, Depends()]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


#############################
# SECURITY HELPER FUNCTIONS #
#############################

def hash_password(plaintext: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plaintext.encode('utf-8'), salt)
    return hashed


def validate_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


def create_token(data: dict, expires: timedelta | None = ACCESS_TOKEN_EXPIRE_MINUTES):
    cpy = data.copy()
    if expires:
        expire = datetime.now() + expires
    else:
        expire = datetime.now() + timedelta(minutes=60)

    cpy.update({"exp": expire})

    encoded = jwt.encode(cpy, SECRET_KEY, algorithm=ALGORITHM)

    return encoded


def sanitize_user_info(user: Zufechtenuser) -> Zufechtenuser:
    user.auth_hash = None
    return user


def get_current_user(security_scopes: SecurityScopes, session: SessionDep, token: TokenDep) -> Zufechtenuser:
    if security_scopes.scopes:
        auth_val = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        auth_val = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": auth_val},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        token_scopes = payload.get("scopes", [])

    except InvalidTokenError:
        raise credentials_exception

    user = get_user_by_username(session, username)
    if user is None:
        raise credentials_exception
    
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Insufficient permissions",
                headers={"WWW-Authenticate": auth_val},
            )

    return sanitize_user_info(user)


def get_user_scopes(user_id: int, session: SessionDep, requested_scopes: list[str]) -> list[str]:
    # TODO: Reconcile scopes (login_info.scopes vs. db-driven)
    scopes = ['read-user']
    return scopes