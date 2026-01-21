#!/usr/bin/env python3
"""
GitHub 仓库自动创建工具
使用GitHub API创建仓库并推送代码
"""

import requests
import json
import subprocess
import sys
from pathlib import Path

def create_github_repo(token, repo_name="blog-ultrawork", description="UltraWork Blog with PR-Agent"):
    """使用GitHub API创建仓库"""

    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": description,
        "private": False,
        "auto_init": False
    }

    print(f"正在创建仓库: {repo_name}")
    print(f"描述: {description}")
    print()

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        repo_info = response.json()
        print("✓ 仓库创建成功！")
        print(f"  仓库URL: {repo_info['html_url']}")
        print(f"  克隆URL: {repo_info['clone_url']}")
        return repo_info
    else:
        print(f"✗ 仓库创建失败")
        print(f"  状态码: {response.status_code}")
        print(f"  错误信息: {response.text}")
        return None

def setup_git_remote(repo_url):
    """配置git远程仓库并推送"""

    # 检查是否已有remote
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("✓ 添加远程仓库...")
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
    else:
        existing_url = result.stdout.strip()
        if existing_url != repo_url:
            print(f"✓ 更新远程仓库 ({existing_url} -> {repo_url})...")
            subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=True)
        else:
            print("✓ 远程仓库已配置")

    print("✓ 正在推送代码到 master 分支...")
    result = subprocess.run(
        ["git", "push", "-u", "origin", "master"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✓ 代码推送成功！")
        print()
        print("=" * 50)
        print("  下一步：配置 GitHub Secrets")
        print("=" * 50)
        print()
        print("1. 访问以下URL配置Secret:")
        print(f"   https://github.com/ycxxxxxccc/blog-ultrawork/settings/secrets/actions")
        print()
        print("2. 添加 Secret:")
        print("   Name: ZAI_API_KEY")
        print("   Value: 52d6d1a828c248ae8f0480906e5218cc.9rrqqsJkD8KYiSOI")
        print()
        print("3. 创建测试PR验证功能:")
        print("   git checkout -b test-pr-agent")
        print('   echo "## Test PR" >> README.md')
        print("   git add README.md")
        print('   git commit -m "Test PR for pr-agent"')
        print("   git push -u origin test-pr-agent")
        print()
        print("然后在GitHub上创建Pull Request即可！")
    else:
        print(f"✗ 代码推送失败")
        print(f"  错误: {result.stderr}")

def main():
    print("=" * 50)
    print("  GitHub 仓库自动创建工具")
    print("=" * 50)
    print()

    # 获取GitHub Token
    token = input("请输入 GitHub Personal Access Token: ").strip()

    if not token:
        print("✗ Token不能为空")
        print()
        print("如何获取Token:")
        print("1. 访问: https://github.com/settings/tokens")
        print("2. 点击 'Generate new token' → 'Generate new token (classic)'")
        print("3. 勾选 'repo' 权限")
        print("4. 设置过期时间并生成")
        print("5. 复制Token并粘贴到这里")
        sys.exit(1)

    # 创建仓库
    repo_info = create_github_repo(token)

    if repo_info:
        # 推送代码
        clone_url = repo_info['clone_url']
        setup_git_remote(clone_url)

if __name__ == "__main__":
    main()
