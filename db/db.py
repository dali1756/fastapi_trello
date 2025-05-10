import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

# 資料庫連線 URL
DATABASE_URL = f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
# 創建引擎
engine = create_engine(DATABASE_URL)
# 創建會話工廠
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 創建基礎類別
BaseModel = declarative_base()
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
Base = declarative_base()