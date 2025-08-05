@echo off
echo 🚀 GALIAS Installer - Global Command Setup
echo =============================================

echo 📦 Installing GALIAS package...
python -m pip install --user . --quiet

if %errorlevel% neq 0 (
    echo ❌ Package installation failed!
    pause
    exit /b 1
)

echo ✅ Package installed successfully!

echo 🔧 Setting up global galias command...

REM Get the Scripts directory
for /f "tokens=*" %%i in ('python -c "import site, os; print(os.path.join(site.USER_BASE, 'Scripts'))"') do set SCRIPTS_DIR=%%i

echo 📁 Scripts directory: %SCRIPTS_DIR%

REM Create the directory if it doesn't exist
if not exist "%SCRIPTS_DIR%" mkdir "%SCRIPTS_DIR%"

REM Add to PATH using PowerShell (permanent)
powershell -Command "& {$path = [Environment]::GetEnvironmentVariable('PATH', 'User'); if ($path -notlike '*%SCRIPTS_DIR%*') {[Environment]::SetEnvironmentVariable('PATH', $path + ';%SCRIPTS_DIR%', 'User'); Write-Host 'PATH updated'} else {Write-Host 'Already in PATH'}}"

REM Update current session PATH
set PATH=%PATH%;%SCRIPTS_DIR%

echo 📝 Creating .env configuration...
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ .env file created from template
    )
) else (
    echo ✅ .env file already exists
)

echo 🧪 Testing galias command...
galias --version

if %errorlevel% equ 0 (
    echo.
    echo 🎉 SUCCESS! GALIAS is ready to use!
    echo =============================================
    echo 📋 You can now use these commands from anywhere:
    echo    galias --version
    echo    galias list
    echo    galias add
    echo    galias delete
    echo    galias status
    echo.
    echo 📝 Next steps:
    echo 1. Edit .env with your ImprovMX API key and domain
    echo 2. Run: galias list
    echo.
    echo ✅ The galias command works globally now!
) else (
    echo.
    echo ⚠️  Command test failed - restart your terminal
    echo 📋 After restart, you can use:
    echo    galias --version
    echo    galias list
    echo.
    echo 📝 Next steps:
    echo 1. CLOSE and REOPEN your terminal
    echo 2. Edit .env with your ImprovMX API key and domain  
    echo 3. Run: galias list
)

echo.
pause
