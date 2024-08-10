from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from ..database import get_db
from .. import models, schemas, utils
from sqlalchemy.orm import Session
import validators

router = APIRouter(tags=['URL Tools'])

@router.get('/{url_key}')
def forward_to_URL(url_key : str, db : Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.url_key == url_key, models.URL.is_active).first()
    if not db_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shortened URL ({url_key}) does not exist")
    if not validators.url(db_url.target_url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{db_url.target_url} is not valid")
    utils.visits_update(db_url, db)
    return RedirectResponse(db_url.target_url)

@router.get('/peek/{url_key}', response_model=schemas.URL)
def peek_at_URL(url_key : str, db : Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.url_key == url_key, models.URL.is_active).first()
    if not db_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shortened URL ({url_key}) does not exist")
    return db_url

