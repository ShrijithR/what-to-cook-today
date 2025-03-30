from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost/what-to-cook-today"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Food Items Table
class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    quantity = Column(Integer)
def init_db():
    Base.metadata.create_all(bind=engine)

