from typing import Annotated

from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Agents
from schemas import CreateAgentRequest

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_agent(db: db_dependency, create_agent_request: CreateAgentRequest):
    create_agent_model = Agents(
        name=create_agent_request.name,
        email=create_agent_request.email,
        username=create_agent_request.username,
        hashed_password=bcrypt_context.hash(create_agent_request.password),
        phone=create_agent_request.phone,
        role=create_agent_request.role,
    )

    db.add(create_agent_model)
    db.commit()
