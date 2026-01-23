# PR-Agent 部署指南

## 📋 快速开始

### 1. 选择 LLM 提供商

编辑 `.github/workflows/pr_agent.yml` 文件，取消注释你想要的提供商配置。

**可用的提供商**：

| 提供商                 | 模型             | 配置环境变量       | 成本       |
| ---------------------- | ---------------- | ------------------ | ---------- |
| **OpenAI**             | gpt-4.1          | `OPENAI_KEY`       | 💰💰💰 高  |
| **智谱 AI**            | glm-4.5-flash    | `ZAI_API_KEY`      | 💰 免费/低 |
| **DeepSeek**           | deepseek-chat    | `DEEPSEEK_API_KEY` | 💰💰 中    |
| **Gemini** (Google)    | gemini-1.5-flash | `GEMINI_API_KEY`   | 💰 中      |
| **Claude** (Anthropic) | claude-3-opus    | `ANTHROPIC_KEY`    | 💰💰💰 高  |

### 2. 添加 API Key 到 GitHub Secrets

1. 访问你的 GitHub 仓库
2. 进入 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下内容：

| Secret 名称        | 说明                  | 获取地址                                                             |
| ------------------ | --------------------- | -------------------------------------------------------------------- |
| `OPENAI_KEY`       | OpenAI API 密钥       | [platform.openai.com](https://platform.openai.com/api-keys)          |
| `ZAI_API_KEY`      | 智谱 AI 密钥          | [open.bigmodel.cn](https://open.bigmodel.cn/usercenter/apikeys)      |
| `DEEPSEEK_API_KEY` | DeepSeek 密钥         | [platform.deepseek.com](https://platform.deepseek.com/api_keys)      |
| `GEMINI_API_KEY`   | Google Gemini 密钥    | [aistudio.google.com](https://aistudio.google.com/apikeys)           |
| `ANTHROPIC_KEY`    | Anthropic Claude 密钥 | [console.anthropic.com](https://console.anthropic.com/settings/keys) |

### 3. 提交并推送到 GitHub

```bash
git add .github/workflows/pr_agent.yml
git commit -m "Add PR-Agent workflow"
git push origin master
```

### 4. 创建测试 PR

创建一个新的 Pull Request 来测试 PR-Agent：

```bash
git checkout -b test-pr-agent
echo "## Test PR for PR-Agent" >> README.md
git add README.md
git commit -m "Test: PR-Agent setup"
git push -u origin test-pr-agent
```

然后在 GitHub 上创建 PR，你会看到：

- ✅ 自动代码审查
- ✅ 自动生成的 PR 描述
- ✅ 代码改进建议

---

## 🛠️ 高级配置

### 自定义审查规则

在 `.github/workflows/pr_agent.yml` 中添加：

```yaml
env:
  # ... 其他配置
  pr_reviewer.extra_instructions: """\
  - 检查 SQL 注入漏洞
  - 验证所有用户输入
  - 确保敏感数据不被记录
  - 遵循 Clean Code 命名约定
  """
```

### 配置响应语言

默认为英文，可设置为中文：

```yaml
env:
  config.response_language: "zh-CN"
```

### 调整代码建议数量

```yaml
env:
  pr_code_suggestions.num_code_suggestions: "8"
  pr_code_suggestions.suggestions_score_threshold: "7"
```

### 仅运行特定工具

如果只想运行审查和描述，不运行改进：

```yaml
env:
  github_action_config.auto_review: "true"
  github_action_config.auto_describe: "true"
  github_action_config.auto_improve: "false"
```

---

## 💬 支持的 PR 命令

在 PR 中使用以下命令：

| 命令              | 功能             | 触发方式          |
| ----------------- | ---------------- | ----------------- |
| `/review`         | 运行代码审查     | 自动（PR 打开时） |
| `/describe`       | 生成 PR 描述     | 自动（PR 打开时） |
| `/improve`        | 获取代码改进建议 | 手动（PR 评论）   |
| `/ask "question"` | 询问 PR 相关问题 | 手动（PR 评论）   |
| `/test`           | 生成单元测试     | 手动（PR 评论）   |
| `/help`           | 显示帮助信息     | 手动（PR 评论）   |

---

## 🔧 故障排查

### 问题 1：PR-Agent 没有运行

**检查**：

- ✅ Workflow 文件是否在 `.github/workflows/pr_agent.yml`
- ✅ API Key 是否正确添加到 Secrets
- ✅ Secrets 名称是否完全匹配（区分大小写）

### 问题 2：错误 "Model not found"

**解决方案**：

- ✅ 检查模型名称格式（如：`gemini/gemini-1.5-flash`）
- ✅ 确保对应的 API Key 已设置
- ✅ 查看官方支持的模型列表

### 问题 3：错误 "API key not found"

**解决方案**：

- ✅ 确认 Secret 名称正确
- ✅ 确认 Secret 值没有多余空格
- ✅ 重新保存 Secret

### 问题 4：错误 "Rate limit exceeded"

**解决方案**：

- ✅ 添加备用模型：`config.fallback_models`
- ✅ 增加超时时间：`config.ai_timeout: "300"`
- ✅ 切换到更高额度的 API 提供商

---

## 📚 更多资源

- [官方文档](https://qodo-merge-docs.qodo.ai/)
- [GitHub 仓库](https://github.com/qodo-ai/pr-agent)
- [配置选项](https://qodo-merge-docs.qodo.ai/usage-guide/configuration_options/)
- [支持的模型](https://qodo-merge-docs.qodo.ai/usage-guide/changing_a_model/)

---

## 🤝 贡献

如果遇到问题或有改进建议：

1. 查看官方文档
2. 搜索 [GitHub Issues](https://github.com/qodo-ai/pr-agent/issues)
3. 提交 Issue 或 Pull Request
