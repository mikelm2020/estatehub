from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import States
from schemas import StateRequest
from utils import convert_to_uuid

from .auth import get_current_agent

router = APIRouter(
    prefix="/states",
    tags=["states"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
agent_dependency = Annotated[dict, Depends(get_current_agent)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(States).all()


@router.get("/{state_id}", status_code=status.HTTP_200_OK)
async def read_state(db: db_dependency, state_id: str):
    state_model = (
        db.query(States).filter(States.id == convert_to_uuid(state_id)).first()
    )

    if state_model is not None:
        return state_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="State not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_state(
    agent: agent_dependency, db: db_dependency, state_request: StateRequest
):
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    state_model = States(**state_request.dict())
    db.add(state_model)
    db.commit()


@router.put("/{state_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_state(db: db_dependency, state_request: StateRequest, state_id: str):
    state_model = (
        db.query(States).filter(States.id == convert_to_uuid(state_id)).first()
    )
    if state_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="State not found"
        )
        state_model.state = state_request.state

        db.add(state_model)
        db.commit()


@router.delete("/{state_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_state(db: db_dependency, state_id: str):
    state_model = (
        db.query(States).filter(States.id == convert_to_uuid(state_id)).first()
    )
    if state_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="State not found"
        )
    db.query(States).filter(States.id == state_id).delete()

    db.commit()
