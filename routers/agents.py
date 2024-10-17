from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Agents
from schemas import AgentVerification
from utils import convert_to_uuid

from .auth import get_current_agent

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
agent_dependency = Annotated[dict, Depends(get_current_agent)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_agent(agent: agent_dependency, db: db_dependency):
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    return (
        db.query(Agents).filter(Agents.id == convert_to_uuid(agent.get("id"))).first()
    )


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    agent: agent_dependency, db: db_dependency, agent_verification: AgentVerification
):
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )

    agent_model = (
        db.query(Agents).filter(Agents.id == convert_to_uuid(agent.get("id"))).first()
    )

    if not bcrypt_context.verify(
        agent_verification.password, agent_model.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password change"
        )

    agent_model.hashed_password = bcrypt_context.hash(agent_verification.new_password)

    db.add(agent_model)
    db.commit()
