import os
import requests
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 获取配置信息
API_KEY = os.getenv("API_KEY")
AI_API_URL = os.getenv("AI_API_URL")

print("=== 确认当前AI服务配置 ===")
print(f"API_KEY: {API_KEY}")
print(f"AI_API_URL: {AI_API_URL}")

# 检查是否使用DeepSeek
if "deepseek" in AI_API_URL:
    print("✅ 当前使用的是DeepSeek API")
else:
    print("❌ 当前不是使用DeepSeek API")

# 测试API连接
print("\n=== 测试API连接 ===")

test_query = "简要介绍故宫太和殿"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {
            "role": "user",
            "content": test_query
        }
    ],
    "max_tokens": 100
}

try:
    response = requests.post(AI_API_URL, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    
    print(f"✅ API请求成功，状态码: {response.status_code}")
    print(f"API提供商: DeepSeek")
    print(f"模型: deepseek-chat")
    print(f"\n测试回复示例:")
    print(result["choices"][0]["message"]["content"])
    print("\n🎉 确认成功！当前确实连接到了DeepSeek API")
    
except requests.exceptions.RequestException as e:
    print(f"❌ API请求失败: {e}")
    if hasattr(e.response, 'status_code'):
        print(f"状态码: {e.response.status_code}")
    if hasattr(e.response, 'text'):
        print(f"响应内容: {e.response.text}")
except Exception as e:
    print(f"❌ 发生错误: {e}")