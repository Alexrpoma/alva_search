import logging

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
        try:
            query_vector = self.__encoder.encode(query).tolist()
        except Exception as e:
            logging.error(f"Error encoding query: {e}")
            return []
        try:
            search_result = self.__client.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=3,
                timeout=1000
            ).points
            return search_result
        except Exception as e:
            logging.error(f"Error searching in collection '{collection_name}': {e}")
            return []