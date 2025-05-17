# app/init_db.py

from database import engine
from models import Base

def init_db():
    print("📦 Création des tables dans la base PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées.")

if __name__ == "__main__":
    init_db()
