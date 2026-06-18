import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from config import get_settings
from models.user import User, UserRole
from utils.security import get_password_hash
from routes import auth, candidate, recruiter, admin, pdf

settings = get_settings()


def seed_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@portal.com").first()
        if not admin:
            admin = User(
                name="System Admin",
                email="admin@portal.com",
                password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
            )
            db.add(admin)
            db.commit()
            print("Default admin created: admin@portal.com / admin123")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    seed_admin()
    yield


app = FastAPI(
    title="HireHub",
    description="Connecting Talent with Opportunity",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(candidate.router, prefix="/api")
app.include_router(recruiter.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(pdf.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Recruitment Portal API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
