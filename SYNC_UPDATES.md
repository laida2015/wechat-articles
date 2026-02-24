# 如何同步原仓库的更新

如果你通过 Vercel 一键部署按钮 clone 了仓库，这个文档教你如何获取原仓库的更新。

## 🎯 推荐方案

### 方案 1：直接连接原仓库（最简单）⭐⭐⭐⭐⭐

**优点：** 自动获取所有更新，无需手动同步

**步骤：**

1. **删除当前的 Vercel 项目和 clone 的仓库**
   - Vercel Dashboard → 你的项目 → Settings → Delete Project
   - GitHub → 你的 clone 仓库 → Settings → Delete repository

2. **重新从原仓库部署**
   - 访问 https://vercel.com/new
   - 点击 "Import Git Repository"
   - 选择原仓库：`j-lab-10404/wechat-articles`
   - 配置：
     ```
     Root Directory: frontend
     Framework: Vite
     Build Command: npm run build
     Output Directory: dist
     ```
   - 点击 Deploy

3. **完成！**
   - 现在所有更新都会自动部署
   - 无需任何手动操作

---

### 方案 2：手动同步更新

**优点：** 保留你的仓库，可以自定义修改

**一次性设置：**

```bash
# 1. Clone 你的仓库到本地
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名

# 2. 添加原仓库作为上游
git remote add upstream https://github.com/j-lab-10404/wechat-articles.git

# 3. 验证
git remote -v
# 应该看到：
# origin    https://github.com/你的用户名/你的仓库名.git (fetch)
# origin    https://github.com/你的用户名/你的仓库名.git (push)
# upstream  https://github.com/j-lab-10404/wechat-articles.git (fetch)
# upstream  https://github.com/j-lab-10404/wechat-articles.git (push)
```

**每次同步更新：**

```bash
# 1. 获取上游更新
git fetch upstream

# 2. 切换到主分支
git checkout main

# 3. 合并更新
git merge upstream/main

# 4. 推送到你的仓库
git push origin main
```

Vercel 会自动检测到推送并重新部署。

---

### 方案 3：Fork 原仓库

**优点：** GitHub 原生支持，一键同步

**步骤：**

1. **Fork 原仓库**
   - 访问 https://github.com/j-lab-10404/wechat-articles
   - 点击右上角 "Fork" 按钮
   - Fork 到你的账号

2. **删除旧的 clone 仓库**
   - GitHub → 你的 clone 仓库 → Settings → Delete

3. **更新 Vercel 连接**
   - Vercel Dashboard → 你的项目 → Settings → Git
   - 重新连接到 Fork 的仓库

4. **同步更新**
   - 当原仓库有更新时
   - GitHub 会提示 "This branch is X commits behind"
   - 点击 "Sync fork" → "Update branch"
   - Vercel 自动重新部署

---

### 方案 4：自动同步（GitHub Actions）

**优点：** 完全自动化，每天自动检查更新

**设置步骤：**

1. **复制 GitHub Actions 工作流**
   - 在你的仓库中创建文件：`.github/workflows/sync-fork.yml`
   - 内容见下方

2. **启用 Actions**
   - GitHub → 你的仓库 → Actions
   - 启用 GitHub Actions

3. **完成！**
   - 每天自动检查并同步更新
   - 也可以手动触发：Actions → Sync Fork → Run workflow

**工作流文件内容：**

```yaml
name: Sync Fork with Upstream

on:
  schedule:
    - cron: '0 0 * * *'  # 每天 UTC 0:00
  workflow_dispatch:      # 允许手动触发

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
          
      - name: Sync with upstream
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git remote add upstream https://github.com/j-lab-10404/wechat-articles.git || true
          git fetch upstream
          git merge upstream/main --no-edit || echo "Already up to date"
          git push origin main
```

---

## 🔍 检查是否有更新

### 方法 1：GitHub 网页

访问你的仓库，如果有更新会显示：
```
This branch is X commits behind j-lab-10404:main
```

### 方法 2：命令行

```bash
git fetch upstream
git log HEAD..upstream/main --oneline
```

如果有输出，说明有新的提交。

---

## 📝 同步时的注意事项

### 如果你修改了代码

如果你在 clone 的仓库中做了自定义修改：

```bash
# 1. 先提交你的修改
git add .
git commit -m "My custom changes"

# 2. 获取上游更新
git fetch upstream

# 3. 变基（保持历史清晰）
git rebase upstream/main

# 4. 推送（可能需要强制推送）
git push origin main --force-with-lease
```

### 如果遇到冲突

```bash
# 1. 查看冲突文件
git status

# 2. 手动解决冲突
# 编辑冲突文件，删除冲突标记

# 3. 标记为已解决
git add 冲突文件

# 4. 继续合并
git merge --continue

# 5. 推送
git push origin main
```

---

## 🎯 我的建议

**如果你不需要修改代码：**
→ 使用**方案 1**（直接连接原仓库）

**如果你想保留自己的副本：**
→ 使用**方案 3**（Fork）+ **方案 4**（自动同步）

**如果你需要自定义修改：**
→ 使用**方案 2**（手动同步）

---

## 🆘 需要帮助？

- 查看原仓库更新：https://github.com/j-lab-10404/wechat-articles/commits/main
- 提交 Issue：https://github.com/j-lab-10404/wechat-articles/issues
- 发送邮件：liujie@njfu.edu.cn
