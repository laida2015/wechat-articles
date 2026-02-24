# 🚀 立即部署到云端（5分钟）

## 最简单的方式：Vercel + Render（完全免费，无需信用卡）

### 第一步：点击按钮部署前端

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/j-lab-10404/wechat-articles&root-directory=frontend&env=VITE_API_BASE_URL&envDescription=Backend%20API%20URL&project-name=wechat-articles&repository-name=wechat-articles)

1. 点击上面的按钮
2. 用 GitHub 登录 Vercel
3. 填写环境变量（先留空，后面再填）
4. 点击 "Deploy"
5. 等待部署完成，记下你的 URL

### 第二步：点击按钮部署后端

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/j-lab-10404/wechat-articles)

1. 点击上面的按钮
2. 用 GitHub 登录 Render
3. 填写环境变量：
   - `OPENAI_API_KEY`: 你的 OpenAI Key
   - `SECRET_KEY`: 随机字符串（[生成](https://randomkeygen.com/)）
   - 其他保持默认
4. 点击 "Apply"
5. 等待部署完成，记下你的 URL

### 第三步：配置数据库

#### Neon PostgreSQL（免费）

1. 访问 https://neon.tech/
2. 注册并创建项目
3. 复制连接字符串
4. 在 Render 后端服务中添加环境变量：
   ```
   DATABASE_URL = postgresql://...
   ```

#### Upstash Redis（免费）

1. 访问 https://upstash.com/
2. 注册并创建 Redis 数据库
3. 复制 REST URL
4. 在 Render 后端服务中添加环境变量：
   ```
   REDIS_URL = https://...
   ```

### 第四步：连接前后端

1. 回到 Vercel 项目设置
2. 添加环境变量：
   ```
   VITE_API_BASE_URL = https://your-backend.onrender.com/api
   ```
3. 重新部署

### 第五步：更新 CORS

1. 在 Render 后端服务中
2. 更新环境变量：
   ```
   CORS_ORIGINS = https://your-app.vercel.app
   ```
3. 重新部署

---

## 🎉 完成！

你的应用已经部署成功了！

- **前端**: https://your-app.vercel.app
- **后端**: https://your-backend.onrender.com
- **API 文档**: https://your-backend.onrender.com/docs

---

## 📖 详细教程

如果遇到问题，查看详细教程：
- [免费部署方案](docs/FREE_DEPLOYMENT.md)
- [手把手部署教程](docs/DEPLOY_TUTORIAL.md)

---

## 💡 其他部署选项

### Railway（推荐，需要信用卡但不扣费）

1. 访问 https://railway.app/
2. 连接 GitHub
3. 选择 `wechat-articles` 仓库
4. Railway 会自动检测配置并部署
5. 添加 PostgreSQL 和 Redis 服务
6. 配置环境变量

### Fly.io（适合技术用户）

```bash
# 安装 Fly CLI
curl -L https://fly.io/install.sh | sh

# 登录
fly auth login

# 部署
fly deploy

# 创建数据库
fly postgres create
fly postgres attach
```

---

## 🆘 需要帮助？

- 查看 [常见问题](docs/DEPLOY_TUTORIAL.md#常见问题)
- 提交 [Issue](https://github.com/j-lab-10404/wechat-articles/issues)
- 发送邮件：liujie@njfu.edu.cn

---

## 📊 费用说明

所有推荐的服务都是**完全免费**的：

| 服务 | 免费额度 | 够用吗？ |
|------|---------|---------|
| Vercel | 100GB 带宽/月 | ✅ 够用 |
| Render | 750 小时/月 | ✅ 够用 |
| Neon | 3GB 存储 | ✅ 够用 |
| Upstash | 10K 请求/天 | ✅ 够用 |

**总费用：0 元** 🎉

---

## 🎁 额外提示

### 防止 Render 休眠

Render 免费版 15 分钟无访问会休眠。解决方案：

1. 注册 https://uptimerobot.com/（免费）
2. 添加监控，每 10 分钟 ping 一次你的后端
3. 这样后端就永远不会休眠了

### 自定义域名

**Vercel：**
- 项目设置 → Domains → 添加域名
- 配置 DNS CNAME 记录

**Render：**
- 服务设置 → Custom Domain → 添加域名
- 配置 DNS CNAME 记录

---

祝你部署顺利！🚀
