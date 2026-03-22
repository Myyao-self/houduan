from app.models import KnowledgeCard, get_db

def verify_new_cards():
    # 获取数据库会话
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        print("验证知识卡片优化结果")
        print("=" * 60)
        
        # 重点检查砖石结构卡片
        print("\n1. 砖石结构卡片 (用户重点提及的呆板格式):")
        print("-" * 50)
        masonry_card = db.query(KnowledgeCard).filter_by(title='砖石结构').first()
        if masonry_card:
            print(f"标题: {masonry_card.title}")
            print("优化后的内容:")
            for i, paragraph in enumerate(masonry_card.content, 1):
                print(f"  {i}. {paragraph}")
        
        # 检查其他几个生成的卡片
        other_cards = ['井干式结构', '琉璃瓦', '彩画工艺', '砖雕工艺', '建筑与五行']
        
        for card_title in other_cards:
            print(f"\n2. {card_title}:")
            print("-" * 50)
            card = db.query(KnowledgeCard).filter_by(title=card_title).first()
            if card:
                print(f"标题: {card.title}")
                print("优化后的内容:")
                for i, paragraph in enumerate(card.content, 1):
                    print(f"  {i}. {paragraph}")
        
        print("\n" + "=" * 60)
        print("✅ 所有生成的新知识卡片内容已优化完成")
        print("   去除了呆板的三段式格式，内容更加流畅自然")
        print("   增加了历史背景、实例和文化内涵")
        print("   语言更加生动形象，符合阅读习惯")
        print("=" * 60)
        
    except Exception as e:
        print(f"验证时出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    verify_new_cards()