@echo off
cd /d "%~dp0"
git pull --ff-only || exit /b 1
python scripts\install_external.py --all --update || exit /b 1
python scripts\install.py --all --update || exit /b 1
echo Skills atualizadas.
