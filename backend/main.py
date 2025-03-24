from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.payments import router as payments_router
from database import engine
from models.user import Base  # Make sure to import Base explicitly

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from React
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include authentication routes
app.include_router(auth_router)
app.include_router(payments_router)

# @app.on_event("startup")
# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#         print("✅ Tables created successfully.")



@app.get("/")
async def root():
    return {"message": "Welcome to the SaaS Boilerplate API!"}
