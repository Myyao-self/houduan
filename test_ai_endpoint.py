import requests
import json

# 测试后端AI检索端点
BASE_URL = "http://localhost:8000"
SEARCH_ENDPOINT = f"{BASE_URL}/api/search"

print("测试后端AI检索端点...")
print(f"使用的端点: {SEARCH_ENDPOINT}")

# 测试查询
query = "故宫太和殿的建筑结构"

payload = {
    "query": query
}

try:
    response = requests.post(SEARCH_ENDPOINT, json=payload)
    response.raise_for_status()
    result = response.json()
    
    print("\n✅ 后端端点访问成功！")
    print(f"状态码: {response.status_code}")
    
    if result["status"] == "success":
        print("\n后端返回结果:")
        print("=" * 50)
        
        ai_data = result["data"]
        if "error" in ai_data:
            print(f"❌ AI服务出错: {ai_data['error']['message']}")
        else:
            print(f"查询内容: {ai_data['query']}")
            print(f"AI分析结果:")
            print("-" * 50)
            print(ai_data['content'])
            print("-" * 50)
            print("\n🎉 AI检索功能正常工作！")
    else:
        print(f"\n❌ 后端返回错误: {result.get('detail', '未知错误')}")
        
except requests.exceptions.RequestException as e:
    print(f"\n❌ 端点访问失败: {e}")
    if hasattr(e.response, 'status_code'):
        print(f"状态码: {e.response.status_code}")
    if hasattr(e.response, 'text'):
        print(f"响应内容: {e.response.text}")
except Exception as e:
    print(f"\n❌ 发生错误: {e}")