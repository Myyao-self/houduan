from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

# 定义请求模型
class SearchRequest(BaseModel):
    query: str

@router.post("/search")
async def search_buildings(request: SearchRequest):
    try:
        result = ai_service.search_buildings(request.query)
        return {"data": result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
