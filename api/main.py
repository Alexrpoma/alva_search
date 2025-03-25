from fastapi import FastAPI, HTTPException

from api.models import SearchQuery, UploadData, UpdatePoint, DeletePoint, GetPoint, SearchResponse
from qdrant import SearchService, DataBaseService
from config.logging_config import setup_logging


search_service = SearchService()

app = FastAPI()
db_service = DataBaseService()

"""
API Endpoints
    Client:
        /api/search - Search for a query in a collection
    Qdrant DB:
        /api/{collection_name}/create - Create a collection
        /api/upload-data - Upload data to a collection
        /api/update-point - Update a point in a collection
        /api/delete-point - Delete a point in a collection
        /api/get-point - Get a point from a collection
        /api/{collection_name}/exists - Check if a collection exists
"""

@app.post("/api/search")
async def search(search_query: SearchQuery):
    search_result = search_service.run(search_query.collection_name, search_query.query)
    if search_result:
        response = []
        for point in search_result:
            response.append(SearchResponse(**point.payload))
        return response
    else:
        raise HTTPException(status_code=404, detail="No results found")

@app.post("/api/{collection_name}/create")
async def create_collection(collection_name: str):
    if db_service.create_collection(collection_name):
        return {"message": f"Collection '{collection_name}' created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to create collection")

@app.delete("/api/{collection_name}/delete")
async def delete_collection(collection_name: str):
    if db_service.delete_collection(collection_name):
        return {"message": f"Collection '{collection_name}' deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete collection.")

@app.post("/api/upload-data")
async def upload_data(upload_data: UploadData):
    if db_service.upload_data(upload_data.collection_name, upload_data.data):
        return {"message": f"Data uploaded to collection '{upload_data.collection_name}'"}
    else:
        raise HTTPException(status_code=500, detail="Failed to upload data")

@app.put("/api/update-point")
async def update_point(update_point: UpdatePoint):
    if db_service.update_point(update_point.collection_name, update_point.point_id, update_point.new_data):
        return {"message": f"Point {update_point.point_id} updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update point")

@app.delete("/api/delete-point")
async def delete_point(delete_point: DeletePoint):
    if db_service.delete_point(delete_point.collection_name, delete_point.point_id):
        return {"message": f"Point {delete_point.point_id} deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete point")

@app.get("/api/get-point")
async def get_point(get_point: GetPoint):
    point = db_service.get_point(get_point.collection_name, get_point.point_id)
    if point:
        return point
    else:
        raise HTTPException(status_code=404, detail="Point not found")

@app.get("/api/{collection_name}/exists")
async def collection_exists(collection_name: str):
    exists = db_service.collection_exist(collection_name)
    return {"exists": exists}

if __name__ == "__main__":
    setup_logging()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)