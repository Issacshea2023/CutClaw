# CutClaw API 部署到 Railway/Render/Vercel

## 快速部署（推荐 Railway）

### 步骤 1: 创建 GitHub 仓库

1. 打开 https://github.com/new
2. 仓库名称: `cutclaw-api`
3. 选择 **Public**
4. 点击 **Create repository** （不要勾选 README）
5. 复制仓库 URL（如 `https://github.com/Issacshea2023/cutclaw-api.git`）

### 步骤 2: 初始化本地仓库

在 CutClaw 目录执行：

```bash
cd C:/Users/梁丽娟/CutClaw

# 添加新的远程仓库
git remote add deploy https://github.com/Issacshea2023/cutclaw-api.git

# 创建分支
git checkout -b api

# 添加 API 文件
git add cutclaw_api.py requirements_api.txt railway.json

# 提交
git commit -m "Add API server"

# 推送到 GitHub
git push -u deploy api
```

### 步骤 3: 部署到 Railway

1. 打开 https://railway.app/
2. 用 GitHub 登录
3. 点击 **New Project** → **Deploy from GitHub repo**
4. 选择 `cutclaw-api` 仓库
5. Railway 会自动检测 `railway.json` 配置
6. 点击 **Deploy**

### 步骤 4: 获取 API 地址

部署完成后，在 Railway 面板找到分配的域名，如：
`https://cutclaw-api-xxxx.railway.app`

---

## 测试 API

```bash
# 健康检查
curl https://your-railway-domain.railway.app/health

# 处理视频
curl -X POST https://your-railway-domain.railway.app/process \
  -F "video=@video.mp4" \
  -F "instruction=保留对话"
```

---

## 本地运行

```bash
cd C:/Users/梁丽娟/CutClaw
pip install -r requirements_api.txt
uvicorn cutclaw_api:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档# Trigger redeploy
