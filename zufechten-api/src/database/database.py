from fastapi import Depends
from sqlmodel import Session, create_engine
from typing import Annotated

# TODO: Get connection params from env
db_engine = create_engine('postgresql://zufechten:changeme@localhost:5432')

def get_session():
    with Session(db_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
