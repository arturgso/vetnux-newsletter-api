from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/newsletter_db")

engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    connect_args={"server_settings": {"search_path": "vetnux_newsletter,public"}}
)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()
Base.metadata.schema = "vetnux_newsletter"