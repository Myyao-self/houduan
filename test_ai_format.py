import os
import requests
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 获取配置信息
API_KEY = os.getenv("API_KEY")
AI_API_URL = os.getenv("AI_API_URL")

# 测试查询
user_query = "福建土楼的建筑结构"

# 系统提示词，指导AI按照指定格式输出
system_prompt = "你是一个中国古建筑专家，负责回答关于中国古建筑的问题。请按照以下格式回答：\n"
system_prompt += "1. 分多个层面进行剖析，每个层面有明确的标题\n"
system_prompt += "2. 每个层面下分点阐述，使用数字编号\n"
system_prompt += "3. 内容要有深度，包含专业知识\n"
system_prompt += "4. 排版清晰，要有换行\n"
system_prompt += "5. 不要使用任何markdown格式，直接输出文本\n"
system_prompt += "6. 内容要条理清晰，逻辑严谨"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_query
        }
    ],
    "max_tokens": 2000,
    "temperature": 0.7
}

try:
    print(f"测试AI格式输出...")
    print(f"查询内容: {user_query}")
    print("=" * 80)
    
    response = requests.post(AI_API_URL, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    
    ai_response = result["choices"][0]["message"]["content"]
    print("AI回复:")
    print("=" * 80)
    print(ai_response)
    print("=" * 80)
    print("\n✅ AI格式测试完成！")
    
except requests.exceptions.RequestException as e:
    print(f"❌ API请求失败: {e}")
    if hasattr(e.response, 'text'):
        print(f"响应内容: {e.response.text}")
except Exception as e:
    print(f"❌ 发生错误: {e}")