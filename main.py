from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Feedback Board")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-1234")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

VALID_STATUSES = ["ثبت شده", "در حال بررسی", "رسیدگی شده"]


ADMIN_USERNAME = "sepideh"
ADMIN_PASSWORD = "pashayan"



def require_login(request: Request):
    if not request.session.get("logged_in"):
        return False
    return True




@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if request.session.get("logged_in"):
        return RedirectResponse("/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["logged_in"] = True
        return RedirectResponse("/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "نام کاربری یا رمز عبور اشتباه است"
    })


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    if not require_login(request):
        return RedirectResponse("/login", status_code=302)
    feedbacks = db.query(models.Feedback).order_by(models.Feedback.created_at.desc()).all()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "feedbacks": feedbacks,
        "statuses": VALID_STATUSES
    })



@app.post("/api/feedbacks", response_model=schemas.FeedbackResponse)
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = models.Feedback(title=feedback.title, message=feedback.message)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@app.get("/api/feedbacks", response_model=list[schemas.FeedbackResponse])
def get_feedbacks(db: Session = Depends(get_db)):
    return db.query(models.Feedback).order_by(models.Feedback.created_at.desc()).all()


@app.patch("/api/feedbacks/{feedback_id}", response_model=schemas.FeedbackResponse)
def update_status(feedback_id: int, update: schemas.FeedbackUpdate, db: Session = Depends(get_db)):
    if update.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="وضعیت نامعتبر است")
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="فیدبک پیدا نشد")
    feedback.status = update.status
    db.commit()
    db.refresh(feedback)
    return feedback