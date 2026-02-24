# 🚀 后端快速部署指南（10分钟）

前端已经部署好了，现在部署后端！

## 📋 需要准备的

1. ✅ GitHub 账号（已有）
2. ⏳ Render 账号（免费，无需信用卡）
3. ⏳ Neon 账号（免费数据库）
4. ⏳ Upstash 账号（免费 Redis，可选）
5. ⏳ AI API Key（推荐 DeepSeek，便宜）

---

## 第一步：获取 AI API Key（5分钟）

### 推荐：DeepSeek（最便宜）⭐⭐⭐⭐⭐

**为什么选 DeepSeek？**
- 💰 价格：比 OpenAI 便宜 90%
- 🚀 速度：快
- 🇨🇳 国内可用
- ✅ 完全兼容 OpenAI API

**获取步骤：**

1. **注册账号**
   - 访问：https://platform.deepseek.com/
   - 用手机号注册

2. **充值**
   - 最低充值 10 元
   - 可以用很久（比 OpenAI 便宜很多）

3. **创建 API Key**
   - 进入 API Keys 页面
   - 点击 "创建新密钥"
   - 复制并保存 API Key

4. **记录信息**
   ```
   API Key: sk-xxxxx
   Base URL: https://api.deepseek.com/v1
   Model: deepseek-chat
   ```

### 其他选项：

**Groq（免费但国外）**
- 网址：https://groq.com/
- 完全免费
- 需要科学上网

**OpenAI（最贵）**
- 网址：https://platform.openai.com/
- 需要国外信用卡
- 价格最贵

---

## 第二步：创建数据库（3分钟）

### Neon PostgreSQL（免费）

1. **注册**
   - 访问：https://neon.tech/
   - 用 GitHub 登录

2. **创建项目**
   - 点击 "Create a project"
   - Project name: `wechat-articles`
   - Region: 选择 `Asia Pacific (Singapore)`
   - 点击 "Create project"

3. **获取连接字符串**
   - 复制 "Connection string"
   - 格式：`postgresql://user:pass@host/db?sslmode=require`
   - 保存这个字符串

---

## 第三步：创建 Redis（2分钟，可选）

### Upstash Redis（免费）

1. **注册**
   - 访问：https://upstash.com/
   - 用 GitHub 登录

2. **创建数据库**
   - 点击 "Create Database"
   - Name: `wechat-articles-redis`
   - Type: `Regional`
   - Region: 选择离你最近的
   - 点击 "Create"

3. **获取连接信息**
   - 复制 "UPSTASH_REDIS_REST_URL"
   - 保存这个 URL

---

## 第四步：部署后端到 Render（5分钟）

### 方法 1：一键部署（推荐）

1. **点击按钮**
   
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/j-lab-10404/wechat-articles)

2. **填写环境变量**
   
   ```
   DATABASE_URL = postgresql://user:pass@host/db?sslmode=require
   （使用第二步获取的 Neon 连接字符串）
   
   REDIS_URL = https://your-redis-url.upstash.io
   （使用第三步获取的 Upstash URL，可选）
   
   OPENAI_API_KEY = sk-xxxxx
   （使用第一步获取的 DeepSeek API Key）
   
   OPENAI_BASE_URL = https://api.deepseek.com/v1
   （如果用 DeepSeek）
   
   OPENAI_MODEL = deepseek-chat
   （如果用 DeepSeek）
   
   SECRET_KEY = 随机生成一个长字符串
   （访问 https://randomkeygen.com/ 生成）
   
   CORS_ORIGINS = https://your-app.vercel.app
   （你的 Vercel 前端地址）
   
   DEBUG = False
   ```

3. **部署**
   - 点击 "Apply"
   - 等待 5-10 分钟

### 方法 2：手动部署

1. **访问 Render**
   - https://render.com/
   - 用 GitHub 登录

2. **创建 Web Service**
   - 点击 "New +" → "Web Service"
   - 选择 `j-lab-10404/wechat-articles` 仓库

3. **配置服务**
   ```
   Name: wechat-articles-backend
   Region: Singapore
   Branch: main
   Root Directory: backend
   Runtime: Docker
   Dockerfile Path: ../docker/backend.Dockerfile
   Instance Type: Free
   ```

4. **添加环境变量**
   - 同上面的环境变量

5. **部署**
   - 点击 "Create Web Service"
   - 等待部署完成

---

## 第五步：初始化数据库（1分钟）

部署成功后：

1. **进入 Render Shell**
   - Render Dashboard → 你的服务
   - 点击 "Shell" 标签

2. **运行初始化命令**
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```

3. **验证**
   - 应该看到 "Database initialized successfully"

---

## 第六步：连接前后端（2分钟）

1. **获取后端 URL**
   - Render 部署成功后会给你一个 URL
   - 格式：`https://wechat-articles-backend.onrender.com`

2. **更新前端环境变量**
   - 进入 Vercel Dashboard
   - 你的项目 → Settings → Environment Variables
   - 添加：
     ```
     VITE_API_BASE_URL = https://wechat-articles-backend.onrender.com/api
     ```

3. **重新部署前端**
   - Deployments → 最新部署 → Redeploy

---

## 🎉 完成！

现在你的完整应用已经部署好了！

### 测试一下：

1. **访问前端**
   - https://your-app.vercel.app

2. **测试 API**
   - https://your-backend.onrender.com/docs
   - 应该能看到 API 文档

3. **测试功能**
   - 在前端添加公众号
   - 同步文章
   - AI 分析

---

## 💰 费用说明

| 服务 | 费用 | 说明 |
|------|------|------|
| Vercel | 免费 | 前端托管 |
| Render | 免费 | 后端托管（会休眠） |
| Neon | 免费 | 3GB 数据库 |
| Upstash | 免费 | 10K 请求/天 |
| DeepSeek | ~10元 | 可以用很久 |

**总计：约 10 元人民币**（只需要充值 AI API）

---

## 🔧 常见问题

### Q1: Render 后端休眠怎么办？

**A:** 使用 UptimeRobot 定时 ping
1. 注册 https://uptimerobot.com/
2. 添加监控，每 10 分钟 ping 一次
3. 后端就不会休眠了

### Q2: DeepSeek API 怎么配置？

**A:** 需要修改后端代码，添加环境变量：
```
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
```

### Q3: 如何查看后端日志？

**A:** Render Dashboard → 你的服务 → Logs

---

## 📚 相关文档

- [完整部署教程](docs/DEPLOY_TUTORIAL.md)
- [免费部署方案](docs/FREE_DEPLOYMENT.md)
- [API 文档](https://your-backend.onrender.com/docs)

---

需要帮助？
- 提交 Issue: https://github.com/j-lab-10404/wechat-articles/issues
- 发送邮件: liujie@njfu.edu.cn
