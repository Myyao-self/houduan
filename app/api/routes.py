from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.ai_service import AIService
from app.models import KnowledgeCard, Building, get_db

router = APIRouter()
ai_service = AIService()

# 定义请求模型
class SearchRequest(BaseModel):
    query: str

# 定义知识卡片请求/响应模型
class KnowledgeCardBase(BaseModel):
    title: str
    category: str
    image: str | None = None
    content: list[str]
    tags: list[str]

class KnowledgeCardCreate(KnowledgeCardBase):
    pass

class KnowledgeCardResponse(KnowledgeCardBase):
    id: int
    
    class Config:
        from_attributes = True

# 定义建筑请求/响应模型
class BuildingBase(BaseModel):
    title: str
    brief: str
    detail: str
    image: str | None = None
    type: str
    tags: list[str]

class BuildingCreate(BuildingBase):
    pass

class BuildingResponse(BuildingBase):
    id: int
    
    class Config:
        from_attributes = True

@router.post("/search")
async def search_buildings(request: SearchRequest):
    try:
        result = ai_service.search_buildings(request.query)
        return {"data": result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 知识卡片相关API

# 获取知识卡片列表
@router.get("/knowledge-cards", response_model=list[KnowledgeCardResponse])
async def get_knowledge_cards(category: str = None, db: Session = Depends(get_db)):
    try:
        query = db.query(KnowledgeCard)
        if category:
            query = query.filter(KnowledgeCard.category == category)
        cards = query.all()
        return cards
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取单个知识卡片
@router.get("/knowledge-cards/{card_id}", response_model=KnowledgeCardResponse)
async def get_knowledge_card(card_id: int, db: Session = Depends(get_db)):
    try:
        card = db.query(KnowledgeCard).filter(KnowledgeCard.id == card_id).first()
        if not card:
            raise HTTPException(status_code=404, detail="Knowledge card not found")
        return card
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 创建知识卡片
@router.post("/knowledge-cards", response_model=KnowledgeCardResponse)
async def create_knowledge_card(card: KnowledgeCardCreate, db: Session = Depends(get_db)):
    try:
        db_card = KnowledgeCard(**card.dict())
        db.add(db_card)
        db.commit()
        db.refresh(db_card)
        return db_card
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 建筑分类相关API

# 获取建筑列表
@router.get("/buildings", response_model=list[BuildingResponse])
async def get_buildings(type: str = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Building)
        if type:
            query = query.filter(Building.type == type)
        buildings = query.all()
        return buildings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取单个建筑详情
@router.get("/buildings/{building_id}", response_model=BuildingResponse)
async def get_building(building_id: int, db: Session = Depends(get_db)):
    try:
        building = db.query(Building).filter(Building.id == building_id).first()
        if not building:
            raise HTTPException(status_code=404, detail="Building not found")
        return building
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 创建建筑
@router.post("/buildings", response_model=BuildingResponse)
async def create_building(building: BuildingCreate, db: Session = Depends(get_db)):
    try:
        db_building = Building(**building.dict())
        db.add(db_building)
        db.commit()
        db.refresh(db_building)
        return db_building
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 获取知识图谱数据
@router.get("/knowledge-graph")
async def get_knowledge_graph(db: Session = Depends(get_db)):
    try:
        # 获取所有建筑
        buildings = db.query(Building).all()
        # 获取所有知识卡片
        knowledge_cards = db.query(KnowledgeCard).all()
        
        # 构建节点和边
        nodes = []
        links = []
        node_id_map = {}
        next_id = 1
        
        # 节点分类映射
        category_map = {
            'building': 0,
            'structure': 1,
            'material': 2,
            'craft': 3,
            'culture': 4,
            'history': 5
        }
        
        # 添加建筑节点
        for building in buildings:
            node_id = str(next_id)
            node_id_map[f"building_{building.id}"] = node_id
            nodes.append({
                'id': node_id,
                'name': building.title,
                'category': category_map['building'],
                'symbolSize': 70,
                'description': building.brief,
                'type': 'building'
            })
            next_id += 1
        
        # 添加知识卡片节点
        for card in knowledge_cards:
            node_id = str(next_id)
            node_id_map[f"knowledge_{card.id}"] = node_id
            nodes.append({
                'id': node_id,
                'name': card.title,
                'category': category_map[card.category],
                'symbolSize': 50,
                'description': card.content[0] if card.content else '',
                'type': 'knowledge'
            })
            next_id += 1
        
        # 构建关联规则
        # 1. 建筑与结构知识关联
        structure_related_buildings = {
            'palace': ['抬梁式结构', '斗拱结构体系'],
            'residence': ['穿斗式结构', '井干式结构'],
            'bridge': ['砖石结构'],
            'garden': ['抬梁式结构'],
            'temple': ['抬梁式结构'],
            'fort': ['砖石结构']
        }
        
        # 2. 建筑与材料知识关联
        material_related_buildings = {
            'palace': ['琉璃瓦', '古建筑木材的选用'],
            'residence': ['生土建筑材料', '砖瓦烧制工艺'],
            'bridge': ['砖石结构', '石灰浆'],
            'garden': ['琉璃瓦', '古建筑木材的选用'],
            'temple': ['琉璃瓦', '古建筑木材的选用'],
            'fort': ['砖石结构', '石灰浆']
        }
        
        # 3. 建筑与工艺知识关联
        craft_related_buildings = {
            'palace': ['彩画工艺', '榫卯工艺'],
            'residence': ['榫卯工艺', '砖雕工艺'],
            'bridge': ['砖瓦烧制工艺', '榫卯工艺'],
            'garden': ['彩画工艺', '砖雕工艺'],
            'temple': ['彩画工艺', '砖雕工艺'],
            'fort': ['砖瓦烧制工艺', '砖雕工艺']
        }
        
        # 4. 建筑与文化知识关联
        culture_related_buildings = {
            'palace': ['建筑与礼制', '古建筑的等级制度'],
            'residence': ['建筑与五行', '古建筑的风水理念'],
            'bridge': ['建筑与五行'],
            'garden': ['建筑与五行', '古建筑的风水理念'],
            'temple': ['建筑与礼制', '建筑与五行'],
            'fort': ['建筑与礼制']
        }
        
        # 5. 建筑与历史知识关联
        history_related_buildings = {
            'palace': ['明清建筑的特点', '唐宋建筑风格演变'],
            'residence': ['原始社会建筑', '近代建筑转型'],
            'bridge': ['唐宋建筑风格演变'],
            'garden': ['明清建筑的特点'],
            'temple': ['唐宋建筑风格演变'],
            'fort': ['明清建筑的特点']
        }
        
        # 创建关联映射
        relation_maps = {
            'structure': structure_related_buildings,
            'material': material_related_buildings,
            'craft': craft_related_buildings,
            'culture': culture_related_buildings,
            'history': history_related_buildings
        }
        
        # 构建边
        for building in buildings:
            building_node_id = node_id_map[f"building_{building.id}"]
            
            # 为每个知识分类添加关联
            for category, relation_map in relation_maps.items():
                if building.type in relation_map:
                    related_knowledge_titles = relation_map[building.type]
                    
                    for knowledge_title in related_knowledge_titles:
                        # 查找对应的知识卡片
                        for card in knowledge_cards:
                            if card.title == knowledge_title:
                                knowledge_node_id = node_id_map[f"knowledge_{card.id}"]
                                links.append({
                                    'source': building_node_id,
                                    'target': knowledge_node_id,
                                    'name': category
                                })
        
        # 添加知识卡片之间的关联
        knowledge_relations = [
            ('抬梁式结构', '榫卯工艺'),
            ('穿斗式结构', '榫卯工艺'),
            ('井干式结构', '榫卯工艺'),
            ('斗拱结构体系', '榫卯工艺'),
            ('砖石结构', '砖瓦烧制工艺'),
            ('琉璃瓦', '砖瓦烧制工艺'),
            ('明清建筑的特点', '古建筑的等级制度'),
            ('唐宋建筑风格演变', '古建筑的等级制度')
        ]
        
        for source_title, target_title in knowledge_relations:
            source_node = None
            target_node = None
            
            for node in nodes:
                if node['name'] == source_title:
                    source_node = node
                if node['name'] == target_title:
                    target_node = node
            
            if source_node and target_node:
                links.append({
                    'source': source_node['id'],
                    'target': target_node['id'],
                    'name': '相关'
                })
        
        return {
            'nodes': nodes,
            'links': links,
            'categories': [
                { 'name': '建筑', 'itemStyle': { 'color': '#8b0000' } },
                { 'name': '结构', 'itemStyle': { 'color': '#ff6b6b' } },
                { 'name': '材料', 'itemStyle': { 'color': '#4ecdc4' } },
                { 'name': '工艺', 'itemStyle': { 'color': '#45b7d1' } },
                { 'name': '文化', 'itemStyle': { 'color': '#96ceb4' } },
                { 'name': '历史', 'itemStyle': { 'color': '#ffeaa7' } }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
