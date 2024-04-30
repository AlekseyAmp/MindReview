from pydantic import BaseModel

from src.application.constants import SystemConstants


class SystemInfoResponse(BaseModel):
    version: str = SystemConstants.SYSTEM_VERSION
    client_host: str = SystemConstants.CLIENT_HOST
    api_host: str = SystemConstants.API_HOST
    api_docs: str = SystemConstants.API_DOCS
    ws_host: str = SystemConstants.WS_HOST
    rabbitmq_host: str = SystemConstants.RABBITMQ_HOST


class LogResponse(BaseModel):
    id: int
    dt: str
    level: str
    message: str
