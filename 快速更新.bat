@echo off
chcp 65001 >nul
echo ========================================
echo    Git 快速更新脚本
echo ========================================
echo.

cd /d "%~dp0"

echo 正在检查 Git 状态...
git status --short
echo.

if %errorlevel% neq 0 (
    echo 错误：当前目录不是 Git 仓库！
    pause
    exit /b 1
)

echo 请选择操作：
echo [1] 查看当前状态
echo [2] 更新所有文件到 GitHub（需要输入提交信息）
echo [3] 只查看修改内容（不提交）
echo [4] 快速更新所有文件到 GitHub（自动提交信息）
echo [5] 退出
echo.
set /p choice=请输入选项 (1-5): 

if "%choice%"=="1" goto status
if "%choice%"=="2" goto update
if "%choice%"=="3" goto diff
if "%choice%"=="4" goto quickupdate
if "%choice%"=="5" goto end
goto invalid

:status
echo.
echo ========================================
echo    当前 Git 状态
echo ========================================
git status
echo.
pause
goto end

:diff
echo.
echo ========================================
echo    修改内容预览
echo ========================================
git diff
echo.
pause
goto end

:quickupdate
echo.
echo ========================================
echo    快速更新文件到 GitHub
echo ========================================
echo.

echo 正在添加所有修改的文件...
git add .
if %errorlevel% neq 0 (
    echo 错误：添加文件失败！
    pause
    exit /b 1
)

echo.
echo 正在生成提交信息...
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set mydate=%%c-%%a-%%b
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a%%b
set mytime=%mytime: =0%
set commit_msg=快速更新 %mydate% %mytime%

echo 提交信息：%commit_msg%
echo.
echo 正在提交更改...
git commit -m "%commit_msg%"
if %errorlevel% neq 0 (
    echo 警告：提交失败，可能没有需要提交的更改
    pause
    exit /b 1
)

echo.
echo 正在推送到 GitHub...
git push
if %errorlevel% neq 0 (
    echo 错误：推送失败！请检查网络连接和权限。
    pause
    exit /b 1
)

echo.
echo ========================================
echo    ✓ 快速更新成功！
echo ========================================
echo.
pause
goto end

:update
echo.
echo ========================================
echo    更新文件到 GitHub
echo ========================================
echo.

echo 正在添加所有修改的文件...
git add .
if %errorlevel% neq 0 (
    echo 错误：添加文件失败！
    pause
    exit /b 1
)

echo.
set /p commit_msg=请输入提交信息: 

if "%commit_msg%"=="" (
    echo 警告：提交信息为空，使用默认信息
    set commit_msg=更新文件
)

echo.
echo 正在提交更改...
git commit -m "%commit_msg%"
if %errorlevel% neq 0 (
    echo 警告：提交失败，可能没有需要提交的更改
    pause
    exit /b 1
)

echo.
echo 正在推送到 GitHub...
git push
if %errorlevel% neq 0 (
    echo 错误：推送失败！请检查网络连接和权限。
    pause
    exit /b 1
)

echo.
echo ========================================
echo    ✓ 更新成功！
echo ========================================
echo.
pause
goto end

:invalid
echo.
echo 无效的选项，请重新运行脚本
pause
goto end

:end
exit /b 0









