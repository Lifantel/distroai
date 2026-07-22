import itertools
import random
import csv
from collections import Counter, defaultdict

# Sorular:
# q1: Linux/terminal tecrübesi
# q2: Güçlü/güncel donanım
# q3: Kararlılıktan çok en yeni güncellemeler önemli mi 
# q4: Oyun / performans odaklı kullanım
# q5: NVIDIA ekran kartı var mı
# q6: Düşük RAM/CPU tüketimi kritik mi (hafiflik)
# q7: Macera / özelleştirme isteği
# q8: Büyük şirket desteği önemli mi
# q9: Siber güvenlik / pentest ilgisi
# q10: Windows a benzer olsun mu
# q11 Usb üzerinden çalışmasını istiyormusunuz?
# q12 Sağlıklı bir yaşam istiyormusun?
# q13 Biraz daha mobile, laptop uyumlu bir arayüz istiyormusun?
# q14 Tamamen anonimlik ve iz bırakmamayı mı amaçlıyorsunuz? (Sadece USB üzerinden çalışan TailsOS e yönlendirir)

agirliklar = {
    #               q1   q2   q3   q4   q5   q6   q7   q8   q9 q10 q11 q12 q13 q14
    0: [          -1,  -1,  -1,  -1,   0,   2,  -1,   0,  -1,  2, -1,  0,  -1, -4],  # Linux Mint
    1: [          -1,   0,  -1,  -1,   0,   0,  -1,   2,   0, -1, -1,  0,   2, -4],  # Ubuntu
    2: [           1,   1,   2,   0,  -1,   0,   2,   1,  -1,  0, -1,  0,   1, -4],  # Fedora
    3: [           1,   1,   1,   2,   1,  -1,   0,  -1,  -1,  0, -1,  0,   0, -4],  # CachyOS
    4: [           2,   0,   1,   0,   0,   1,   2,  -1,  -1,  0,  2, -4,   0, -4],  # Arch Linux
    5: [           0,  -1,  -1,  -1,   0,   1,   1,   2,  -1,  0, -1,  0,   1, -4],  # openSUSE
    6: [          -1,   1,   0,   2,   2,  -1,  -1,   1,  -1, -1, -1,  0,   0, -4],  # Pop!_OS
    7: [           2,   0,   0,  -1,   0,  -1,   1,  -1,   4, -1,  2,  0,  -1, -4],  # Kali Linux
    8: [          -1,   1,  -1,  -1,   0,   0,  -1,   2,   0,  0, -1,  0,   1, -4],  # Pardus
    9: [           0,   0,   0,   0,   0,   0,   0,   0,   0,  0,  0,  0,   0,  5],  # Tails
}

distro_isimleri = {
    0: "Linux Mint", 1: "Ubuntu", 2: "Fedora", 3: "CachyOS",
    4: "Arch Linux", 5: "openSUSE", 6: "Pop!_OS", 7: "Kali Linux", 8: "Pardus", 9: "Tails"
}

def etiketle(cevaplar):
    en_iyi_puan, en_iyi_label = None, None
    for label, w in agirliklar.items():
        puan = sum(c * wi for c, wi in zip(cevaplar, w))
        if en_iyi_puan is None or puan > en_iyi_puan:
            en_iyi_puan, en_iyi_label = puan, label
    return en_iyi_label
SKALA = [0.0, 0.25, 0.5, 0.75, 1.0]
random.seed(42)
HEDEF_HER_SINIF = 1000
MAX_DENEME = 3_000_000

sinif_sayaci = Counter()
satirlar = []
deneme = 0
while deneme < MAX_DENEME and min(sinif_sayaci.get(l, 0) for l in agirliklar) < HEDEF_HER_SINIF:
    deneme += 1
    cevaplar = tuple(random.choice(SKALA) for _ in range(14))
    label = etiketle(cevaplar)
    if sinif_sayaci[label] >= HEDEF_HER_SINIF:
        continue
    satirlar.append(list(cevaplar) + [label])
    sinif_sayaci[label] += 1

print("Ornekleme bitti. Deneme sayisi:", deneme)
print("Her sinifin topladigi ornek sayisi:")
for l in sorted(agirliklar):
    print(f"  {distro_isimleri[l]}: {sinif_sayaci.get(l, 0)}")

random.shuffle(satirlar)

with open("dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["q1","q2","q3","q4","q5","q6","q7","q8","q9","q10","q11","q12","q13","q14","label"])
    writer.writerows(satirlar)


kontrol = {}
celiski = 0
for row in satirlar:
    anahtar = tuple(row[:14])
    etiket = row[14]
    if anahtar in kontrol and kontrol[anahtar] != etiket:
        celiski += 1
    kontrol[anahtar] = etiket

print("\nToplam satır:", len(satirlar))
print("Çelişkili satır sayısı:", celiski)
print("\nSınıf dağılımı (dataset.csv içinde):")
print(Counter(row[14] for row in satirlar))
