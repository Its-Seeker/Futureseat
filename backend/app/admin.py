from sqladmin import Admin, AuthenticationBackend, ModelView
from starlette.requests import Request

from app.core.config import settings
from app.models.college import College
from app.models.cutoff import Cutoff


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"admin_token": "ok"})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin_token") == "ok"


class CollegeAdmin(ModelView, model=College):
    column_list = [
        College.id,
        College.name,
        College.state,
        College.type,
        College.exam_type,
        College.course,
        College.fees_lpa,
        College.seats,
        College.naac_grade,
    ]

    column_filters = ["exam_type", "type", "state"]
    
    name = "College"
    name_plural = "Colleges"
    can_export = True


class CutoffAdmin(ModelView, model=Cutoff):
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

    column_filters = ["category", "gender", "quota"]  

    # Optional but recommended (prevents relation issues)
    column_details_exclude_list = ["college"]

    name = "Cutoff"
    name_plural = "Cutoffs"
    can_export = True

def setup_admin(app, engine) -> Admin:
    authentication_backend = AdminAuth(secret_key=settings.ADMIN_SESSION_SECRET)
    admin = Admin(app, engine, authentication_backend=authentication_backend)
    admin.add_view(CollegeAdmin)
    admin.add_view(CutoffAdmin)
    return admin
