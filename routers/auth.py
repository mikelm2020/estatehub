import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Agents
from schemas import CreateAgentRequest, Token

router = APIRouter()
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_agent(username: str, password: str, db):
    agent = db.query(Agents).filter(Agents.username == username).first()
    if not agent:
        return False
    if not bcrypt_context.verify(password, agent.hashed_password):
        return False
    return agent


def create_access_token(username: str, agent_id: str, expires_delta: timedelta):
    encode = {"sub": username, "id": agent_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


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


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    agent = authenticate_agent(form_data.username, form_data.password, db)
    if not agent:
        return "Failed authentication"
    token = create_access_token(agent.username, str(agent.id), timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}
