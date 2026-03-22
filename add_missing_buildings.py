from app.models import Building, get_db

# 添加缺失的寺庙和防御分类建筑
def add_missing_buildings():
    # 获取数据库会话
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # 检查并添加寺庙(temple)分类建筑
        temple_count = db.query(Building).filter(Building.type == 'temple').count()
        if temple_count == 0:
            # 添加大雁塔
            db.add(Building(
                title='大雁塔',
                brief='西安标志性建筑，唐代佛教建筑的杰出代表',
                detail='大雁塔位于陕西省西安市大慈恩寺内，又名慈恩寺塔。唐永徽三年（652年），玄奘为保存由天竺经丝绸之路带回长安的经卷佛像主持修建了大雁塔。大雁塔是现存最早、规模最大的唐代四方楼阁式砖塔，是佛塔这种古印度佛寺的建筑形式随佛教传入中原地区，并融入华夏文化的典型物证，是凝聚了中国古代劳动人民智慧结晶的标志性建筑。',
                image='/images/dayanta.jpg',
                tags=['寺庙', '佛塔', '唐代', '西安'],
                type='temple'
            ))
            
            # 添加北京鼓楼
            db.add(Building(
                title='北京鼓楼',
                brief='北京中轴线标志性建筑，古代报时中心',
                detail='北京鼓楼位于北京市东城区地安门外大街北端，是北京中轴线的重要组成部分。鼓楼始建于元至元九年（1272年），明永乐十八年（1420年）重建，清嘉庆五年（1800年）重修。鼓楼是中国古代城市的报时中心，每天击鼓报时，是北京古都的重要象征。',
                image='/images/beijinggulou.jpg',
                tags=['楼阁', '明代', '北京', '报时'],
                type='temple'
            ))
            
            print('成功添加2条寺庙(temple)分类建筑')
        
        # 检查并添加防御(fort)分类建筑
        fort_count = db.query(Building).filter(Building.type == 'fort').count()
        if fort_count == 0:
            # 添加平遥古城墙
            db.add(Building(
                title='平遥古城墙',
                brief='中国现存最完整的明清古城墙，兼具军事防御和城市功能',
                detail='平遥古城墙位于山西省中部的平遥县，是中国现存最完整的明清古县城。平遥古城墙始建于西周宣王时期（公元前827年～公元前782年），明洪武三年（1370年）扩建，距今已有2700多年的历史。迄今为止，它还较为完好地保留着明清时期县城的基本风貌，堪称中国汉民族地区现存最为完整的古城。',
                image='/images/pingyao.png',
                tags=['防御', '城墙', '明清', '平遥'],
                type='fort'
            ))
            
            # 添加八达岭长城
            db.add(Building(
                title='八达岭长城',
                brief='明长城中保存最好的一段，是万里长城的精华所在',
                detail='八达岭长城位于北京市延庆区，是明长城中保存最好的一段，也是最具代表性的一段，是万里长城的精华所在。八达岭长城建于1504年，地势险峻，城关坚固，是明代长城中最具代表性的地段。八达岭长城是万里长城向游人开放最早的地段，也是至今为止保护最好，最具代表性的一段。',
                image='/images/badaling.jpg',
                tags=['防御', '长城', '明代', '军事'],
                type='fort'
            ))
            
            print('成功添加2条防御(fort)分类建筑')
        
        # 提交更改
        db.commit()
        
        # 打印最终统计
        print('\n最终建筑分类统计：')
        print('宫殿(palace)：', db.query(Building).filter(Building.type == 'palace').count())
        print('民居(residence)：', db.query(Building).filter(Building.type == 'residence').count())
        print('桥梁(bridge)：', db.query(Building).filter(Building.type == 'bridge').count())
        print('园林(garden)：', db.query(Building).filter(Building.type == 'garden').count())
        print('寺庙(temple)：', db.query(Building).filter(Building.type == 'temple').count())
        print('防御(fort)：', db.query(Building).filter(Building.type == 'fort').count())
        print('总计：', db.query(Building).count())
        
    except Exception as e:
        db.rollback()
        print(f"添加建筑时出错: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_missing_buildings()
