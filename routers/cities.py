from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Cities
from schemas import CityRequest
from utils import convert_to_uuid

from .auth import get_current_agent

router = APIRouter(
    prefix="/cities",
    tags=["cities"],
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
    return db.query(Cities).all()


@router.get("/{city_id}", status_code=status.HTTP_200_OK)
async def read_city(db: db_dependency, city_id: str):
    city_model = db.query(Cities).filter(Cities.id == convert_to_uuid(city_id)).first()

    if city_model is not None:
        return city_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_city(
    agent: agent_dependency, db: db_dependency, city_request: CityRequest
):
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    city_model = Cities(**city_request.dict())
    db.add(city_model)
    db.commit()


@router.put("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_city(db: db_dependency, city_request: CityRequest, city_id: str):
    city_model = db.query(Cities).filter(Cities.id == convert_to_uuid(city_id)).first()
    if city_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
        city_model.city = city_request.city

        db.add(city_model)
        db.commit()


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(db: db_dependency, city_id: str):
    city_model = db.query(Cities).filter(Cities.id == convert_to_uuid(city_id)).first()
    if city_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    db.query(Cities).filter(Cities.id == city_id).delete()

    db.commit()
