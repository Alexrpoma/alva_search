import configparser
import logging

import httpx

from api.models import SearchResponse

class LLMService:
    def __init__(self):
        config = configparser.ConfigParser()
        try:
            config.read('config.ini')
            self.__context_url = config.get("CONTEXT_SERVICE", "URL")
            if not self.__context_url:
                 raise ValueError("URL not found.")
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            logging.error(f"Error config.ini: {e}")
        except Exception as e:
            logging.error(f"Error LLMService: {e}")
            raise

    async def send_process(self, item_data: SearchResponse):
        if not self.__context_url:
             logging.error("Error: Not valid URL.")
             return

        try:
            payload = item_data.model_dump()
        except Exception as e:
            logging.error(f"Error convert SearchResponse to dictionary: {e}")
            return

        logging.info(f"Sending Qdrant Result to {self.__context_url}")

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(self.__context_url, json=payload)
                response.raise_for_status()
                try:
                    response_json = response.json()
                    logging.info(f"Data sent successfully. Response: {response_json}")
                except Exception as json_error:
                    logging.error(f"Data sent successfully. Cannot parce response to JSON: {json_error}. Response: {response.text}")

            except httpx.RequestError as exc:
                logging.error(f"Error to connect to {self.__context_url}: {exc}")
            except httpx.HTTPStatusError as exc:
                logging.error(f"Error HTTP {exc.response.status_code} of {self.__context_url}: {exc.response.text}")
            except Exception as e:
                logging.error(f"Unexpected error HTTP: {e}")
