import logging

from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

from .transformer_service import TransformerService
from .qdrant_connect import QdrantConnect

class DataBaseService:
    def __init__(self):
        self.__encoder: SentenceTransformer = TransformerService().get_encoder()
        self.__client: QdrantClient = QdrantConnect().get_grpc_client()

    def create_collection(self, collection_name: str):
        try:
            collections = self.__client.get_collections().collections
            collection_names = [col.name for col in collections]
            if collection_name not in collection_names:
                self.__client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=self.__encoder.get_sentence_embedding_dimension(),
                        distance=models.Distance.COSINE
                    )
                )
                logging.info(f"Collection '{collection_name}' created")
                return True
            else:
                logging.info(f"Collection '{collection_name}' already exists")
                return False
        except Exception as e:
            logging.error(f"Create collection error: {e}")
            return False

    def delete_collection(self, collection_name: str):
        try:
            collections = self.__client.get_collections().collections
            collection_names = [col.name for col in collections]
            if collection_name in collection_names:
                self.__client.delete_collection(
                    collection_name=collection_name,
                    timeout=1000
                )
                logging.info(f"Collection '{collection_name}' deleted")
                return True
            else:
                logging.info(f"Collection '{collection_name}' doesn't exists")
                return False
        except Exception as e:
            logging.error(f"Delete collection error: {e}")
            return False

    def upload_data(self, collection_name: str, data: list):
        collections = self.__client.get_collections().collections
        collection_names = [col.name for col in collections]
        if collection_name not in collection_names:
            logging.error(f"Collection {collection_name} does not exist")
            return
        try:
            text_list = [item['summary'] for item in data]
            embeddings = self.__encoder.encode(text_list, batch_size=16, show_progress_bar=True)

            self.__client.create_payload_index(
                collection_name=collection_name,
                field_name="date",
                field_schema=models.PayloadSchemaType.DATETIME
            )

            self.__client.upload_points(
                collection_name=collection_name,
                points=[
                    models.PointStruct(id=idx, vector=vector, payload=doc)
                    for idx, (vector, doc) in enumerate(zip(embeddings, data))
                ]
            )
            logging.info(f"Data uploaded to collection {collection_name}")
            return True
        except Exception as e:
            logging.error(f"Upload data error: {e}")
            return False

    def update_point(self, collection_name: str, point_id: int, new_data: dict):
        collections = self.__client.get_collections().collections
        collection_names = [col.name for col in collections]
        if collection_name not in collection_names:
            logging.error(f"Collection {collection_name} does not exist")
            return
        try:
            new_vector = self.__encoder.encode(new_data['summary']).tolist()
            self.__client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(id=point_id, vector=new_vector, payload=new_data)
                ]
            )
            logging.info(f"Point {point_id} updated in collection '{collection_name}' - OK")
            return True
        except Exception as e:
            logging.error(f"Update point error: {e}")
            return False

    def delete_point(self, collection_name: str, point_id: int):
        collections = self.__client.get_collections().collections
        collection_names = [col.name for col in collections]
        if collection_name not in collection_names:
            logging.error(f"Collection {collection_name} does not exist")
            return
        try:
            self.__client.delete(
                collection_name=collection_name,
                points_selector=models.PointIdsList(
                    points=[point_id]
                )
            )
            logging.info(f"Point {point_id} deleted from collection '{collection_name}' - OK")
            return True
        except Exception as e:
            logging.error(f"Delete point error: {e}")
            return False

    def get_point(self, collection_name: str, point_id: int):
        collections = self.__client.get_collections().collections
        collection_names = [col.name for col in collections]
        if collection_name not in collection_names:
            logging.error(f"Collection {collection_name} does not exist")
            return None
        try:
            point = self.__client.retrieve(
                collection_name=collection_name,
                ids=[point_id]
            )
            if point:
                logging.info(f"Point {point_id} retrieved from '{collection_name}' - OK")
                return point[0]
            else:
                logging.warning(f"Point {point_id} not found in '{collection_name}'")
                return None
        except Exception as e:
            logging.error(f"Get point error: {e}")
            return None

    def collection_exist(self, collection_name) -> bool:
        collections = self.__client.get_collections().collections
        return any(col.name == collection_name for col in collections)
