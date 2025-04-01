from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, FoodItem, init_db, User
from auth import create_user, authenticate_user
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    init_db()
    yield
    print("Cleanup tasks here if needed")

app = FastAPI(lifespan=lifespan)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Singup endpoint
@app.post("/signup/")
def signup(username:str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    user = create_user(username, password, db)
    return {"message": "User created successfully", "user": user.username}

# Login Endpoint
@app.post("/logn/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"message": "Login successfuly", "user": user.username}


# Get all food items
@app.get("/food/")
def get_all_food(db:Session = Depends(get_db)):
    return db.query(FoodItem).all()

# Get a specific food item by name
@app.get("/food/{name}")
def get_food(name: str, db: Session = Depends(get_db)):
    food = db.query(FoodItem).filter(FoodItem.name == name).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food    not found")
    return food

# Update food quantity
@app.put("/food/{name}")
def update_food(name: str, quantity: int, db: Session = Depends(get_db)):
    food = db.query(FoodItem).filter(FoodItem.name == name).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
        return food
    food.quantity = quantity
    db.commit()
    db.refresh(food)
    return {"message": "Food updated", "food": food}

# Delete a food item
@app.delete("/food/{name}")
def delete_food(name: str, db: Session = Depends(get_db)):
    food = db.query(FoodItem).filter(FoodItem.name == name).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    db.delete(food)
    db.commit()
    return {"message": "Food was deleted"}

@app.post("/add_food/")
def add_food(name: str, quantity: int, db: Session = Depends(get_db)):
    new_food = FoodItem(name=name, quantity=quantity)
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return {"message": "Food added", "food": new_food}
  
@app.get("/")
def read_root():
    return {"message":"What do I cook today?"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host ="0.0.0.0", port=8000)
