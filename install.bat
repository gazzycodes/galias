@echo off
echo 🚀 GALIAS Setup
echo ========================================

echo 📝 Creating .env file...
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ .env file created from template
    ) else (
        echo ⚠️  No .env.example found
    )
) else (
    echo ✅ .env file already exists
)

echo 🧪 Testing GALIAS...
.\galias.bat --version

echo.
echo 🎉 Setup Complete!
echo ========================================
echo 📋 Usage:
echo    .\galias.bat --version
echo    .\galias.bat list
echo    .\galias.bat add
echo    .\galias.bat delete
echo.
echo 📝 Next steps:
echo 1. Edit .env with your ImprovMX API key and domain
echo 2. Start using GALIAS with the commands above!
echo.
echo 💡 No installation or PATH setup needed - just works!
echo.
pause
