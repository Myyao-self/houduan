import requests
import logging
import time
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
        
        # 统一使用DeepSeek API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 严格按照用户要求的格式生成内容
        system_prompt = "你是一个中国古建筑专家，负责回答关于中国古建筑的问题。请严格按照以下要求回答用户问题，不偏离、不简化：\n\n"
        system_prompt += "1. 回答结构：\n"
        system_prompt += "   a. 首先写100-200字的简要介绍，对主题进行概括性说明\n"
        system_prompt += "   b. 然后分大标题（一、二、三...）和小标题（1. 2. 3...）进行详细分析，每个大标题下至少包含2个小标题\n"
        system_prompt += "   c. 最后写100-200字的总结，对主题进行归纳\n"
        system_prompt += "2. 排版要求：\n"
        system_prompt += "   a. 每个大标题独占一行，大标题之间必须空一行\n"
        system_prompt += "   b. 每个小标题独占一行，段落之间必须空一行\n"
        system_prompt += "   c. 开头介绍后空一行，再开始写大标题\n"
        system_prompt += "   d. 总结前空一行\n"
        system_prompt += "3. 内容要求：\n"
        system_prompt += "   a. 要求深度分析，每个要点必须有具体信息支撑\n"
        system_prompt += "   b. 语言正式、严谨、有条理\n"
        system_prompt += "4. 注意事项：\n"
        system_prompt += "   a. 不要在开头添加任何标记，直接开始写介绍\n"
        system_prompt += "   b. 不要在结尾添加任何标记，直接写总结\n"
        system_prompt += "   c. 不要使用'[开头：'、'[结尾：'等任何形式的标记\n"
        system_prompt += "   d. 整体逻辑从核心到细节、从整体到局部展开\n\n"
        system_prompt += "请基于以上要求，针对我的问题进行深度、结构化回答，确保排版清晰、内容详实、逻辑连贯。"
        
        data = {
            "model": "glm-4",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "max_tokens": 1500,
            "temperature": 0.5
        }
        
        try:
            logger.info(f"Sending request to AI API: {self.api_url}")
            logger.debug(f"Request headers: {headers}")
            logger.debug(f"Request body: {data}")
            
            # 增加超时时间并添加重试机制
            max_retries = 1
            retry_delay = 1  # 秒
            
            for retry in range(max_retries):
                try:
                    response = requests.post(self.api_url, json=data, headers=headers, timeout=30)
                    break
                except requests.exceptions.Timeout:
                    if retry == max_retries - 1:
                        raise  # 最后一次重试失败，抛出异常
                    logger.warning(f"AI API请求超时，正在进行第{retry + 2}次重试...")
                    time.sleep(retry_delay)
            logger.info(f"AI API response status: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")
            logger.debug(f"Response body: {response.text}")
            
            # 检查响应状态码
            if response.status_code != 200:
                logger.error(f"AI API returned non-200 status: {response.status_code}")
                logger.error(f"Error response: {response.text}")
                # 返回详细的错误信息
                return {
                    "choices": [
                        {
                            "message": {
                                "content": f"AI API调用失败，状态码: {response.status_code}，错误信息: {response.text}"
                            }
                        }
                    ]
                }
            
            response.raise_for_status()  # 抛出HTTP错误
            ai_response = response.json()
            
            # 直接返回AI API的原始响应格式，与前端期望的格式一致
            return ai_response
        except requests.exceptions.RequestException as e:
            logger.error(f"AI API request failed: {e}")
            # 详细记录异常信息
            error_detail = str(e)
            if hasattr(e, 'response') and e.response:
                error_detail += f"，响应状态: {e.response.status_code}"
                error_detail += f"，响应内容: {e.response.text}"
                logger.error(f"RequestException response: {e.response.text}")
                logger.error(f"RequestException status: {e.response.status_code}")
            # 返回详细的错误信息
            return {
                "choices": [
                    {
                        "message": {
                            "content": f"AI API连接失败，详细错误: {error_detail}"
                        }
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            # 返回详细的错误信息
            return {
                "choices": [
                    {
                        "message": {
                            "content": f"处理请求时发生错误，详细信息: {str(e)}"
                        }
                    }
                ]
            }