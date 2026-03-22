from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
from app.models import init_db
import os

app = FastAPI()

# 初始化数据库
init_db()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/models", StaticFiles(directory="public/models"), name="models")

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI Search API"}

# 为Cloudflare Workers添加的入口点
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
