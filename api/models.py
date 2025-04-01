from pydantic import BaseModel


class SearchQuery(BaseModel):
    collection_name: str
    query: str
    client_id: str

class SearchResponse(BaseModel):
    client_id: str
    summary: str
    language: str
    url: str

class UploadData(BaseModel):
    collection_name: str
    data: list

class UpdatePoint(BaseModel):
    collection_name: str
    point_id: int
    new_data: dict

class DeletePoint(BaseModel):
    collection_name: str
    point_id: int

class GetPoint(BaseModel):
    collection_name: str
    point_id: int
