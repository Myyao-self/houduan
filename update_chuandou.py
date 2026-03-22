from app.models import KnowledgeCard, get_db
import os

def update_chuandou_card():
    # 获取数据库会话
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # 查找穿斗式结构知识卡片
        card = db.query(KnowledgeCard).filter_by(title='穿斗式结构').first()
        if not card:
            print("未找到穿斗式结构知识卡片")
            return
        
        print(f"当前穿斗式结构卡片：")
        print(f"标题：{card.title}")
        print(f"当前图片：{card.image}")
        print(f"当前内容：{card.content}")
        print(f"当前标签：{card.tags}")
        
        # 检查是否有chuandoushijiegou的图片
        image_dir = '../frontsize/public/images'
        matching_images = []
        for filename in os.listdir(image_dir):
            if filename.startswith('chuandoushijiegou'):
                matching_images.append(filename)
        
        if matching_images:
            # 选择第一个匹配的图片文件
            image_filename = matching_images[0]
            # 构建图片路径
            image_path = f'/images/{image_filename}'
            
            # 更新知识卡片的image字段
            card.image = image_path
            print(f"\n更新图片为：{image_path}")
        
        # 更新内容为更流畅的格式
        card.content = [
            '穿斗式结构是中国古建筑中常用的木结构形式之一，其特点是用穿枋将柱子串联起来，形成一榀榀的房架，檩条直接搁置在柱头上。',
            '这种结构形式在南方地区尤为常见，适用于开间较小的房屋，具有用料经济、施工简便、抗风性能好等特点。',
            '穿斗式结构的柱距较密，空间分隔灵活，适合住宅等建筑类型，与抬梁式结构相比，更能适应南方潮湿多雨的气候条件。'
        ]
        
        # 提交更新
        db.commit()
        print(f"\n✅ 成功更新穿斗式结构知识卡片")
        print(f"新内容：{card.content}")
        
    except Exception as e:
        db.rollback()
        print(f"更新时出错: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_chuandou_card()