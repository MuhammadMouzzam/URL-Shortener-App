from cgitb import text
from sqlalchemy import Boolean, Column, Integer, String, null
from .database import Base

class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, nullable=False)
    target_url = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default='True')
    url_key = Column(String, nullable=False, unique=True)
    clicks = Column(Integer, nullable=False, server_default='0')
    admin_key = Column(String, nullable=False, unique=True)