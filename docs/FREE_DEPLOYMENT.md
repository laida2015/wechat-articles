# 免费云端部署方案

本文档介绍如何将项目免费部署到云端，无需任何费用。

## 🎯 推荐方案组合

### 方案 1：Railway（最推荐，最简单）⭐⭐⭐⭐⭐

**优点：**
- 完全免费（每月 $5 额度，足够小项目使用）
- 支持 Docker + PostgreSQL + Redis
- 自动从 GitHub 部署
- 提供免费域名
- 配置简单

**限制：**
- 每月 500 小时运行时间
- 需要绑定信用卡（但不会扣费）

### 方案 2：Render + Vercel（分离部署）⭐⭐⭐⭐

**优点：**
- 完全免费，无需信用卡
- Render 部署后端 + 数据库
- Vercel 部署前端
- 自动 HTTPS

**限制：**
- Render 免费版会休眠（15分钟无访问）
- PostgreSQL 免费版 90 天后删除

### 方案 3：Fly.io（适合技术用户）⭐⭐⭐⭐

**优点：**
- 免费额度充足
- 支持 Docker
- 全球边缘部署
- 性能好

**限制：**
- 需要信用卡验证
- 配置稍复杂

## 📋 详细部署指南

---

## 方案 1：Railway 一键部署（推荐）

### 步骤 1：准备工作

1. 注册 Railway 账号：https://railway.app/
2. 连接 GitHub 账号
3. 绑定信用卡（不会扣费，仅验证）

### 步骤 2：创建项目配置文件

在项目根目录创建 `railway.json`：

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "docker/backend.Dockerfile"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 步骤 3：修改 Docker 配置

创建 `railway.dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Railway uses PORT environment variable
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 步骤 4：部署到 Railway

1. **访问 Railway Dashboard**
   - 进入 https://railway.app/dashboard
   - 点击 "New Project"

2. **选择部署方式**
   - 选择 "Deploy from GitHub repo"
   - 选择 `wechat-articles` 仓库

3. **添加数据库**
   - 点击 "+ New"
   - 选择 "Database" → "PostgreSQL"
   - Railway 会自动创建数据库

4. **添加 Redis**
   - 点击 "+ New"
   - 选择 "Database" → "Redis"

5. **配置环境变量**
   
   在后端服务中添加环境变量：
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   REDIS_URL=${{Redis.REDIS_URL}}
   OPENAI_API_KEY=your-openai-key
   SECRET_KEY=your-secret-key
   WEWE_RSS_URL=https://your-wewe-rss-url
   PORT=8000
   ```

6. **部署前端**
   - 点击 "+ New"
   - 选择 "Empty Service"
   - 设置构建命令：
     ```
     cd frontend && npm install && npm run build
     ```
   - 设置启动命令：
     ```
     npx serve -s frontend/dist -l $PORT
     ```

7. **获取域名**
   - Railway 会自动分配域名
   - 格式：`your-app.up.railway.app`

### 步骤 5：部署 wewe-rss

由于 wewe-rss 需要微信读书登录，建议：

**选项 A：本地运行 wewe-rss**
- 在本地运行 wewe-rss
- 使用 ngrok 或 Cloudflare Tunnel 暴露到公网

**选项 B：使用公共 wewe-rss 实例**
- 寻找公共的 wewe-rss 服务
- 或者部署到其他支持持久化的平台

---

## 方案 2：Render + Vercel 分离部署

### A. 后端部署到 Render

#### 步骤 1：创建 render.yaml

```yaml
services:
  # Backend API
  - type: web
    name: wechat-articles-backend
    env: docker
    dockerfilePath: ./docker/backend.Dockerfile
    dockerContext: ./backend
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: wechat-articles-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          name: wechat-articles-redis
          type: redis
          property: connectionString
      - key: OPENAI_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.11

databases:
  - name: wechat-articles-db
    databaseName: wechat_articles
    user: admin
    plan: free

  - name: wechat-articles-redis
    plan: free
```

#### 步骤 2：部署到 Render

1. 访问 https://render.com/
2. 注册并连接 GitHub
3. 点击 "New" → "Blueprint"
4. 选择 `wechat-articles` 仓库
5. Render 会自动读取 `render.yaml` 并部署

#### 步骤 3：配置环境变量

在 Render Dashboard 中设置：
- `OPENAI_API_KEY`: 你的 OpenAI Key
- `WEWE_RSS_URL`: wewe-rss 地址

### B. 前端部署到 Vercel

#### 步骤 1：创建 vercel.json

```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend.onrender.com/api/:path*"
    }
  ]
}
```

#### 步骤 2：部署到 Vercel

1. 访问 https://vercel.com/
2. 使用 GitHub 登录
3. 点击 "Add New" → "Project"
4. 选择 `wechat-articles` 仓库
5. 配置：
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. 点击 "Deploy"

#### 步骤 3：配置环境变量

在 Vercel 项目设置中添加：
```
VITE_API_BASE_URL=https://your-backend.onrender.com
```

---

## 方案 3：Fly.io 部署

### 步骤 1：安装 Fly CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# macOS/Linux
curl -L https://fly.io/install.sh | sh
```

### 步骤 2：登录 Fly.io

```bash
fly auth login
```

### 步骤 3：创建 fly.toml

```toml
app = "wechat-articles"
primary_region = "hkg"  # 香港节点

[build]
  dockerfile = "docker/backend.Dockerfile"

[env]
  PORT = "8000"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[services]]
  protocol = "tcp"
  internal_port = 8000

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

### 步骤 4：创建 PostgreSQL

```bash
fly postgres create --name wechat-articles-db --region hkg
fly postgres attach wechat-articles-db
```

### 步骤 5：设置环境变量

```bash
fly secrets set OPENAI_API_KEY=your-key
fly secrets set SECRET_KEY=your-secret
```

### 步骤 6：部署

```bash
fly deploy
```

---

## 🆓 完全免费的最简方案

如果你想要最简单、完全免费（不需要信用卡）的方案：

### 前端：GitHub Pages + Vercel

**GitHub Pages（静态托管）：**
```bash
# 构建前端
cd frontend
npm install
npm run build

# 部署到 GitHub Pages
# 在 GitHub 仓库设置中启用 GitHub Pages
# 选择 gh-pages 分支
```

**Vercel（推荐）：**
- 无需信用卡
- 自动 HTTPS
- 全球 CDN
- 自动从 GitHub 部署

### 后端：Render 免费版

- 无需信用卡
- 自动 HTTPS
- 包含 PostgreSQL
- 缺点：15分钟无访问会休眠

### 数据库：多个免费选项

1. **Neon（推荐）**
   - https://neon.tech/
   - 免费 PostgreSQL
   - 无需信用卡
   - 3GB 存储

2. **Supabase**
   - https://supabase.com/
   - 免费 PostgreSQL
   - 500MB 存储

3. **ElephantSQL**
   - https://www.elephantsql.com/
   - 免费 20MB PostgreSQL

---

## 📝 推荐配置

### 最佳免费方案（无需信用卡）

```
前端：Vercel
后端：Render
数据库：Neon
Redis：Upstash（免费）
```

### 部署步骤：

1. **Neon 数据库**
   ```
   1. 注册 https://neon.tech/
   2. 创建项目
   3. 复制连接字符串
   ```

2. **Upstash Redis**
   ```
   1. 注册 https://upstash.com/
   2. 创建 Redis 数据库
   3. 复制连接字符串
   ```

3. **Render 后端**
   ```
   1. 连接 GitHub
   2. 选择仓库
   3. 设置环境变量
   4. 部署
   ```

4. **Vercel 前端**
   ```
   1. 连接 GitHub
   2. 选择仓库
   3. 配置构建设置
   4. 部署
   ```

---

## 🔧 配置文件

我会为你创建所有需要的配置文件，让部署变得简单！

### 需要添加的文件：

1. `railway.json` - Railway 配置
2. `render.yaml` - Render 配置
3. `vercel.json` - Vercel 配置
4. `fly.toml` - Fly.io 配置
5. `railway.dockerfile` - Railway 专用 Dockerfile

---

## 💰 费用对比

| 平台 | 免费额度 | 需要信用卡 | 限制 |
|------|---------|-----------|------|
| Railway | $5/月 | 是 | 500小时/月 |
| Render | 750小时/月 | 否 | 会休眠 |
| Vercel | 无限 | 否 | 仅前端 |
| Fly.io | 充足 | 是 | 配置复杂 |
| Neon | 3GB | 否 | 数据库 |
| Upstash | 10K请求/天 | 否 | Redis |

---

## 🎯 我的建议

**如果你有信用卡（不会扣费）：**
→ 使用 **Railway**，最简单，一键部署

**如果没有信用卡：**
→ 使用 **Render（后端）+ Vercel（前端）+ Neon（数据库）**

**如果追求性能：**
→ 使用 **Fly.io**

---

## 下一步

我可以帮你：
1. 创建所有部署配置文件
2. 修改代码以适配云端部署
3. 编写详细的部署教程

你想用哪个方案？我立即帮你配置！
