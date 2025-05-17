# app/bdd/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

print("🔄 [database.py] Initialisation du moteur SQLAlchemy...")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/ipsdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

print("✅ [database.py] Moteur et session SQLAlchemy prêts.")
