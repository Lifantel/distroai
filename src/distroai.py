
#GNU GPL 3.0v = sizde aynı lisans altında kodlarla istediğinizi yapabilirsiniz.

import torch
import torch.nn as nn
import torch.optim as optim
import csv
from sklearn.model_selection import train_test_split


distro_isimleri = {
    0: "Linux Mint",
    1: "Ubuntu",
    2: "Fedora",
    3: "CachyOS",
    4: "Arch Linux",
    5: "openSUSE",
    6: "Pop!_OS",
    7: "Kali Linux",
    8: "Pardus",
    9: "Tails"
}

X_list, Y_list = [], []
with open("dataset.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # başlık satırını ("q1,q2,...,label") atla
    for row in reader:
        X_list.append([float(v) for v in row[:14]])
        Y_list.append(int(row[14]))

X = torch.tensor(X_list, dtype=torch.float32)
Y = torch.tensor(Y_list, dtype=torch.long)

X_train, X_val, Y_train, Y_val = train_test_split(
    X, Y, test_size=0.2, random_state=42, stratify=Y
)

class DistroAI(nn.Module):
    def __init__(self, input_size=14, num_classes=10, dropout=0.2):
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
print("\nLINUX DISTRO TAVSİYE YAPAY ZEKASINA HOŞ GELDİNİZ")
print("Lütfen soruları 1 ile 5 arasında bir puanla yanıtlayın:")
print("  1 = Kesinlikle Hayır   2 = Hayır   3 = Kararsızım   4 = Evet   5 = Kesinlikle Evet\n")

sorular = [
    "1. Daha önce Linux veya terminal kullandınız mı? (1-5): ",
    "2. Bilgisayarınız güncel ve donanımı güçlü mü? (1-5): ",
    "3. Sistemin kararlı olmasındansa, en yeni güncellemeleri almak daha mı önemli? (1-5): ",
    "4. Bu sistemi yoğun şekilde oyun veya performans odaklı işler için mi kuruyorsunuz? (1-5): ",
    "5. Bilgisayarınızda NVIDIA ekran kartı var mı? (1-5): ",
    "6. Sistemin çok az RAM ve CPU tüketmesi sizin için kritik mi? (1-5): ",
    "7. Macera/özelleştirme istiyor musunuz? (1-5): ",
    "8. Büyük bir şirket desteği olsun mu? (1-5): ",
    "9. Siber güvenlik veya penetrasyon testi yapmak istiyor musunuz? (1-5): ",
    "10. Windows benzeri olsun mu? (1-5): ",
    "11. Usb üzerinde çalışabilsin mi? (1-5): ",
    "12. Sağlıklı bir yaşam istiyor musun? (1-5): ",
    "13. Biraz daha mobile, laptop uyumlu bir arayüz istiyor musun? (1-5): ",
    "14. Tamamen anonimlik ve iz bırakmamayı mı amaçlıyorsunuz (Sadece USB üzerinden çalışan TailsOS'a yönlendirir)? (1-5): "
]

SKALA_HARITASI = {1: 0.0, 2: 0.25, 3: 0.5, 4: 0.75, 5: 1.0}

kullanici_cevaplari = []

for soru in sorular:
    while True:
        cevap = input(soru).strip()
        if cevap in ['1', '2', '3', '4', '5']:
            kullanici_cevaplari.append(SKALA_HARITASI[int(cevap)])
            break
        print("Lütfen 1 ile 5 arasında bir sayı giriniz!")

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
