from sqlmodel import select
from models.models import Zufechtenuser
from database.database import SessionDep


def get_user_by_email(session: SessionDep, email: str) -> Zufechtenuser | None:
    stmt = select(Zufechtenuser).where(Zufechtenuser.email == email)
    return session.exec(stmt).first()


def get_user_by_username(session: SessionDep, username: str) -> Zufechtenuser | None:
    stmt = select(Zufechtenuser).where(Zufechtenuser.username == username)
    return session.exec(stmt).first()