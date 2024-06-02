from sqlalchemy.orm import registry

from src.adapters.database import tables
from src.application.analyze import entities as analyze_entities
from src.application.collection import entities as collection_entities

mapper = registry()

mapper.map_imperatively(analyze_entities.AnalyzeInput, tables.analyze)
mapper.map_imperatively(collection_entities.StopwordInput, tables.stopwords)
