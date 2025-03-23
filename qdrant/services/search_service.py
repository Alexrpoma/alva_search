from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from qdrant.services import DataBaseService, QdrantConnect
from qdrant.services.transformer_service import TransformerService


class SearchService:
    def __init__(self):
        self.__db_service: DataBaseService = DataBaseService()
        self.__client: QdrantClient = QdrantConnect().get_client()
        self.__encoder: SentenceTransformer = TransformerService().get_encoder()

    def run(self, collection_name: str, query: str) -> list:
        query_vector = self.__encoder.encode(query).tolist()
        search_result = self.__client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=3,
            timeout=1000
        ).points
        return search_result