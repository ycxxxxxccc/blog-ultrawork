#!/usr/bin/env python3
"""
PR-Agent 连接智谱AI 测试脚本
用于验证配置是否正确
"""

import os
import sys

def test_config():
    """测试配置文件是否正确"""

    print("=" * 60)
    print("PR-Agent 智谱AI 配置测试")
    print("=" * 60)
    print()

    # 测试1：检查配置文件存在
    print("【测试1】检查配置文件...")
    config_files = [
        ".pr_agent.toml",
        "test-pr-agent-local.toml"
    ]

    found_config = False
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"  ✅ 找到配置文件: {config_file}")
            found_config = True

            # 读取并检查配置
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()

                # 检查模型配置
                if "openai/glm-4-flash" in content:
                    print(f"  ✅ 模型配置正确: openai/glm-4-flash")
                elif "zai/glm" in content:
                    print(f"  ⚠️  模型配置使用旧格式，建议更新为: openai/glm-4-flash")
                else:
                    print(f"  ❌ 模型配置可能不正确")

                # 检查API Base
                if "https://open.bigmodel.cn/api/paas/v4" in content:
                    print(f"  ✅ API Base配置正确")
                elif "https://open.bigmodel.cn/api/coding/paas/v4" in content:
                    print(f"  ✅ API Base配置正确 (Coding端点)")
                else:
                    print(f"  ⚠️  未找到智谱AI API Base配置")

                # 检查API Key配置
                if "api_key" in content.lower():
                    if "fed973c3bb23450b97dee7c278c665c7.wRInxdhCA9R3KinB" in content:
                        print(f"  ✅ API Key已配置")
                    else:
                        print(f"  ⚠️  API Key需要配置")
                else:
                    print(f"  ⚠️  未找到API Key配置")

    if not found_config:
        print(f"  ❌ 未找到配置文件")
    print()

    # 测试2：检查环境变量
    print("【测试2】检查环境变量...")
    env_vars = [
        ("ZHIPU_API_KEY", "智谱AI API Key"),
        ("OPENAI__API_BASE", "OpenAI API Base"),
        ("OPENAI__KEY", "OpenAI API Key"),
    ]

    for var_name, var_desc in env_vars:
        value = os.environ.get(var_name)
        if value:
            # 只显示前几位，保护密钥
            masked = value[:6] + "..." if len(value) > 6 else "..."
            print(f"  ✅ {var_desc} ({var_name}): {masked}")
        else:
            print(f"  ⚠️  {var_desc} ({var_name}) 未设置")
    print()

    # 测试3：检查workflow配置
    print("【测试3】检查GitHub Workflow配置...")
    workflow_file = ".github/workflows/pr_agent.yml"
    if os.path.exists(workflow_file):
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()

            if "OPENAI__API_BASE" in content:
                print(f"  ✅ Workflow包含 OPENAI__API_BASE 配置")
            else:
                print(f"  ⚠️  Workflow缺少 OPENAI__API_BASE 配置")

            if "OPENAI__KEY" in content or "ZHIPU_API_KEY" in content:
                print(f"  ✅ Workflow包含 API Key 配置")
            else:
                print(f"  ❌ Workflow缺少 API Key 配置")

            if "GITHUB_TOKEN" in content:
                print(f"  ✅ Workflow包含 GITHUB_TOKEN 配置")
            else:
                print(f"  ⚠️  Workflow缺少 GITHUB_TOKEN 配置")
    else:
        print(f"  ❌ 未找到workflow文件: {workflow_file}")
    print()

    # 测试4：验证API连接（需要安装依赖）
    print("【测试4】验证API连接...")
    try:
        import requests

        api_key = os.environ.get("ZHIPU_API_KEY") or "fed973c3bb23450b97dee7c278c665c7.wRInxdhCA9R3KinB"
        api_base = os.environ.get("OPENAI__API_BASE") or "https://open.bigmodel.cn/api/paas/v4"

        print(f"  测试端点: {api_base}")
        print(f"  使用API Key: {api_key[:6]}...")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "glm-4-flash",
            "messages": [
                {"role": "user", "content": "你好，请简单介绍一下你自己"}
            ],
            "stream": False
        }

        response = requests.post(
            f"{api_base}/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"  ✅ API连接成功！")
            print(f"  模型响应: {content[:50]}...")
        else:
            print(f"  ❌ API连接失败")
            print(f"  状态码: {response.status_code}")
            print(f"  错误信息: {response.text[:200]}")

    except ImportError:
        print(f"  ⚠️  未安装requests库，跳过API连接测试")
        print(f"  安装命令: pip install requests")
    except Exception as e:
        print(f"  ❌ API连接测试失败: {str(e)}")
    print()

    # 总结
    print("=" * 60)
    print("测试完成！")
    print("=" * 60)
    print()
    print("下一步：")
    print("1. 确保所有配置项都已设置 ✅")
    print("2. 在本地测试: pr-agent --config-file test-pr-agent-local.toml --pr-url <your-pr-url> describe")
    print("3. 提交到GitHub并创建测试PR")
    print()

if __name__ == "__main__":
    test_config()
