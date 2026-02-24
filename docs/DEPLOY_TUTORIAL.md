# 免费云端部署教程（手把手）

本教程将手把手教你如何将项目免费部署到云端，完全不需要花钱！

## 🎯 我们要做什么

将项目部署到：
- **前端**：Vercel（免费，无需信用卡）
- **后端**：Render（免费，无需信用卡）
- **数据库**：Neon（免费，无需信用卡）
- **Redis**：Upstash（免费，无需信用卡）

总费用：**0 元** ✨

---

## 📋 准备工作

### 1. 注册账号

你需要注册以下账号（都是免费的）：

- [ ] GitHub 账号（你已经有了）
- [ ] Vercel 账号：https://vercel.com/signup
- [ ] Render 账号：https://render.com/register
- [ ] Neon 账号：https://neon.tech/
- [ ] Upstash 账号：https://upstash.com/

**提示：** 所有平台都支持用 GitHub 账号直接登录，非常方便！

### 2. 获取 OpenAI API Key

1. 访问：https://platform.openai.com/api-keys
2. 登录你的 OpenAI 账号
3. 点击 "Create new secret key"
4. 复制并保存 API Key（只显示一次！）

---

## 第一步：部署数据库（Neon）

### 1. 创建 PostgreSQL 数据库

1. 访问 https://neon.tech/ 并登录
2. 点击 "Create a project"
3. 填写信息：
   - Project name: `wechat-articles`
   - Region: 选择 `Asia Pacific (Singapore)` 或 `US East`
4. 点击 "Create project"

### 2. 获取数据库连接字符串

1. 在项目页面，找到 "Connection string"
2. 复制连接字符串，格式类似：
   ```
   postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```
3. 保存这个字符串，后面会用到

---

## 第二步：部署 Redis（Upstash）

### 1. 创建 Redis 数据库

1. 访问 https://upstash.com/ 并登录
2. 点击 "Create Database"
3. 填写信息：
   - Name: `wechat-articles-redis`
   - Type: `Regional`
   - Region: 选择离你最近的区域
4. 点击 "Create"

### 2. 获取 Redis 连接字符串

1. 在数据库详情页面
2. 找到 "REST API" 部分
3. 复制 "UPSTASH_REDIS_REST_URL"
4. 保存这个 URL

---

## 第三步：部署后端（Render）

### 1. 连接 GitHub

1. 访问 https://render.com/ 并登录
2. 点击 "New +" → "Web Service"
3. 选择 "Connect a repository"
4. 授权 Render 访问你的 GitHub
5. 选择 `wechat-articles` 仓库

### 2. 配置服务

填写以下信息：

- **Name**: `wechat-articles-backend`
- **Region**: 选择 `Singapore` 或 `Oregon`
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Docker`
- **Dockerfile Path**: `../docker/backend.Dockerfile`
- **Instance Type**: `Free`

### 3. 添加环境变量

点击 "Advanced" → "Add Environment Variable"，添加以下变量：

```
DATABASE_URL = postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
（使用第一步获取的 Neon 连接字符串）

REDIS_URL = https://your-redis-url.upstash.io
（使用第二步获取的 Upstash URL）

OPENAI_API_KEY = sk-your-openai-api-key
（你的 OpenAI API Key）

SECRET_KEY = 随机生成一个长字符串
（可以用这个生成：https://randomkeygen.com/）

WEWE_RSS_URL = http://localhost:4000
（暂时先这样，后面再配置）

CORS_ORIGINS = https://your-app.vercel.app
（等前端部署后再修改）

DEBUG = False
```

### 4. 部署

1. 点击 "Create Web Service"
2. 等待部署完成（约 5-10 分钟）
3. 部署成功后，你会得到一个 URL，类似：
   ```
   https://wechat-articles-backend.onrender.com
   ```
4. 保存这个 URL

### 5. 初始化数据库

部署成功后，需要初始化数据库表：

1. 在 Render Dashboard 中，找到你的服务
2. 点击 "Shell" 标签
3. 运行以下命令：
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```

---

## 第四步：部署前端（Vercel）

### 1. 连接 GitHub

1. 访问 https://vercel.com/ 并登录
2. 点击 "Add New..." → "Project"
3. 选择 `wechat-articles` 仓库
4. 点击 "Import"

### 2. 配置项目

填写以下信息：

- **Framework Preset**: `Vite`
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

### 3. 添加环境变量

点击 "Environment Variables"，添加：

```
VITE_API_BASE_URL = https://wechat-articles-backend.onrender.com
（使用第三步获取的 Render URL）
```

### 4. 部署

1. 点击 "Deploy"
2. 等待部署完成（约 2-3 分钟）
3. 部署成功后，你会得到一个 URL，类似：
   ```
   https://wechat-articles.vercel.app
   ```

### 5. 更新后端 CORS 配置

1. 回到 Render Dashboard
2. 找到后端服务
3. 进入 "Environment" 标签
4. 修改 `CORS_ORIGINS` 为你的 Vercel URL：
   ```
   CORS_ORIGINS = https://wechat-articles.vercel.app
   ```
5. 保存并重新部署

---

## 第五步：配置 wewe-rss

由于 wewe-rss 需要微信读书登录，有两个选择：

### 选项 A：本地运行（推荐）

1. 在本地运行 wewe-rss：
   ```bash
   cd docker
   docker-compose up wewe-rss
   ```

2. 使用 Cloudflare Tunnel 暴露到公网：
   ```bash
   # 安装 cloudflared
   # Windows: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
   
   # 创建隧道
   cloudflared tunnel --url http://localhost:4000
   ```

3. 复制生成的公网 URL，更新后端环境变量

### 选项 B：使用公共实例

寻找公共的 wewe-rss 服务（不推荐，不稳定）

---

## 第六步：测试部署

### 1. 访问前端

打开你的 Vercel URL：`https://wechat-articles.vercel.app`

### 2. 测试 API

访问：`https://wechat-articles-backend.onrender.com/docs`

你应该能看到 API 文档页面。

### 3. 添加公众号

1. 在前端点击"公众号管理"
2. 添加一个公众号
3. 尝试同步文章

---

## 🎉 完成！

恭喜！你的应用已经成功部署到云端了！

### 你的应用地址：

- **前端**: https://wechat-articles.vercel.app
- **后端**: https://wechat-articles-backend.onrender.com
- **API 文档**: https://wechat-articles-backend.onrender.com/docs

### 下一步：

1. 配置 wewe-rss
2. 添加公众号订阅
3. 开始使用！

---

## 🔧 常见问题

### Q1: Render 后端休眠了怎么办？

**A:** Render 免费版 15 分钟无访问会休眠。解决方案：

1. 使用 UptimeRobot 定时 ping：https://uptimerobot.com/
2. 设置每 10 分钟访问一次你的后端 URL
3. 这样后端就不会休眠了

### Q2: 数据库连接失败

**A:** 检查：
1. DATABASE_URL 是否正确
2. Neon 数据库是否在运行
3. 是否添加了 `?sslmode=require`

### Q3: CORS 错误

**A:** 确保：
1. 后端 CORS_ORIGINS 包含前端 URL
2. 前端 API_BASE_URL 正确
3. 重新部署后端

### Q4: OpenAI API 调用失败

**A:** 检查：
1. API Key 是否正确
2. API 余额是否充足
3. 网络是否能访问 OpenAI

### Q5: 前端无法连接后端

**A:** 
1. 检查 vercel.json 中的 rewrites 配置
2. 确保后端 URL 正确
3. 查看浏览器控制台错误信息

---

## 📊 免费额度说明

| 服务 | 免费额度 | 限制 |
|------|---------|------|
| Vercel | 无限部署 | 100GB 带宽/月 |
| Render | 750 小时/月 | 会休眠 |
| Neon | 3GB 存储 | 1 个项目 |
| Upstash | 10K 请求/天 | 256MB 内存 |

对于个人使用，这些额度完全够用！

---

## 🆘 需要帮助？

- 查看日志：在 Render/Vercel Dashboard 中查看
- 提交 Issue：https://github.com/j-lab-10404/wechat-articles/issues
- 发送邮件：liujie@njfu.edu.cn

---

## 🎁 额外提示

### 自定义域名

**Vercel（前端）：**
1. 在 Vercel 项目设置中
2. 点击 "Domains"
3. 添加你的域名
4. 按照提示配置 DNS

**Render（后端）：**
1. 在 Render 服务设置中
2. 点击 "Custom Domain"
3. 添加你的域名
4. 配置 DNS

### 监控和告警

使用 UptimeRobot 监控你的应用：
1. 注册 https://uptimerobot.com/
2. 添加监控
3. 设置邮件告警

### 备份数据

定期备份 Neon 数据库：
1. 在 Neon Dashboard 中
2. 点击 "Backups"
3. 创建手动备份

---

祝你部署顺利！🚀
