from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend

from app.api.v1.routes import router as v1_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models.college import College
from app.models.cutoff import Cutoff


# â”€â”€ Admin auth backend â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        if (
            form.get("username") == settings.ADMIN_USERNAME
            and form.get("password") == settings.ADMIN_PASSWORD
        ):
            request.session.update({"admin": "logged_in"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin") == "logged_in"


# â”€â”€ Admin views â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class CollegeAdmin(ModelView, model=College):
    name        = "College"
    name_plural = "Colleges"
    icon        = "fa-solid fa-school"
    column_list = [
        College.id,
        College.name,
        College.state,
        College.type,
        College.exam_type,
        College.course,
        College.naac_grade,
        College.fees_lpa,
        College.seats,
    ]
    column_searchable_list  = [College.name, College.state, College.exam_type]
    column_sortable_list    = [College.id, College.name, College.exam_type, College.state]
    column_filters = ["exam_type", "type", "state"]
    page_size               = 50


class CutoffAdmin(ModelView, model=Cutoff):
    name        = "Cutoff"
    name_plural = "Cutoffs"
    icon        = "fa-solid fa-list-ol"
    column_list = [
        Cutoff.id,
        Cutoff.college_id,
        Cutoff.quota,
        Cutoff.category,
        Cutoff.gender,
        Cutoff.special,
        Cutoff.opening_rank,
        Cutoff.closing_rank,
        Cutoff.year,
    ]
    column_sortable_list = [Cutoff.id, Cutoff.college_id, Cutoff.closing_rank]
    column_filters = ["category", "gender", "quota"]
    page_size            = 100


# â”€â”€ App â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

app = FastAPI(title=settings.APP_NAME)

# Session middleware MUST come before Admin
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.ADMIN_SESSION_SECRET,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount admin panel at /admin
authentication = AdminAuth(secret_key=settings.ADMIN_SESSION_SECRET)
admin = Admin(app, engine, authentication_backend=authentication)
admin.add_view(CollegeAdmin)
admin.add_view(CutoffAdmin)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}


