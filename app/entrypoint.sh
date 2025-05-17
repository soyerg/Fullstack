#!/bin/bash

echo "⏳ Attente du démarrage de PostgreSQL..."
sleep 10

echo "📦 Création des tables (init_db.py)..."
python bdd/init_db.py

echo "📥 Import des données IPS (load_ips.py)..."
python bdd/load_ips.py



echo "⏳ Attente (2) pour finaliser l'import de données..."
sleep 2

echo "✅ Lancement des tests unitaires..."
pytest tests/

echo "✅ Fin des tests."  

echo "🚀 Lancement de FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload


