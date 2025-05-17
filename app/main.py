from fastapi import FastAPI
from routers import schools, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(schools.router)
