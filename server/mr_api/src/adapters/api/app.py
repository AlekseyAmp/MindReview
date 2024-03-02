from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.api.analyze import routes as AnalyzeRouter
from src.adapters.api.auth import routes as AuthRouter

app = FastAPI(title="MindReviewAPI", version="0.1")

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_api_websocket_route('/ws', AuthRouter.router)
app.include_router(AuthRouter.router, tags=['auth'], prefix='/api/auth')
app.include_router(
    AnalyzeRouter.router, tags=['analyze'], prefix='/api/analyze'
)
