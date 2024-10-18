from fastapi import FastAPI

import models
from database import engine
from routers import addressses, admin, agents, auth, cities, properties, states

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(agents.router)
app.include_router(states.router)
app.include_router(cities.router)
app.include_router(addressses.router)
app.include_router(properties.router)
