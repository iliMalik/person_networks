from fastapi import FastAPI
from api.endpoints import fast_persons, fast_question, fast_sessions, fast_responses
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(debug=True,
    title="UNICRES",
    version="1.0.0",
    description="Mental Health and Healthcare Services",
    docs_url="/bacb",  # Customize Swagger UI path
    redoc_url=None,  # Disable ReDoc
    openapi_url="/api-openapi.json"  # Customize OpenAPI schema path
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or ["*"] for public access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fast_persons.router)
app.include_router(fast_question.router)
app.include_router(fast_sessions.router)
app.include_router(fast_responses.router)
