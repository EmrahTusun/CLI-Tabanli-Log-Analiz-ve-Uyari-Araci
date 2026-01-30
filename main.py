import json
import time
import os

def kurallari_getir(): #kurallari getirme fonksiyonumu yazdim
    with open('kurallar.json', 'r') as k:#kural dosyami (r=read) okuyor ve ona kisa bir isim veriyorum. k diye
        kural = json.load(k) #python'un json kutuphanesini kullanarak dosyanin icindeki metni sozluk yapisina ceviriyorum.
    return kural["Kural_tabanli_tespit"]#sozlugun icindeki anahtar degere karsilik gelen degerleri tek tek aliyor, 

def rapora_ekle(tarih, log_mesaji, dosya_yolu): #rapor yazma fonsiyonu disaridan zaman, mesaj ve dosya_yolu degiskenlerini aliyor.
    csv_dosyasi = os.path.basename(dosya_yolu).replace(".log", "") + ".csv"# her log icin tutulacak csv dosyasinin adini ayarliyorum mesela "/var/log/auth.log" "auth.csv" seklinde
    with open(csv_dosyasi, 'a') as s:#gene dosya okuyorum gelen mesaji (a ,append) ile csv ye ekliyor.
        log_mesaji2 = log_mesaji.replace(",", ".") #loglardan gelecek mesajlarda virgul varsa degistiriyorum.
        s.write(tarih + "," + log_mesaji2 + "\n")#dosyaya mesaji aralarinda virgul olacak ve tek satir olarak yaziyorum.

def dosya_tara(dosya_yolu, kurallar):
    if not os.path.exists(dosya_yolu): #bakacagimiz log dosyasinin olup olmadigini kotrol ediyoruz.
        print("Dosya yolu bulunamadi hatasi")
        return
    ozet = {}
    for k in kurallar:
        ozet[k] = 0 #kural sayaci
    toplam_satir = 0
    print("\nTarama islemi basladi:")
    with open(dosya_yolu, 'r') as dosya:#dosyayi okuyorum
        for satir in dosya:#satir satir for ile icinde geziyorum.
            toplam_satir += 1
            for kural in kurallar: #kurallarimda ve dosyamin satirlarinda buyuk kucuk harf duyarliligini for dongusu ile ayarliyorum.
                if kural.lower() in satir.lower(): #eger varsa donguye giriyor  
                    ozet[kural] += 1 #bulunan kurallarin sayisi
                    zaman = time.strftime("%Y-%m-%d %H:%M:%S") #bulunma zamani.                    
                    rapora_ekle(zaman, satir.strip(), dosya_yolu) #rapora ekleme 
    print("\n   ANALIZ OZETI")
    print("Incelenen dosya: " + dosya_yolu)
    print("Okunan toplam satir: " + str(toplam_satir))
    print("Bulunan hatalar:")
    for k in ozet:
        if ozet[k]>0:
            print("> " + str(ozet[k]) + " tane " + k + " var.")


def canli_izle(dosya_yolu, kurallar):
    if not os.path.exists(dosya_yolu):
        print("Dosya yolu bulunamadi hatasi")
        return

    print("\nGercek zamanli izleme (tailing) modu: ")
    print("çıkmak için: Ctrl+C ")
    with open(dosya_yolu, 'r') as c: #dosyami okudum ve c dedim kisaca
        c.seek(0, 2)#okuma imlecini baslangictan dosyanin sonuna goturuyorum.
        try:
            while True:
                satir = c.readline() #dosyaya yeni bir satir eklenirse okuyorum.
                if not satir:
                    time.sleep(0.5) #satirda bir degisiklik varmi yokmu bekliyor ve tekrar bakiyor 0.5 saniyeyle 
                    continue
                for kural in kurallar: #bos degilse kontrol ediyoruz.
                    if kural.lower() in satir.lower(): 
                        zaman = time.strftime("%Y-%m-%d %H:%M:%S")
                        print(" [UYARI] " + zaman + " --> " + satir.strip())
                        rapora_ekle(zaman, "CANLI: " + satir.strip(), dosya_yolu)
        except KeyboardInterrupt: #Ctrl+C
            print("\nCanli izleme durduruldu.")

kelimeler = kurallari_getir() #fonksiyon(kurallari) cagirma
    
while True: #sonsuz dongum icin

    print("\n | LOG ANALIZ VE UYARI ARACI |") #secimler icin mesajlar
    print("  ----------------------------")
    print("1- Dosya Bazli Analiz ")
    print("2- Gercek Zamanli Izleme ")
    print("3- Cikis")
        
    secim = input("Seçim için 1-2-3 : ") #kullanicidan alinacak secim
        
    if secim == "1": 
        print("\nAnaliz edilecek dosya yolunu giriniz.")
        dosya = input("örnek yol /var/log/auth.log: ")
        dosya_tara(dosya, kelimeler)
            
    elif secim == "2":
        print("\nİzlenecek dosya yolunu giriniz.")
        dosya = input("örnek yol /var/log/auth.log: ")
        canli_izle(dosya, kelimeler)
            
    elif secim == "3":
        print("cikis yapiliyor.")
        break
            
    else:
        print("Gecersiz secim, lutfen tekrar 1,2,3 numaralarini secin.")
