import logging

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from config.logging_config import setup_logging
from services import DataBaseService, QdrantConnect
from crawler_mock import data
from services.transformer_service import TransformerService


class QdrantSearch:

    def __init__(self):
        self.__collection_name = "alva_search"
        self.__db_service: DataBaseService = DataBaseService()
        self.__client: QdrantClient = QdrantConnect().get_client()
        self.__encoder: SentenceTransformer = TransformerService().get_encoder()

    def create_collection(self):
        if not self.__db_service.collection_exist(self.__collection_name):
            self.__db_service.create_collection(self.__collection_name)
            self.__db_service.upload_data(self.__collection_name, data.summaries)

    def search(self, query: str):
        query_vector = self.__encoder.encode(query).tolist()
        search_result = self.__client.query_points(
            collection_name=self.__collection_name,
            query=query_vector,
            limit=3,
            timeout=1000
        ).points
        if search_result is not None:
            for point in search_result:
                print(point.payload)

if __name__ == "__main__":
    setup_logging()
    try:
        qdrant_search = QdrantSearch()
        qdrant_search.create_collection()
        qdrant_search.search("gasolina")
    except Exception as e:
        logging.error(f"Failed: {e}")