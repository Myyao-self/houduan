import requests
import json

# 智谱AI API配置
API_KEY = "your_api_key_here"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 测试函数
def test_zhipu_ai():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "glm-4",
        "messages": [
            {
                "role": "system",
                "content": "你是一个中国古建筑专家，负责回答关于中国古建筑的问题。请直接返回JSON格式的结果，不要包含任何其他内容，如代码块标记等。JSON必须包含以下字段：title（标题）、type（类型，如'皇宫'、'民居'等）、brief（简介，不超过100字）、detail（详细描述）、tags（标签数组）。请确保JSON格式正确。"
            },
            {
                "role": "user",
                "content": "故宫太和殿的建筑结构"
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        print("API响应:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 提取并打印实际的AI回复
        if "choices" in result and len(result["choices"]) > 0:
            ai_response = result["choices"][0]["message"]["content"]
            print("\nAI回复内容:")
            print(ai_response)
            
            # 尝试解析JSON
            try:
                ai_json = json.loads(ai_response)
                print("\n解析后的JSON:")
                print(json.dumps(ai_json, indent