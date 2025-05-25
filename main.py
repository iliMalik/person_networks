from fastapi import FastAPI
from api.endpoints import question

app = FastAPI()


app.include_router(question.router)

