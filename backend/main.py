from fastapi import FastAPI
from auth.routes import router as auth_router
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Customize as required
origins = [
    "http://localhost:5173", # Vite server
    "http://127.0.0.1:5173"
]

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI backend running"}

app.include_router(auth_router)
