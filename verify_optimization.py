from app.models import KnowledgeCard, get_db

def verify_optimization():
    # 获取数据库会话
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # 获取所有知识卡片
        cards = db.query(KnowledgeCard).all()
        print(f"找到 {len(cards)} 个知识卡片")
        
        print("\n" + "=" * 60)
        print("验证知识卡片优化结果")
        print("=" * 60)
        
        # 重点检查穿斗式结构卡片
        print("\n1. 穿斗式结构卡片:")
        print("-" * 40)
        chuan_dou_card = db.query(KnowledgeCard).filter_by(title='穿斗式结构').first()
        if chuan_dou_card:
            print(f"标题: {chuan_dou_card.title}")
            print(f"图片: {chuan_dou_card.image}")
            print("内容:")
            for i, paragraph in enumerate(chuan_dou_card.content, 1):
                print(f"  {i}. {paragraph}")
            print(f"标签: {chuan_dou_card.tags}")
        
        # 检查其他几个关键卡片
        key_cards = ['抬梁式结构', '斗拱结构体系', '榫卯工艺', '唐宋建筑风格演变', '明清建筑的特点']
        
        for card_title in key_cards:
            print(f"\n2. {card_title}:")
            print("-" * 40)
            card = db.query(KnowledgeCard).filter_by(title=card_title).first()
            if card:
                print(f"标题: {card.title}")
                print("内容:")
                for i, paragraph in enumerate(card.content, 1):
                    print(f"  {i}. {paragraph}")
                print(f"标签: {card.tags}")
        
        print("\n" + "=" * 60)
        print("验证完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"验证时出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    verify_optimization()