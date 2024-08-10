from fastapi import Depends
from sqlalchemy.orm import Session
import secrets, string
from . import models, schemas
from .database import get_db

def generate_key(length: int):
    default = string.ascii_uppercase + string.digits
    key = "".join(secrets.choice(default) for _ in range(length))
    return key


def create_url_key(db: Session):
    default = string.ascii_uppercase + string.digits
    key = generate_key(5)
    while db.query(models.URL).filter(models.URL.url_key == key).first():
        key = generate_key(5)
    return key

def visits_update(db_url: schemas.URLInfo, db : Session):
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)

