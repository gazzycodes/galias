@echo off
echo 🚀 GALIAS Windows Installer
echo ========================================

echo 📦 Installing GALIAS...
python -m pip install --user .

if %errorlevel% neq 0 (
    echo ❌ Installation failed!
    pause
    exit /b 1
)

echo ✅ GALIAS installed successfully!

echo 📝 Adding to PATH...
for /f "tokens=*" %%i in ('python -c "import site, os; print(os.path.join(site.USER_BASE, 'Scripts'))"') do set SCRIPTS_DIR=%%i

echo Scripts directory: %SCRIPTS_DIR%

:: Add to user PATH using PowerShell
powershell -Command "$currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User'); if ($currentPath -notlike '*%SCRIPTS_DIR%*') { $newPath = $currentPath + ';%SCRIPTS_DIR%'; [Environment]::SetEnvironmentVariable('PATH', $newPath, 'User'); Write-Output 'PATH updated successfully' } else { Write-Output 'Directory already in PATH' }"

echo 📝 Creating .env file...
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo ✅ .env file created from template
    ) else (
        echo ⚠️  No .env.example found
    )
) else (
    echo ✅ .env file already exists
)

echo.
echo 🎉 Installation Complete!
echo ========================================
echo 📋 Next steps:
echo 1. RESTART your terminal/PowerShell
echo 2. Edit .env with your ImprovMX API key and domain
echo 3. Run: galias --version
echo 4. Run: galias list
echo.
echo 💡 If 'galias' command doesn't work after restart:
echo    Manually add this to your PATH: %SCRIPTS_DIR%
echo.
pause
