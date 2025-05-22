from models import ZufechtenUser

from sqlmodel import Field, Session, SQLModel, create_engine, select

@app.get("/user/{user_id}")
async def get_user(user_id: str, session: SessionDep) -> ZufechtenUser:
    user = session.get(ZufechtenUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.post("/user")
async def add_user(user: ZufechtenUser, session: SessionDep) -> ZufechtenUser:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user