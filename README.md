# CLI Tabanlı Log Analiz ve Uyarı Aracı

Bu proje, sistem loglarını analiz etmek, belirli kurallara göre filtrelemek ve hem ekrana uyarı basıp hem de rapor oluşturmak amacıyla geliştirilmiştir.

## Özellikler
* **Dosya Bazlı Analiz:** Mevcut log dosyalarını baştan sona tarar.
* **Gerçek Zamanlı İzleme (Tail):** Dosyanın sonuna odaklanarak yeni gelen logları anlık yakalar.
* **Kural Tabanlı Tespit:** Aranacak kelimeler `kurallar.json` dosyasından dinamik olarak okunur.
* **CSV Raporlama:** Tespit edilen loglar `logAdı.csv` dosyasına tarih damgasıyla kaydedilir.

## Çalıştırma Talimatı
### Programı direkt çalıştırmak için:
`python main.py`

#### İmaj oluşturma:
`docker build -t log-analiz-araci .`

#### Konteyner başlatma:
`docker run -it log-analiz-araci`
##### Canlı izleme modunun Docker üzerinde sağlıklı çalışabilmesi için -v(volume) parametresi ile log dosyasının bulunduğu dizinin konteynera bağlanması gerekir.
