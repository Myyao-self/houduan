import requests
import json

# 测试本地API
def test_local_api():
    url = "http://127.0.0.1:8000/api/search"
    data = {
        "query": "故宫太和殿"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

# 测试Railway部署的API
def test_railway_api():
    url = "https://houduan-production-c347.up.railway.app/api/search"
    data = {
        "query": "故宫太和殿"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"\nRailway API Status Code: {response.status_code}")
        print(f"Railway API Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"\nRailway API Error: {e}")

if __name__ == "__main__":
    test_local_api()
    test_railway_api()
