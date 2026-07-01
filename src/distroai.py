
#GNU GPL 3.0v = sizde aynı lisans altında kodlarla istediğinizi yapabilirsiniz.

import torch
import torch.nn as nn
import torch.optim as optim
import csv
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------
# 1. MODEL TANIMLAMASI VE EĞİTİM VERİSİ
# ---------------------------------------------------------
# Soru Mantığı (Evet=1, Hayır=0):

distro_isimleri = {
    0: "Linux Mint",
    1: "Ubuntu",
    2: "Fedora",
    3: "CachyOS",
    4: "Arch Linux",
    5: "openSUSE",
    6: "Pop!_OS",
    7: "Kali Linux"
}

X_list, Y_list = [], []
with open("dataset.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # başlık satırını ("q1,q2,...,label") atla
    for row in reader:
        X_list.append([float(v) for v in row[:12]])
        Y_list.append(int(row[12]))

X = torch.tensor(X_list, dtype=torch.float32)
Y = torch.tensor(Y_list, dtype=torch.long)

X_train, X_val, Y_train, Y_val = train_test_split(
    X, Y, test_size=0.2, random_state=42, stratify=Y
)

class DistroAI(nn.Module):
    def __init__(self, input_size=12, num_classes=8, dropout=0.2):
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
criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
optimizer = optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-4)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=300, gamma=0.5)

EPOCHS = 1000
model.train()
for epoch in range(EPOCHS):
    optimizer.zero_grad()
    output = model(X_train)  
    loss = criterion(output, Y_train)
    loss.backward()
    optimizer.step()
    scheduler.step()
    
    if (epoch + 1) % 200 == 0:
        model.eval()
        with torch.no_grad():
            val_output = model(X_val)
            val_loss = criterion(val_output, Y_val)
            acc = (val_output.argmax(dim=1) == Y_val).float().mean().item()
        print(f"[Epoch {epoch+1}] Train Loss: {loss.item():.4f} | Val Acc: %{acc*100:.1f}")
        model.train()

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
    "9. Siber güvenlik veya penetrasyon testi yapmak istiyor musunuz? (E/H): ",
    "10. Windows benzeri olsun mu? (E/H):",
    "11. Usb üzerinde çalışabilsinmi (E/H):",
    "12. Sağlıklı bir yaşam istiyormusun? (E/H):"
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
print("Linux Distroları hakkında daha fazla bilgi için\n")
url = "https://www.mfgultekin.com/linux.html"
print(f"\033]8;;{url}\033\\{url}\033]8;;\033\\")
print("\nbu adrese gidebilirsiniz")
print("="*40)
