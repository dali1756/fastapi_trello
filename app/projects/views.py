from fastapi import APIRouter, File, Depends, Form, HTTPException, Request, status
from app import templates
from models.projects import Project
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from utils import get_db
from passlib.context import CryptContext
from typing import Annotated

project = APIRouter()

@project.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    pass

@project.post("/")
def create(request: Request, db: Session = Depends(get_db)):
    pass

@project.get("/new")
def new(request: Request, db: Session = Depends(get_db)):
    pass

@project.get("/{project_id}")
def show(request: Request, db: Session = Depends(get_db)):
    pass

@project.get("/{project_id}/edit")
def edit(request: Request, db: Session = Depends(get_db)):
    pass

@project.post("/{project_id}/update")
def update(request: Request, db: Session = Depends(get_db)):
    pass

@project.post("/{project_id}/delete")
def delete(request: Request, db: Session = Depends(get_db)):
    pass