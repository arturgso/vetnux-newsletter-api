from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from database import SessionLocal, engine, Base
from models import Subscriber
from schemas import SubscriberCreate, SubscriberOut
from config import settings

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Vetnux Newsletter API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "cors_origins": len(settings.CORS_ORIGINS)}

# Cria as tabelas automaticamente
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Cria o schema se não existir
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS vetnux_newsletter"))
        await conn.run_sync(Base.metadata.create_all)

# Dependência para obter uma sessão DB
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.post("/subscribe", response_model=SubscriberOut)
async def subscribe(data: SubscriberCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscriber).where(Subscriber.email == data.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email já inscrito.")

    new_subscriber = Subscriber(email=data.email)
    db.add(new_subscriber)
    await db.commit()
    await db.refresh(new_subscriber)
    return new_subscriber
