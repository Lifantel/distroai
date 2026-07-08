
> [!IMPORTANT]
> distroai.py yi çalıştırmadan önce datauret.py i çalıstırarak dataset oluşturmalısınız. Oluşturmak istemiyorsanız hazır dataset.csv yi kullanabilirsiniz


# Linux Distro Tavsiye Yapay Nöron Ağları

Bu proje, kullanıcıya sorduğu 13 soruya göre hangi Linux dağıtımının
ona daha uygun olduğunu tahmin eden basit bir yapay nöron modelidir.
PyTorch ile yazılmış küçük bir yapay nöron ağı, önceden hazırlanmış
örnek profiller üzerinden eğitilir ve ardından kullanıcının cevaplarını
alarak bir öneri sunar.

## Nasıl Çalışıyor

Model, deneyim seviyesi, donanım gücü, kararlılık tercihi, oyun/performans
ihtiyacı, NVIDIA ekran kartı varlığı, düşük kaynak tüketimi önemi, macera
isteği ve kurumsal destek beklentisi gibi soruya verilen puanlama cevaplarını sayısal bir vektöre çevirir ve bu vektörü ağdan
geçirir. Çıktı olarak dağıtımlardan hangisinin en uygun olduğunu yüzdelik olasılıklarla
gösterir.

Not: datauret.py dosyasındaki ağrlıkları değiştirerek modelin çıktılarını da 
değiştirirsiniz bir soruda bir distro için ne kadar çok puan verirseniz o 
soruda o kadar daha çok o distroyu ödülllendirir. o puanı düşürürseniz bir o kadar cezalandırır.

## Desteklenen Dağıtımlar

- Linux Mint
- Ubuntu
- Fedora
- CachyOS
- Arch Linux
- openSUSE
- Pop_OS
- Kali Linux
- Pardus
- Tails

## Çalıştırma (Bu Linux için yapılan run_distroai.sh dosyasını anlatır)

run_distroai.sh ile biten dosyayı ve aynı klasörde terminalinizi açın.

1. Çalıştırma İzni Verin:
Terminali açın ve indirdiğiniz veya oluşturduğunuz dosyanın bulunduğu dizine giderek dosyaya çalıştırma yetkisi verin:

```bash
chmod +x run_distroai.sh
```

2. Betiği Çalıştırın:
Ardından betiği çalıştırmanız yeterlidir:

```bash
./run_distroai.sh
```

Betik Nasıl Çalışır?
İlk çalıştırmada bulunduğunuz dizinde temiz bir venv klasörü (sanal ortam) oluşturur.
Sanal ortamı aktif hale getirerek sisteminizdeki global paketleri kirletmeden torch (PyTorch) ve scikit-learn kütüphanelerini yükler.
Verdiğiniz GitHub reposunu distroai_repo adında bir klasöre klonlar. Eğer bu klasör zaten varsa, kodların en güncel halini almak için git pull yapar.
Son olarak hedef klasörün içine girerek yapay zeka uygulamanız olan distroai.py dosyasını otomatik olarak başlatır.

Sorulara 1,2,3,4,5 yazarak cevap verin, model size
en uygun dağıtımı ve diğer ihtimalleri yüzde olarak gösterecektir.

## Hızlı Test İçin

Kendi bilgisayarınıza kurulum yapmadan denemek isteyenler, dosyayı
Google Colab'a yükleyip orada da çalıştırabilir. Colab üzerinde PyTorch
zaten hazır geldiği için sadece kodu bir hücreye yapıştırıp çalıştırmak
yeterlidir.
