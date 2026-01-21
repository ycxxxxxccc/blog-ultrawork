# PR-Agent 部署指南

## 📋 概述

本文档说明如何在GitHub上部署pr-agent代码审查工具，使用智谱AI作为LLM提供商。

## ✅ 已完成配置

- ✅ GitHub Actions工作流已配置
- ✅ 智谱AI模型集成（glm-4.5-flash 免费）
- ✅ 自动代码审查功能已启用
- ✅ 本地git仓库已初始化

## 🚀 剩余部署步骤

### 步骤1：创建GitHub仓库

1. 访问：https://github.com/new
2. 配置参数：
   - **Repository name**: `blog-ultrawork`
   - **Visibility**: Public 或 Private（建议Public测试）
   - **不要勾选** "Add a README file"
3. 点击 "Create repository"

### 步骤2：推送代码

创建仓库后，在本地终端运行：

```bash
# 切换到项目目录
cd C:\Users\miemie\Desktop\blog-ultrawork

# 添加远程仓库
git remote add origin https://github.com/ycxxxxxccc/blog-ultrawork.git

# 推送代码
git push -u origin master
```

### 步骤3：配置GitHub Secrets

1. 访问：https://github.com/ycxxxxxccc/blog-ultrawork/settings/secrets/actions
2. 点击 "New repository secret"
3. 添加以下Secret：

| Name          | Value                                               | 说明           |
| ------------- | --------------------------------------------------- | -------------- |
| `ZAI_API_KEY` | `52d6d1a828c248ae8f0480906e5218cc.9rrqqsJkD8KYiSOI` | 智谱AI API Key |

4. 点击 "Add secret"

### 步骤4：测试pr-agent

创建测试PR来验证pr-agent是否正常工作：

```bash
# 创建测试分支
git checkout -b test-pr-agent

# 修改README.md添加测试内容
echo "
## PR-Agent 测试

此PR用于测试PR-Agent代码审查功能。
" >> README.md

# 提交更改
git add README.md
git commit -m "Test: Add PR-Agent test section"

# 推送分支
git push -u origin test-pr-agent
```

然后在GitHub上：

1. 访问：https://github.com/ycxxxxxccc/blog-ultrawork
2. 点击 "Compare & pull request"
3. 创建Pull Request
4. 等待GitHub Actions自动运行
5. pr-agent会在PR评论中自动添加代码审查意见

## 📊 验证清单

部署成功后，你应该看到：

- [ ] 代码已推送到GitHub
- [ ] `ZAI_API_KEY` Secret已配置
- [ ] Pull Request创建后，GitHub Actions自动运行
- [ ] pr-agent在PR中添加评论：
  - 📝 `/review` - 代码审查
  - 📋 `/describe` - PR描述
- [ ] Action日志显示使用 `zai/glm-4.5-flash` 模型

## 🔧 配置说明

### 已配置的功能

1. **自动触发审查**
   - PR打开时自动运行 `/review`
   - PR打开时自动运行 `/describe`

2. **手动触发改进**
   - 在PR评论中输入 `/improve` 手动触发代码改进建议

3. **使用的模型**
   - 主模型：`zai/glm-4.5-flash`（免费）
   - 备用模型：`zai/glm-4.5`

### 工作流文件位置

`.github/workflows/pr-agent-review.yml`

### 可用的pr-agent命令

| 命令                | 触发方式 | 说明             |
| ------------------- | -------- | ---------------- |
| `/review`           | 自动     | 对PR进行代码审查 |
| `/describe`         | 自动     | 生成PR描述摘要   |
| `/improve`          | 手动评论 | 提供代码改进建议 |
| `/ask "问题"`       | 手动评论 | 询问关于PR的问题 |
| `/update_changelog` | 手动评论 | 更新CHANGELOG.md |
| `/config`           | 手动评论 | 查看当前配置     |

## 📈 成本估算

使用智谱AI `glm-4.5-flash` 免费模型：

| 场景           | 费用 |
| -------------- | ---- |
| 每次PR审查     | FREE |
| 每次代码改进   | FREE |
| 每月10次PR审查 | FREE |

## 🐛 故障排查

### 问题1：Action失败，提示 "ZAI_API_KEY not found"

**解决方法**：

- 检查Secret名称是否正确（必须大写：`ZAI_API_KEY`）
- 确保Secret值没有多余空格

### 问题2：pr-agent没有添加评论

**解决方法**：

- 检查PR是否触发了Action
- 查看 "Actions" 标签页查看运行日志
- 确认 `GITHUB_TOKEN` 权限设置正确（workflow中已配置）

### 问题3：智谱AI API调用失败

**解决方法**：

- 验证API Key是否有效
- 检查智谱AI账户状态
- 查看Action日志中的具体错误信息

## 🎯 下一步：GitLab部署

GitHub部署验证通过后，可以按照类似方式部署到GitLab：

1. 创建 `.gitlab-ci.yml` 文件
2. 配置GitLab CI Variables（`ZAI_API_KEY`）
3. 使用 `codiumai/pr-agent:latest` Docker镜像

## 📚 参考资源

- [PR-Agent官方文档](https://qodo-merge-docs.qodo.ai/)
- [智谱AI API文档](https://open.bigmodel.cn/dev/api)
- [LiteLLM Z.AI支持](https://docs.litellm.ai/docs/providers/zai)

---

**部署日期**: 2026-01-21
**配置版本**: PR-Agent v0.31
**LLM提供商**: 智谱AI (Z.AI)
