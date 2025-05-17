# app/load_ips.py

import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
from models import School
import os

def load_data_from_csv(filepath: str):
    try:
        df = pd.read_csv(filepath, sep=";", encoding="utf-8")
        print("📄 Colonnes détectées :", df.columns.tolist())
        print("🔢 Nombre de lignes :", len(df))
        print(df.head(3))
    except Exception as e:
        print("❌ Erreur de lecture CSV :", e)
        return

    if df.empty:
        print("⚠️ Le fichier est vide. Aucun enregistrement à traiter.")
        return

    df = df.fillna("")

    db: Session = SessionLocal()

    inserted = 0
    for _, row in df.iterrows():
        try:
            school = School(
                rentree_scolaire=row.get("rentree_scolaire", ""),
                academie=row.get("academie", ""),
                code_du_departement=row.get("code_du_departement", ""),
                departement=row.get("departement", ""),
                uai=row.get("uai", ""),
                nom_de_l_etablissment=row.get("nom_de_l_etablissment", ""),
                code_insee_de_la_commune=row.get("code_insee_de_la_commune", ""),
                nom_de_la_commune=row.get("nom_de_la_commune", ""),
                secteur=row.get("secteur", ""),
                ips=row.get("ips") if pd.notnull(row.get("ips")) else None,
            )
            db.add(school)
            inserted += 1
        except Exception as e:
            print(f"❌ Erreur ligne {row}: {e}")

    db.commit()
    db.close()
    print(f"✅ {inserted} écoles IPS insérées avec succès.")

def insert_test_school():
    db = SessionLocal()
    school = School(
        rentree_scolaire="2025",
        academie="TEST",
        code_du_departement="99",
        departement="TEST",
        uai="9999999Z",
        nom_de_l_etablissment="École de test",
        code_insee_de_la_commune="99999",
        nom_de_la_commune="Testville",
        secteur="public",
        ips=100.0
    )
    db.add(school)
    db.commit()
    db.close()
    print("✅ École de test insérée.")

if __name__ == "__main__":
    filepath = os.getenv("IPS_FILE", "ips.csv")

    print("🔍 Tentative d'injection depuis fichier CSV...")
    load_data_from_csv(filepath)

    # Test d'insertion manuelle
    print("➕ Insertion manuelle d'une école de test pour validation")
    insert_test_school()
