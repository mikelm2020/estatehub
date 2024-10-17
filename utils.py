import uuid


def convert_to_uuid(value):
    try:
        return uuid.UUID(value)
    except ValueError:
        return None
