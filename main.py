from fastapi import FastAPI
from api.endpoints import fast_persons, fast_organizations, fast_countries
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(debug=True,
    title="PMS",
    version="1.0.0",
    description="Persons_Networks",
    docs_url="/SNA",  # Customize Swagger UI path
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
app.include_router(fast_organizations.router)
app.include_router(fast_countries.router)


