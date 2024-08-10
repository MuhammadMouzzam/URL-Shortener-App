from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from .. import models, schemas
from sqlalchemy.orm import Session

router = APIRouter(tags=['Administrator Tools'])

@router.get('/admin/{admin_key}', response_model=schemas.URLInfo)
def get_admin_info(admin_key : str, db : Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.admin_key == admin_key).first()
    if not db_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shortened URL with admin key ({admin_key}) does not exist")
    return db_url

@router.delete('/admin/{admin_key}/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_URL(admin_key : str, db : Session = Depends(get_db)):
    db_url_query = db.query(models.URL).filter(models.URL.admin_key == admin_key)
    db_url = db_url_query.first()
    if not db_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shortened URL with admin key ({admin_key}) does not exist")
    db_url_query.delete()
    db.commit()

@router.get('/admin/{admin_key}/deactivate', response_model=schemas.URLInfo)
def deactivate_URL(admin_key : str, db : Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.admin_key == admin_key).first()
    if not db_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shortened URL with admin key ({admin_key}) does not exist")
    db_url.is_active = False
    db.commit()
    db.refresh(db_url)
    return db_url