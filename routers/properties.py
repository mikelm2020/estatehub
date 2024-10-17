from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Properties
from schemas import PropertyRequest
from utils import convert_to_uuid

from .auth import get_current_agent

router = APIRouter(
    prefix="/properties",
    tags=["properties"],
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
    return db.query(Properties).all()


@router.get("/{property_id}", status_code=status.HTTP_200_OK)
async def read_property(db: db_dependency, property_id: str):
    property_model = (
        db.query(Properties)
        .filter(Properties.id == convert_to_uuid(property_id))
        .first()
    )
    if property_model is not None:
        return property_model
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Property not found"
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_property(
    agent: agent_dependency, db: db_dependency, property_request: PropertyRequest
):
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    property_model = Properties(**property_request.dict(), agent_id=agent.get("id"))
    db.add(property_model)
    db.commit()


@router.put("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_property(
    agent: agent_dependency,
    db: db_dependency,
    property_request: PropertyRequest,
    property_id: str,
):
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )

    property_model = (
        db.query(Properties)
        .filter(Properties.id == convert_to_uuid(property_id))
        .filter(Properties.agent_id == convert_to_uuid(agent.get("id")))
        .first()
    )
    if property_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Property not found"
        )
        property_model.address_id = property_request.address_id
        property_model.type = property_request.type
        property_model.price = property_request.price
        property_model.status = property_request.status
        property_model.agent_id = property_request.agent_id
        property_model.title = property_request.title
        property_model.subtitle = property_request.subtitle
        property_model.size = property_request.size
        property_model.bedrooms = property_request.bedrooms
        property_model.rooms = property_request.rooms
        property_model.bathrooms = property_request.bathrooms
        property_model.description = property_request.description
        property_model.video = property_request.video
        property_model.map = property_request.map

        db.add(property_model)
        db.commit()


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(agent: agent_dependency, db: db_dependency, property_id: str):
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    property_model = (
        db.query(Properties)
        .filter(Properties.id == convert_to_uuid(property_id))
        .filter(Properties.agent_id == convert_to_uuid(agent.get("id")))
        .first()
    )
    if property_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Property not found"
        )
    db.query(Properties).filter(Properties.id == property_id).filter(
        Properties.agent_id == convert_to_uuid(agent.get("id"))
    ).delete()

    db.commit()
