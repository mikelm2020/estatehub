from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Addresses
from schemas import AddressRequest
from utils import convert_to_uuid

from .auth import get_current_agent

router = APIRouter(
    prefix="/adresses",
    tags=["addresses"],
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
    return db.query(Addresses).all()


@router.get("/{address_id}", status_code=status.HTTP_200_OK)
async def read_address(db: db_dependency, address_id: str):
    address_model = (
        db.query(Addresses).filter(Addresses.id == convert_to_uuid(address_id)).first()
    )

    if address_model is not None:
        return address_model
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_address(
    agent: agent_dependency, db: db_dependency, address_request: AddressRequest
):
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    address_model = Addresses(**address_request.dict())
    db.add(address_model)
    db.commit()


@router.put("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_address(
    db: db_dependency, address_request: AddressRequest, address_id: str
):
    address_model = (
        db.query(Addresses).filter(Addresses.id == convert_to_uuid(address_id)).first()
    )
    if address_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
        address_model.address = address_request.address

        db.add(address_model)
        db.commit()


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(db: db_dependency, address_id: str):
    address_model = (
        db.query(Addresses).filter(Addresses.id == convert_to_uuid(address_id)).first()
    )
    if address_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    db.query(Addresses).filter(Addresses.id == address_id).delete()

    db.commit()
