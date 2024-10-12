from fastapi import FastAPI

import models
from database import engine
from routers import admin, auth, properties, states

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(admin.router)
app.include_router(states.router)
