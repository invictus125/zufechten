from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

db_engine = create_engine('http://localhost:5432', connect_args={})

def get_session():
    with Session(db_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

###########################
#          User           #
###########################

class ZufechtenUser(SQLModel, table=True):
    id: int = Field()
    username: str = Field()
    email: str = Field()
    first_name: str = Field()
    surname: str = Field()
    pronouns: str = Field()
    bio_info: str = Field()


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