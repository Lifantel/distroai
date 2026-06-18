
#GNU GPL 3.0v = sizde aynı lisans altında kodlarla istediğinizi yapabilirsiniz.

import torch
import torch.nn as nn
import torch.optim as optim
import csv

# ---------------------------------------------------------
# 1. MODEL TANIMLAMASI VE EĞİTİM VERİSİ
# ---------------------------------------------------------
# Soru Mantığı (Evet=1, Hayır=0):
# Dataseti genişletirseniz (X tensörünü ve Y yi) soruları arttırıp aynı oranda distroların kombinasyanunu arttırırsanız model dahada gelişir.
# Not: Matematiğini bende bilmiyorum matematiksel hata yaptıysam kusura bakmayın googledan baktım.

distro_isimleri = {
    0: "Linux Mint",
    1: "Ubuntu",
    2: "Fedora",
    3: "CachyOS",
    4: "Arch Linux",
    5: "openSUSE",
}

X_list, Y_list = [], []
with open("dataset.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # başlık satırını ("q1,q2,...,label") atla
    for row in reader:
        X_list.append([float(v) for v in row[:8]])
        Y_list.append(int(row[8]))

X = torch.tensor(X_list, dtype=torch.float32)
Y = torch.tensor(Y_list, dtype=torch.long)

class DistroAI(nn.Module):
    def __init__(self, input_size=8, num_classes=6, dropout=0.2):
        super(DistroAI, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(16, num_classes)
        )

    def forward(self, x):
        return self.network(x)
model = DistroAI()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-4)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=300, gamma=0.5)

EPOCHS = 1000
model.train()
for epoch in range(EPOCHS):
    optimizer.zero_grad()
    output = model(X)
    loss = criterion(output, Y)
    loss.backward()
    optimizer.step()
    scheduler.step()

    if (epoch + 1) % 200 == 0:
        with torch.no_grad():
            acc = (output.argmax(dim=1) == Y).float().mean().item()
        print(f"[Epoch {epoch+1}/{EPOCHS}] Loss: {loss.item():.4f} | Eğitim Doğruluğu: %{acc*100:.1f}")

model.eval() 
print("LINUX DISTRO TAVSİYE YAPAY ZEKASINA HOŞ GELDİNİZ")
print("Lütfen soruları 'E' (Evet) veya 'H' (Hayır) olarak yanıtlayın.\n")

sorular = [
    "1. Daha önce Linux veya terminal kullandınız mı? (E/H): ",
    "2. Bilgisayarınız güncel ve donanımı güçlü mü? (E/H): ",
    "3. Sistemin kararlı olmasındansa, en yeni güncellemeleri almak daha mı önemli? (E/H): ",
    "4. Bu sistemi yoğun şekilde oyun veya performans odaklı işler için mi kuruyorsunuz? (E/H): ",
    "5. Bilgisayarınızda NVIDIA ekran kartı var mı? (E/H): ",
    "6. Sistemin çok az RAM ve CPU tüketmesi sizin için kritik mi? (E/H): ",
    "7. Macera/özelleştirme istiyor musunuz? (E/H): ",
    "8. Büyük bir şirket desteği olsun mu? (E/H): ",
]

kullanici_cevaplari = []

for soru in sorular:
    while True:
        cevap = input(soru).strip().upper()
        if cevap in ['E', 'H']:
            kullanici_cevaplari.append(1.0 if cevap == 'E' else 0.0)
            break
        print("Lütfen sadece 'E' veya 'H' giriniz!")

girdi_vektoru = torch.tensor([kullanici_cevaplari], dtype=torch.float32)

with torch.no_grad():
    model_ciktisi = model(girdi_vektoru)
    olasiliklar = torch.nn.functional.softmax(model_ciktisi, dim=1)[0]
    tahmin_indeks = torch.argmax(olasiliklar).item()
print("\n" + "="*40)
print("YAPAY ZEKA ANALİZ SONUCU:")
print(f"Önerilen Dağıtım: ** {distro_isimleri[tahmin_indeks]} **")
print("-"*40)
print("Diğer ihtimaller:")
sirali = sorted(distro_isimleri.items(), key=lambda kv: olasiliklar[kv[0]].item(), reverse=True)
for idx, isim in sirali:
    print(f"- {isim}: %{olasiliklar[idx].item()*100:.1f}")
print("="*40)
