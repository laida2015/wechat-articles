# 系统架构设计

## 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                         前端层 (Vue 3)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ 订阅管理 │  │ 文章列表 │  │ 文章详情 │  │ 知识库   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                      后端层 (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    API 路由层                         │  │
│  │  /api/accounts  /api/articles  /api/knowledge        │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    业务逻辑层                         │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐ │  │
│  │  │订阅服务 │  │文章服务 │  │AI服务   │  │知识服务│ │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    数据访问层                         │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐ │  │
│  │  │Account  │  │Article  │  │Analysis │  │Knowledge│ │  │
│  │  │Repository│  │Repository│  │Repository│ │Repository│ │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      数据层                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ PostgreSQL   │  │ Redis        │  │ 文件存储     │     │
│  │ (主数据库)   │  │ (缓存/队列)  │  │ (图片等)     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      外部服务                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ wewe-rss     │  │ OpenAI API   │  │ 微信读书     │     │
│  │ (RSS服务)    │  │ (AI分析)     │  │ (数据源)     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 目录结构

```
wechat-articles/
├── backend/                    # 后端代码
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI 应用入口
│   │   ├── config.py          # 配置管理
│   │   ├── database.py        # 数据库连接
│   │   ├── models/            # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── account.py
│   │   │   ├── article.py
│   │   │   ├── analysis.py
│   │   │   └── knowledge.py
│   │   ├── schemas/           # Pydantic 模型
│   │   │   ├── __init__.py
│   │   │   ├── account.py
│   │   │   ├── article.py
│   │   │   ├── analysis.py
│   │   │   └── knowledge.py
│   │   ├── api/               # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── accounts.py
│   │   │   ├── articles.py
│   │   │   ├── analysis.py
│   │   │   └── knowledge.py
│   │   ├── services/          # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── account_service.py
│   │   │   ├── article_service.py
│   │   │   ├── ai_service.py
│   │   │   ├── rss_service.py
│   │   │   └── knowledge_service.py
│   │   └── utils/             # 工具函数
│   │       ├── __init__.py
│   │       ├── html_parser.py
│   │       └── text_cleaner.py
│   ├── alembic/               # 数据库迁移
│   ├── tests/                 # 测试
│   ├── requirements.txt       # Python 依赖
│   └── .env.example           # 环境变量示例
│
├── frontend/                   # 前端代码
│   ├── src/
│   │   ├── main.ts            # 应用入口
│   │   ├── App.vue            # 根组件
│   │   ├── router/            # 路由配置
│   │   │   └── index.ts
│   │   ├── stores/            # 状态管理 (Pinia)
│   │   │   ├── account.ts
│   │   │   ├── article.ts
│   │   │   └── knowledge.ts
│   │   ├── views/             # 页面组件
│   │   │   ├── Home.vue
│   │   │   ├── Accounts.vue
│   │   │   ├── Articles.vue
│   │   │   ├── ArticleDetail.vue
│   │   │   └── Knowledge.vue
│   │   ├── components/        # 通用组件
│   │   │   ├── ArticleCard.vue
│   │   │   ├── ArticleList.vue
│   │   │   ├── AccountCard.vue
│   │   │   └── SearchBar.vue
│   │   ├── api/               # API 调用
│   │   │   ├── client.ts
│   │   │   ├── accounts.ts
│   │   │   ├── articles.ts
│   │   │   └── knowledge.ts
│   │   ├── types/             # TypeScript 类型
│   │   │   └── index.ts
│   │   ├── assets/            # 静态资源
│   │   └── styles/            # 样式文件
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── docker/                     # Docker 配置
│   ├── docker-compose.yml     # 完整服务编排
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
│
├── docs/                       # 文档
│   ├── API.md                 # API 文档
│   ├── DEPLOYMENT.md          # 部署文档
│   └── DEVELOPMENT.md         # 开发文档
│
├── scripts/                    # 脚本
│   ├── init_db.py             # 初始化数据库
│   └── sync_articles.py       # 同步文章脚本
│
├── .gitignore
├── README.md
├── REQUIREMENTS.md            # 需求文档
└── ARCHITECTURE.md            # 本文件
```

## 核心模块设计

### 1. 数据获取模块 (RSS Service)

**职责**: 从 wewe-rss 获取文章数据

**核心功能**:
- 连接 wewe-rss API
- 解析 RSS/Atom feed
- 提取文章元数据
- 下载文章内容
- 图片本地化

**关键类**:
```python
class RSSService:
    def __init__(self, wewe_rss_url: str):
        self.base_url = wewe_rss_url
    
    async def get_feeds(self) -> List[Feed]:
        """获取所有订阅源"""
        pass
    
    async def get_articles(self, feed_id: str, limit: int = 20) -> List[Article]:
        """获取指定订阅源的文章"""
        pass
    
    async def fetch_article_content(self, url: str) -> str:
        """获取文章完整内容"""
        pass
    
    async def sync_all_articles(self):
        """同步所有订阅源的文章"""
        pass
```

### 2. AI 分析模块 (AI Service)

**职责**: 使用 AI 分析文章内容

**核心功能**:
- 生成文章摘要
- 提取关键词
- 自动分类
- 实体识别
- 结构化信息提取

**关键类**:
```python
class AIService:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    async def generate_summary(self, content: str) -> str:
        """生成文章摘要"""
        pass
    
    async def classify_article(self, title: str, content: str) -> ArticleCategory:
        """文章分类"""
        pass
    
    async def extract_entities(self, content: str) -> Dict:
        """提取实体信息"""
        pass
    
    async def extract_paper_info(self, content: str) -> Optional[PaperInfo]:
        """提取论文信息"""
        pass
    
    async def extract_tool_info(self, content: str) -> Optional[ToolInfo]:
        """提取工具信息"""
        pass
    
    async def analyze_article(self, article: Article) -> ArticleAnalysis:
        """完整分析文章"""
        pass
```

### 3. 文章服务 (Article Service)

**职责**: 文章的 CRUD 和业务逻辑

**核心功能**:
- 文章列表查询
- 文章详情获取
- 文章收藏/取消收藏
- 文章搜索
- 文章标签管理

**关键类**:
```python
class ArticleService:
    def __init__(self, db: Session, ai_service: AIService):
        self.db = db
        self.ai_service = ai_service
    
    async def get_articles(
        self, 
        account_id: Optional[int] = None,
        category: Optional[str] = None,
        is_favorite: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Article]:
        """获取文章列表"""
        pass
    
    async def get_article(self, article_id: int) -> Article:
        """获取文章详情"""
        pass
    
    async def create_article(self, article_data: ArticleCreate) -> Article:
        """创建文章"""
        pass
    
    async def toggle_favorite(self, article_id: int) -> Article:
        """切换收藏状态"""
        pass
    
    async def search_articles(self, query: str) -> List[Article]:
        """搜索文章"""
        pass
    
    async def analyze_article(self, article_id: int) -> ArticleAnalysis:
        """分析文章"""
        pass
```

### 4. 知识库服务 (Knowledge Service)

**职责**: 知识库的管理和查询

**核心功能**:
- 知识条目创建
- 知识检索
- 关联文章管理
- 知识导出

**关键类**:
```python
class KnowledgeService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_knowledge(
        self, 
        knowledge_type: str,
        title: str,
        content: Dict,
        source_articles: List[int]
    ) -> Knowledge:
        """创建知识条目"""
        pass
    
    async def get_knowledge_list(
        self,
        knowledge_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Knowledge]:
        """获取知识列表"""
        pass
    
    async def search_knowledge(self, query: str) -> List[Knowledge]:
        """搜索知识"""
        pass
    
    async def export_knowledge(self, knowledge_id: int, format: str) -> str:
        """导出知识"""
        pass
```

## 数据库设计

### 表结构

#### accounts (公众号表)
```sql
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    weread_id VARCHAR(255) UNIQUE,
    avatar TEXT,
    description TEXT,
    feed_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### articles (文章表)
```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    content TEXT,
    content_text TEXT,
    url TEXT UNIQUE,
    published_at TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_favorite BOOLEAN DEFAULT FALSE,
    category VARCHAR(50),
    tags JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_articles_account_id ON articles(account_id);
CREATE INDEX idx_articles_category ON articles(category);
CREATE INDEX idx_articles_published_at ON articles(published_at DESC);
CREATE INDEX idx_articles_is_favorite ON articles(is_favorite);
```

#### article_analysis (文章分析表)
```sql
CREATE TABLE article_analysis (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(id) ON DELETE CASCADE,
    summary TEXT,
    keywords JSONB,
    entities JSONB,
    category_confidence FLOAT,
    paper_info JSONB,
    tool_info JSONB,
    news_info JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analysis_article_id ON article_analysis(article_id);
```

#### knowledge_base (知识库表)
```sql
CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(500) NOT NULL,
    content JSONB NOT NULL,
    source_articles JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_knowledge_type ON knowledge_base(type);
```

## API 设计

### 公众号管理

```
GET    /api/accounts              # 获取公众号列表
POST   /api/accounts              # 添加公众号
GET    /api/accounts/{id}         # 获取公众号详情
PUT    /api/accounts/{id}         # 更新公众号
DELETE /api/accounts/{id}         # 删除公众号
POST   /api/accounts/{id}/sync    # 同步公众号文章
```

### 文章管理

```
GET    /api/articles              # 获取文章列表
GET    /api/articles/{id}         # 获取文章详情
POST   /api/articles              # 手动添加文章
PUT    /api/articles/{id}         # 更新文章
DELETE /api/articles/{id}         # 删除文章
POST   /api/articles/{id}/favorite # 收藏/取消收藏
POST   /api/articles/{id}/analyze  # 分析文章
GET    /api/articles/search       # 搜索文章
```

### 知识库管理

```
GET    /api/knowledge             # 获取知识列表
POST   /api/knowledge             # 创建知识条目
GET    /api/knowledge/{id}        # 获取知识详情
PUT    /api/knowledge/{id}        # 更新知识
DELETE /api/knowledge/{id}        # 删除知识
GET    /api/knowledge/search      # 搜索知识
GET    /api/knowledge/{id}/export # 导出知识
```

## 部署架构

### Docker Compose 部署

```yaml
version: '3.8'

services:
  # PostgreSQL 数据库
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: wechat_articles
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  # Redis 缓存
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # wewe-rss 服务
  wewe-rss:
    image: cooderl/wewe-rss:latest
    environment:
      DATABASE_URL: postgresql://admin:password@postgres:5432/wewe_rss
      AUTH_CODE: your_auth_code
    ports:
      - "4000:4000"
    depends_on:
      - postgres

  # 后端服务
  backend:
    build:
      context: ./backend
      dockerfile: ../docker/backend.Dockerfile
    environment:
      DATABASE_URL: postgresql://admin:password@postgres:5432/wechat_articles
      REDIS_URL: redis://redis:6379
      WEWE_RSS_URL: http://wewe-rss:4000
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - wewe-rss
    volumes:
      - ./backend:/app
      - media_files:/app/media

  # 前端服务
  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/frontend.Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  postgres_data:
  media_files:
```

## 安全考虑

1. **API 认证**: 使用 JWT token
2. **数据加密**: 敏感数据加密存储
3. **CORS 配置**: 限制跨域访问
4. **SQL 注入防护**: 使用 ORM 参数化查询
5. **XSS 防护**: 前端输入验证和转义
6. **Rate Limiting**: API 请求频率限制

## 性能优化

1. **数据库索引**: 关键字段建立索引
2. **缓存策略**: Redis 缓存热点数据
3. **分页加载**: 大列表分页查询
4. **异步处理**: 耗时任务异步执行
5. **CDN 加速**: 静态资源 CDN 分发
6. **数据库连接池**: 复用数据库连接

## 监控和日志

1. **应用日志**: 使用 structlog 结构化日志
2. **错误追踪**: Sentry 错误监控
3. **性能监控**: 接口响应时间监控
4. **数据库监控**: 慢查询日志
5. **资源监控**: CPU、内存、磁盘使用率
