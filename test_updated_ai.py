import requests
import json

# 测试更新后的后端AI检索端点
BASE_URL = "http://localhost:8000"
SEARCH_ENDPOINT = f"{BASE_URL}/api/search"

print("测试更新后的AI服务...")
print(f"使用的端点: {SEARCH_ENDPOINT}")

# 测试查询 - 使用用户提供的示例风格
query = "福建土楼的建筑结构"

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
        print("=" * 80)
        
        ai_data = result["data"]
        if "error" in ai_data:
            print(f"❌ AI服务出错: {ai_data['error']['message']}")
        else:
            print(f"查询内容: {ai_data['query']}")
            print(f"AI分析结果:")
            print("=" * 80)
            print(ai_data['content'])
            print("=" * 80)
            print("\n🎉 AI服务已更新，现在按照指定格式返回深度分析内容！")
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