from enum import Enum


class PropertiesStatus(Enum):
    VENDIDO = "sold"
    RENTADO = "rented"
    EN_VENTA = "for sale"
    EN_ALQUILER = "for rent"


class PropertiesType(Enum):
    CASA = "house"
    APARTAMENTO = "apartment"
    TERRENO = "land"
    LOCAL = "local"
    COMERCIAL = "commercial"
    OTRO = "other"


class TransactionType(Enum):
    ALQUILER = "rent"
    VENTA = "sale"
    OTRA = "other"


class InteractionProgressStage(Enum):
    INICIADA = "started"
    COMPLETADA = "completed"
    CANCELADA = "canceled"
    PENDIENTE = "pending"
    EN_SEGUIMIENTO = "follow up"


class InteractionType(Enum):
    CONSULTA = "inquiry"
    CONTACTO = "contact"
    SOLICITUD = "request"
    LLAMADA = "call"
    EMAIL = "email"
    VISITA = "visit"
    REUNION = "meeting"
    OTRO = "other"


class AppointmentStatus(Enum):
    CREADA = "created"
    CONFIRMADA = "confirmed"
    CANCELADA = "canceled"
    REPROGRAMADA = "reprogrammed"
    RECUPERADA = "recovered"
    EN_SEGUIMIENTO = "follow up"
    COMPLETADA = "completed"
    AGENDADA = "scheduled"


class RoleUser(Enum):
    ADMIN = "admin"
    AGENT = "agent"
