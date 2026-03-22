import requests
import json

def test_deepseek_api(api_key=None):
    """测试DeepSeek API的交互式脚本"""
    
    if not api_key:
        api_key = input("请输入您的DeepSeek API密钥: ").strip()
        if not api_key:
            print("错误：API密钥不能为空")
            return
    
    # DeepSeek API配置
    API_URL = "https://api.deepseek.com/chat/completions"
    
    # 用户可以输入自定义查询
    query = input("请输入您要测试的查询内容（例如：故宫太和殿的建筑结构）: ").strip()
    if not query:
        query = "故宫太和殿的建筑结构"  # 默认查询
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "你是一个中国古建筑专家，负责回答关于中国古建筑的问题。你的回答应该：\n1. 以学术分析的方式进行深度解析\n2. 条理清晰，分点阐述\n3. 内容准确，引用权威信息\n4. 语言流畅，适合阅读\n5. 不要使用任何markdown格式，直接输出文本"
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    print(f"\n正在发送请求到DeepSeek API...")
    print(f"查询内容: {query}")
    print("=" * 50)
    
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        # 提取AI回复内容
        if "choices" in result and len(result["choices"]) > 0:
            ai_response = result["choices"][0]["message"]["content"]
            
            print("\n✅ DeepSeek API响应成功！")
            print("\nAI分析结果:")
            print("=" * 50)
            print(ai_response)
            print("=" * 50)
            
            # 询问是否要保存新的API密钥到.env文件
            save_key = input("\n是否要将此API密钥保存到.env文件？(y/n): ").lower()
            if save_key == 'y':
                update_env_file(api_key)
        else:
            print(f"❌ AI API返回格式不正确: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        if hasattr(e.response, 'text'):
            print(f"响应内容: {e.response.text}")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

def update_env_file(api_key):
    """更新.env文件中的API_KEY"""
    env_path = "f:\\Mycode\\project\\backend\\.env"
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        with open(env_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.startswith("API_KEY="):
                    f.write(f"API_KEY={api_key}\n")
                else:
                    f.write(line)
        
        print(f"✅ API密钥已成功保存到 {env_path}")
    except Exception as e:
        print(f"❌ 更新.env文件失败: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("DeepSeek API 测试工具")
    print("=" * 50)
    print("此工具允许您测试DeepSeek API并更新配置")
    print("=" * 50)
    
    # 运行测试
    test_deepseek_api()