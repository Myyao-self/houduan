import requests
import logging
from config.config import Config

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.api_key = Config.API_KEY
        self.api_url = Config.AI_API_URL
        logger.info(f"AIService initialized with API URL: {self.api_url}")
        logger.info(f"API Key configured: {bool(self.api_key)}")

    def search_buildings(self, query):
        logger.info(f"Received search query: {query}")
        
        # 根据API URL判断使用哪个AI服务
        if "deepseek" in self.api_url:
            # 使用DeepSeek API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",  # 选择适合的模型
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个中国古建筑专家，负责回答关于中国古建筑的问题"
                    },
                    {
                        "role": "user",
                        "content": f"请搜索与以下内容相关的中国古建筑：{query}，并提供相关的建筑名称、描述和特点"
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
        else:
            # 使用智谱AI API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "glm-4",  # 智谱AI的免费模型
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个中国古建筑专家，负责回答关于中国古建筑的问题。请直接返回JSON格式的结果，不要包含任何其他内容，如代码块标记等。JSON必须包含以下字段：title（标题）、type（类型，如'皇宫'、'民居'等）、brief（简介，不超过100字）、detail（详细描述）、tags（标签数组）。请确保JSON格式正确。"
                    },
                    {
                        "role": "user",
                        "content": f"请搜索与以下内容相关的中国古建筑：{query}，并提供相关的建筑名称、描述和特点"
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
        
        try:
            logger.info(f"Sending request to AI API: {self.api_url}")
            logger.debug(f"Request headers: {headers}")
            logger.debug(f"Request body: {data}")
            
            response = requests.post(self.api_url, json=data, headers=headers)
            logger.info(f"AI API response status: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")
            logger.debug(f"Response body: {response.text}")
            
            response.raise_for_status()  # 抛出HTTP错误
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"AI API request failed: {e}")
            # 返回错误信息，便于前端调试
            return {
                "error": {
                    "type": "api_error",
                    "message": str(e),
                    "status_code": getattr(e.response, 'status_code', None),
                    "response_text": getattr(e.response, 'text', None)
                }
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "error": {
                    "type": "unexpected_error",
                    "message": str(e)
                }
            }