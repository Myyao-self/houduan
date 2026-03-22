from sqlalchemy import create_engine, inspect
from app.models import KnowledgeCard, Building, get_db

# 创建数据库引擎
from config.config import Config
engine = create_engine(Config.DATABASE_URL)

# 使用inspect查看数据库表
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"数据库中的表: {tables}")

# 如果有knowledge_cards表，查看其结构
if 'knowledge_cards' in tables:
    print("\nknowledge_cards表结构:")
    columns = inspector.get_columns('knowledge_cards')
    for column in columns:
        print(f"  - {column['name']}: {column['type']}")
    
    # 查看数据
    print("\n查看知识卡片数据:")
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        cards = db.query(KnowledgeCard).all()
        print(f"找到 {len(cards)} 个知识卡片")
        
        # 打印生成的10个新知识卡片
        generated_titles = [
            '井干式结构', '砖石结构', '琉璃瓦', '石灰浆', 
            '彩画工艺', '砖雕工艺', '建筑与五行', '建筑与礼制', 
            '原始社会建筑', '近代建筑转型'
        ]
        
        print("\n生成的10个新知识卡片:")
        for title in generated_titles:
            card = db.query(KnowledgeCard).filter_by(title=title).first()
            if card:
                status = "✅" if card.image else "❌"
                print(f"{status} {card.title}: {card.image if card.image else '无图片'}")
    finally:
        db.close()

print("\n操作完成")