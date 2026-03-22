from app.models import Building, KnowledgeCard, get_db

def check_buildings():
    # 获取数据库会话
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # 获取所有建筑分类
        buildings = db.query(Building).all()
        print(f"找到 {len(buildings)} 个建筑记录")
        print("\n建筑分类详情：")
        print("=" * 60)
        
        # 按类型分组
        buildings_by_type = {}
        for building in buildings:
            if building.type not in buildings_by_type:
                buildings_by_type[building.type] = []
            buildings_by_type[building.type].append(building)
        
        # 打印建筑分类
        for building_type, type_buildings in buildings_by_type.items():
            print(f"\n建筑类型: {building_type} ({len(type_buildings)}个建筑)")
            print("-" * 40)
            for building in type_buildings:
                print(f"  建筑名称: {building.title}")
                print(f"  简短描述: {building.brief}")
                print(f"  标签: {building.tags}")
        
        # 获取知识卡片分类
        print("\n" + "=" * 60)
        print("知识卡片分类：")
        print("=" * 60)
        
        knowledge_cards = db.query(KnowledgeCard).all()
        cards_by_category = {}
        for card in knowledge_cards:
            if card.category not in cards_by_category:
                cards_by_category[card.category] = []
            cards_by_category[card.category].append(card)
        
        for category, category_cards in cards_by_category.items():
            print(f"\n知识分类: {category} ({len(category_cards)}个卡片)")
            print("-" * 40)
            for card in category_cards[:3]:  # 只显示前3个
                print(f"  卡片标题: {card.title}")
                print(f"  标签: {card.tags}")
            if len(category_cards) > 3:
                print(f"  ... 等 {len(category_cards)} 个卡片")
        
    except Exception as e:
        print(f"查询时出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_buildings()