from app.models import KnowledgeCard, get_db
import os

# 知识卡片标题与图片名的映射关系
title_image_map = {
    '井干式结构': 'jingganshijiegou',
    '砖石结构': 'zhuanshijiegou',
    '琉璃瓦': 'liuliwa',
    '石灰浆': 'shihuijiang',
    '彩画工艺': 'caihuagongyi',
    '砖雕工艺': 'zhuandiaogongyi',
    '建筑与五行': 'jianzhuyuwuxing',
    '建筑与礼制': 'jianzhuyulizhi',
    '原始社会建筑': 'yuanshishehuijianzhu',
    '近代建筑转型': 'jindaijianzhuzhuanxing'
}

# 图片目录
image_dir = '../frontsize/public/images'

def update_image_paths():
    print("开始更新知识卡片图片路径...")
    print(f"图片目录: {image_dir}")
    
    # 检查图片目录是否存在
    if not os.path.exists(image_dir):
        print(f"错误: 图片目录 {image_dir} 不存在")
        return
    
    # 列出图片目录中的文件
    print("\n图片目录中的文件:")
    image_files = os.listdir(image_dir)
    for f in image_files[:10]:  # 只显示前10个文件
        print(f"  - {f}")
    if len(image_files) > 10:
        print(f"  ... 等 {len(image_files)} 个文件")
    
    # 获取数据库会话
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # 获取所有知识卡片
        cards = db.query(KnowledgeCard).all()
        print(f"\n找到 {len(cards)} 个知识卡片")
        
        updated_count = 0
        for card in cards:
            print(f"\n处理知识卡片: {card.title}")
            if card.title in title_image_map:
                print(f"  标题在映射表中")
                # 获取图片文件名前缀
                image_prefix = title_image_map[card.title]
                print(f"  图片前缀: {image_prefix}")
                
                # 在图片目录中查找匹配的图片文件
                matching_images = []
                for filename in image_files:
                    if filename.startswith(image_prefix):
                        matching_images.append(filename)
                
                print(f"  匹配到的图片: {matching_images}")
                
                if matching_images:
                    # 选择第一个匹配的图片文件
                    image_filename = matching_images[0]
                    # 构建图片路径
                    image_path = f'/images/{image_filename}'
                    
                    # 更新知识卡片的image字段
                    card.image = image_path
                    updated_count += 1
                    print(f"  ✅ 更新为: {image_path}")
                else:
                    print(f"  ❌ 未找到匹配的图片")
            else:
                print(f"  标题不在映射表中")
        
        # 提交更新
        db.commit()
        print(f"\n✅ 成功更新了 {updated_count} 个知识卡片的图片路径")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ 更新图片路径时出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        print("\n数据库连接已关闭")

if __name__ == "__main__":
    update_image_paths()