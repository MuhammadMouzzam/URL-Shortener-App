from pydantic import BaseModel

class URLBase(BaseModel):
    target_url : str

class URL(URLBase):
    is_active : bool
    clicks : int
    class config:
        orm_mode = True

class URLInfo(URL):
    url_key : str
    admin_key : str