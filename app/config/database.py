from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote
from contextlib import contextmanager
from dotenv import load_dotenv, find_dotenv
import os 
# Charger automatiquement le premier `.env` trouvé dans l'arborescence
load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL non défini dans .env")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Nouvelle implémentation plus robuste
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Connexion à la base de données réussie.")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return False

# Test automatique seulement si exécuté directement
if __name__ == "__main__":
    test_connection()