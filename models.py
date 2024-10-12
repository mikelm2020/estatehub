import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
)
from sqlalchemy import Enum as SqlEnum

from config import PropertiesStatus, PropertiesType, RoleUser
from database import Base


def get_enum_values(enum_class):
    return [member.value for member in enum_class]


class Properties(Base):
    __tablename__ = "properties"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    address_id = Column(Uuid, ForeignKey("addresses.id"))
    type = Column(
        SqlEnum(PropertiesType, values_callable=get_enum_values), nullable=False
    )
    price = Column(Float, nullable=False)
    status = Column(
        SqlEnum(PropertiesStatus, values_callable=get_enum_values), nullable=False
    )
    agent_id = Column(Uuid, ForeignKey("agents.id"))
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=False)
    size = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False, default=0)
    rooms = Column(Integer, nullable=False, default=0)
    bathrooms = Column(Integer, nullable=False, default=0)
    description = Column(Text, nullable=False)
    video = Column(String, nullable=True)
    map = Column(String, nullable=True)


class Agents(Base):
    __tablename__ = "agents"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(Date, nullable=False, default=datetime.now(timezone.utc))
    upated_at = Column(
        Date,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    is_active = Column(Boolean, nullable=False, default=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    role = Column(
        SqlEnum(RoleUser, values_callable=get_enum_values),
        nullable=False,
        default=RoleUser.AGENT,
    )


class SimilarProperties(Base):
    __tablename__ = "similar_properties"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    property_id = Column(Uuid, ForeignKey("properties.id"))
    similar_property_id = Column(Uuid, ForeignKey("properties.id"))


class PropertieImages(Base):
    __tablename__ = "propertie_images"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    property_id = Column(Uuid, ForeignKey("properties.id"))
    image_url = Column(String, nullable=False)
    is_thimbnail = Column(Boolean, nullable=False, default=False)
    created_at = Column(Date, nullable=False, default=datetime.now(timezone.utc))


class PropertieOptions(Base):
    __tablename__ = "propertie_options"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(Date, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(
        Date,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    is_active = Column(Boolean, nullable=False, default=True)
    name = Column(String, nullable=False)


class PropertieAssignedOptions(Base):
    __tablename__ = "propertie_assigned_options"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    property_id = Column(Uuid, ForeignKey("properties.id"))
    property_option_id = Column(Uuid, ForeignKey("propertie_options.id"))


class Addresses(Base):
    __tablename__ = "addresses"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    state_id = Column(Uuid, ForeignKey("states.id"))
    city_id = Column(Uuid, ForeignKey("cities.id"))
    address = Column(String, nullable=False)


class States(Base):
    __tablename__ = "states"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(Date, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(
        Date,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    is_active = Column(Boolean, nullable=False, default=True)
    state = Column(String, nullable=False)


class Cities(Base):
    __tablename__ = "cities"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(Date, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(
        Date,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    is_active = Column(Boolean, nullable=False, default=True)
    city = Column(String, nullable=False)
    state_id = Column(Uuid, ForeignKey("states.id"))
