@echo off
echo DistroAI Baslatiliyor...

if not exist venv (
    echo Venv olusturuluyor...
    python -m venv venv
) else (
    echo Venv mevcut.
)

call venv\Scripts\activate

echo Pip guncelleniyor...
python -m pip install --upgrade pip
echo Paketler yukleniyor...
pip install torch scikit-learn

set REPO_URL=https://github.com/Lifantel/distroai.git
set REPO_DIR=distroai_repo

if not exist %REPO_DIR% (
    echo Git clone...
    git clone %REPO_URL% %REPO_DIR%
    cd %REPO_DIR%
) else (
    echo Git pull...
    cd %REPO_DIR%
    git pull
)

cd src

if exist requirements.txt (
    echo Pip requirements...
    pip install -r requirements.txt
)

if exist distroai.py (
    python distroai.py
) else (
    echo Hata: distroai.py yok!
    exit /b 1
)
