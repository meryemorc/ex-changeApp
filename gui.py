from tkinter import *
import sqlite3

# Ana pencereyi oluştur
master = Tk()
master.title("Exchanger App")

# Bir Canvas oluştur ve boyutunu ayarla
canvas = Canvas(master, height=600, width=600)
canvas.pack()

# Üst frame
frame_ust = Frame(master, bg='#2980b9')
frame_ust.place(relx=0.1, rely=0.1, relwidth=0.81, relheight=0.15)

mevcut_para_birimi = Label(frame_ust, bg='#2980b9', text="Mevcut Birim:", font="Arial 17 bold")
mevcut_para_birimi.pack(padx=10, pady=10, side=LEFT)

mevcut_para_opsiyon = StringVar(frame_ust)
mevcut_para_opsiyon.set("EUR")
mevcut_para_acılır_menu = OptionMenu(
    frame_ust,
    mevcut_para_opsiyon,
    "USD",
    "EUR",
    "TRY",
    "GBP",
    "JPY",
    "AUD",
    "BRL",
    "CZK",
    "SAR",
    "RUB")
mevcut_para_acılır_menu.pack(padx=10, pady=10, side=LEFT)

dönüştürülecek_para_birimi = Label(frame_ust, bg='#2980b9', text="Dönüştürülecek Para Birim:", font="Arial 17 bold")
dönüştürülecek_para_birimi.pack(padx=10, pady=10, side=LEFT)

hedef_para_opsiyon = StringVar(frame_ust)
hedef_para_opsiyon.set("USD")
hedef_para_acılır_menu = OptionMenu(
    frame_ust,
    hedef_para_opsiyon,
    "USD",
    "EUR",
    "TRY",
    "GBP",
    "JPY",
    "AUD",
    "BRL",
    "CZK",
    "SAR",
    "RUB")
hedef_para_acılır_menu.pack(padx=10, pady=10, side=LEFT)

miktar_label = Label(frame_ust, text="Miktar:", font="Arial 17 bold", bg='#2980b9')
miktar_label.pack(padx=10, pady=10, side=LEFT)

miktar_entry = Entry(frame_ust)
miktar_entry.pack(padx=10, pady=10, side=LEFT)

hesaplama_butonu = Button(frame_ust, text="Hesapla", command=lambda: hesapla())
hesaplama_butonu.pack(padx=10, pady=10, side=LEFT)

sonuc_label = Label(frame_ust, text="Sonuç:", font="Arial 17 bold", bg='#2980b9')
sonuc_label.pack(padx=10, pady=10, side=LEFT)

sonuc_text = Text(frame_ust, height=1, width=20)
sonuc_text.pack(padx=10, pady=10, side=LEFT)

# Altsol ve Altsag frame'leri
frame_altsol = Frame(master, bg='#7fb3d5')
frame_altsol.place(relx=0.1, rely=0.26, relwidth=0.2, relheight=0.40)

frame_altsag = Frame(master, bg='#7fb3d5')
frame_altsag.place(relx=0.31, rely=0.26, relwidth=0.6, relheight=0.40)

doviz_donusumu = Label(frame_altsag, bg='#7fb3d5', text="Döviz Dönüştürme:", font="Arial 17 bold")
doviz_donusumu.pack(padx=10, pady=10, anchor=NW)

tablo_alani = Text(frame_altsag, height=12, width=60)
tablo_alani.tag_configure('style', foreground='#bfbfbf', font=(',Calibri', 7, 'bold'))
tablo_alani.pack()

karsilama_metni = 'Değerleri burda görüntüleyin...'
tablo_alani.insert(END, karsilama_metni, 'style')

kur_butonu = Button(frame_altsag, text="Kuru Görüntüle", command=lambda: goruntule())
kur_butonu.pack(anchor=S)

# Yeni para birimi eklemek için widget'lar (Sol Alt Frame'de)
yeni_birim_label = Label(frame_altsol, text="Yeni Birim:", font="Arial 12 bold", bg='#7fb3d5')
yeni_birim_label.pack(padx=10, pady=10, anchor=NW)

yeni_birim_entry = Entry(frame_altsol)
yeni_birim_entry.pack(padx=10, pady=10, anchor=NW)

kur_degeri_label = Label(frame_altsol, text="Kur Değeri:", font="Arial 12 bold", bg='#7fb3d5')
kur_degeri_label.pack(padx=10, pady=10, anchor=NW)

kur_degeri_entry = Entry(frame_altsol)
kur_degeri_entry.pack(padx=10, pady=10, anchor=NW)

ekle_butonu = Button(frame_altsol, text="Ekle", command=lambda: para_birimi_ekle())
ekle_butonu.pack(padx=10, pady=10, anchor=NW)

def hesapla():
    mevcut_birim = mevcut_para_opsiyon.get()
    hedef_birim = hedef_para_opsiyon.get()
    miktar = miktar_entry.get()

    if not miktar or not miktar.replace('.', '', 1).isdigit():
        sonuc_text.delete(1.0, END)  # Önceki içeriği temizle
        sonuc_text.insert(END, "Geçerli bir miktar girin")
        return

    miktar = float(miktar)

    conn = sqlite3.connect('currency.db')
    cursor = conn.cursor()

    # Mevcut birimin kuru (TRY'ye göre)
    cursor.execute('SELECT rate_to_usd FROM currency WHERE name=?', (mevcut_birim,))
    mevcut_rate_row = cursor.fetchone()
    if mevcut_rate_row is None:
        sonuc_text.delete(1.0, END)
        sonuc_text.insert(END, "Mevcut birim bulunamadı")
        conn.close()
        return
    mevcut_rate = mevcut_rate_row[0]

    # Hedef birimin kuru (TRY'ye göre)
    cursor.execute('SELECT rate_to_usd FROM currency WHERE name=?', (hedef_birim,))
    hedef_rate_row = cursor.fetchone()
    if hedef_rate_row is None:
        sonuc_text.delete(1.0, END)
        sonuc_text.insert(END, "Hedef birim bulunamadı")
        conn.close()
        return
    hedef_rate = hedef_rate_row[0]

    conn.close()

    # Dönüşüm hesaplama
    if mevcut_birim == "TRY" and hedef_birim != "TRY":
        sonuc = miktar * (1 / hedef_rate)  # TRY'den diğer birime dönüşüm
    elif mevcut_birim != "TRY" and hedef_birim == "TRY":
        sonuc = miktar * mevcut_rate  # Diğer birimden TRY'ye dönüşüm
    else:
        sonuc = miktar * (hedef_rate / mevcut_rate)  # Diğer birimden diğer birime dönüşüm

    sonuc_text.delete(1.0, END)  # Önceki içeriği temizle
    sonuc_text.insert(END, f"{sonuc:.2f} {hedef_birim}")

def goruntule():
    conn = sqlite3.connect('currency.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name, rate_to_usd FROM currency')
    rows = cursor.fetchall()
    conn.close()

    tablo_alani.delete(1.0, END)  # Önceki içeriği temizle
    for row in rows:
        tablo_alani.insert(END, f"{row[0]}: {row[1]:.2f} TRY\n")

def para_birimi_ekle():
    yeni_birim = yeni_birim_entry.get().upper()
    kur_degeri = kur_degeri_entry.get()

    if not yeni_birim or not kur_degeri.replace('.', '', 1).isdigit():
        tablo_alani.insert(END, "Geçerli bir para birimi ve kur değeri girin.\n")
        return

    kur_degeri = float(kur_degeri)

    conn = sqlite3.connect('currency.db')
    cursor = conn.cursor()

    # Yeni para birimini veritabanına ekle
    cursor.execute('INSERT INTO currency (name, rate_to_usd) VALUES (?, ?)', (yeni_birim, kur_degeri))
    conn.commit()
    conn.close()

    tablo_alani.insert(END, f"{yeni_birim} başarıyla eklendi!\n")

    # Girdileri temizle
    yeni_birim_entry.delete(0, END)
    kur_degeri_entry.delete(0, END)

master.mainloop()
