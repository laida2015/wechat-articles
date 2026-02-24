# Vercel 部署修复指南

如果你在 Vercel 部署时遇到 "No such file or directory" 错误，按照以下步骤修复：

## 问题原因

Vercel 默认在项目根目录构建，但我们的前端代码在 `frontend` 文件夹中。

## 解决方案

### 方法 1：在 Vercel Dashboard 中配置（推荐）

1. 进入你的 Vercel 项目
2. 点击 "Settings"
3. 找到 "Build & Development Settings"
4. 配置如下：
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```
5. 点击 "Save"
6. 重新部署：Deployments → 最新部署 → 三个点 → "Redeploy"

### 方法 2：重新导入项目

1. 删除当前项目
2. 重新点击部署按钮
3. 在配置页面**务必选择** Root Directory 为 `frontend`
4. 其他配置：
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

### 方法 3：使用 Vercel CLI

```bash
# 安装 Vercel CLI
npm i -g vercel

# 进入 frontend 目录
cd frontend

# 部署
vercel

# 生产部署
vercel --prod
```

## 验证配置

部署成功后，你应该看到：

```
✓ Building...
✓ Compiled successfully
✓ Uploading...
✓ Deployment ready
```

访问你的 Vercel URL，应该能看到应用首页。

## 常见错误

### 错误 1: "cd: frontend: No such file or directory"

**原因**: Root Directory 没有设置为 `frontend`

**解决**: 在 Vercel 项目设置中设置 Root Directory

### 错误 2: "Cannot find module 'vite'"

**原因**: 依赖没有正确安装

**解决**: 
1. 检查 `frontend/package.json` 是否存在
2. 确保 Install Command 是 `npm install`

### 错误 3: API 请求失败

**原因**: 环境变量没有配置

**解决**: 
1. 在 Vercel 项目设置中
2. 添加环境变量：
   ```
   VITE_API_BASE_URL = https://your-backend.onrender.com/api
   ```
3. 重新部署

## 完整的 Vercel 配置示例

在 Vercel Dashboard 中应该看到：

```
Root Directory: frontend
Framework: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm install

Environment Variables:
VITE_API_BASE_URL = https://your-backend.onrender.com/api
```

## 需要帮助？

如果还有问题：
1. 查看 Vercel 部署日志
2. 检查 `frontend` 目录是否存在
3. 确认 `frontend/package.json` 文件存在
4. 提交 Issue: https://github.com/j-lab-10404/wechat-articles/issues

---

**快速链接：**
- [完整部署教程](docs/DEPLOY_TUTORIAL.md)
- [5分钟快速部署](DEPLOY_NOW.md)
- [免费部署方案](docs/FREE_DEPLOYMENT.md)
