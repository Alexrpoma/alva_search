import configparser
import logging

from sentence_transformers import SentenceTransformer

class TransformerService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TransformerService, cls).__new__(cls)
            config = configparser.ConfigParser()

            try:
                config.read('config.ini')
                transformer_model = config.get('TRANSFORMER', 'MODEL')
                dim = config.getint('TRANSFORMER', 'DIM')
                cls._instance.__encoder = SentenceTransformer(transformer_model, truncate_dim=dim)
            except Exception as e:
                logging.error(f"Failed: {e}")
        return cls._instance

    def get_encoder(self):
        try:
            return self.__encoder
        except Exception as e:
            logging.error(f"Failed: {e}")
            return None