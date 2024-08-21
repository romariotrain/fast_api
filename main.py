import random
import uuid

from fastapi import FastAPI, HTTPException
from fastapi_pagination import add_pagination
from fastapi_users import FastAPIUsers

from app.core.jwt import auth_backend
from app.database import SessionLocal
from app.models import Sname, Lname
from app.users.models import User
from app.users.routers import router as user_router
from app.category.routers import router as category_router
from app.article.routers import router as article_router
from app.users.views import get_user_manager

app = FastAPI()
add_pagination(app)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(category_router, prefix="/category", tags=["category"])
app.include_router(article_router, prefix="/article", tags=["article"])
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)





@app.post("/fill-table/short")
async def fill_table():
    async with SessionLocal() as db:
        statuses = [0, 1, 2, 3]
        try:
            data = []
            for i in range(700, 0, -1):  # От 700 до 1
                name = f"name_{i}"
                status = random.choice(statuses) # Чередуем статусы 0 и 1
                data.append((name, status))

            for name, status in data:
                db_record = Sname(name=name, status=status)
                db.add(db_record)

            await db.commit()
            return {"message": "700 records inserted successfully"}

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))


@app.post("/fill-table/long")
async def fill_table_():
    async with SessionLocal() as db:
        try:
            extensions = ['.jpeg', '.mp3', '.png', '.pdf', '.docx', '.xls', '.ppt', '.txt', '.zip', '.gif']
            data = []
            for i in range(700, 200, -1):  # От 700 до 1
                name = f"name_{i}"
                extension = random.choice(extensions)  # Выбираем случайное расширение
                name_with_extension = name + extension
                data.append(name_with_extension)

            for name in data:
                db_record = Lname(name=name)
                db.add(db_record)

            await db.commit()
            return {"message": "500 records inserted successfully"}

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))