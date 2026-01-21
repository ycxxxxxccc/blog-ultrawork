@echo off
REM PR-Agent 部署脚本 - 剩余步骤自动化工具
REM 使用前请先在GitHub上创建仓库

echo ==========================================
echo    PR-Agent 部署助手
echo ==========================================
echo.

REM 检查是否已配置远程仓库
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到远程仓库配置
    echo.
    echo 请先在GitHub上创建仓库：
    echo 1. 访问: https://github.com/new
    echo 2. 仓库名称: blog-ultrawork
    echo 3. 不要勾选 "Add a README file"
    echo 4. 点击 "Create repository"
    echo.
    pause
    goto :configure_remote
) else (
    echo [√] 已检测到远程仓库
    echo 远程URL: 
    git remote get-url origin
    echo.
)

:menu
echo ==========================================
echo 请选择操作：
echo ==========================================
echo 1. 配置远程仓库
echo 2. 推送代码到GitHub
echo 3. 创建测试PR
echo 4. 查看部署状态
echo 5. 退出
echo.
set /p choice=请输入选项 (1-5):

if "%choice%"=="1" goto :configure_remote
if "%choice%"=="2" goto :push_code
if "%choice%"=="3" goto :create_test_pr
if "%choice%"=="4" goto :check_status
if "%choice%"=="5" goto :exit
goto :menu

:configure_remote
echo.
echo ==========================================
echo 配置远程仓库
echo ==========================================
echo.
set /p repo_url=请输入GitHub仓库URL (例如: https://github.com/ycxxxxxccc/blog-ultrawork.git):

git remote add origin %repo_url%
if %errorlevel%==0 (
    echo [√] 远程仓库配置成功
) else (
    echo [错误] 远程仓库配置失败
)
echo.
pause
goto :menu

:push_code
echo.
echo ==========================================
echo 推送代码到GitHub
echo ==========================================
echo.
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未配置远程仓库，请先执行选项1
    echo.
    pause
    goto :menu
)

echo 正在推送代码到 master 分支...
git push -u origin master
if %errorlevel%==0 (
    echo [√] 代码推送成功
    echo.
    echo 下一步：
    echo 1. 访问: https://github.com/ycxxxxxccc/blog-ultrawork/settings/secrets/actions
    echo 2. 点击 "New repository secret"
    echo 3. 添加 Secret:
    echo    Name: ZAI_API_KEY
    echo    Value: 52d6d1a828c248ae8f0480906e5218cc.9rrqqsJkD8KYiSOI
) else (
    echo [错误] 代码推送失败，请检查网络连接和权限
)
echo.
pause
goto :menu

:create_test_pr
echo.
echo ==========================================
echo 创建测试PR
echo ==========================================
echo.
echo 正在创建测试分支...
git checkout -b test-pr-agent 2>nul
if %errorlevel% neq 0 (
    echo 分支已存在，切换到现有分支
    git checkout test-pr-agent
)

echo 正在修改README.md...
echo. >> README.md
echo ## PR-Agent 测试 >> README.md
echo 此PR用于测试PR-Agent代码审查功能。 >> README.md

echo 正在提交更改...
git add README.md
git commit -m "Test: Add PR-Agent test section" 2>nul
if %errorlevel% neq 0 (
    echo [提示] 没有新的更改需要提交
) else (
    echo [√] 测试更改已提交
)

echo 正在推送测试分支...
git push -u origin test-pr-agent
if %errorlevel%==0 (
    echo [√] 测试分支推送成功
    echo.
    echo 下一步：
    echo 1. 访问: https://github.com/ycxxxxxccc/blog-ultrawork
    echo 2. 点击 "Compare & pull request"
    echo 3. 创建Pull Request
    echo 4. 等待GitHub Actions自动运行
    echo 5. pr-agent会在PR评论中添加审查意见
) else (
    echo [错误] 测试分支推送失败
)
echo.
pause
goto :menu

:check_status
echo.
echo ==========================================
echo 部署状态检查
echo ==========================================
echo.

echo [1] 远程仓库状态:
git remote get-url origin 2>nul
if %errorlevel%==0 (
    echo [√] 已配置
    git remote get-url origin
) else (
    echo [×] 未配置
)

echo.
echo [2] 工作流文件:
if exist .github\workflows\pr-agent-review.yml (
    echo [√] .github/workflows/pr-agent-review.yml 存在
) else (
    echo [×] 工作流文件缺失
)

echo.
echo [3] 提交历史:
git log --oneline -n 3

echo.
echo [4] 当前分支:
git branch --show-current

echo.
pause
goto :menu

:exit
echo.
echo 感谢使用！
echo.
echo 如需帮助，请查看: PR_AGENT_DEPLOYMENT.md
echo.
pause
exit
