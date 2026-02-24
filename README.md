# 微信公众号文章知识库系统

一个智能的微信公众号文章管理和知识提取系统，帮助你将碎片化的公众号文章转化为结构化的知识库。

## 🚀 快速部署

### 一键部署到云端（完全免费）

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/laida2015/wechat-articles&root-directory=frontend)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/laida2015/wechat-articles)

**5 分钟部署指南：** [DEPLOY_NOW.md](DEPLOY_NOW.md)

**详细部署教程：** [docs/DEPLOY_TUTORIAL.md](docs/DEPLOY_TUTORIAL.md)

## 🌟 核心功能

### 1. 数据获取
- 基于 wewe-rss 自动订阅公众号
- 自动抓取历史文章
- 支持手动添加文章链接
- 定时同步新文章

### 2. 内容管理
- 文章列表展示（按公众号、时间、分类）
- 文章详情阅读
- 收藏/标记功能
- 标签管理
- 全文搜索

### 3. AI 智能分析
- 自动生成文章摘要
- 智能分类（学术论文/工具资讯/行业动态）
- 关键词提取
- 实体识别
- 结构化信息提取

### 4. 知识库
- 论文追踪库
- 工具库
- 资讯库
- 知识导出（Markdown/PDF）

## 🏗️ 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: PostgreSQL
- **缓存**: Redis
- **AI**: OpenAI GPT-4
- **RSS**: wewe-rss

### 前端
- **框架**: Vue 3 + TypeScript
- **UI**: Element Plus
- **状态管理**: Pinia
- **构建工具**: Vite

### 部署
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx (可选)

## 🚀 快速开始

### 前置要求

- Docker 和 Docker Compose
- OpenAI API Key
- 至少 2GB 可用内存

### 1. 克隆项目

```bash
git clone https://github.com/j-lab-10404/wechat-articles.git
cd wechat-articles
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp backend/.env.example backend/.env

# 编辑 .env 文件，填入你的配置
# 必须配置：
# - OPENAI_API_KEY: 你的 OpenAI API Key
# - SECRET_KEY: 随机生成的密钥
```

### 3. 启动服务

```bash
cd docker
docker-compose up -d
```

### 4. 访问应用

- 前端: http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs
- wewe-rss: http://localhost:4000

### 5. 初始化数据库

```bash
# 进入后端容器
docker exec -it wechat-articles-backend bash

# 运行数据库迁移
alembic upgrade head
```

## 📖 使用指南

### 添加公众号订阅

1. 访问 wewe-rss (http://localhost:4000)
2. 扫码登录微信读书账号
3. 添加公众号订阅
4. 在系统中添加对应的公众号信息

### 同步文章

系统会自动定时同步文章，你也可以手动触发：

```bash
# 通过 API 触发同步
curl -X POST http://localhost:8000/api/accounts/{account_id}/sync
```

### AI 分析文章

```bash
# 分析单篇文章
curl -X POST http://localhost:8000/api/articles/{article_id}/analyze
```

## 🔧 开发指南

### 后端开发

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
uvicorn app.main:app --reload
```

### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

### 数据库迁移

```bash
# 创建新迁移
alembic revision --autogenerate -m "description"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 📁 项目结构

```
wechat-articles/
├── backend/              # 后端代码
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── models/      # 数据模型
│   │   ├── schemas/     # Pydantic 模型
│   │   ├── services/    # 业务逻辑
│   │   └── utils/       # 工具函数
│   ├── alembic/         # 数据库迁移
│   └── tests/           # 测试
├── frontend/            # 前端代码
│   └── src/
│       ├── api/         # API 调用
│       ├── components/  # 组件
│       ├── views/       # 页面
│       ├── stores/      # 状态管理
│       └── router/      # 路由
├── docker/              # Docker 配置
├── docs/                # 文档
└── scripts/             # 脚本

```

## 🔐 安全建议

1. **修改默认密码**: 修改 docker-compose.yml 中的数据库密码
2. **保护 API Key**: 不要将 .env 文件提交到 Git
3. **使用 HTTPS**: 生产环境使用 HTTPS
4. **限制访问**: 配置防火墙规则
5. **定期备份**: 定期备份数据库

## 📝 待办事项

- [ ] 批量文章分析
- [ ] 知识图谱可视化
- [ ] 移动端适配
- [ ] 数据导出功能
- [ ] 多用户支持
- [ ] 文章推荐系统

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [wewe-rss](https://github.com/cooderl/wewe-rss) - 微信公众号 RSS 服务
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [Vue 3](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Element Plus](https://element-plus.org/) - Vue 3 UI 组件库

## 📧 联系方式

- Email: liujie@njfu.edu.cn
- GitHub: [@j-lab-10404](https://github.com/j-lab-10404)
