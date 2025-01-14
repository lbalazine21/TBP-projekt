procesor('Intel Core i5-12600K', 'Intel', 300, ['Gaming', 'Rendering'], 3).
procesor('AMD Ryzen 5 5600X', 'AMD', 250, ['Gaming', 'Rendering'], 3).
procesor('Intel Core i9-12900K', 'Intel', 500, ['Rendering', 'Gaming'], 4).
procesor('Intel Core i7-12700F', 'Intel', 350, ['Gaming', 'Office'], 3).
procesor('AMD Athlon 3000G', 'AMD', 80, ['Office'], 2).
procesor('Intel Core i3', 'Intel', 100, ['Office'], 2).

maticna('Gigabyte Z790 Aorus Elite', 'Intel', 300, ['Rendering', 'Gaming'], 2).
maticna('MSI MAG B660M Mortar', 'Intel', 180, ['Office', 'Gaming'], 2).
maticna('Gigabyte B450M', 'AMD', 100, ['Office', 'Gaming'], 2).
maticna('ASUS Prime H510', 'Intel', 80, ['Office'], 2).
maticna('ASUS TUF Gaming Z690', 'Intel', 200, ['Gaming', 'Rendering'], 2).
maticna('MSI B550-A Pro', 'AMD', 150, ['Gaming', 'Rendering'], 2).

graficka('AMD Radeon RX 6800 XT', 'AMD', 500, ['Rendering', 'Gaming'], 3).
graficka('NVIDIA RTX 3060', 'NVIDIA', 350, ['Gaming', 'Rendering'], 3).
graficka('AMD Radeon RX 6500 XT', 'AMD', 200, ['Gaming'], 2).
graficka('NVIDIA RTX 4090', 'NVIDIA', 1200, ['Rendering', 'Gaming'], 4).
graficka('NVIDIA GTX 1650', 'NVIDIA', 150, ['Office', 'Gaming'], 2).
graficka('AMD Radeon RX 7900 XTX', 'AMD', 1000, ['Rendering', 'Gaming'], 4).

ram('TeamGroup T-Force Delta 32GB', 'TeamGroup', 130, ['Gaming', 'Office'], 2).
ram('G.Skill Trident Z RGB 64GB', 'G.Skill', 250, ['Rendering', 'Gaming'], 3).
ram('Corsair Vengeance 16GB', 'Corsair', 70, ['Gaming', 'Office'], 2).
ram('Kingston Fury 8GB', 'Kingston', 40, ['Office'], 2).
ram('Corsair Dominator Platinum 128GB', 'Corsair', 500, ['Rendering'], 3).
ram('Patriot Viper Steel 32GB', 'Patriot', 140, ['Gaming', 'Rendering'], 2).

spremanje('Crucial MX500 1TB SSD', 'Crucial', 100, ['Gaming', 'Rendering'], 2).
spremanje('WD Black SN850X 4TB SSD', 'WD', 500, ['Rendering'], 3).
spremanje('Kingston A400 240GB SSD', 'Kingston', 30, ['Office'], 2).
spremanje('Samsung 970 Evo Plus 2TB SSD', 'Samsung', 250, ['Rendering', 'Gaming'], 3).
spremanje('ADATA XPG SX8200 Pro 1TB SSD', 'ADATA', 120, ['Gaming', 'Office'], 2).
spremanje('Seagate Barracuda 1TB HDD', 'Seagate', 50, ['Office', 'Gaming'], 2).

hladenje('Deepcool Assassin III', 'Deepcool', 110, ['Gaming', 'Rendering'], 2).
hladenje('Corsair iCUE H150i Elite', 'Corsair', 150, ['Rendering', 'Gaming'], 2).
hladenje('Cooler Master Hyper 212', 'Cooler Master', 50, ['Gaming'], 2).
hladenje('Arctic Freezer 7X', 'Arctic', 30, ['Office'], 2).
hladenje('Be Quiet! Dark Rock Pro 4', 'Be Quiet!', 90, ['Gaming', 'Rendering'], 2).
hladenje('Noctua NH-U12A', 'Noctua', 250, ['Rendering'], 3).

% PRAVILO ZA PREPORUKU KOMPONENTI
preporuci_komponente(Namjena, Minimalno, Maksimalno, Proizvodjac, P, G, M, R, S, H, CijenaP, CijenaG, CijenaM, CijenaR, CijenaS, CijenaH, UkupnaCijena) :-
    procesor(P, ProizvodjacP, CijenaP, NamjeneP, _),
    graficka(G, _, CijenaG, NamjeneG, _),
    maticna(M, ProizvodjacM, CijenaM, NamjeneM, _),
    ram(R, _, CijenaR, NamjeneR, _),
    spremanje(S, _, CijenaS, NamjeneS, _),
    hladenje(H, _, CijenaH, NamjeneH, _),
    ProizvodjacP = Proizvodjac,
    ProizvodjacM = Proizvodjac,
    member(Namjena, NamjeneP),
    member(Namjena, NamjeneG),
    member(Namjena, NamjeneM),
    member(Namjena, NamjeneR),
    member(Namjena, NamjeneS),
    member(Namjena, NamjeneH),
    UkupnaCijena is CijenaP + CijenaG + CijenaM + CijenaR + CijenaS + CijenaH,
    UkupnaCijena >= Minimalno,
    UkupnaCijena =< Maksimalno.

% DOHVATI SVE KOMPONENTE
dohvati_sve_komponente(Komponente) :-
    findall((Naziv, Cijena), (
        procesor(Naziv, _, Cijena, _, _);
        graficka(Naziv, _, Cijena, _, _);
        maticna(Naziv, _, Cijena, _, _);
        ram(Naziv, _, Cijena, _, _);
        spremanje(Naziv, _, Cijena, _, _);
        hladenje(Naziv, _, Cijena, _, _)
    ), Komponente).

% SORTIRANJA
sortiraj_uzlazno_po_imenu(Komponente, Sorted) :-
    sort(1, @=<, Komponente, Sorted).

sortiraj_silazno_po_imenu(Komponente, Sorted) :-
    sort(1, @>=, Komponente, Sorted).

sortiraj_uzlazno_po_cijeni(Komponente, Sorted) :-
    sort(2, @=<, Komponente, Sorted).

sortiraj_silazno_po_cijeni(Komponente, Sorted) :-
    sort(2, @>=, Komponente, Sorted).

% DOHVATI TIP KOMPONENTE
dohvati_tip_komponente(procesor, Komponente) :-
    findall((Naziv, Cijena), procesor(Naziv, _, Cijena, _, _), Komponente).

dohvati_tip_komponente(graficka, Komponente) :-
    findall((Naziv, Cijena), graficka(Naziv, _, Cijena, _, _), Komponente).

dohvati_tip_komponente(maticna, Komponente) :-
    findall((Naziv, Cijena), maticna(Naziv, _, Cijena, _, _), Komponente).

dohvati_tip_komponente(ram, Komponente) :-
    findall((Naziv, Cijena), ram(Naziv, _, Cijena, _, _), Komponente).

dohvati_tip_komponente(spremanje, Komponente) :-
    findall((Naziv, Cijena), spremanje(Naziv, _, Cijena, _, _), Komponente).

dohvati_tip_komponente(hladenje, Komponente) :-
    findall((Naziv, Cijena), hladenje(Naziv, _, Cijena, _, _), Komponente).