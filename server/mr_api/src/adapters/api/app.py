from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.api.analyze import routes as AnalyzeRouter
from src.adapters.api.auth import routes as AuthRouter
from src.adapters.api.feedback import routes as FeedbackRouter
from src.adapters.api.system import routes as SystemRouter
from src.adapters.api.user import routes as UserRouter
from src.application.constants import SystemConstants

app = FastAPI(title="MindReviewAPI", version=SystemConstants.SYSTEM_VERSION)

origins = [
    SystemConstants.CLIENT_HOST
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
    UserRouter.router, tags=['user'], prefix='/api/user'
)
app.include_router(
    AnalyzeRouter.router, tags=['analyze'], prefix='/api/analyze'
)
app.include_router(
    FeedbackRouter.router, tags=['feedback'], prefix='/api/feedback'
)
app.include_router(
    SystemRouter.router, tags=['system'], prefix='/api/system'
)
