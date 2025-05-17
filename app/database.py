# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Récupère l'URL depuis .env ou utilise une valeur par défaut
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/ipsdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
