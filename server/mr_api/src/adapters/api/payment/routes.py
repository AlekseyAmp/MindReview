from fastapi import APIRouter, Depends

from src.adapters.api.payment.dependencies import get_payment_service
from src.adapters.api.user.dependencies import get_user_id
from src.application.payment.services import PaymentService

router = APIRouter()


@router.patch(
    path="/premium",
    response_model=dict[str, str]
)
async def set_premium(
    user_id: int = Depends(get_user_id),
    payment_service: PaymentService = Depends(
        get_payment_service
    ),
) -> dict[str, str]:
    return await payment_service.set_premium(user_id)
