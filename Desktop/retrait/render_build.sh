#!/bin/bash

echo "📦 Installation des dépendances..."
pip install -r requirements.txt

echo "🛠️ Migration de la base de données et création admin..."
python run.py --migrate-only
