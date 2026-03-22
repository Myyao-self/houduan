import requests
import json

# 使用用户提供的API密钥
API_KEY = "sk-1aec05f0a4a84d1dba3dbedd3e163d91"
API_URL = "https://api.deepseek.com/chat/completions"

print("验证DeepSeek API密钥...")
print(f"使用的密钥: {API_KEY}")
print(f"使用的URL: {API_URL}")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {
            "role": "system",
            "content": "你是一个中国古建筑专家，负责回答关于中国古建筑的问题。请简要回答，不要超过100字。"
        },
        {
            "role": "user",
            "content": "故宫太和殿的建筑结构特点"
        }
    ],
    "max_tokens": 200,
    "temperature": 0.7
}

try:
    response = requests.post(API_URL, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    
    print("\n✅ API连接成功！")
    print(f"状态码: {response.status_code}")
    
    if "choices" in result and len(result["choices"]) > 0:
        ai_response = result["choices"][0]["message"]["content"]
        print("\nAI回复示例:")
        print("=" * 50)
        print(ai_response)
        print("=" * 50)
        print("\n🎉 验证通过！DeepSeek API可以正常使用。")
    else:
        print(f"\n❌ API返回格式不正确: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
except requests.exceptions.RequestException as e:
    print(f"\n❌ API连接失败: {e}")
    if hasattr(e.response, 'status_code'):
        print(f"状态码: {e.response.status_code}")
    if hasattr(e.response, 'text'):
        print(f"响应内容: {e.response.text}")
except Exception as e:
    print(f"\n❌ 发生错误: {e}")