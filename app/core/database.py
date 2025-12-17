from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Cria a "Engine" de conexão
# O argumento connect_args={"check_same_thread": False} era só pro SQLite. 
# Como vamos de Supabase (Postgres), removemos ele.
engine = create_engine(settings.DATABASE_URL)

# 2. Cria a fábrica de sessões (SessionLocal)
# Cada requisição vai criar uma sessão nova e fechar quando terminar.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Cria a classe Base para os Models herdarem
Base = declarative_base()

# 4. A Dependência (Dependency Injection)
# Essa função é mágica. Ela entrega o banco de dados para a rota e garante
# que a conexão seja fechada mesmo se der erro no código.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()