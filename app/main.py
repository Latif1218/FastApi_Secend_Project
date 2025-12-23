# step 1.1

from fastapi import FastAPI
from .routes import user, admin
from . database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(admin.router)