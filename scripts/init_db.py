#!/usr/bin/env python3
"""
Script de inicialização e provisionamento do banco de dados (Neon PostgreSQL ou SQLite local).
Cria a tabela 'tasks' caso ainda não exista.
"""
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from api.database import Base, engine
import api.models  # Garante registro das tabelas no metadata

def init_database():
    print(f"Provisionando banco de dados usando engine: {engine.url.render_as_string(hide_password=True)}")
    Base.metadata.create_all(bind=engine)
    print("[OK] Tabela 'tasks' criada/verificada com sucesso!")

if __name__ == "__main__":
    init_database()
