from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.api.auth import routes as AuthRouter

app = FastAPI(title="MindReview", version="0.1")


origins = [
    "http://example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRouter.router, tags=['auth'], prefix='/api')
