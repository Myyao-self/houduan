from app.models import KnowledgeCard, get_db

# 获取数据库会话
db_gen = get_db()
db = next(db_gen)

try:
    # 获取所有知识卡片
    cards = db.query(KnowledgeCard).all()
    
    print("知识卡片图片更新情况：")
    for card in cards:
        if card.image:
            print(f"- {card.title}: {card.image}")
        else:
            print(f"- {card.title}: 未设置图片")
    
finally:
    db.close()