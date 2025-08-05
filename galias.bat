@echo off
cd /d "%~dp0"
python -c "import improvctl; improvctl.main()" %*
