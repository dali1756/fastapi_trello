from app import app
from app.users.views import user as user_route, get_current_user, project_route
from fastapi.responses import RedirectResponse
from fastapi import Request, status, Depends
from app import templates
from starlette.middleware.sessions import SessionMiddleware
from db.db import SESSION_SECRET_KEY
from models.users import User
from sqlalchemy.orm import Session
from app.users.views import get_db

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

app.include_router(user_route, prefix="/users")
app.include_router(project_route, prefix="/projects")

@app.get("/")
def root():
    return RedirectResponse(url="/index")

@app.get("/index")
def index(request: Request, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    users = db.query(User).all()
    return templates.TemplateResponse("index.html", {"request": request, "message": "welcome to homepage", "users": users})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)