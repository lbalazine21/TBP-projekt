from pyswip import Prolog
import tkinter as tk
from tkinter import messagebox
import random
from fpdf import FPDF
from tkinter import ttk

# POVEZIVANJE NAZIVA KOMPONENTI PYTHONA I PROLOGA
prolog_component_map = {
    "Procesor": "procesor",
    "Grafička kartica": "graficka",
    "Matična ploča": "maticna",
    "RAM": "ram",
    "Spremanje": "spremanje",
    "Hlađenje": "hladenje",
}

# VARIJABLE ZA SPREMANJE KONFIGURACIJE I OMILJENIH KOMPONENTI
spremljena_konfiguracija = None
set_omiljenih = set()

# FUNKCIJA ZA SPREMANJE KONFIGURACIJE U PDF
def spremi_u_pdf():
    if spremljena_konfiguracija is None:
        messagebox.showinfo("Informacija", "Nema spremljene konfiguracije za spremanje.")
        return

    pdf = FPDF()
    pdf.add_page()

    # KORIŠTENJE UNICODE FONTA
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', size=12)

    pdf.cell(200, 10, txt="Spremljena konfiguracija", ln=True, align="C")
    pdf.ln(10)

    # ISPISIVANJE KONFIGURACIJE U PDF
    ukupna_cijena = 0
    for tip_komponente, value in spremljena_konfiguracija.items():
        pdf.cell(0, 10, txt=f"{tip_komponente}: {value}", ln=True)
        cijena = int(value.split(' - ')[1].replace('€', ''))
        ukupna_cijena += cijena

    pdf.ln(10)
    pdf.cell(0, 10, txt=f"Ukupna cijena: {ukupna_cijena}€", ln=True)

    try:
        pdf.output("konfiguracija.pdf")
        messagebox.showinfo("Uspjeh", "Konfiguracija je spremljena u PDF.")
    except Exception as e:
        messagebox.showerror("Greška", f"Došlo je do pogreške prilikom spremanja PDF-a: {str(e)}")

# PROZOR ZA PRIKAZIVANJE KONFIGURACIJA I MIJENJANJE KOMPONENTI
def prikazi_konfiguraciju(rezultat=None):
    global odabrane_komponente
    if rezultat:
        odabrane_komponente = rezultat
    
    for widget in root.winfo_children():
        widget.pack_forget()

    tk.Label(root, text="Prikaz konfiguracije", font=("Arial", 14, "bold")).pack(pady=(40,20))

    # MIJENJANJE KOMPONENTI
    def azuriraj_komponentu(vrsta_komponente):
        def odaberi_opciju():
            # MIJENJANJE OPCIJE POJEDINE KOMPONENTE
            nova_komponenta = lista_opcija.get()
            odabrane_komponente[vrsta_komponente] = nova_komponenta

            # AZURIRANJE UKUPNE CIJENE NAKON ODABIRA
            ukupna_cijena = sum([int(comp.split(' - ')[1].replace('€', '')) for comp in odabrane_komponente.values()])
            ukupna_cijena_label.config(text=f"Ukupna cijena: {ukupna_cijena}€")

            # AZURIRANJE IMENA NOVE KOMPONENTE
            for frame in komponenta_frames:
                if frame["type"] == vrsta_komponente:
                    frame["label"].config(text=f"{vrsta_komponente}: {nova_komponenta}")
                    break

            novi_prozor.destroy()

        # NOVI PROZOR ZA MIJENJANJE OPCIJE KOMPONENTE
        novi_prozor = tk.Toplevel(root)
        novi_prozor.resizable(False, False)
        novi_prozor.title(f"Zamjena - {vrsta_komponente}")
        tk.Label(novi_prozor, text=f"Odaberi novu opciju za {vrsta_komponente}").pack(pady=(20,5))
        
        # DEFINIRANJE STRUKTURE PROZORA
        window_width = 600
        window_height = 300
        screen_width = novi_prozor.winfo_screenwidth()
        screen_height = novi_prozor.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (window_width // 2)
        y_coordinate = (screen_height // 2) - (window_height // 2)
        novi_prozor.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # DOHVACANJE OPCIJA I CIJENA IZ PROLOGA
        lista_opcija = tk.StringVar(value="")
        prolog = Prolog()
        prolog.consult("baza.pl")
        query = f"{prolog_component_map[vrsta_komponente]}(X, _, Cijena, _, _)"
        opcije = list(prolog.query(query))
        lista = [f"{op['X']} - {op['Cijena']}€" for op in opcije]

        # POSTAVLJANJE OPCIJA U DROPDOWN MENI
        lista_opcija.set(lista[0])
        option_menu = tk.OptionMenu(novi_prozor, lista_opcija, *lista)
        option_menu.pack(pady=5)

        tk.Button(novi_prozor, text="Odaberi", command=odaberi_opciju).pack(pady=10)

    # PRIKAZIVANJE IMENA KOMPONENTI UNUTAR OKVIRA
    global komponenta_frames
    komponenta_frames = []

    # PRIKAZIVANJE KOMPONENTI I GUMBA ZA MIJENJANJE
    for tip_komponente, value in odabrane_komponente.items():
        frame = tk.Frame(root)
        frame.pack(pady=5, fill="x")

        label = tk.Label(frame, text=f"{tip_komponente}: {value}", anchor="w")
        label.pack(side="left", padx=(50,0), fill="x", expand=True)

        tk.Button(frame, text="Promijeni", command=lambda ct=tip_komponente: azuriraj_komponentu(ct)).pack(side="right", padx=(0,50))
        komponenta_frames.append({"type": tip_komponente, "label": label})

    # UKUPNA CIJENA
    ukupna_cijena = sum([int(val.split(' - ')[1].replace('€', '')) for val in odabrane_komponente.values()])
    ukupna_cijena_label = tk.Label(root, text=f"Ukupna cijena: {ukupna_cijena}€", font=("Arial", 12))
    ukupna_cijena_label.pack(pady=(20,20))

    # GUMB ZA SPREMANJE KONFIGURACIJE
    def spremi_konfiguraciju():
        global spremljena_konfiguracija
        spremljena_konfiguracija = odabrane_komponente.copy()
        messagebox.showinfo("Spremljeno", "Konfiguracija je uspješno spremljena.")

    # GUMBOVI ZA SPREMANJE I POVRATAK
    button_frame = tk.Frame(root)
    button_frame.pack(pady=(20,40))
    tk.Button(button_frame, text="Spremi", command=spremi_konfiguraciju).pack(side="left", padx=5)
    tk.Button(button_frame, text="Povratak", command=vrati_na_pocetni_prozor).pack(side="left", padx=5)

    # IZRAČUN FPS-A ZA ODABRANE IGRE
    def izracunaj_fps(tezinski_faktor):
        prolog = Prolog()
        prolog.consult("baza.pl")
        
        ukupna_ocjena = 1 
        for komponenta, vrijednost in odabrane_komponente.items():
            naziv = vrijednost.split(' - ')[0]
            query = f"{prolog_component_map[komponenta]}('{naziv}', _, _, _, Ocjena)"
            rezultat = list(prolog.query(query))
            if rezultat:
                ukupna_ocjena *= rezultat[0]['Ocjena']
    
        fps = ukupna_ocjena / tezinski_faktor
        return int(fps)

    def prikazi_fps(ime_igre, tezinski_faktor):
        fps = izracunaj_fps(tezinski_faktor)
        messagebox.showinfo("Rezultat", f"Konfiguracija će igricu {ime_igre} pokretati sa {fps} FPS.")

    fps_frame = tk.Frame(root)
    fps_frame.pack(pady=(20, 40))
    tk.Button(fps_frame, text="Minecraft", command=lambda: prikazi_fps("Minecraft", 1)).pack(side="left", padx=5)
    tk.Button(fps_frame, text="League of Legends", command=lambda: prikazi_fps("League of Legends", 1.4)).pack(side="left", padx=5)
    tk.Button(fps_frame, text="GTA V", command=lambda: prikazi_fps("GTA V", 2)).pack(side="left", padx=5)

# PROZOR ZA PRIKAZIVANJE SPREMLJENE KONFIGURACIJE
def prikazi_spremljenu_konfiguraciju():
    if spremljena_konfiguracija is None:
        messagebox.showinfo("Informacija", "Nema spremljene konfiguracije.")
        return

    for widget in root.winfo_children():
        widget.pack_forget()

    tk.Label(root, text="Spremljena konfiguracija", font=("Arial", 14, "bold")).pack(pady=(40,20))

    # PRIKAZIVANJE SPREMLJENIH KOMPONENTI
    ukupna_cijena = 0
    for tip_komponente, value in spremljena_konfiguracija.items():
        tk.Label(root, text=f"{tip_komponente}: {value}").pack(pady=5)
        cijena = int(value.split(' - ')[1].replace('€', ''))
        ukupna_cijena += cijena

    tk.Label(root, text=f"Ukupna cijena: {ukupna_cijena}€", font=("Arial", 12)).pack(pady=(20,20))

    # DODAVANJE GUMBA ZA SPREMANJE U PDF
    button_frame = tk.Frame(root)
    button_frame.pack(pady=(20,40))
    tk.Button(button_frame, text="Spremi u PDF", command=spremi_u_pdf).pack(side="left", padx=5)
    tk.Button(button_frame, text="Izmijeni konfiguraciju", command=lambda: prikazi_konfiguraciju(spremljena_konfiguracija)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Povratak", command=vrati_na_pocetni_prozor).pack(side="left", padx=5)

# PROZOR ZA PRIKAZIVANJE INVENTARA KOMPONENTI
def prikazi_inventar():
    global tree, container, parsirane_komponente

    for widget in root.winfo_children():
        widget.pack_forget()

    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Inventar komponenti", font=("Arial", 14, "bold")).pack(pady=(20, 10))

    # TABLICA I SCROLLBAR
    tree_frame = tk.Frame(container)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
    scrollbar = tk.Scrollbar(tree_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")
    tree = ttk.Treeview(tree_frame, columns=("Omiljena", "Naziv", "Cijena"), show="headings", yscrollcommand=scrollbar.set)
    tree.pack(fill="both", expand=True)
    scrollbar.config(command=tree.yview)

    # STUPCI
    tree.heading("Omiljena", text="✔")
    tree.heading("Naziv", text="Naziv komponente")
    tree.heading("Cijena", text="Cijena (€)")
    tree.column("Omiljena", anchor="center", width=20)
    tree.column("Naziv", anchor="w", width=500)
    tree.column("Cijena", anchor="center", width=100)

    # RETCI
    style = ttk.Style()
    style.configure("Treeview", rowheight=50)

    filter_sort_frame = tk.Frame(container)
    filter_sort_frame.pack(pady=10)

    # DROPDOWN ZA FILTRIRANJE
    tk.Label(filter_sort_frame, text="Komponenta:").pack(side="left", padx=5)
    tip_var = tk.StringVar()
    tip_combo = ttk.Combobox(
        filter_sort_frame,
        textvariable=tip_var,
        values=["Sve", "Procesor", "Grafička kartica", "Matična ploča", "RAM", "Spremanje", "Hlađenje", "Omiljene"],  # Tipovi komponenti
        state="readonly",
        width=15
    )
    tip_combo.pack(side="left", padx=5)
    tip_combo.set("Sve")

    # DROPDOWN ZA SORTIRANJE
    tk.Label(filter_sort_frame, text="Sortiranje:").pack(side="left", padx=5)
    sortiranje_var = tk.StringVar()
    sortiranje_combo = ttk.Combobox(
        filter_sort_frame,
        textvariable=sortiranje_var,
        values=["Uzlazno po imenu", "Silazno po imenu", "Uzlazno po cijeni", "Silazno po cijeni", "Standardno"],
        state="readonly",
        width=15
    )
    sortiranje_combo.pack(side="left", padx=5)
    sortiranje_combo.set("Standardno")

    # OZNAKA ZA OMILJENE KOMPONENTE
    def oznaci_omiljenu(event):
        item = tree.selection()[0]
        values = tree.item(item, "values")
        naziv = values[1]  # Naziv komponente
        if naziv in set_omiljenih:
            set_omiljenih.remove(naziv)  # Uklanja iz omiljenih
            tree.set(item, "Omiljena", "")  # Očisti checkbox
        else:
            set_omiljenih.add(naziv)  # Dodaje u omiljene
            tree.set(item, "Omiljena", "✔")  # Postavi checkbox

    tree.bind("<Double-1>", oznaci_omiljenu)

    # GUMB ZA PRIMJENU FILTRIRANJA I SORTIRANJA
    def primijeni_filter_sort():
        odabrani_tip = tip_var.get().lower()
        odabrano_sortiranje = sortiranje_var.get()

        if odabrani_tip == "sve":
            query_tip = "dohvati_sve_komponente(Komponente)"
        elif odabrani_tip == "omiljene":
            filtriraj_omiljene(odabrano_sortiranje)
            return
        elif odabrani_tip == "grafička kartica":
            query_tip = "dohvati_tip_komponente('graficka', Komponente)"
        elif odabrani_tip == "matična ploča":
            query_tip = "dohvati_tip_komponente('maticna', Komponente)"
        elif odabrani_tip == "hlađenje":
            query_tip = "dohvati_tip_komponente('hladenje', Komponente)"
        else:
            query_tip = f"dohvati_tip_komponente({odabrani_tip}, Komponente)"

        if odabrano_sortiranje == "Uzlazno po imenu":
            sortiranje = "sortiraj_uzlazno_po_imenu"
        elif odabrano_sortiranje == "Silazno po imenu":
            sortiranje = "sortiraj_silazno_po_imenu"
        elif odabrano_sortiranje == "Uzlazno po cijeni":
            sortiranje = "sortiraj_uzlazno_po_cijeni"
        elif odabrano_sortiranje == "Silazno po cijeni":
            sortiranje = "sortiraj_silazno_po_cijeni"
        else:
            sortiranje = None

        ucitaj_komponente(query_tip, sortiranje)

    tk.Button(filter_sort_frame, text="Primijeni", command=primijeni_filter_sort).pack(side="left", padx=5)
    tk.Button(container, text="Povratak", command=vrati_na_pocetni_prozor).pack(pady=20)

    # UCITAVANJE POCETNIH PODATAKA
    prolog = Prolog()
    prolog.consult("baza.pl")
    komponente = list(prolog.query("dohvati_sve_komponente(Komponente)"))
    if komponente and "Komponente" in komponente[0]:
        parsirane_komponente = []
        for komponenta in komponente[0]["Komponente"]:
            komponenta = komponenta.strip("',()")
            naziv, cijena = komponenta.rsplit(", ", 1)
            parsirane_komponente.append((naziv, cijena))
    
    for naziv, cijena in parsirane_komponente:
        omiljena = "✔" if naziv in set_omiljenih else ""
        tree.insert("", "end", values=(omiljena, naziv, cijena))

# FILTRIRANJE OMILJENIH KOMPONENTI
def filtriraj_omiljene(sortiranje):
    global tree, set_omiljenih, parsirane_komponente
    tree.delete(*tree.get_children())

    omiljene_komponente = [komp for komp in parsirane_komponente if komp[0] in set_omiljenih]

    # SORTIRANJE OMILJENIH KOMPONENTI
    if sortiranje == "Uzlazno po imenu":
        omiljene_komponente.sort(key=lambda x: x[0])
    elif sortiranje == "Silazno po imenu":
        omiljene_komponente.sort(key=lambda x: x[0], reverse=True)
    elif sortiranje == "Uzlazno po cijeni":
        omiljene_komponente.sort(key=lambda x: int(x[1]))
    elif sortiranje == "Silazno po cijeni":
        omiljene_komponente.sort(key=lambda x: int(x[1]), reverse=True)

    for naziv, cijena in omiljene_komponente:
        tree.insert("", "end", values=("✔", naziv, cijena))

# UCITAVANJE KOMPONENTI U TABLICU
def ucitaj_komponente(query_tip, sortiranje):
    global tree, parsirane_komponente, set_omiljenih
    tree.delete(*tree.get_children())

    prolog = Prolog()
    prolog.consult("baza.pl")

    # IZVRSAVANJE UPITA IZ PROLOGA
    query = query_tip
    if sortiranje:
        query += f", {sortiranje}(Komponente, Sorted)"
    else:
        query += ", Komponente = Sorted"

    # DOHVACANJE KOMPONENTI I CIJENA IZ PROLOGA
    komponente = list(prolog.query(query))
    parsirane_komponente = [] 
    if komponente and "Sorted" in komponente[0]:
        for komponenta in komponente[0]["Sorted"]:
            komponenta = komponenta.strip("',()").encode('utf-8').decode('utf-8') 
            naziv, cijena = komponenta.rsplit(", ", 1)
            parsirane_komponente.append((naziv, cijena))

    for naziv, cijena in parsirane_komponente:
        omiljena_oznaka = "✔" if naziv in set_omiljenih else ""
        tree.insert("", "end", values=(omiljena_oznaka, naziv, cijena))

# POVRATAK NA POCETNI PROZOR
def vrati_na_pocetni_prozor():
    for widget in root.winfo_children():
        widget.pack_forget()
    postavi_pocetni_prozor()

# PREPORUKA KOMPONENTI
def preporuci_komponente():
    namjena = namjena_var.get()
    proizvodac = proizvodac_var.get()

    try:
        minimalno = int(min_entry.get())
    except ValueError:
        messagebox.showerror("Greška", "Unesite minimalnu vrijednost.")
        return

    try:
        maksimalno = int(max_entry.get())
    except ValueError:
        messagebox.showerror("Greška", "Unesite maksimalnu vrijednost.")
        return

    # KOMUNIKACIJA S PROLOGOM
    prolog = Prolog()
    prolog.consult("baza.pl")
    query = f"preporuci_komponente('{namjena}', {minimalno}, {maksimalno}, '{proizvodac}', P, G, M, R, S, H, CijenaP, CijenaG, CijenaM, CijenaR, CijenaS, CijenaH, UkupnaCijena)"
    rezultati = list(prolog.query(query))

    # PRIKAZ REZULTATA
    if rezultati:
        rezultat = random.choice(rezultati)
        global odabrane_komponente
        odabrane_komponente = {
            'Procesor': f"{rezultat['P']} - {rezultat['CijenaP']}€",
            'Grafička kartica': f"{rezultat['G']} - {rezultat['CijenaG']}€",
            'Matična ploča': f"{rezultat['M']} - {rezultat['CijenaM']}€",
            'RAM': f"{rezultat['R']} - {rezultat['CijenaR']}€",
            'Spremanje': f"{rezultat['S']} - {rezultat['CijenaS']}€",
            'Hlađenje': f"{rezultat['H']} - {rezultat['CijenaH']}€"
        }
        prikazi_konfiguraciju(odabrane_komponente)
    else:
        messagebox.showinfo("Preporuka", "Nema dostupnih komponenti za navedeni budžet i namjenu.")

# POSTAVLJANJE POCETNOG PROZORA
def postavi_pocetni_prozor():
    tk.Label(root, text="Generirajte konfiguraciju", font=("Arial", 14, "bold")).pack(pady=(80,20))

    # NAMJENA
    namjena_frame = tk.Frame(root)
    namjena_frame.pack(pady=(20,10))
    tk.Label(namjena_frame, text="Namjena:").pack(side="left", padx=10)
    namjena_var.set("Gaming") 
    namjena_menu = tk.OptionMenu(namjena_frame, namjena_var, *namjene)
    namjena_menu.pack(side="left", padx=10)

    # PROIZVODAC
    proizvodac_frame = tk.Frame(root)
    proizvodac_frame.pack(pady=(10,10))
    tk.Label(proizvodac_frame, text="Proizvođač:").pack(side="left", padx=10)
    proizvodac_var.set("Intel")
    tk.Radiobutton(proizvodac_frame, text="Intel", variable=proizvodac_var, value="Intel").pack(side="left", padx=10)
    tk.Radiobutton(proizvodac_frame, text="AMD", variable=proizvodac_var, value="AMD").pack(side="left", padx=10)

    # BUDZET
    global min_entry
    global max_entry
    budzet_frame = tk.Frame(root)
    budzet_frame.pack(pady=(10,20))
    tk.Label(budzet_frame, text="Minimalno:").pack(side="left", padx=5, pady=5)
    min_entry = tk.Entry(budzet_frame, width=7)
    min_entry.pack(side="left", pady=5)
    tk.Label(budzet_frame, text="Maksimalno:").pack(side="left", padx=(30,5), pady=5)
    max_entry = tk.Entry(budzet_frame, width=7)
    max_entry.pack(side="left", pady=5)

    # GUMBOVI ZA PREPORUKU, PRIKAZ SPREMLJENE KONFIGURACIJE I INVENTARA
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=(20,10))
    tk.Button(buttons_frame, text="Generiraj", command=preporuci_komponente).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Spremljeno", command=prikazi_spremljenu_konfiguraciju).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Inventar", command=prikazi_inventar).pack(side="left", padx=5)

# POCETNI PROZOR
root = tk.Tk()
root.title("PcPartPicker")
root.resizable(False, False)

# DEFINICIJE PROZORA
window_width = 1200
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width // 2) - (window_width // 2)
y_coordinate = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# VARIJABLE I OPCIJE
namjena_var = tk.StringVar()
proizvodac_var = tk.StringVar()
namjene = ["Gaming", "Office", "Rendering"]

# POSTAVI POCETNI PROZOR
postavi_pocetni_prozor()

root.mainloop()