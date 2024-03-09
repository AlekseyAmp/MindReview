from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import FileResponse

from src.adapters.api.analyze import schemas
from src.adapters.api.analyze.dependencies import (
    get_result_analyze_service,
    get_review_processing_service,
    get_websocket_manager,
)
from src.adapters.api.user.dependencies import get_user_id
from src.adapters.notify.websocket import WebSocketManager
from src.application.review.services import (
    ResultAnalyzeService,
    ReviewProcessingService,
)

router = APIRouter()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int,
    websocket_manager: WebSocketManager = Depends(get_websocket_manager)
) -> None:
    await websocket_manager.add_websocket(client_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.remove_websocket(client_id)


@router.post(path="/test", response_model=schemas.AnalyzeResponse)
async def make_test_analyze(
    test: schemas.TestReviews,
    review_processing_service: ReviewProcessingService = Depends(
        get_review_processing_service
    )
) -> schemas.AnalyzeResponse:
    return await review_processing_service.process_test_reviews(test)


@router.post(path="/file", response_model=dict[str, str])
async def make_analyze_from_file(
    file: UploadFile,
    background_task: BackgroundTasks,
    user_id: int = Depends(get_user_id),
    review_processing_service: ReviewProcessingService = Depends(
        get_review_processing_service
    ),
) -> dict[str, str]:

    await review_processing_service.process_reviews_from_file_middleware(
        file,
        user_id
    )
    background_task.add_task(
        review_processing_service.process_reviews_from_file,
        file,
        user_id,
    )

    return {"message": "Ваши отзывы отправлены на анализ."}


@router.get(
    path="/get/{analyze_id}",
    response_model=schemas.AnalyzeResponse
)
async def get_analyze_results_by_id(
    analyze_id: int,
    user_id: int = Depends(get_user_id),
    result_analyze_service: ResultAnalyzeService = Depends(
        get_result_analyze_service
    ),
) -> schemas.AnalyzeResponse:
    return await result_analyze_service.get_analyze_results(
        user_id,
        analyze_id
    )


@router.get(path="/get_last", response_model=schemas.AnalyzeResponse)
async def get_last_analyze_results(
    result_analyze_service: ResultAnalyzeService = Depends(
        get_result_analyze_service
    ),
    user_id: int = Depends(get_user_id)
) -> schemas.AnalyzeResponse:
    return await result_analyze_service.get_analyze_results(
        user_id
    )


@router.get(
    path="/get_all",
    response_model=list[schemas.AnalyzeResponse | None]
)
async def get_all_analyze_results(
    result_analyze_service: ResultAnalyzeService = Depends(
        get_result_analyze_service
    ),
    user_id: int = Depends(get_user_id)
) -> list[schemas.AnalyzeResponse | None]:
    return await result_analyze_service.get_all_analyze_results(user_id)


@router.get(path="/download/{analyze_id}", response_class=FileResponse)
async def download_analyze_results(
    analyze_id: int,
    user_id: int = Depends(get_user_id),
    result_analyze_service: ResultAnalyzeService = Depends(
        get_result_analyze_service
    ),
) -> FileResponse:
    analyze_results = await result_analyze_service.generate_analyze_results(
        analyze_id,
        user_id
    )
    return FileResponse(
        path=analyze_results["file_path"],
        filename=analyze_results["file_name"],
        media_type='multipart/form-data'
    )
