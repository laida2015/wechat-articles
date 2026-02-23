# 快速开始指南

本指南将帮助你在 10 分钟内启动并运行微信公众号文章知识库系统。

## 第一步：准备工作

### 1.1 安装 Docker

**Windows:**
- 下载并安装 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- 启动 Docker Desktop

**macOS:**
- 下载并安装 [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- 启动 Docker Desktop

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl start docker
```

### 1.2 获取 OpenAI API Key

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制并保存 API Key

## 第二步：部署系统

### 2.1 克隆项目

```bash
git clone https://github.com/j-lab-10404/wechat-articles.git
cd wechat-articles
```

### 2.2 配置环境变量

```bash
# 复制环境变量模板
cp backend/.env.example backend/.env

# 编辑配置文件
# Windows: notepad backend/.env
# macOS/Linux: nano backend/.env
```

**必须配置的项目：**

```env
# OpenAI API Key (必填)
OPENAI_API_KEY=sk-your-api-key-here

# 数据库密码 (建议修改)
DATABASE_URL=postgresql://admin:your_password@postgres:5432/wechat_articles

# 应用密钥 (必须修改为随机字符串)
SECRET_KEY=your-random-secret-key-here

# wewe-rss 授权码 (可选，建议设置)
WEWE_RSS_AUTH_CODE=your_auth_code
```

**生成随机密钥：**

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32
```

### 2.3 启动服务

```bash
cd docker
docker-compose up -d
```

**首次启动需要下载镜像，可能需要 5-10 分钟。**

### 2.4 检查服务状态

```bash
docker-compose ps
```

所有服务应该显示为 "Up" 状态。

### 2.5 初始化数据库

```bash
# 等待数据库启动（约 30 秒）
sleep 30

# 初始化数据库表
docker exec -it wechat-articles-backend python -c "from app.database import init_db; init_db()"
```

## 第三步：配置 wewe-rss

### 3.1 访问 wewe-rss

打开浏览器访问：http://localhost:4000

### 3.2 添加微信读书账号

1. 点击"账号管理"
2. 点击"添加账号"
3. 使用微信扫码登录微信读书
4. **注意：不要勾选"24小时后自动退出"**

### 3.3 订阅公众号

1. 点击"公众号源"
2. 点击"添加"
3. 在微信中打开公众号，点击右上角"..."，选择"分享"
4. 复制分享链接
5. 粘贴到 wewe-rss 中
6. 点击"提交"

**注意：添加频率不要太高，建议每次添加后等待 1-2 分钟。**

## 第四步：使用系统

### 4.1 访问前端

打开浏览器访问：http://localhost:3000

### 4.2 添加公众号

1. 点击"公众号管理"
2. 点击"添加公众号"
3. 填写公众号信息：
   - 名称：公众号名称
   - weread_id：从 wewe-rss 的 feed URL 中获取（格式：MP_WXS_xxx）
   - feed_url：wewe-rss 的 feed URL

**获取 feed_url：**
- 在 wewe-rss 中，点击公众号右侧的"RSS"图标
- 复制显示的 URL（例如：http://localhost:4000/feeds/MP_WXS_123.json）

### 4.3 同步文章

1. 在公众号列表中，点击"同步"按钮
2. 系统会自动从 wewe-rss 获取文章
3. 等待同步完成（首次同步可能需要几分钟）

### 4.4 查看文章

1. 点击"文章列表"
2. 浏览文章列表
3. 点击文章标题查看详情
4. 点击"收藏"按钮收藏文章

### 4.5 AI 分析

1. 在文章详情页，点击"AI 分析"按钮
2. 系统会自动：
   - 生成文章摘要
   - 提取关键词
   - 自动分类
   - 提取结构化信息（论文/工具/资讯）
3. 分析结果会显示在文章下方

### 4.6 知识库

1. 点击"知识库"
2. 查看 AI 提取的结构化知识
3. 按类型筛选（论文/工具/资讯）
4. 搜索知识条目

## 第五步：日常使用

### 5.1 自动同步

系统默认每小时自动同步一次文章。你也可以手动触发同步。

### 5.2 批量分析

```bash
# 分析所有未分析的文章
curl -X POST http://localhost:8000/api/articles/batch-analyze
```

### 5.3 数据备份

```bash
# 备份数据库
docker exec wechat-articles-db pg_dump -U admin wechat_articles > backup.sql

# 恢复数据库
docker exec -i wechat-articles-db psql -U admin wechat_articles < backup.sql
```

## 常见问题

### Q1: Docker 启动失败

**A:** 检查端口是否被占用：
```bash
# Windows
netstat -ano | findstr "8000"
netstat -ano | findstr "4000"

# macOS/Linux
lsof -i :8000
lsof -i :4000
```

如果端口被占用，修改 docker-compose.yml 中的端口映射。

### Q2: wewe-rss 账号被封

**A:** 这是正常现象，等待 24 小时后会自动解封。建议：
- 不要频繁添加公众号
- 使用多个微信读书账号轮换
- 降低同步频率

### Q3: AI 分析失败

**A:** 检查：
1. OpenAI API Key 是否正确
2. API 余额是否充足
3. 网络是否能访问 OpenAI API

### Q4: 文章内容为空

**A:** 可能原因：
1. wewe-rss 未正确获取内容
2. 公众号文章已被删除
3. 需要等待 wewe-rss 更新

### Q5: 前端无法访问后端

**A:** 检查：
1. 后端服务是否正常运行：`docker logs wechat-articles-backend`
2. 网络配置是否正确
3. CORS 配置是否正确

## 下一步

- 阅读 [API 文档](http://localhost:8000/docs)
- 查看 [完整文档](./DEPLOYMENT.md)
- 了解 [开发指南](./DEVELOPMENT.md)

## 获取帮助

- 提交 Issue: https://github.com/j-lab-10404/wechat-articles/issues
- 发送邮件: liujie@njfu.edu.cn

祝你使用愉快！🎉
