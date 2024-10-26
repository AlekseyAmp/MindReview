from sqlalchemy.orm import registry

from src.adapters.database import tables
from src.application.feedback import entities as feedback_entities
from src.application.review import entities as analyze_entities
from src.application.user import entities as user_entities

mapper = registry()

mapper.map_imperatively(user_entities.User, tables.users)
mapper.map_imperatively(analyze_entities.AnalyzeInput, tables.analyze)
mapper.map_imperatively(feedback_entities.FeedbackInput, tables.feedbacks)
