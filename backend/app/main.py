from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import funds, management, share_classes, legal_entities, subfunds

app = FastAPI(
    title="Fund Referential API",
    description="API for managing fund relationships and hierarchies",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(funds.router)
app.include_router(management.router)
app.include_router(share_classes.router)
app.include_router(legal_entities.router)
app.include_router(subfunds.router)

@app.get("/")
async def root():
    return {
        "message": "Fund Referential API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }