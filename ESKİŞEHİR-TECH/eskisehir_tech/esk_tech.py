# -*- coding: utf-8 -*-
"""
Created on Sun May 31 23:32:05 2026

@author: Asus
"""

import os
from datetime import datetime

DOSYA_KULLANICILAR = "kullanicilar_notebook.txt"
DOSYA_DEVAMSIZLIK = "devamsizlik_notebook.txt"
DOSYA_NOTLAR = "notlar_notebook.txt"
DOSYA_DEGERLENDIRME = "degerlendirme_notebook.txt"
DOSYA_MESAJLAR = "mesajlar_notebook.txt"

VARSAYILAN_KULLANICILAR = [
    "1|gonul|571|Gönül Arıcı|ogretmen|",
    "2|esmanur|572|Esmanur Örsdemir|ogrenci|",
    "3|naz|573|Naz Efe|ogrenci|",
    "4|bilge|574|Bilge Sapmaz|veli|2"
]

aktif_kullanici_id = ""
aktif_kullanici_adi = ""
aktif_ad_soyad = ""
aktif_rol = ""
aktif_veli_ogrenci_id = ""

def dosyalari_olustur():
    if not os.path.exists(DOSYA_KULLANICILAR):
        dosya = open(DOSYA_KULLANICILAR, "w", encoding="utf-8")
        for k in VARSAYILAN_KULLANICILAR:
            dosya.write(k + "\n")
        dosya.close()

    dosya_listesi = [DOSYA_DEVAMSIZLIK, DOSYA_NOTLAR, DOSYA_DEGERLENDIRME, DOSYA_MESAJLAR]
    for dosya_adi in dosya_listesi:
        if not os.path.exists(dosya_adi):
            dosya = open(dosya_adi, "w", encoding="utf-8")
            dosya.close()

def ogrenci_ismi_bul(ogrenci_id):
    dosyalari_olustur()
    dosya = open(DOSYA_KULLANICILAR, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 5:
            k_id = parcalar[0]
            ad_soyad = parcalar[3]
            rol = parcalar[4]
            if k_id == ogrenci_id and rol == "ogrenci":
                return ad_soyad
    return "Bilinmeyen Öğrenci"

def kullanici_olustur():
    print("\n" + "-"*40)
    print("          YENİ KULLANICI OLUŞTUR")
    print("-"*40)
    print("1. Öğretmen")
    print("2. Öğrenci")
    print("3. Veli")
    rol_secim = input("Kullanıcı rolünü seçin (1-3): ").strip()

    rol = ""
    if rol_secim == "1":
        rol = "ogretmen"
    elif rol_secim == "2":
        rol = "ogrenci"
    elif rol_secim == "3":
        rol = "veli"
    else:
        print("\n[HATA] Geçersiz seçim yaptınız!")
        return

    ad_soyad = input("Adınız Soyadınız: ").strip()
    kullanici_adi = input("Giriş Adınız (Küçük harflerle): ").strip().lower()
    sifre = input("Giriş Şifreniz: ").strip()

    if ad_soyad == "" or kullanici_adi == "" or sifre == "":
        print("\n[HATA] Alanlar boş bırakılamaz!")
        return

    dosya = open(DOSYA_KULLANICILAR, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 2:
            mevcut_kadi = parcalar[1]
            if mevcut_kadi == kullanici_adi:
                print("\n[HATA] Bu kullanıcı adı zaten kayıtlı!")
                return

    en_buyuk_id = 0
    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if parcalar[0].isdigit():
            en_buyuk_id = max(en_buyuk_id, int(parcalar[0]))
    yeni_id = str(en_buyuk_id + 1)

    veli_ogrenci_id = ""

    if rol == "veli":
        ogrenciler = []
        for satir in satirlar:
            satir = satir.strip()
            if satir == "":
                continue
            parcalar = satir.split("|")
            if len(parcalar) >= 5:
                o_id = parcalar[0]
                o_ad = parcalar[3]
                o_rol = parcalar[4]
                if o_rol == "ogrenci":
                    ogrenciler.append([o_id, o_ad])

        if len(ogrenciler) == 0:
            print("\n[HATA] Sistemde kayıtlı öğrenci bulunmadığı için veli oluşturulamaz!")
            return

        print("\nSistemdeki Kayıtlı Öğrenciler:")
        sira = 1
        for og in ogrenciler:
            print(f" {sira}. {og[1]} (ID: {og[0]})")
            sira = sira + 1

        og_secim = input("Kimin velisisiniz? (Öğrenci Sıra Numarasını Girin): ").strip()
        
        if og_secim.isdigit():
            secim_indeks = int(og_secim) - 1
            if secim_indeks >= 0 and secim_indeks < len(ogrenciler):
                secilen_ogrenci = ogrenciler[secim_indeks]
                veli_ogrenci_id = secilen_ogrenci[0]
            else:
                print("\n[HATA] Geçersiz sıra numarası!")
                return
        else:
            print("\n[HATA] Lütfen geçerli bir sayı girin!")
            return

    yeni_satir = f"{yeni_id}|{kullanici_adi}|{sifre}|{ad_soyad}|{rol}|{veli_ogrenci_id}\n"
    
    dosya = open(DOSYA_KULLANICILAR, "a", encoding="utf-8")
    dosya.write(yeni_satir)
    dosya.close()
    
    print(f"\n[BAŞARILI] {ad_soyad} kaydı başarıyla 'kullanicilar_notebook.txt' dosyasına eklendi.")

def giris_yap():
    global aktif_kullanici_id, aktif_kullanici_adi, aktif_ad_soyad, aktif_rol, aktif_veli_ogrenci_id

    print("\n" + "-"*40)
    print("               SİSTEME GİRİŞ")
    print("-"*40)
    kullanici_adi = input("Kullanıcı Adınız: ").strip().lower()
    sifre = input("Şifreniz: ").strip()

    dosya = open(DOSYA_KULLANICILAR, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 5:
            k_id = parcalar[0]
            u_name = parcalar[1]
            pwd = parcalar[2]
            f_name = parcalar[3]
            rol = parcalar[4]
            
            st_id = parcalar[5].strip() if len(parcalar) >= 6 else ""

            if u_name == kullanici_adi and pwd == sifre:
                aktif_kullanici_id = k_id
                aktif_kullanici_adi = u_name
                aktif_ad_soyad = f_name
                aktif_rol = rol
                aktif_veli_ogrenci_id = st_id
                
                print(f"\n[GİRİŞ BAŞARILI] Hoş geldiniz, Sayın {f_name} ({rol.upper()})")
                panel_yonlendir()
                return

    print("\n[HATA] Kullanıcı adı veya şifre yanlış!")

def panel_yonlendir():
    if aktif_rol == "ogretmen":
        ogretmen_paneli()
    elif aktif_rol == "ogrenci":
        ogrenci_paneli()
    elif aktif_rol == "veli":
        veli_paneli()

def ogretmen_paneli():
    devam_et = True
    while devam_et:
        print("\n" + "="*45)
        print(f" ÖĞRETMEN PORTALİ | Aktif: {aktif_ad_soyad}")
        print("="*45)
        print(" 1. Öğrenci Devamsızlık Girişi (Gün-Ay-Yıl)")
        print(" 2. Yeni Ders Notu Ekle (Örn: Algoritma 85)")
        print(" 3. Öğrenci Gelişim Raporu / Değerlendirme Yaz")
        print(" 4. Öğrencilerden Gelen Mesajları Oku")
        print(" 5. Ana Menüye Dön (Oturumu Kapat)")
        print("="*45)
        secim = input("Seçiminiz (1-5): ").strip()

        if secim == "1":
            devamsizlik_giris()
        elif secim == "2":
            not_giris()
        elif secim == "3":
            degerlendirme_yaz()
        elif secim == "4":
            mesajlari_oku()
        elif secim == "5":
            print("\nÖğretmen oturumu kapatıldı.")
            devam_et = False
        else:
            print("\n[HATA] Geçersiz seçim!")

def devamsizlik_giris():
    dosya = open(DOSYA_KULLANICILAR, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    ogrenciler = []
    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 5:
            if parcalar[4] == "ogrenci":
                ogrenciler.append(parcalar)

    if len(ogrenciler) == 0:
        print("\n[BİLGİ] Sistemde kayıtlı öğrenci bulunmuyor.")
        return

    print("\nÖğrenci Listesi:")
    sira = 1
    for og in ogrenciler:
        print(f" {sira}. {og[3]} (ID: {og[0]})")
        sira = sira + 1

    secim = input("İşlem yapılacak öğrenci sıra numarası: ").strip()
    if not secim.isdigit():
        print("\n[HATA] Lütfen bir sayı girin!")
        return

    secim_indeks = int(secim) - 1
    if secim_indeks < 0 or secim_indeks >= len(ogrenciler):
        print("\n[HATA] Geçersiz sıra numarası!")
        return

    secilen_ogrenci = ogrenciler[secim_indeks]

    tarih = input("Tarih Girin (Örn: 24-05-2026 veya Boş bırakıp Enter'a basarak Bugün): ").strip()
    if tarih == "":
        tarih = datetime.now().strftime("%d-%m-%Y")

    print("Devamsızlık Durumu Seçin:")
    print(" 1. GELMEDİ\n 2. GELDİ\n 3. İZİNLİ (Raporlu)")
    durum_secim = input("Seçiminiz (1-3): ").strip()
    
    durum = "GELMEDİ"
    if durum_secim == "2":
        durum = "GELDİ"
    elif durum_secim == "3":
        durum = "İZİNLİ"

    yeni_kayit = f"{secilen_ogrenci[0]}|{tarih}|{durum}|{aktif_ad_soyad}\n"
    
    dosya = open(DOSYA_DEVAMSIZLIK, "a", encoding="utf-8")
    dosya.write(yeni_kayit)
    dosya.close()
    
    print(f"\n[KAYDEDİLDİ] {secilen_ogrenci[3]} için {tarih} tarihindeki durumu '{durum}' olarak kaydedildi.")

def not_giris():
    dosya = open(DOSYA_KULLANICILAR, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    ogrenciler = []
    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 5:
            if parcalar[4] == "ogrenci":
                ogrenciler.append(parcalar)

    if len(ogrenciler) == 0:
        print("\n[BİLGİ] Sistemde kayıtlı öğrenci bulunmuyor.")
        return

    print("\nÖğrenci Listesi:")
    sira = 1
    for og in ogrenciler:
        print(f" {sira}. {og[3]}")
        sira = sira + 1

    secim = input("Not girilecek öğrenci sıra numarası: ").strip()
    if not secim.isdigit():
        print("\n[HATA] Geçersiz giriş!")
        return

    secim_indeks = int(secim) - 1
    if secim_indeks < 0 or secim_indeks >= len(ogrenciler):
        print("\n[HATA] Geçersiz öğrenci seçimi!")
        return

    secilen_ogrenci = ogrenciler[secim_indeks]

    ders_adi = input("Ders / Konu Adı (Örn: Algoritma, Web Tasarimi): ").strip()
    if ders_adi == "":
        print("\n[HATA] Ders adı boş olamaz!")
        return

    puan_str = input("Öğrenci Notu (0-100): ").strip()
    if not puan_str.isdigit():
        print("\n[HATA] Not sayısal bir değer olmalıdır!")
        return

    puan = int(puan_str)
    if puan < 0 or puan > 100:
        print("\n[HATA] Not 0 ile 100 arasında olmalıdır!")
        return

    yeni_not_kaydi = f"{secilen_ogrenci[0]}|{ders_adi}|{puan}\n"
    
    dosya = open(DOSYA_NOTLAR, "a", encoding="utf-8")
    dosya.write(yeni_not_kaydi)
    dosya.close()
    
    print(f"\n[KAYDEDİLDİ] {secilen_ogrenci[3]} - {ders_adi} Notu: {puan} olarak kaydedildi.")

def degerlendirme_yaz():
    dosya = open(DOSYA_KULLANICILAR, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    ogrenciler = []
    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 5:
            if parcalar[4] == "ogrenci":
                ogrenciler.append(parcalar)

    if len(ogrenciler) == 0:
        print("\n[BİLGİ] Sistemde kayıtlı öğrenci bulunmuyor.")
        return

    print("\nÖğrenci Listesi:")
    sira = 1
    for og in ogrenciler:
        print(f" {sira}. {og[3]}")
        sira = sira + 1

    secim = input("Değerlendirme yapılacak öğrenci sıra numarası: ").strip()
    if not secim.isdigit():
        print("\n[HATA] Geçersiz seçim!")
        return

    secim_indeks = int(secim) - 1
    if secim_indeks < 0 or secim_indeks >= len(ogrenciler):
        print("\n[HATA] Geçersiz sıra numarası!")
        return

    secilen_ogrenci = ogrenciler[secim_indeks]

    baslik = input("Değerlendirme Başlığı (Örn: Haftalık Algoritma Gelişimi): ").strip()
    metin = input("Öğretmen Görüşü ve Detaylı Görüşünüz: ").strip()
    tarih = datetime.now().strftime("%d-%m-%Y")

    if baslik == "" or metin == "":
        print("\n[HATA] Alanlar boş bırakılamaz!")
        return

    yeni_degerlendirme = f"{secilen_ogrenci[0]}|{baslik}|{metin}|{tarih}|{aktif_ad_soyad}\n"
    
    dosya = open(DOSYA_DEGERLENDIRME, "a", encoding="utf-8")
    dosya.write(yeni_degerlendirme)
    dosya.close()
    
    print(f"\n[KAYDEDİLDİ] {secilen_ogrenci[3]} için hazırlanan değerlendirme rapora eklendi.")

def mesajlari_oku():
    if not os.path.exists(DOSYA_MESAJLAR):
        print("\n[BİLGİ] Henüz bir mesaj yok.")
        return

    dosya = open(DOSYA_MESAJLAR, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    mesaj_bulundu = False
    print("\n" + "-"*45)
    print("          GELEN ÖĞRENCİ MESAJLARI")
    print("-"*45)

    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 6:
            gonderen_adi = parcalar[1]
            alici_id = parcalar[2]
            konu = parcalar[3]
            icerik = parcalar[4]
            tarih = parcalar[5]

            if alici_id == aktif_kullanici_id:
                print(f"Tarih: {tarih} | Gönderen Öğrenci: {gonderen_adi}")
                print(f"Konu : {konu}")
                print(f"Mesaj: {icerik}")
                print("-" * 40)
                mesaj_bulundu = True

    if not mesaj_bulundu:
        print("Gelen kutunuzda herhangi bir mesaj bulunmamaktadır.")

def ogrenci_paneli():
    devam_et = True
    while devam_et:
        print("\n" + "="*45)
        print(f" ÖĞRENCİ PORTALİ | Aktif: {aktif_ad_soyad}")
        print("="*45)
        print(" 1. Ders Notlarımı Gör (Algoritma vb.)")
        print(" 2. Devamsızlık Takvimimi Gör")
        print(" 3. Gelişim Değerlendirme Raporlarımı Oku")
        print(" 4. Öğretmene Mesaj Gönder / Not Yaz")
        print(" 5. Ana Menüye Dön (Oturumu Kapat)")
        print("="*45)
        secim = input("Seçiminiz (1-5): ").strip()

        if secim == "1":
            ogrenci_not_gor()
        elif secim == "2":
            ogrenci_devamsizlik_gor()
        elif secim == "3":
            ogrenci_degerlendirme_gor()
        elif secim == "4":
            ogretmene_mesaj_gonder()
        elif secim == "5":
            print("\nÖğrenci oturumu kapatıldı.")
            devam_et = False
        else:
            print("\n[HATA] Geçersiz seçim!")

def ogrenci_not_gor():
    if not os.path.exists(DOSYA_NOTLAR):
        print("\nHala girilmiş bir notunuz bulunmuyor.")
        return

    dosya = open(DOSYA_NOTLAR, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    not_bulundu = False
    print("\n" + "-"*40)
    print("                DERS NOTLARIM")
    print("-"*40)

    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 3:
            og_id = parcalar[0]
            ders = parcalar[1]
            puan = parcalar[2]

            if og_id == aktif_kullanici_id:
                print(f" • Ders: {ders:<20} | Notu: {puan}/100")
                not_bulundu = True

    if not not_bulundu:
        print("Sistemde henüz girilmiş bir ders notunuz bulunmuyor.")

def ogrenci_devamsizlik_gor():
    if not os.path.exists(DOSYA_DEVAMSIZLIK):
        print("\nHenüz bir devamsızlık kaydınız yok.")
        return

    dosya = open(DOSYA_DEVAMSIZLIK, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    kayit_bulundu = False
    print("\n" + "-"*40)
    print("             DEVAMSIZLIK BİLGİLERİM")
    print("-"*40)

    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 4:
            og_id = parcalar[0]
            tarih = parcalar[1]
            durum = parcalar[2]
            giren = parcalar[3]

            if og_id == aktif_kullanici_id:
                print(f" • Tarih: {tarih} | Durum: {durum:<8} | Ekleyen: {giren}")
                kayit_bulundu = True

    if not kayit_bulundu:
        print("Tebrikler! Sisteme işlenmiş bir devamsızlık kaydınız bulunmuyor.")

def ogrenci_degerlendirme_gor():
    if not os.path.exists(DOSYA_DEGERLENDIRME):
        print("\nHenüz gelişim değerlendirmeniz bulunmuyor.")
        return

    dosya = open(DOSYA_DEGERLENDIRME, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    rapor_bulundu = False
    print("\n" + "-"*40)
    print("          ÖĞRETMEN GELİŞİM RAPORLARIM")
    print("-"*40)

    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 5:
            og_id = parcalar[0]
            baslik = parcalar[1]
            metin = parcalar[2]
            tarih = parcalar[3]
            ogretmen = parcalar[4]

            if og_id == aktif_kullanici_id:
                print(f"Tarih   : {tarih} | Öğretmen: {ogretmen}")
                print(f"Başlık  : {baslik}")
                print(f"Görüşler: \"{metin}\"")
                print("-" * 35)
                rapor_bulundu = True

    if not rapor_bulundu:
        print("Henüz adınıza yazılmış bir gelişim raporu bulunmuyor.")

def ogretmene_mesaj_gonder():
    dosya = open(DOSYA_KULLANICILAR, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    ogretmenler = []
    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 5:
            if parcalar[4] == "ogretmen":
                ogretmenler.append(parcalar)

    if len(ogretmenler) == 0:
        print("\n[BİLGİ] Sistemde kayıtlı öğretmen bulunmuyor.")
        return

    print("\nSistemdeki Öğretmenler:")
    sira = 1
    for ogr in ogretmenler:
        print(f" {sira}. {ogr[3]} (ID: {ogr[0]})")
        sira = sira + 1

    secim = input("Mesaj gönderilecek öğretmen sıra numarası: ").strip()
    if not secim.isdigit():
        print("\n[HATA] Geçersiz giriş!")
        return

    secim_indeks = int(secim) - 1
    if secim_indeks < 0 or secim_indeks >= len(ogretmenler):
        print("\n[HATA] Geçersiz sıra numarası!")
        return

    secilen_ogretmen = ogretmenler[secim_indeks]

    konu = input("Mesaj Konusu: ").strip()
    icerik = input("Mesajınız: ").strip()
    tarih = datetime.now().strftime("%d-%m-%Y")

    if konu == "" or icerik == "":
        print("\n[HATA] Boş mesaj gönderilemez!")
        return

    yeni_mesaj = f"{aktif_kullanici_id}|{aktif_ad_soyad}|{secilen_ogretmen[0]}|{konu}|{icerik}|{tarih}\n"
    
    dosya = open(DOSYA_MESAJLAR, "a", encoding="utf-8")
    dosya.write(yeni_mesaj)
    dosya.close()
    
    print(f"\n[BAŞARILI] Mesajınız '{secilen_ogretmen[3]}' öğretmenimize iletildi.")

def veli_paneli():
    ogrenci_adi = ogrenci_ismi_bul(aktif_veli_ogrenci_id)

    devam_et = True
    while devam_et:
        print("\n" + "="*45)
        print(f" VELİ PORTALİ | Aktif Veli: {aktif_ad_soyad}")
        print(f" Takip Edilen Öğrenciniz: {ogrenci_adi}")
        print("="*45)
        print(" 1. Öğrencimin Ders Notlarını Gör")
        print(" 2. Öğrencimin Devamsızlık Geçmişini Gör")
        print(" 3. Öğretmenin Öğrencim Hakkındaki Gelişim Raporlarını Oku")
        print(" 4. Ana Menüye Dön (Oturumu Kapat)")
        print("\n (Bilgi: Güvenlik politikası gereği öğrencinin özel mesajları gösterilmez)")
        print("="*45)
        secim = input("Seçiminiz (1-4): ").strip()

        if secim == "1":
            veli_ogrenci_notu_gor()
        elif secim == "2":
            veli_ogrenci_devamsizlik_gor()
        elif secim == "3":
            veli_ogrenci_degerlendirme_gor()
        elif secim == "4":
            print("\nVeli oturumu kapatıldı.")
            devam_et = False
        else:
            print("\n[HATA] Geçersiz seçim!")

def veli_ogrenci_notu_gor():
    if not os.path.exists(DOSYA_NOTLAR):
        print("\nÖğrencinizin henüz bir notu bulunmuyor.")
        return

    dosya = open(DOSYA_NOTLAR, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    not_bulundu = False
    print("\n" + "-"*40)
    print("              ÖĞRENCİMİN DERS NOTLARI")
    print("-"*40)

    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 3:
            og_id = parcalar[0]
            ders = parcalar[1]
            puan = parcalar[2]

            if og_id == aktif_veli_ogrenci_id:
                print(f" • Ders: {ders:<20} | Notu: {puan}/100")
                not_bulundu = True

    if not not_bulundu:
        print("Öğrencinizin sisteme işlenmiş ders notu bulunmamaktadır.")

def veli_ogrenci_devamsizlik_gor():
    if not os.path.exists(DOSYA_DEVAMSIZLIK):
        print("\nÖğrencinizin devamsızlık kaydı yok.")
        return

    dosya = open(DOSYA_DEVAMSIZLIK, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    kayit_bulundu = False
    print("\n" + "-"*40)
    print("          ÖĞRENCİMİN DEVAMSIZLIK GEÇMİŞİ")
    print("-"*40)

    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 4:
            og_id = parcalar[0]
            tarih = parcalar[1]
            durum = parcalar[2]
            giren = parcalar[3]

            if og_id == aktif_veli_ogrenci_id:
                print(f" • Tarih: {tarih} | Durum: {durum:<8} | Ekleyen: {giren}")
                kayit_bulundu = True

    if not kayit_bulundu:
        print("Öğrencinizin sisteme işlenmiş bir devamsızlık kaydı bulunmuyor.")

def veli_ogrenci_degerlendirme_gor():
    if not os.path.exists(DOSYA_DEGERLENDIRME):
        print("\nÖğrencinizin henüz gelişim değerlendirmesi yok.")
        return

    dosya = open(DOSYA_DEGERLENDIRME, "r", encoding="utf-8")
    satirlar = dosya.readlines()
    dosya.close()

    rapor_bulundu = False
    print("\n" + "-"*40)
    print("       ÖĞRETMENİN ÖĞRENCİM HAKKINDAKİ RAPORLARI")
    print("-"*40)

    for satir in satirlar:
        satir = satir.strip()
        if satir == "":
            continue
        parcalar = satir.split("|")
        if len(parcalar) >= 5:
            og_id = parcalar[0]
            baslik = parcalar[1]
            metin = parcalar[2]
            tarih = parcalar[3]
            ogretmen = parcalar[4]

            if og_id == aktif_veli_ogrenci_id:
                print(f"Tarih   : {tarih} | Öğretmen: {ogretmen}")
                print(f"Başlık  : {baslik}")
                print(f"Görüşler: \"{metin}\"")
                print("-" * 35)
                rapor_bulundu = True

    if not rapor_bulundu:
        print("Öğretmen tarafından yazılmış bir gelişim raporu bulunmuyor.")

def baslat():
    dosyalari_olustur()
    
    program_calisiyor = True
    while program_calisiyor:
        print("\n" + "="*50)
        print("     ESKİŞEHİR-TECH YAZILIM AKADEMİSİ YÖNETİM SİSTEMİ")
        print("="*50)
        print(" 1. Sisteme Giriş Yap")
        print(" 2. Yeni Kullanıcı Oluştur")
        print(" 3. Çıkış")
        print("="*50)
        secim = input("Lütfen yapmak istediğiniz işlemi seçin (1-3): ").strip()

        if secim == "1":
            giris_yap()
        elif secim == "2":
            kullanici_olustur()
        elif secim == "3":
            print("\nSistem başarıyla kapatıldı. İyi çalışmalar dileriz!")
            program_calisiyor = False
        else:
            print("\n[HATA] Geçersiz seçim! Lütfen tekrar deneyin.")

if __name__ == "__main__":
    baslat()
























        
        
        
            
        
        



