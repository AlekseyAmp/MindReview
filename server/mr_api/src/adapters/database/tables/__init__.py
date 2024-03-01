from src.adapters.database.tables.common import analyze, feedbacks
from src.adapters.database.tables.common import metadata as common_metadata
from src.adapters.database.tables.common import users
from src.adapters.database.tables.data import cities
from src.adapters.database.tables.data import metadata as data_metadata
from src.adapters.database.tables.data import stopwords
from src.adapters.database.tables.logs import logs
from src.adapters.database.tables.logs import metadata as logs_metadata

__all__ = [
    users,
    feedbacks,
    analyze,
    cities,
    stopwords,
    logs,
    common_metadata,
    data_metadata,
    logs_metadata,
]
