# Sinyaller ve Sistemler — Sinyal Görselleştirici

Python (`CustomTkinter` ve `Matplotlib`) kullanılarak geliştirilmiş, sürekli ve ayrık zamanlı 20 farklı temel/özel sinyali etkileşimli olarak görselleştiren masaüstü uygulaması.

## Özellikler
- **20 Sinyal Kütüphanesi:** 10 Temel Sürekli Sinyal ve 10 Ayrık / Periyodik / Modüleli Sinyal.
- **Gerçek Zamanlı Parametre Kontrolü:** Genlik ($A$) ve Frekans / Ölçek ($f$) kaydırıcıları ile anlık grafik ve formül güncellemesi.
- **Akıllı Eksen Ölçekleme:** Pozitif tanımlı sinyaller için `[-0.8, 5.5]`, çift yönlü sinyaller için `[-5.5, 5.5]` sabit genlik aralığı.
- **Modern Arayüz:** Koyu tema destekli, temiz ve sade masaüstü arayüzü.

## Desteklenen Sinyaller

**Temel Sinyaller (10):**
1. Birim Dürtü (Approx) $\delta_w(t)$
2. Birim Basamak $u(t)$
3. Birim Rampa $r(t)$
4. İşaret Fonksiyonu $\text{sgn}(t)$
5. Dikdörtgen Darbe $\text{rect}(t)$
6. Üçgen Darbe $\text{tri}(t)$
7. Sinc Fonksiyonu $\text{sinc}(t)$
8. Üstel Azalan $e^{-at}u(t)$
9. Sinüs Dalgası $\sin(2\pi f t)$
10. Kosinüs Dalgası $\cos(2\pi f t)$

**Diğer Sinyaller (10):**
1. Ayrık Birim Dürtü $\delta[n]$
2. Ayrık Birim Basamak $u[n]$
3. Ayrık Rampa $r[n]$
4. Ayrık Üstel $a^n u[n]$
5. Ayrık Sinüzoid $\sin(\omega n)$
6. Kare Dalga (Square)
7. Testere Dişi (Sawtooth)
8. Sönümlü Sinüzoid
9. Gauss Darbesi
10. Genlik Modülasyonu (AM)

## Kurulum ve Çalıştırma

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/yusuf-kiraz/python-signal-visualizer.git
    cd python-signal-visualizer
   ```

2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Uygulamayı başlatın:
   ```bash
   python3 main.py
   ```

## Kullanılan Teknolojiler
- Python 3
- CustomTkinter
- Matplotlib
- NumPy & SciPy