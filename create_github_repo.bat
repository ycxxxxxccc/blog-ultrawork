@echo off
REM 自动创建GitHub仓库并推送代码
REM 需要提供GitHub Personal Access Token

echo ==========================================
echo    GitHub 仓库自动创建工具
echo ==========================================
echo.

set /p github_token=请输入 GitHub Personal Access Token (PAT):
set /p repo_name=请输入仓库名称 (默认: blog-ultrawork):
set /p repo_desc=请输入仓库描述 (默认: UltraWork Blog with PR-Agent):

if "%repo_name%"=="" set repo_name=blog-ultrawork
if "%repo_desc%"=="" set repo_desc=UltraWork Blog with PR-Agent

echo.
echo [信息] 正在创建 GitHub 仓库...
echo 仓库名: %repo_name%
echo 描述: %repo_desc%
echo.

REM 使用GitHub API创建仓库
curl -X POST ^
  -H "Authorization: token %github_token%" ^
  -H "Accept: application/vnd.github.v3+json" ^
  https://api.github.com/user/repos ^
  -d "{\"name\":\"%repo_name%\",\"description\":\"%repo_desc%\",\"private\":false,\"auto_init\":false}"

echo.
if %errorlevel%==0 (
    echo [√] 仓库创建成功！
    echo.
    echo 仓库URL: https://github.com/ycxxxxxccc/%repo_name%
    echo.
    echo ==========================================
    echo    正在推送代码...
    echo ==========================================
    echo.

    git remote get-url origin >nul 2>&1
    if %errorlevel% neq 0 (
        git remote add origin https://github.com/ycxxxxxccc/%repo_name%.git
        echo [√] 已添加远程仓库
    )

    git push -u origin master

    if %errorlevel%==0 (
        echo.
        echo [√] 代码推送成功！
        echo.
        echo ==========================================
        echo    下一步：配置 GitHub Secrets
        echo ==========================================
        echo.
        echo 1. 访问: https://github.com/ycxxxxxccc/%repo_name%/settings/secrets/actions
        echo 2. 点击 "New repository secret"
        echo 3. 添加以下 Secret:
        echo    Name: ZAI_API_KEY
        echo    Value: 52d6d1a828c248ae8f0480906e5218cc.9rrqqsJkD8KYiSOI
        echo.
        echo 4. 创建测试PR验证功能
        echo    git checkout -b test-pr-agent
        echo    echo "## Test" ^>^> README.md
        echo    git add README.md ^&^& git commit -m "Test PR" ^&^& git push -u origin test-pr-agent
        echo.
    ) else (
        echo [错误] 代码推送失败
    )
) else (
    echo [错误] 仓库创建失败
    echo.
    echo 可能原因:
    echo 1. Token无效或权限不足
    echo 2. 网络连接问题
    echo.
    echo 如何获取Token:
    echo 1. 访问: https://github.com/settings/tokens
    echo 2. 点击 "Generate new token"
    echo 3. 勾选 "repo" 权限
    echo 4. 生成并复制Token
)

echo.
pause
