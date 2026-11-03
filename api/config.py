import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env caso exista
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback para SQLite local para desenvolvimento sem necessidade de credenciais de nuvem
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./tasks_dev.db"
elif DATABASE_URL.startswith("postgres://"):
    # Compatibilidade com prefixo herdado do Heroku/Vercel
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
