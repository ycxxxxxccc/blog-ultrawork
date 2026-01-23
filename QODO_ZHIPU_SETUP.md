# PR-Agent 连接智谱AI 配置指南

## ✅ 配置完成

你的 PR-Agent 现在已配置为使用智谱AI的OpenAI兼容API。

## 🔧 配置说明

### 1. 配置文件结构

#### `.pr_agent.toml`（仓库配置文件）

```toml
[config]
model = "openai/glm-4-flash"
fallback_models = ["openai/glm-4-flash"]
custom_model_max_tokens = 4096
response_language = "zh-CN"

[openai]
api_base = "https://open.bigmodel.cn/api/paas/v4"
api_key = "your-zhipu-api-key"
api_type = "openai"
```

**关键点**：

- ✅ 模型名使用 `openai/` 前缀
- ✅ API Base指向智谱的通用端点
- ✅ API Key配置在 `[openai]` 部分

#### `.github/workflows/pr_agent.yml`（GitHub Actions配置）

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  OPENAI__API_BASE: https://open.bigmodel.cn/api/paas/v4
  OPENAI__KEY: ${{ secrets.ZHIPU_API_KEY }}
```

**关键点**：

- ✅ 使用**双下划线** `OPENAI__API_BASE`
- ✅ Secret名称为 `ZHIPU_API_KEY`

### 2. 端点选择

| 端点类型       | URL                                           | 使用场景             |
| -------------- | --------------------------------------------- | -------------------- |
| **通用端点**   | `https://open.bigmodel.cn/api/paas/v4`        | 通用对话、代码审查等 |
| **Coding端点** | `https://open.bigmodel.cn/api/coding/paas/v4` | 仅用于GLM编码套餐    |

**注意**：除非你购买了GLM编码套餐，否则使用通用端点即可。

## 🧪 本地测试（推荐）

### 步骤1：安装PR-Agent

```bash
# 克隆PR-Agent仓库
git clone https://github.com/qodo-ai/pr-agent.git
cd pr-agent

# 安装依赖
pip install -r requirements.txt

# 或者使用pip安装
pip install pr-agent
```

### 步骤2：使用测试配置

```bash
# 运行测试命令
pr-agent --config-file test-pr-agent-local.toml \
  --pr-url "https://github.com/your-repo/your-project/pull/1" \
  describe
```

### 步骤3：验证输出

如果配置正确，你应该看到：

- ✅ 成功连接到智谱AI
- ✅ 模型响应正常
- ✅ PR描述被正确生成

如果看到错误：

- ❌ "Model not found" - 检查模型名称格式（需要 `openai/` 前缀）
- ❌ "API key invalid" - 检查API Key是否正确
- ❌ "401 Unauthorized" - 检查API Base URL是否正确

## 🚀 GitHub Actions 测试

### 步骤1：添加Secret到GitHub

1. 访问你的GitHub仓库
2. 进入 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下Secret：

   | Name            | Value           |
   | --------------- | --------------- |
   | `ZHIPU_API_KEY` | 你的智谱API Key |

### 步骤2：验证配置

```bash
# 确认workflow文件正确
cat .github/workflows/pr_agent.yml

# 确认配置文件正确
cat .pr_agent.toml
```

### 步骤3：提交并推送

```bash
git add .pr_agent.toml .github/workflows/pr_agent.yml
git commit -m "Configure PR-Agent to use Zhipu AI"
git push origin main
```

### 步骤4：创建测试PR

```bash
# 创建测试分支
git checkout -b test-pr-agent

# 创建测试变更
echo "## Test PR for PR-Agent" >> README.md
git add README.md
git commit -m "Test: Verify PR-Agent configuration"

# 推送到GitHub
git push -u origin test-pr-agent
```

然后在GitHub上创建PR，PR-Agent将自动运行。

### 步骤5：查看运行结果

1. 在GitHub上打开你的PR
2. 查看 **Actions** 标签
3. 点击最新的 workflow run
4. 检查日志，确认：
   - ✅ 没有认证错误
   - ✅ 成功连接到智谱AI
   - ✅ 工具正常运行（review、describe等）

## 📋 验证清单

### 配置验证

- [ ] `.pr_agent.toml` 中模型名为 `openai/glm-4-flash`
- [ ] `[openai]` 部分配置了 `api_base`
- [ ] `[openai]` 部分配置了 `api_key`
- [ ] GitHub Secret `ZHIPU_API_KEY` 已添加
- [ ] `.github/workflows/pr_agent.yml` 中使用了正确的环境变量名

### 功能验证

- [ ] 本地测试成功（使用 `test-pr-agent-local.toml`）
- [ ] GitHub Actions workflow运行无错误
- [ ] PR评论中能看到PR-Agent的响应
- [ ] `/review` 命令正常工作
- [ ] `/describe` 命令正常工作
- [ ] `/improve` 命令正常工作

## 🔍 故障排查

### 问题：本地测试时 "ModuleNotFoundError"

**原因**：未安装PR-Agent

**解决**：

```bash
pip install pr-agent
```

### 问题：GitHub Actions中 "OPENAI\_\_KEY not found"

**原因**：Secret未正确配置

**解决**：

1. 检查Secret名称是否为 `ZHIPU_API_KEY`
2. 检查workflow文件中是否使用了 `OPENAI__KEY: ${{ secrets.ZHIPU_API_KEY }}`
3. 重新保存Secret

### 问题：模型响应为空或格式错误

**原因**：可能是API Base URL配置错误

**解决**：

```toml
[openai]
# 确保使用正确的端点
api_base = "https://open.bigmodel.cn/api/paas/v4"  # 通用端点
# api_base = "https://open.bigmodel.cn/api/coding/paas/v4"  # Coding端点（需要编码套餐）
```

### 问题：响应速度很慢

**原因**：上下文窗口设置过大或请求过于频繁

**解决**：

```toml
[config]
custom_model_max_tokens = 4096  # 减小上下文窗口

[pr_reviewer]
num_max_findings = 3  # 减少审查数量
```

## 📚 相关文档

- [PR-Agent官方文档](https://qodo-merge-docs.qodo.ai/)
- [LiteLLM OpenAI兼容配置](https://docs.litellm.ai/docs/providers/openai_compatible)
- [智谱AI官方文档](https://docs.bigmodel.cn/cn/api/introduction)
- [智谱AI API Key管理](https://open.bigmodel.cn/usercenter/apikeys)

## 💡 最佳实践

1. **先本地测试，再部署**：使用 `test-pr-agent-local.toml` 在本地验证配置
2. **使用环境变量**：不要在代码中硬编码API Key
3. **设置fallback模型**：配置备用模型，提高可靠性
4. **监控使用量**：在智谱控制台监控API调用次数和费用
5. **定期更新密钥**：定期更换API Key，提高安全性
