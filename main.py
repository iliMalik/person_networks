from fastapi import FastAPI
from api.endpoints import question, person

app = FastAPI(
    title="UNICRES",
    version="1.0.0",
    description="Mental Health and Healthcare Services",
    docs_url="/bacb",  # Customize Swagger UI path
    redoc_url=None,  # Disable ReDoc
    openapi_url="/api-openapi.json"  # Customize OpenAPI schema path
)


app.include_router(question.router)
app.include_router(person.router)


