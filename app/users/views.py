from fastapi import APIRouter, File, Depends, Form, HTTPException, Request, status
from app import templates
from models.users import User
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.db import SessionLocal, engine
from passlib.context import CryptContext
from typing import Annotated


user = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/users/login", status_code=status.HTTP_302_FOUND)
    return user_id

@user.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("layouts/login.html", {"request": request})

@user.post("/login")
def login(request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user or pwd_context.verify(password, user.password):
        request.session["user_id"] = user.id
        return RedirectResponse(url="/index", status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

@user.post("/logout")
def logout(request: Request):
    request.session.pop("user_id", None)
    return RedirectResponse(url="/users/login", status_code=status.HTTP_302_FOUND)

@user.get("/")
def index(request: Request, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    users = db.query(User).all()
    return templates.TemplateResponse("users/index.html", {"request": request, "users": users})

@user.get("/new")
def new(request: Request):
    return templates.TemplateResponse("layouts/register.html", {"request": request})

@user.post("/")
def create(request: Request, name: Annotated[str, Form()], password: Annotated[str, Form()], email: Annotated[str, Form()], db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="電子郵件已經註冊！")
    hashed_password = pwd_context.hash(password)
    new_user = User(name = name, password = hashed_password, email = email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse(url="/users/login", status_code=status.HTTP_302_FOUND)

@user.get("/{user_id}")
def show(request: Request, user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return templates.TemplateResponse("users/show.html", {"request": request, "user": user})
    else:
        raise HTTPException(status_code=404, detail="查無使用者")

@user.get("/{user_id}/edit")
def edit(request: Request, user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return templates.TemplateResponse("users/edit.html", {"request": request, "user": user})
    else:
        raise HTTPException(status_code=404, detail="User not found")

@user.post("/{user_id}/update")
def update(user_id: int, name: Annotated[str, Form()], email: Annotated[str, Form()], db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = name
        user.email = email
        db.commit()
        return RedirectResponse(url=f"/users/{user_id}", status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(status_code=404, detail="查無使用者")

@user.post("/{user_id}/delete")
def delete(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return RedirectResponse(url="/index", status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(status_code=404, detail="查無使用者")