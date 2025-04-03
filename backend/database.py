from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


DATABASE_URL = "postgresql://postgres:postgres@localhost/what-to-cook-today"
Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Food Items Table
class FoodItem(Base):
    __tablename__ = "food_items"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    quantity = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="food_items")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    food_items = relationship("FoodItem", back_populates="owner")

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database updated!")
