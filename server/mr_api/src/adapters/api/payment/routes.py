from fastapi import APIRouter, Depends, Response

from src.adapters.api.payment.dependencies import get_payment_service
from src.adapters.api.settings import AuthJWT
from src.adapters.api.user.dependencies import get_user_id
from src.application.payment.services import PaymentService

router = APIRouter()


@router.patch(
    path="/premium",
    response_model=dict[str, str]
)
async def set_premium(
    response: Response,
    user_id: int = Depends(get_user_id),
    authorize: AuthJWT = Depends(),
    payment_service: PaymentService = Depends(
        get_payment_service
    ),
) -> dict[str, str]:
    return await payment_service.set_premium(user_id, response, authorize)
