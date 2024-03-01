from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)

from src.adapters.api.analyze import schemas
from src.adapters.api.analyze.dependencies import (
    get_review_processing_service,
    get_websocket_manager,
)
from src.adapters.api.user.dependencies import get_user_id
from src.adapters.notify.websocket import WebSocketManager
from src.application.review.services import ReviewProcessingService

router = APIRouter()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int,
    websockets_manager: WebSocketManager = Depends(get_websocket_manager)
) -> None:
    await websockets_manager.add_websocket(client_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websockets_manager.remove_websocket(client_id)


@router.post(path="/test", response_model=schemas.AnalyzeResponse)
async def make_test_analyze(
    test: schemas.TestReviews,
    review_processing_service: ReviewProcessingService = Depends(
        get_review_processing_service
    )
) -> schemas.AnalyzeResponse:
    return await review_processing_service.process_test_reviews(test)


@router.post(path="/file", response_model=schemas.AnalyzeResponse)
async def make_analyze_from_file(
    file: UploadFile,
    review_processing_service: ReviewProcessingService = Depends(
        get_review_processing_service
    ),
    user_id: int = Depends(get_user_id)
) -> schemas.AnalyzeResponse:
    return await review_processing_service.process_reviews_from_file(
        file,
        user_id
    )
