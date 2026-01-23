# PR-Agent 部署指南

## 📋 两种部署方式

PR-Agent 支持两种配置方式：

| 方式                         | 配置文件                | 优点                    | 适用场景 |
| ---------------------------- | ----------------------- | ----------------------- | -------- |
| **方式 1**：纯 `.yml`        | GitHub Actions Workflow | 一个文件搞定，简单直接  | 快速上手 |
| **方式 2**：`.yml` + `.toml` | Workflow + 配置文件     | 配置专门化，官方推荐 ✨ | 长期维护 |

本文档使用**方式 2**（官方推荐）。

---

## 🚀 快速开始（方式 2）

### 步骤 1：理解配置文件分工

| 文件                             | 作用                           | 位置             |
| -------------------------------- | ------------------------------ | ---------------- |
| `.github/workflows/pr_agent.yml` | 定义**什么时候**运行 + API Key | 触发器和环境变量 |
| `.pr_agent.toml`                 | 定义**怎么**工作 + 审查规则    | 仓库根目录       |

### 步骤 2：选择 LLM 提供商

编辑 `.pr_agent.toml` 文件，修改 `config.model` 部分：

```toml
[config]
# 智谱 AI（推荐，使用OpenAI兼容API）
model = "openai/glm-4-flash"
fallback_models = ["openai/glm-4-flash"]

# 其他选项：
# model = "deepseek/deepseek-chat"  # DeepSeek
# model = "gemini/gemini-1.5-flash"  # Gemini
# model = "anthropic/claude-3-opus-20240229"  # Claude
# model = "gpt-4.1"  # OpenAI
```

**智谱AI配置说明**：

智谱AI提供OpenAI兼容的API，有两种配置方式：

#### 方式1：使用OpenAI兼容端点（推荐）

在 `.pr_agent.toml` 中添加：

```toml
[openai]
api_base = "https://open.bigmodel.cn/api/paas/v4"
api_key = "your-zhipu-api-key"
api_type = "openai"

[config]
model = "openai/glm-4-flash"
fallback_models = ["openai/glm-4-flash"]
```

**注意事项**：

- 模型名需要 `openai/` 前缀，告诉LiteLLM使用OpenAI客户端
- 端点URL：通用端点用 `/api/paas/v4`，Coding端点用 `/api/coding/paas/v4`

#### 方式2：使用GitHub Secrets（生产环境推荐）

在 `.github/workflows/pr_agent.yml` 中：

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  OPENAI__API_BASE: https://open.bigmodel.cn/api/paas/v4
  OPENAI__KEY: ${{ secrets.ZHIPU_API_KEY }}
```

**注意事项**：

- 环境变量使用**双下划线** `OPENAI__API_BASE`
- Secret名称为 `ZHIPU_API_KEY`

### 步骤 3：添加 API Key 到 GitHub Secrets

1. 访问你的 GitHub 仓库
2. 进入 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下内容：

| 提供商                 | Secret 名称        | 获取地址                                                             |
| ---------------------- | ------------------ | -------------------------------------------------------------------- |
| **智谱 AI**            | `ZHIPU_API_KEY`    | [open.bigmodel.cn](https://open.bigmodel.cn/usercenter/apikeys)      |
| **DeepSeek**           | `DEEPSEEK_API_KEY` | [platform.deepseek.com](https://platform.deepseek.com/api_keys)      |
| **Gemini** (Google)    | `GEMINI_API_KEY`   | [aistudio.google.com](https://aistudio.google.com/apikeys)           |
| **Claude** (Anthropic) | `ANTHROPIC_KEY`    | [console.anthropic.com](https://console.anthropic.com/settings/keys) |
| **OpenAI**             | `OPENAI_KEY`       | [platform.openai.com](https://platform.openai.com/api-keys)          |

⚠️ **重要**：只添加你选择的一个提供商的 API Key！

### 步骤 4：配置 `.github/workflows/pr_agent.yml`

编辑 `.github/workflows/pr_agent.yml`，选择对应提供商的配置方式：

#### 对于智谱 AI（OpenAI兼容方式）

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # 智谱 AI - OpenAI兼容配置
  OPENAI__API_BASE: https://open.bigmodel.cn/api/paas/v4
  OPENAI__KEY: ${{ secrets.ZHIPU_API_KEY }}
```

**重要**：

- 使用**双下划线** `OPENAI__API_BASE` 和 `OPENAI__KEY`
- Secret名称为 `ZHIPU_API_KEY`（或自定义名称）

#### 对于其他提供商

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # --- 选择一个，取消注释 ---
  # DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}  # DeepSeek
  # GOOGLE_AI_STUDIO.GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}  # Gemini
  # ANTHROPIC.KEY: ${{ secrets.ANTHROPIC_KEY }}  # Claude
  # OPENAI_KEY: ${{ secrets.OPENAI_KEY }}  # OpenAI
```

### 步骤 5：提交并推送到 GitHub

```bash
git add .github/workflows/pr_agent.yml .pr_agent.toml
git commit -m "Add PR-Agent with TOML configuration"
git push origin master
```

### 步骤 6：创建测试 PR

创建一个新的 Pull Request 来测试 PR-Agent：

```bash
git checkout -b test-pr-agent
echo "## Test PR for PR-Agent" >> README.md
git add README.md
git commit -m "Test: Verify PR-Agent configuration"
git push -u origin test-pr-agent
```

然后在 GitHub 上创建 PR，你会看到：

- ✅ 自动代码审查（`/review`）
- ✅ 自动生成的 PR 描述（`/describe`）
- ✅ 代码改进建议（`/improve`）

---

## ⚙️ 配置文件详解

### `.pr_agent.toml` 完整结构

```toml
# ============================================
# 核心配置
# ============================================
[config]
model = "zai/glm-4.5-flash"
fallback_models = ["zai/glm-4.5-flash"]
custom_model_max_tokens = 4096
response_language = "zh-CN"

# ============================================
# 审查工具配置
# ============================================
[pr_reviewer]
require_security_review = true
require_tests_review = true
num_max_findings = 5
extra_instructions = """\
自定义审查指令...
"""

# ============================================
# 描述工具配置
# ============================================
[pr_description]
generate_ai_title = true
extra_instructions = "生成清晰的 PR 描述"

# ============================================
# 代码建议配置
# ============================================
[pr_code_suggestions]
num_code_suggestions_per_chunk = 6
focus_only_on_problems = false
extra_instructions = """\
代码改进建议...
"""

# ============================================
# 忽略文件配置
# ============================================
[ignore]
glob = ["*.generated.*", "dist/*", "node_modules/*"]
regex = [".*\\.min\\.js$"]
```

### 支持的配置选项

| 配置项                           | 说明                  | 默认值            |
| -------------------------------- | --------------------- | ----------------- |
| `model`                          | 使用的 LLM 模型       | `gpt-4`           |
| `fallback_models`                | 备用模型（JSON 数组） | `["gpt-4o-mini"]` |
| `custom_model_max_tokens`        | 最大上下文窗口        | 根据模型自动      |
| `response_language`              | 响应语言              | `en-US`           |
| `require_security_review`        | 启用安全审查          | `true`            |
| `require_tests_review`           | 启用测试审查          | `true`            |
| `num_max_findings`               | 最多发现的问题数      | `5`               |
| `num_code_suggestions_per_chunk` | 每次代码建议数量      | `4`               |

完整配置选项：[官方文档](https://qodo-merge-docs.qodo.ai/usage-guide/configuration_options/)

---

## 🛠️ 高级配置

### 1. 自定义审查规则（公司编码规范）

编辑 `.pr_agent.toml` 中的 `[pr_reviewer]` 部分：

```toml
[pr_reviewer]
extra_instructions = """\
遵循公司编码规范：

安全要求：
- 检查 SQL 注入、XSS、CSRF 等漏洞
- 验证所有用户输入
- 确保敏感数据不被记录

代码质量：
- 遵循 Clean Code 原则
- 函数单一职责
- 适当的错误处理和日志

Python 特定：
- 遵循 PEP 8 风格指南
- 使用类型提示
- 编写文档字符串

TypeScript 特定：
- 避免使用 `any` 类型
- 使用接口定义数据结构
- 确保类型安全
"""
```

### 2. 配置响应语言

```toml
[config]
# 可选值：
# - "en-US" (默认，英文）
# - "zh-CN" (简体中文）
# - "zh-TW" (繁体中文）
# - "ja-JP" (日语）
# - "ko-KR" (韩语）
# - "es-ES" (西班牙语）
# - "fr-FR" (法语）
# - "de-DE" (德语）
response_language = "zh-CN"
```

### 3. 调整代码建议数量

```toml
[pr_code_suggestions]
num_code_suggestions_per_chunk = 8  # 建议数量
suggestions_score_threshold = 7  # 最低质量分数
focus_only_on_problems = false  # 是否只关注问题
```

### 4. 忽略特定文件

```toml
[ignore]
# glob 模式
glob = [
    "*.generated.*",
    "*.d.ts",
    "dist/*",
    "node_modules/*",
    ".astro/*",
    "public/assets/*"
]

# 正则表达式模式
regex = [
    ".*\\.min\\.js$",
    ".*\\.min\\.css$",
    ".*lock\\.json$"
]
```

### 5. 仅运行特定工具

编辑 `.github/workflows/pr_agent.yml`：

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  ZAI_API_KEY: ${{ secrets.ZAI_API_KEY }}

  # 只运行审查和描述，不运行改进
  github_action_config.auto_review: "true"
  github_action_config.auto_describe: "true"
  github_action_config.auto_improve: "false"
```

---

## 💬 支持的 PR 命令

在 PR 评论中使用以下命令：

| 命令                | 功能             | 触发方式          | 说明     |
| ------------------- | ---------------- | ----------------- | -------- |
| `/review`           | 运行代码审查     | 自动（PR 打开时） | 自动运行 |
| `/describe`         | 生成 PR 描述     | 自动（PR 打开时） | 自动生成 |
| `/improve`          | 获取代码改进建议 | 手动（PR 评论）   | 提供建议 |
| `/test`             | 生成单元测试     | 手动（PR 评论）   | 创建测试 |
| `/ask "question"`   | 询问 PR 相关问题 | 手动（PR 评论）   | 问答交互 |
| `/help`             | 显示帮助信息     | 手动（PR 评论）   | 命令帮助 |
| `/update_changelog` | 更新 CHANGELOG   | 手动（PR 评论）   | 更新日志 |

**示例用法**：

```bash
# 在 PR 评论中输入
/improve

# 提问
/ask 这个函数有什么潜在的安全问题吗？

# 重新运行审查
/review
```

---

## 🔧 故障排查

### 问题 1：PR-Agent 没有运行

**检查清单**：

- ✅ Workflow 文件是否在 `.github/workflows/pr_agent.yml`
- ✅ API Key 是否正确添加到 Secrets
- ✅ Secret 名称是否完全匹配（区分大小写）
- ✅ Workflow 文件语法是否正确（YAML 缩进）
- ✅ 是否使用了正确的提供商配置

**查看日志**：

1. 访问 GitHub 仓库的 **Actions** 标签
2. 点击最新的 workflow run
3. 展开失败的步骤查看错误信息

### 问题 2：错误 "Model not found"

**可能原因**：

1. 模型名称格式错误
2. 模型不在此提供商的列表中
3. 提供商配置错误

**解决方案**：

```toml
# ❌ 错误格式
model = "glm-4.5-flash"

# ✅ 正确格式（智谱AI使用OpenAI兼容配置）
model = "openai/glm-4-flash"
```

**智谱AI特殊说明**：

智谱AI通过OpenAI兼容API使用，需要在模型名前加 `openai/` 前缀：

```toml
[config]
model = "openai/glm-4-flash"  # 通用端点
# model = "openai/glm-4-flash"  # Coding端点（需要编码套餐）

[openai]
api_base = "https://open.bigmodel.cn/api/paas/v4"  # 通用端点
# api_base = "https://open.bigmodel.cn/api/coding/paas/v4"  # Coding端点
api_key = "your-zhipu-api-key"
api_type = "openai"
```

完整模型列表：[模型文档](https://qodo-merge-docs.qodo.ai/usage-guide/changing_a_model/)

### 问题 3：错误 "API key not found"

**解决方案**：

1. **智谱AI**：确认 Secret 名称正确（如：`ZHIPU_API_KEY` 或 `OPENAI__KEY`）
2. 确认 Secret 值没有多余空格
3. 重新保存 Secret
4. 等待 1-2 分钟后重新触发 workflow

**检查GitHub Secrets**：

```bash
# 查看当前仓库的 Secrets（需要GitHub CLI）
gh secret list
```

### 问题 4：错误 "Rate limit exceeded"

**解决方案**：

**方案 1：添加备用模型**

```toml
[config]
model = "zai/glm-4.5-flash"
fallback_models = ["zai/glm-4.5-flash", "deepseek/deepseek-chat"]
```

**方案 2：增加超时时间**

```yaml
# .github/workflows/pr_agent.yml
env:
  config.ai_timeout: "300" # 300 秒
```

**方案 3：减少审查数量**

```toml
[pr_reviewer]
num_max_findings = 3  # 减少从 5 到 3
```

### 问题 5：错误 "Permission denied"

**解决方案**：
检查 `.github/workflows/pr_agent.yml` 中的权限配置：

```yaml
permissions:
  issues: write # 必须有
  pull-requests: write # 必须有
  contents: write # 必须有
```

### 问题 6：审查结果不符合预期

**解决方案**：

1. **检查自定义指令**：

```toml
[pr_reviewer]
extra_instructions = """\
确保指令清晰、具体、可执行
"""
```

2. **调整响应语言**：

```toml
[config]
response_language = "zh-CN"  # 改为中文
```

3. **增加上下文窗口**（对于大文件）：

```toml
[config]
custom_model_max_tokens = 8192  # 增加到 8192
```

4. **查看详细日志**：

```toml
[config]
config.verbosity_level = "2"  # 0=静音, 1=基本, 2=详细
```

---

## 📊 性能优化

### 大型仓库优化

```toml
[config]
# 大型 PR 处理策略
large_patch_policy = "clip"  # "clip" 或 "summary"

# 上下文窗口优化
custom_model_max_tokens = 32000

# Patch 上下文行数
patch_extra_lines_before = 3
patch_extra_lines_after = 1
```

### 减少审查时间

```toml
[pr_reviewer]
num_max_findings = 3  # 减少发现数量

[pr_code_suggestions]
num_code_suggestions_per_chunk = 4  # 减少建议数量
```

---

## 🌐 不同部署平台

### GitLab

编辑 `.pr_agent.toml` 添加 GitLab 配置：

```toml
[gitlab]
url = "https://gitlab.example.com"
personal_access_token = "glpat-xxxxxxxxxx"
auth_type = "oauth_token"  # or "private_token"
ssl_verify = true
```

创建 `.gitlab-ci.yml`：

```yaml
stages:
  - pr_agent

pr_agent_job:
  stage: pr_agent
  image: codiumai/pr-agent:latest
  script:
    - export MR_URL="$CI_MERGE_REQUEST_PROJECT_URL/merge_requests/$CI_MERGE_REQUEST_IID"
    - python -m pr_agent.cli --pr_url="$MR_URL" review
    - python -m pr_agent.cli --pr_url="$MR_URL" describe
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

### Bitbucket

配置类似 GitLab，详见[官方文档](https://qodo-merge-docs.qodo.ai/installation/bitbucket/)

---

## 📚 更多资源

### 官方文档

- [安装指南](https://qodo-merge-docs.qodo.ai/installation/)
- [使用指南](https://qodo-merge-docs.qodo.ai/usage-guide/)
- [配置选项](https://qodo-merge-docs.qodo.ai/usage-guide/configuration_options/)
- [模型切换](https://qodo-merge-docs.qodo.ai/usage-guide/changing_a_model/)
- [故障排查](https://qodo-merge-docs.qodo.ai/faq/)

### GitHub 仓库

- [PR-Agent 仓库](https://github.com/qodo-ai/pr-agent)
- [配置文件示例](https://github.com/qodo-ai/pr-agent/blob/main/pr_agent/settings/configuration.toml)
- [Issue 跟踪](https://github.com/qodo-ai/pr-agent/issues)

### 社区资源

- [Discord 社区](https://discord.gg/SgSxuQ65GF)
- [Twitter/X](https://twitter.com/QodoAI)
- [LinkedIn](https://www.linkedin.com/company/qodoai)

---

## 🤝 贡献

如果遇到问题或有改进建议：

1. 查看 [FAQ](https://qodo-merge-docs.qodo.ai/faq/)
2. 搜索 [GitHub Issues](https://github.com/qodo-ai/pr-agent/issues)
3. 提交新的 Issue
4. 参与 [Discord 讨论](https://discord.gg/SgSxuQ65GF)

---

## 📝 版本信息

- **PR-Agent 版本**: latest (main branch)
- **文档版本**: 2026年1月
- **配置方式**: GitHub Actions + TOML 配置文件（官方推荐）
