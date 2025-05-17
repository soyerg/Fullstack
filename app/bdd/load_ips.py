# app/load_ips.py
from bdd.database import Base, engine, SessionLocal
from bdd.models import School, User
from auth import get_password_hash
import pandas as pd
import os

# Facultatif : Base.metadata.create_all(bind=engine) — à éviter si déjà fait

db = SessionLocal()

# 👤 Créer admin
existing_admin = db.query(User).filter(User.username == "admin").first()
if not existing_admin:
    admin_user = User(
        username="admin",
        hashed_password=get_password_hash("1234")
    )
    db.add(admin_user)
    print("✅ Admin créé.")
else:
    print("✅ Admin déjà présent.")

# 🏫 Charger les données IPS si fichier existe
filepath = os.getenv("IPS_FILE", "bdd/ips.csv")
if os.path.exists(filepath):
    df = pd.read_csv(filepath, sep=";")
    for _, row in df.iterrows():
        db.add(School(
            rentree_scolaire=row["rentree_scolaire"],
            academie=row["academie"],
            code_du_departement=row["code_du_departement"],
            departement=row["departement"],
            uai=row["uai"],
            nom_de_l_etablissment=row["nom_de_l_etablissment"],
            code_insee_de_la_commune=row["code_insee_de_la_commune"],
            nom_de_la_commune=row["nom_de_la_commune"],
            secteur=row["secteur"],
            ips=row["ips"] if pd.notnull(row["ips"]) else None,
        ))
    print(f"✅ {len(df)} lignes IPS insérées.")
else:
    print("❌ Fichier IPS non trouvé")

db.commit()
db.close()
