> [!CAUTION]
> Nöronu besleyen datasette cezalandırma sisteminde bir takım sorunlar yaşıyorum, en yakın zamanda çözeceğim.
 
---


# Linux Distro Tavsiye Yapay Nöronu

Bu proje, kullanıcıya sorduğu 8 soruya göre hangi Linux dağıtımının
ona daha uygun olduğunu tahmin eden basit bir yapay nöron modelidir.
PyTorch ile yazılmış küçük bir yapay nöron ağı, önceden hazırlanmış
örnek profiller üzerinden eğitilir ve ardından kullanıcının cevaplarını
alarak bir öneri sunar.

## Nasıl Çalışıyor

Model, deneyim seviyesi, donanım gücü, kararlılık tercihi, oyun/performans
ihtiyacı, NVIDIA ekran kartı varlığı, düşük kaynak tüketimi önemi, macera
isteği ve kurumsal destek beklentisi gibi sekiz farklı soruya verilen
evet/hayır cevaplarını sayısal bir vektöre çevirir ve bu vektörü ağdan
geçirir. Çıktı olarak altı dağıtımdan (Mint, Ubuntu, Fedora, CachyOS,
Arch, openSUSE) hangisinin en uygun olduğunu yüzdelik olasılıklarla
gösterir.

## Desteklenen Dağıtımlar

- Linux Mint
- Ubuntu
- Fedora
- CachyOS
- Arch Linux
- openSUSE

## Çalıştırma

```bash
pip install torch
python3 distro_ai.py
```

Sorulara `E` (Evet) veya `H` (Hayır) yazarak cevap verin, model size
en uygun dağıtımı ve diğer ihtimalleri yüzde olarak gösterecektir.

## Hızlı Test İçin

Kendi bilgisayarınıza kurulum yapmadan denemek isteyenler, dosyayı
Google Colab'a yükleyip orada da çalıştırabilir. Colab üzerinde PyTorch
zaten hazır geldiği için sadece kodu bir hücreye yapıştırıp çalıştırmak
yeterlidir.

## Not

Dataset Claude ile yazılmıştır. Eğitim verisi küçük örneklerden oluştuğundan, yapay
nöron her zaman mükemmel sonuç vermeyebilir. Daha fazla örnek eklemek
kararlarını daha tutarlı hale getirir.
