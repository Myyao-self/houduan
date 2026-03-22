from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from config.config import Config

# 创建数据库引擎
engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 知识卡片模型
class KnowledgeCard(Base):
    __tablename__ = "knowledge_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)  # 分类：structure, material, craft, culture, history
    image = Column(String)
    _content = Column(Text, nullable=False, name="content")  # 存储为JSON字符串
    _tags = Column(Text, nullable=False, name="tags")  # 存储为JSON字符串
    
    # 配置SQLite支持
    __table_args__ = {
        'sqlite_autoincrement': True,
    }
    
    # content属性的getter和setter
    @property
    def content(self):
        return json.loads(self._content)
    
    @content.setter
    def content(self, value):
        self._content = json.dumps(value)
    
    # tags属性的getter和setter
    @property
    def tags(self):
        return json.loads(self._tags)
    
    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(value)

# 建筑分类模型
class Building(Base):
    __tablename__ = "buildings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)  # 建筑名称
    brief = Column(Text, nullable=False)  # 简短描述
    detail = Column(Text, nullable=False)  # 详细描述
    image = Column(String)  # 图片路径
    type = Column(String, index=True, nullable=False)  # 建筑类型：palace, residence, bridge等
    _tags = Column(Text, nullable=False, name="tags")  # 标签数组，存储为JSON字符串
    
    # 配置SQLite支持
    __table_args__ = {
        'sqlite_autoincrement': True,
    }
    
    # tags属性的getter和setter
    @property
    def tags(self):
        return json.loads(self._tags)
    
    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(value)

# 初始化数据库
def init_db():
    Base.metadata.create_all(bind=engine)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
