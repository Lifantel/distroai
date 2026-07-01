#!/bin/bash

set -e


echo "DistroAI Kurulum ve Çalıştırma Betiği"

# 1. Sanal ortamı oluştur
if [ ! -d "venv" ]; then
    echo "Python sanal ortamı (venv) oluşturuluyor..."
    python3 -m venv venv
else
    echo "Sanal ortam zaten mevcut."
fi

echo "Sanal ortam aktifleştiriliyor..."
source venv/bin/activate
echo "Pip güncelleniyor..."
pip install --upgrade pip
echo "Gerekli temel kütüphaneler yükleniyor (torch, scikit-learn)..."
pip install torch scikit-learn

REPO_URL="https://github.com/Lifantel/distroai.git"
REPO_DIR="distroai_repo"

echo "Kodlar GitHub'dan çekiliyor..."
if [ ! -d "$REPO_DIR" ]; then
    git clone "$REPO_URL" "$REPO_DIR"
    cd "$REPO_DIR"
else
    echo "Klasör zaten mevcut, güncel kodlar çekiliyor (git pull)..."
    cd "$REPO_DIR"
    git pull
fi
if [ -f "requirements.txt" ]; then
    echo "requirements.txt dosyası bulundu, bağımlılıklar kontrol ediliyor..."
    pip install -r requirements.txt
fi

if [ -f "distroai.py" ]; then
    echo "DistroAI başarıyla başlatılıyor..."
    python3 distroai.py
else
    echo "Hata: distroai.py dosyası bulunamadı!"
    exit 1
fi
