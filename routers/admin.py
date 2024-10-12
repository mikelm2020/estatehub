from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

# from schemas import PropertyRequest
import config
from database import SessionLocal
from models import Properties

from .auth import get_current_agent

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
agent_dependency = Annotated[dict, Depends(get_current_agent)]


@router.delete("/property/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(agent: agent_dependency, db: db_dependency, property_id: str):
    if agent is None or agent.get("role") != config.RoleUser.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    property_model = db.query(Properties).filter(Properties.id == property_id).first()
    if property_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Property not found"
        )
    db.query(Properties).filter(Properties.id == property_id).delete()

    db.commit()
