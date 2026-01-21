# PR-Agent 测试

此PR用于测试PR-Agent代码审查功能是否正常工作。

## 测试内容

- ✅ GitHub Actions是否自动触发
- ✅ PR-Agent是否成功运行
- ✅ 智谱AI API是否正常调用
- ✅ 代码审查评论是否自动添加

## 预期结果

在PR评论中应该看到PR-Agent自动添加的：

1. `/review` - 代码审查意见
2. `/describe` - PR描述摘要
