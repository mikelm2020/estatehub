from pydantic import BaseModel, Field

from config import PropertiesStatus, PropertiesType, RoleUser


class PropertyRequest(BaseModel):
    address_id: str
    type: PropertiesType
    price: float = Field(ge=0)
    status: PropertiesStatus
    agent_id: str
    title: str = Field(min_length=1, max_length=100)
    subtitle: str = Field(min_length=1, max_length=100)
    size: float = Field(ge=0)
    bedrooms: int = Field(ge=0)
    rooms: int = Field(ge=0)
    bathrooms: int = Field(ge=0)
    description: str = Field(min_length=1)
    video: str
    map: str


class CreateAgentRequest(BaseModel):
    name: str
    email: str
    username: str
    password: str
    phone: str
    role: RoleUser


class Token(BaseModel):
    access_token: str
    token_type: str


class StateRequest(BaseModel):
    state: str


class AgentVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
