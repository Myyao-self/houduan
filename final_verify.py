import sqlite3

# 连接到数据库
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# 查询所有知识卡片的标题和图片
cursor.execute("SELECT title, image FROM knowledge_cards")
cards = cursor.fetchall()

print("知识卡片图片更新结果：")
print("=" * 50)

# 遍历结果并打印
for title, image in cards:
    status = "✅" if image else "❌"
    image_path = image if image else "无图片"
    print(f"{status} {title}: {image_path}")

# 查询生成的10个新知识卡片的图片情况
generated_titles = [
    '井干式结构', '砖石结构', '琉璃瓦', '石灰浆', 
    '彩画工艺', '砖雕工艺', '建筑与五行', '建筑与礼制', 
    '原始社会建筑', '近代建筑转型'
]

print("\n" + "=" * 50)
print("生成的10个新知识卡片图片更新情况：")
print("=" * 50)

for title in generated_titles:
    cursor.execute("SELECT image FROM knowledge_cards WHERE title = ?", (title,))
    result = cursor.fetchone()
    image = result[0] if result else None
    status = "✅" if image else "❌"
    image_path = image if image else "无图片"
    print(f"{status} {title}: {image_path}")

# 关闭数据库连接
conn.close()