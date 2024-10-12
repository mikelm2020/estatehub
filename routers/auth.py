import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Agents
from schemas import CreateAgentRequest, Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


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


def create_access_token(
    username: str, agent_id: str, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": agent_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_agent(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        agent_id: str = payload.get("id")
        agent_role: str = payload.get("role")
        if username is None or agent_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        return {"username": username, "id": agent_id, "role": agent_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
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
    token = create_access_token(
        agent.username, str(agent.id), str(agent.role), timedelta(minutes=20)
    )

    return {"access_token": token, "token_type": "bearer"}
