from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from .. import models, schemas, utils
from sqlalchemy.orm import Session
import validators

router = APIRouter(tags=['Create URLs'])

@router.post('/', response_model=schemas.URLInfo)
def create_shortened_URL(url : schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{url.target_url} is not valid")
    key = utils.create_url_key(db)
    admin_key = f"{key}_{utils.generate_key(8)}"
    db_url = models.URL(target_url=url.target_url, url_key=key, admin_key=admin_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url