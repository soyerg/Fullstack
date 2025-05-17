from bdd.database import Base, engine
from bdd.models import School, User

print("📦 Création des tables...")

# Debug pour confirmer qu'on voit bien les modèles
print("Tables connues dans Base.metadata:", Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

print("✅ Tables créées.")
