from fastapi import FastAPI
from .database import engine
from . import models
from .routers import admins, create, forward

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='URL Shortener App', description='Dealing with long URLs is a Hasle. Here, you can shorten any URL if it exists and access it after shortening it for once. You can also Deactivate it if you do not want to use it for sometime', docs_url='/')

@app.get('/')
def Main_Page():
    return "Welcome to My URL Shortener Website"

app.include_router(create.router)
app.include_router(forward.router)
app.include_router(admins.router)
