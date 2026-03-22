import sqlite3

# 连接到数据库
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# 查询所有知识卡片
cursor.execute("SELECT title, image FROM knowledge_cards")
cards = cursor.fetchall()

print("知识卡片图片路径：")
for card in cards:
    title, image = card
    if image:
        print(f"- {title}: {image}")
    else:
        print(f"- {title}: 无图片")

# 关闭数据库连接
conn.close()