from fastapi import FastAPI
from api.routes import tasks, users, auth

app = FastAPI(title="Todo List API")


app.include_router(auth.router, tags=["authentication"])
app.include_router(users.router, tags=["users"])
app.include_router(tasks.router, tags=["tasks"])