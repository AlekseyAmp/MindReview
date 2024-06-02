from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.api.analyze import routes as AnalyzeRouter
from src.adapters.api.auth import routes as AuthRouter
from src.adapters.api.data import routes as DataRouter
from src.adapters.api.feedback import routes as FeedbackRouter
from src.adapters.api.payment import routes as PaymentRouter
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
    UserRouter.router, tags=['users'], prefix='/api/users'
)
app.include_router(
    AnalyzeRouter.router, tags=['analyze'], prefix='/api/analyze'
)
app.include_router(
    FeedbackRouter.router, tags=['feedbacks'], prefix='/api/feedbacks'
)
app.include_router(
    DataRouter.router, tags=['data'], prefix='/api/data'
)
app.include_router(
    SystemRouter.router, tags=['system'], prefix='/api/system'
)
app.include_router(
    PaymentRouter.router, tags=['payment'], prefix='/api/payment'
)
