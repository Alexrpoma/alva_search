import configparser
import logging

from qdrant_client import QdrantClient

class QdrantConnect:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QdrantConnect, cls).__new__(cls)
            config = configparser.ConfigParser()

            try:
                config.read('../config.ini')
                cls._instance.__host = config.get('QDRANT', 'HOST')
                cls._instance.__port = config.getint('QDRANT', 'PORT')
                cls._instance.__grpc_port = config.getint('QDRANT', 'GRPC_PORT')

                cls._instance.__client = QdrantClient(url=f"{cls._instance.__host}:{cls._instance.__port}")
                logging.info(f"HTTP_PORT: {cls._instance.__port} - OK")
                cls._instance.__grpc_client = QdrantClient(host=cls._instance.__host, grpc_port=cls._instance.__grpc_port, prefer_grpc=True)
                logging.info(f"GRPC_PORT: {cls._instance.__grpc_port} - OK")
            except Exception as e:
                logging.error(f"Failed: {e}")
        return cls._instance

    def get_client(self) -> QdrantClient:
        return self.__client

    def get_grpc_client(self) -> QdrantClient:
        return self.__grpc_client