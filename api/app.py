from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import tasks, users, auth

app = FastAPI(title="Todo List API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["authentication"])
app.include_router(users.router, tags=["users"])
app.include_router(tasks.router, tags=["tasks"])