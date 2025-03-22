from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Mapeia as tabelas existentes no banco de dados
Base = automap_base()
Base.prepare(engine, reflect=True)

# Acessa a tabela mapeada
SoybeanMealPrice = Base.classes.migrations_soybeanmealprice

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()