from app.models import KnowledgeCard, get_db

# 添加一条缺失的知识卡片
def add_missing_card():
    # 获取数据库会话
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # 检查是否已有11条数据
        existing_count = db.query(KnowledgeCard).count()
        if existing_count >= 11:
            print(f"数据库中已有 {existing_count} 条知识卡片，无需添加")
            return
        
        # 添加一条新的知识卡片（以结构类型为例）
        new_card = KnowledgeCard(
            title="穿斗式结构",
            category="structure",
            image="/images/chuandou.png",
            content=[
                "穿斗式结构是中国古建筑中常用的结构形式之一，尤其适用于南方民居建筑。其特点是：用穿枋把柱子串联起来，形成一榀榀的房架，檩条直接搁置在柱头上。",
                "穿斗式结构的优点是用料小，整体性强，但柱子排列较密，室内空间不开阔。常见于江南、西南等地区的民居建筑。",
                "穿斗式结构的关键构件包括：柱、穿枋、檩条等，各构件之间通过榫卯连接，体现了中国传统木作工艺的高超水平。"
            ],
            tags=["穿斗式", "木结构", "民居建筑"]
        )
        
        db.add(new_card)
        db.commit()
        
        print(f"成功添加1条知识卡片，现在数据库中有 {db.query(KnowledgeCard).count()} 条")
        
    except Exception as e:
        db.rollback()
        print(f"添加知识卡片时出错: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_missing_card()
