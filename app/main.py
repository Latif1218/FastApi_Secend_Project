from fastapi import FastAPI
from .routes import register_user, user, admin, forgot, moods
from . database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(register_user.router)
app.include_router(admin.router)
app.include_router(forgot.router)
app.include_router(moods.router)