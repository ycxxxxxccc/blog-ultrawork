# 🚀 快速开始指南

## 一键部署到GitHub

### 方法1：使用自动化脚本（推荐）

```bash
# 双击运行
deploy_pr_agent.bat
```

按照脚本提示完成以下步骤：

1. 配置远程仓库
2. 推送代码
3. 配置GitHub Secrets
4. 创建测试PR

### 方法2：手动部署

```bash
# 1. 在GitHub创建仓库: https://github.com/new
# 仓库名: blog-ultrawork

# 2. 添加远程仓库
git remote add origin https://github.com/ycxxxxxccc/blog-ultrawork.git

# 3. 推送代码
git push -u origin master

# 4. 配置Secret
# 访问: https://github.com/ycxxxxxccc/blog-ultrawork/settings/secrets/actions
# 添加:
#   Name: ZAI_API_KEY
#   Value: 52d6d1a828c248ae8f0480906e5218cc.9rrqqsJkD8KYiSOI

# 5. 创建测试PR
git checkout -b test-pr-agent
echo "## Test PR" >> README.md
git add README.md
git commit -m "Test PR"
git push -u origin test-pr-agent
```

### 验证部署

创建PR后，访问：

- https://github.com/ycxxxxxccc/blog-ultrawork/pulls

你应该看到pr-agent自动添加的评论！

## 使用pr-agent

### 自动触发（已配置）

- ✅ PR打开时自动审查
- ✅ PR打开时自动描述

### 手动触发

在PR评论区输入：

- `/improve` - 获取代码改进建议
- `/ask "你的问题"` - 询问关于PR的问题
- `/update_changelog` - 更新CHANGELOG

## GitLab部署

将 `gitlab-ci.yml.template` 重命名为 `.gitlab-ci.yml` 并推送到GitLab

## 📚 详细文档

查看 `PR_AGENT_DEPLOYMENT.md` 获取完整配置说明
