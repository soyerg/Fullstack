#!/bin/bash

echo "⏳ Attente du démarrage de PostgreSQL..."
sleep 10

echo "🔍 Vérification du contenu de la table schools..."
SCHOOL_COUNT=$(psql "$DATABASE_URL" -tAc "SELECT COUNT(*) FROM schools;")

if [ "$SCHOOL_COUNT" -eq "0" ]; then
  echo "📥 Table vide : lancement de l'import CSV..."
  python load_ips.py
else
  echo "✅ Table déjà remplie ($SCHOOL_COUNT lignes), pas d'import nécessaire."
fi

echo "🚀 Lancement de FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
