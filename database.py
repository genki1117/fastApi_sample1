from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHENY_DATABASE_URL = 'postgresql://fastapiuser:fastapipass@0.0.0.0:5432/fleamarket'

engine = create_engine(SQLALCHENY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dbのセッションを作成する関数を定義
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()