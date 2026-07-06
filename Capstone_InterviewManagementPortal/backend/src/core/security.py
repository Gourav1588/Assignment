import base64
from fastapi.security import HTTPBasic

security_scheme = HTTPBasic()


def hash_password(password: str) -> str:
    """
    Encodes password as Base64 for storage.
    """
    return base64.b64encode(password.encode("utf-8")).decode("utf-8")


def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    Encodes the incoming plain password as Base64 and compares with stored value.
    Returns True if match, False if not.
    """
    encoded_incoming = base64.b64encode(plain_password.encode("utf-8")).decode("utf-8")
    return encoded_incoming == stored_password