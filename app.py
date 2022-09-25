from fastapi import FastAPI, Request
from api import neural_network
from db.base import YTrain, Base
from db.session import scope, current_session, engine
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Table
from uuid import uuid4

app = FastAPI()
app.include_router(neural_network.router, prefix="")


@app.middleware("http")
def set_current_session(request: Request, call_next):
    scope.set(str(uuid4()))
    try:
        response = call_next(request)
        current_session.commit()
        return response
    finally:
        current_session.remove()

@app.on_event("startup")
def startup():
    pass


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)