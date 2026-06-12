import re

import streamlit as st

st.set_page_config(page_title="Asystent - Finanse Międzynarodowe", layout="wide")

# Podpis w lewym górnym rogu
st.sidebar.success("Narzędzie zostało stworzone przez:\n**Kacper Żywczak 195477**")
st.sidebar.markdown("---")

# Menu boczne (zawsze widoczne pozycje)
st.sidebar.markdown("### Wybierz moduł do obliczeń:")
opcja = st.sidebar.radio(
    "Moduły",
    [
        "1. Odwracanie kursów",
        "2. Kursy krzyżowe (Bid/Ask)",
        "3. Kontrakty FRA (Pojedyncza transakcja)",
        "4. Portfel FRA (Złożona strategia)",
        "5. Kontrakty Forward (Zabezpieczenie walutowe)",
        "6. Hedging Krzyżowy (Cross-Hedging)",
        "7. Forwardy Towarowe i Ryzyko Bazy",
        "8. Emisja Obligacji i Lokaty (Strip FRA)",
        "9. Wyszukiwarka Teorii (Baza Wiedzy)",
    ],
    label_visibility="collapsed",
)

st.title("🌍 Kalkulator Zadań: Finanse Międzynarodowe")
st.markdown("Wypełniaj pola od lewej do prawej. Aplikacja automatycznie dobierze odpowiednie pozycje rynkowe.")
st.markdown("---")

# --------------------------------------------------------------------------------
# MODUŁ 1: ODWRACANIE KURSÓW
# --------------------------------------------------------------------------------
if opcja == "1. Odwracanie kursów":
    st.header("🔄 Odwracanie kursów walutowych")

    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "Spójrz na treść zadania. Jeśli masz podany kurs w formacie `A/B`, a każą znaleźć `B/A` (np. masz USD/PLN, a szukasz PLN/USD):\n"
            "1. Jako 'Walutę bazową' wpisz pierwszą walutę z zadania (np. USD).\n"
            "2. Jako 'Walutę kwotowaną' wpisz drugą walutę (np. PLN).\n"
            "3. Pierwsza kwota w zadaniu to najczęściej mniejsza cyfra (Kupno/Bid), druga to większa (Sprzedaż/Ask). Wpisz je poniżej.")

    col1, col2, col3 = st.columns(3)
    with col1:
        waluta_bazowa = st.text_input("Pierwsza waluta z zadania (bazowa)", "USD")
    with col2:
        waluta_kwotowana = st.text_input("Druga waluta z zadania (kwotowana)", "PLN")

    col4, col5 = st.columns(2)
    with col4:
        kurs_bid = st.number_input("Wpisz niższy kurs (Bid / Kupno)", value=3.6480, format="%.4f", step=0.0001)
    with col5:
        kurs_ask = st.number_input("Wpisz wyższy kurs (Ask / Sprzedaż)", value=3.7828, format="%.4f", step=0.0001)

    if st.button("Wylicz nowy kurs"):
        if kurs_bid > kurs_ask:
            st.warning("⚠️ Pierwszy kurs (Bid) jest WIĘKSZY od drugiego (Ask). Najpewniej zamieniłeś pola — sprawdź zadanie zanim przepiszesz wynik.")

        odwrotny_bid = 1 / kurs_ask
        odwrotny_ask = 1 / kurs_bid

        st.success(f"**Gotowy wynik:** Odwrócony kurs {waluta_kwotowana}/{waluta_bazowa} wynosi **{odwrotny_bid:.4f} - {odwrotny_ask:.4f}**")

        st.subheader("Rozpisanie na kartkę:")
        st.latex(rf"Bid_{{{waluta_kwotowana}/{waluta_bazowa}}} = \frac{{1}}{{Ask_{{{waluta_bazowa}/{waluta_kwotowana}}}}} = \frac{{1}}{{{kurs_ask}}} = {odwrotny_bid:.4f}")
        st.latex(rf"Ask_{{{waluta_kwotowana}/{waluta_bazowa}}} = \frac{{1}}{{Bid_{{{waluta_bazowa}/{waluta_kwotowana}}}}} = \frac{{1}}{{{kurs_bid}}} = {odwrotny_ask:.4f}")

# --------------------------------------------------------------------------------
# MODUŁ 2: KURSY KRZYŻOWE (wersja automatyczna)
# --------------------------------------------------------------------------------
elif opcja == "2. Kursy krzyżowe (Bid/Ask)":
    st.header("✖️ Wyznaczanie kursów krzyżowych")

    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "1. Przepisz z zadania OBIE pary walutowe dokładnie tak, jak są zapisane (np. `EUR/USD`), razem z ich kursami Bid (niższy) i Ask (wyższy).\n"
            "2. W trzeciej kolumnie wpisz parę, o którą pyta zadanie (np. `USD/GBP`).\n"
            "3. Program SAM rozpozna walutę wspólną, sam zdecyduje czy mnożyć, dzielić czy odwracać i pokaże Ci gotowy wzór do przepisania.\n\n"
            "📌 Jeśli zadanie podaje tylko **kurs średni** (jedna liczba, np. zad. o GBP/CHF), wpisz tę samą wartość w pole Bid i Ask.")

    def parse_pair(txt):
        czysty = txt.replace(" ", "").upper()
        czesci = czysty.split("/")
        if len(czesci) != 2 or not czesci[0] or not czesci[1] or czesci[0] == czesci[1]:
            return None
        return (czesci[0], czesci[1])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Para nr 1 z zadania**")
        para1_txt = st.text_input("Nazwa pary 1 (format: XXX/YYY)", "EUR/USD")
        p1_bid = st.number_input("Niższy kurs (Bid) pary 1", value=1.1577, format="%.4f", step=0.0001)
        p1_ask = st.number_input("Wyższy kurs (Ask) pary 1", value=1.1578, format="%.4f", step=0.0001)
    with c2:
        st.markdown("**Para nr 2 z zadania**")
        para2_txt = st.text_input("Nazwa pary 2 (format: XXX/YYY)", "EUR/GBP")
        p2_bid = st.number_input("Niższy kurs (Bid) pary 2", value=0.8402, format="%.4f", step=0.0001)
        p2_ask = st.number_input("Wyższy kurs (Ask) pary 2", value=0.8405, format="%.4f", step=0.0001)
    with c3:
        st.markdown("**Czego szuka zadanie?**")
        cel_txt = st.text_input("Para wynikowa (np. USD/GBP)", "USD/GBP")
        st.caption("Kolejność ma znaczenie! USD/GBP to NIE to samo co GBP/USD. Przepisz dokładnie tak, jak w poleceniu.")

    if st.button("Policz kurs krzyżowy"):
        para1 = parse_pair(para1_txt)
        para2 = parse_pair(para2_txt)
        cel = parse_pair(cel_txt)

        if not (para1 and para2 and cel):
            st.error("Wpisz wszystkie pary w formacie XXX/YYY (dwie RÓŻNE waluty rozdzielone ukośnikiem), np. EUR/USD.")
        else:
            wspolne = set(para1) & set(para2)
            if len(wspolne) == 0:
                st.error("Obie pary muszą mieć JEDNĄ walutę wspólną (np. EUR/USD i EUR/GBP mają wspólne EUR). Sprawdź, czy dobrze przepisałeś nazwy.")
            elif len(wspolne) == 2:
                st.error("Obie pary składają się z tych samych walut — to nie jest kurs krzyżowy, tylko odwrócenie kursu. Użyj **Modułu 1**.")
            else:
                X = wspolne.pop()
                if X in cel:
                    st.error(f"Waluta wspólna ({X}) nie może występować w parze wynikowej. Jeśli chcesz odwrócić kurs — użyj **Modułu 1**.")
                elif set(cel) != (set(para1) | set(para2)) - {X}:
                    st.error("Para wynikowa musi składać się z dwóch walut NIE-wspólnych (po jednej z każdej pary). Sprawdź pisownię.")
                else:
                    # Każdą nogę liczymy w kierunku: waluta bazowa wyniku -> waluta wspólna -> waluta kwotowana wyniku.
                    # Jeśli para z zadania jest zapisana "w drugą stronę", odwracamy ją (Bid = 1/Ask, Ask = 1/Bid).
                    def noga(od, do):
                        for (para, b, a) in [(para1, p1_bid, p1_ask), (para2, p2_bid, p2_ask)]:
                            nazwa = f"{para[0]}/{para[1]}"
                            if (od, do) == para:
                                return (b, a,
                                        rf"Bid_{{{nazwa}}}", rf"Ask_{{{nazwa}}}",
                                        f"{b:.4f}", f"{a:.4f}",
                                        f"kurs {nazwa} bierzemy wprost")
                            if (od, do) == (para[1], para[0]):
                                return (1 / a, 1 / b,
                                        rf"\frac{{1}}{{Ask_{{{nazwa}}}}}", rf"\frac{{1}}{{Bid_{{{nazwa}}}}}",
                                        rf"\frac{{1}}{{{a:.4f}}}", rf"\frac{{1}}{{{b:.4f}}}",
                                        f"kurs {nazwa} odwracamy")
                        return None

                    n1 = noga(cel[0], X)
                    n2 = noga(X, cel[1])
                    wynik_bid = n1[0] * n2[0]
                    wynik_ask = n1[1] * n2[1]
                    nazwa_cel = f"{cel[0]}/{cel[1]}"

                    st.success(f"**Gotowy wynik:** {nazwa_cel} = **{wynik_bid:.4f} - {wynik_ask:.4f}**")
                    st.caption(f"🧭 Waluta wspólna: **{X}**. Schemat: {n1[6]}, następnie {n2[6]}; wyniki cząstkowe MNOŻYMY (Bid×Bid oraz Ask×Ask).")

                    st.subheader("Rozpisanie na kartkę:")
                    st.latex(rf"Bid_{{{nazwa_cel}}} = {n1[2]} \times {n2[2]} = {n1[4]} \times {n2[4]} = {wynik_bid:.4f}")
                    st.latex(rf"Ask_{{{nazwa_cel}}} = {n1[3]} \times {n2[3]} = {n1[5]} \times {n2[5]} = {wynik_ask:.4f}")
                    st.caption("Wynik podany z dokładnością do 4 miejsc po przecinku — zaokrąglij tak, jak wymaga prowadzący.")

# --------------------------------------------------------------------------------
# MODUŁ 3: KONTRAKTY FRA (Pojedyncze)
# --------------------------------------------------------------------------------
elif opcja == "3. Kontrakty FRA (Pojedyncza transakcja)":
    st.header("🛡️ Zabezpieczanie stóp procentowych (FRA)")

    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "1. Co chce zrobić firma? Jeśli ma kasę ('ulokować nadwyżkę') ➔ wybierz **Lokata**. Jeśli chce pożyczyć ('zaciągnąć kredyt') ➔ wybierz **Kredyt**.\n"
            "2. Notacja **2x5** oznacza: transakcja ZACZYNA SIĘ za 2 miesiące i TRWA 3 miesiące (bo 5 - 2 = 3). Wpisz start i czas trwania w pola poniżej.\n"
            "3. Przepisz kwotę oraz kursy FRA z tabeli (Bid to mniejszy, Ask to większy).\n"
            "4. W polu 'Scenariusze WIBOR' wpisz WSZYSTKIE stopy z podpunktów a), b), c) — rozdziel je średnikami. Dostaniesz gotową tabelkę do każdego podpunktu.")

    c1, c2, c3 = st.columns(3)
    with c1:
        typ_ekspozycji = st.selectbox("Co robi firma w zadaniu?",
                                      ["Kredyt (Potrzebuje pieniędzy / PŁACI odsetki)",
                                       "Lokata (Ma nadwyżkę / OTRZYMUJE odsetki)"])
        is_lokata = typ_ekspozycji.startswith("Lokata")
        kwota = st.number_input("Kwota z zadania (PLN)", value=15000000, step=100000)
    with c2:
        start_za = st.number_input("Start transakcji (za ile miesięcy?)", value=4, step=1, min_value=0)
        trwa = st.number_input("Czas trwania (ile miesięcy będzie trwać?)", value=6, step=1, min_value=1)
    with c3:
        if is_lokata:
            marza = 0.0
            st.caption("ℹ️ Marża banku dotyczy tylko KREDYTU — przy lokacie nic nie doliczamy, więc pole jest ukryte.")
        else:
            marza = st.number_input("Marża banku z zadania (w %; jeśli brak — zostaw 0)", value=1.80, step=0.01)

    st.markdown(f"> 🔎 **Automatyczna podpowiedź:** Szukaj w tabelce kontraktu FRA o symbolu: **{start_za}X{start_za + trwa}**")

    st.markdown("---")
    c4, c5, c6 = st.columns(3)
    with c4:
        fra_bid = st.number_input("Niższy kurs FRA z tabeli (Bid w %)", value=5.128, step=0.001, format="%.3f")
    with c5:
        fra_ask = st.number_input("Wyższy kurs FRA z tabeli (Ask w %)", value=5.138, step=0.001, format="%.3f")
    with c6:
        scenariusze_txt = st.text_input("Scenariusze WIBOR z zadania (%) — rozdziel średnikami", "5.40; 5.90; 6.15")

    if st.button("Pokaż jak rozliczyć to zadanie"):
        surowe = [s.strip().replace(",", ".") for s in scenariusze_txt.split(";") if s.strip()]
        try:
            lista_wibor = [float(s) for s in surowe]
        except ValueError:
            lista_wibor = []

        if not lista_wibor:
            st.error("Nie udało się odczytać scenariuszy WIBOR. Wpisz np.: 5.40; 5.90; 6.15")
        else:
            typ_fra = "SPRZEDAŻ kontraktu FRA (pozycja krótka na rynku)" if is_lokata else "KUPNO kontraktu FRA (pozycja długa na rynku)"
            kurs_fra = fra_bid if is_lokata else fra_ask
            uzasadnienie = ("Spółka zabezpiecza się przed SPADKIEM stóp procentowych. Sprzedaż FRA 'zamraża' jej stały zysk z lokaty."
                            if is_lokata else
                            "Spółka zabezpiecza się przed WZROSTEM stóp procentowych. Kupno FRA 'zamraża' stały koszt kredytu, chroniąc przed podwyżkami.")

            st.success(f"**Co musisz napisać na kolokwium (Wybór strategii):**\n\n"
                       f"Należy zawrzeć pozycję: **{typ_fra}**.\n\n"
                       f"**Dlaczego?** {uzasadnienie}\n\n"
                       f"**Zastosowany kurs (Cena FRA):** Używamy kursu {'Bid' if is_lokata else 'Ask'} wynoszącego **{kurs_fra:.3f}%**.")

            czas_ulamek = trwa / 12
            fra_dec = kurs_fra / 100

            wiersze = []
            for w in lista_wibor:
                w_dec = w / 100
                roznica = w_dec - fra_dec
                rozliczenie = kwota * abs(roznica) * czas_ulamek / (1 + w_dec * czas_ulamek)

                if abs(roznica) < 1e-12:
                    kierunek = "Brak rozliczenia (WIBOR = FRA)"
                elif is_lokata:
                    kierunek = "✅ Spółka OTRZYMUJE płatność" if w < kurs_fra else "❌ Spółka PŁACI rozliczenie"
                else:
                    kierunek = "✅ Spółka OTRZYMUJE płatność" if w > kurs_fra else "❌ Spółka PŁACI rozliczenie"

                wiersze.append({
                    "WIBOR w dniu startu (%)": f"{w:.2f}",
                    "Rozliczenie FRA (PLN)": f"{rozliczenie:,.2f}",
                    "Kierunek płatności": kierunek,
                    "Stopa efektywna BEZ zabezpieczenia (%)": f"{w + marza:.3f}",
                    "Stopa efektywna Z zabezpieczeniem (%)": f"{kurs_fra + marza:.3f}",
                })

            st.subheader("Tabela do podpunktów a), b), c):")
            st.table(wiersze)
            if marza > 0:
                st.caption(f"ℹ️ Obie kolumny ze stopami zawierają już marżę banku (+{marza:.2f} p.p.).")
            st.caption("🎯 **Kluczowy wniosek do komentarza:** kwota rozliczenia FRA (wypłacana z dyskontem) dokładnie kompensuje różnicę między rynkowym WIBOR-em a stopą FRA — dlatego stopa Z zabezpieczeniem jest STAŁA we wszystkich scenariuszach. Na tym polega skuteczność hedgingu.")

            with st.expander("📝 Rozpisanie wzoru dla każdego scenariusza (przepisz na kartkę)"):
                for w in lista_wibor:
                    w_dec = w / 100
                    rozliczenie = kwota * abs(w_dec - fra_dec) * czas_ulamek / (1 + w_dec * czas_ulamek)
                    st.markdown(f"**Scenariusz WIBOR = {w:.2f}%:**")
                    st.latex(rf"\text{{Kwota rozliczenia}} = \frac{{{kwota:,.0f} \times |{w_dec:.4f} - {fra_dec:.4f}| \times \frac{{{trwa}}}{{12}}}}{{1 + {w_dec:.4f} \times \frac{{{trwa}}}{{12}}}} = {rozliczenie:,.2f}\ \text{{PLN}}")

# --------------------------------------------------------------------------------
# MODUŁ 4: PORTFEL FRA
# --------------------------------------------------------------------------------
elif opcja == "4. Portfel FRA (Złożona strategia)":
    st.header("🗂️ Złożona strategia (Portfel FRA)")

    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "Zadanie opisuje KILKA przyszłych transakcji na raz (np. 'za 3 miesiące klient wpłaci 25 mln', 'za 6 miesięcy bank udzieli kredytu 40 mln'). Wpisz każdą w osobnym wierszu.\n\n"
            "⚠️ **NAJWAŻNIEJSZA PUŁAPKA — patrz z perspektywy podmiotu z zadania:**\n"
            "- Jeśli BANK **udziela** kredytu klientowi ➔ bank będzie OTRZYMYWAĆ odsetki ➔ to jest AKTYWO ➔ wybierz pierwszą opcję (sprzedaż FRA)!\n"
            "- Opcję 'będziemy PŁACIĆ odsetki' wybierz tylko wtedy, gdy podmiot SAM zaciąga dług / pozyskuje finansowanie.\n"
            "- 'Napływ środków, które zostaną zainwestowane' = przyszła lokata = OTRZYMUJEMY odsetki.")

    OPCJA_AKTYWO = "Będziemy OTRZYMYWAĆ odsetki (lokata / inwestycja / UDZIELENIE komuś kredytu)"
    OPCJA_PASYWO = "Będziemy PŁACIĆ odsetki (ZACIĄGNIĘCIE kredytu / pozyskanie finansowania)"

    liczba = st.number_input("Ile transakcji opisuje zadanie?", min_value=1, max_value=6, value=3, step=1)

    st.subheader("Wypisz z zadania wszystkie zaplanowane działania:")

    domyslne = [(25.0, 3, 6), (40.0, 6, 6), (20.0, 9, 3), (10.0, 3, 3), (10.0, 6, 3), (10.0, 9, 3)]
    transakcje = []
    for i in range(int(liczba)):
        d_kwota, d_start, d_trwa = domyslne[i]
        kol = st.columns(4)
        with kol[0]:
            typ = st.selectbox(f"Transakcja {i + 1}: rola odsetek", [OPCJA_AKTYWO, OPCJA_PASYWO], key=f"t{i}_typ")
        with kol[1]:
            kw = st.number_input(f"Ile milionów? (T{i + 1})", value=d_kwota, step=1.0, key=f"t{i}_k")
        with kol[2]:
            s = st.number_input(f"Za ile miesięcy rusza? (T{i + 1})", value=d_start, step=1, min_value=0, key=f"t{i}_s")
        with kol[3]:
            t = st.number_input(f"Na jaki czas (miesiące)? (T{i + 1})", value=d_trwa, step=1, min_value=1, key=f"t{i}_t")
        transakcje.append((typ, kw, s, t))

    if st.button("Pokaż jak opisać cały portfel"):
        symbole = []
        for i, (typ, kw, s, t) in enumerate(transakcje, start=1):
            kontrakt = f"{s}X{s + t}"
            symbole.append(kontrakt)
            if typ == OPCJA_AKTYWO:
                akcja = "SPRZEDAŻ kontraktu FRA (stosujemy kurs Bid)"
                cel = "ochrona przed SPADKIEM stóp procentowych — przyszła pozycja w aktywach odsetkowych (otrzymywane odsetki)"
            else:
                akcja = "KUPNO kontraktu FRA (stosujemy kurs Ask)"
                cel = "ochrona przed WZROSTEM stóp procentowych — przyszła pozycja w pasywach odsetkowych (płacone odsetki)"

            st.success(f"**Co musisz napisać dla Transakcji {i}:**\n\n"
                       f"Należy użyć kontraktu **{kontrakt}** na nominał **{kw:g} mln PLN**. Właściwa decyzja to **{akcja}**.\n\n"
                       f"Uzasadnienie: *{cel}.*")

        st.markdown(f"> 🔎 **Symbole do odszukania w tabeli kwotowań:** {', '.join(symbole)}")
        st.caption("📌 Jeśli któregoś symbolu nie ma w tabeli z zadania — napisz, że dany okres pozostaje niezabezpieczony lub wymaga najbliższego dostępnego kontraktu (prowadzący sprawdza, czy to zauważysz).")

# --------------------------------------------------------------------------------
# MODUŁ 5: KONTRAKTY FORWARD
# --------------------------------------------------------------------------------
elif opcja == "5. Kontrakty Forward (Zabezpieczenie walutowe)":
    st.header("💱 Kontrakty Forward (Zabezpieczenie kursu)")

    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "1. Co kupuje/sprzedaje firma z zadania?\n"
            "- Ściąga towar z zagranicy (Import) i **Musi zapłacić** np. w USD? Zaznacz 'Import (płatność faktury)'.\n"
            "- Wysyła towar (Eksport) i **Dostanie pieniądze** np. w EUR? Zaznacz 'Eksport (wpływy z zewnątrz)'.\n"
            "2. Wpisz kwotę waluty, którą firma ma zapłacić/otrzymać.\n"
            "3. **UWAGA NA JPY (Jeny japońskie)!** Zaznacz ptaszka w polu obok, jeśli kwotowanie z tabeli jest podane za 100 jednostek (tak jest zawsze przy JPY).")

    c1, c2 = st.columns(2)
    with c1:
        rodzaj_transakcji = st.selectbox("Cel działania w zadaniu?",
                                         ["Import (Firma ma dług / Płatność faktury w walucie)",
                                          "Eksport (Firma zarobiła / Wpływ na konto w walucie)"])
        kwota_fx = st.number_input("Wpisz kwotę z zadania (w walucie obcej)", value=2400000, step=100000)
        mnoznik_jpy = st.checkbox("Zaznacz to, jeśli walutą w zadaniu są Jeny (JPY) lub kwotowanie jest za 100 jednostek")

    with c2:
        tryb_wprowadzania = st.radio("Jak zadanie podaje kursy rynkowe?",
                                     ["Są gotowe kursy (Bid/Ask) Forward podane na tacy",
                                      "Zadanie podaje kurs SPOT i oddzielnie Punkty Swap"])
        if tryb_wprowadzania == "Są gotowe kursy (Bid/Ask) Forward podane na tacy":
            kurs_fwd_bid = st.number_input("Niższy kurs Forward (Bid)", value=3.9425, format="%.4f", step=0.0001)
            kurs_fwd_ask = st.number_input("Wyższy kurs Forward (Ask)", value=3.9575, format="%.4f", step=0.0001)
        else:
            spot_bid = st.number_input("Niższy kurs Spot (Bid)", value=4.3320, format="%.4f", step=0.0001)
            spot_ask = st.number_input("Wyższy kurs Spot (Ask)", value=4.3320, format="%.4f", step=0.0001)
            swap = st.number_input("Punkty Swap z zadania (DYSKONTO wpisz z minusem, np. -0.0022)", value=0.0155, format="%.4f", step=0.0001)
            kurs_fwd_bid = spot_bid + swap
            kurs_fwd_ask = spot_ask + swap
            st.info(f"Program wyliczył kursy Forward: Bid = {kurs_fwd_bid:.4f}, Ask = {kurs_fwd_ask:.4f}")
            st.caption("⚠️ Ten tryb daje kurs PRZYBLIŻONY (punkty swap z tabeli liczone są zwykle od kursu średniego). "
                       "Jeśli tabela z zadania ma gotowe kolumny 'Forward Bid' i 'Forward Ask' — zawsze wybieraj pierwszy tryb!")

    if st.button("Pokaż rozliczenie zabezpieczenia"):
        is_import = "Import" in rodzaj_transakcji
        typ_fwd = "KUPNO kontraktu Forward po kursie wyższym (Ask)" if is_import else "SPRZEDAŻ kontraktu Forward po kursie niższym (Bid)"
        zastosowany_kurs = kurs_fwd_ask if is_import else kurs_fwd_bid

        dzielnik = 100 if mnoznik_jpy else 1
        kwota_pln = (kwota_fx / dzielnik) * zastosowany_kurs

        wyjasnienie = ("Firma IMPORTOWA musi zapłacić fakturę dostawcy. Nie ma waluty, więc musi ją KUPIĆ na rynku Forward — bank sprzedaje walutę po kursie Ask (gorszym dla klienta)."
                       if is_import else
                       "Firma EKSPORTOWA dostanie zapłatę w walucie od zagranicznego klienta. Wpływy będzie chciała SPRZEDAĆ, wymieniając je na złotówki — bank skupuje walutę po kursie Bid.")

        st.success(f"**Co pisać na kartkę (Strategia):** Należy dokonać operacji: **{typ_fwd}**.\n\n**Dlaczego?** {wyjasnienie}")
        st.info(f"Firma zagwarantowała sobie równowartość dokładnie **{kwota_pln:,.2f} PLN**")
        st.caption("📌 Termin kontraktu dobieraj możliwie najbliżej daty płatności z zadania. Jeśli dokładny termin nie jest kwotowany — wybierz najbliższy dostępny i zaznacz to w odpowiedzi.")

        st.subheader("Wzór matematyczny do przepisania:")
        if mnoznik_jpy:
            st.latex(rf"\text{{Wartosc PLN}} = \frac{{{kwota_fx:,.0f}}}{{100}} \times {zastosowany_kurs:.4f} = {kwota_pln:,.2f} \text{{ PLN}}")
        else:
            st.latex(rf"\text{{Wartosc PLN}} = {kwota_fx:,.0f} \times {zastosowany_kurs:.4f} = {kwota_pln:,.2f} \text{{ PLN}}")

# --------------------------------------------------------------------------------
# MODUŁ 6: HEDGING KRZYŻOWY
# --------------------------------------------------------------------------------
elif opcja == "6. Hedging Krzyżowy (Cross-Hedging)":
    st.header("🔀 Hedging Krzyżowy (Cross-Hedging)")

    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "Zadania tego typu łatwo rozpoznać — firma ma zarobić/wydać walutę X, ale do zabezpieczenia używa waluty Y (bo X ma słabą płynność albo wysokie koszty, a obie waluty są mocno skorelowane).\n"
            "1. **Waluta Target** (cel) — ta oryginalna z faktury (np. NOK, SEK, DKK z zadań skandynawskich).\n"
            "2. **Waluta Proxy** (ochrona) — ta większa, płynniejsza, używana zamiast właściwej (np. EUR).\n"
            "3. Wybierz, czy zabezpieczamy EKSPORT (przyszły wpływ ➔ sprzedajemy proxy forward po **Bid**), czy IMPORT (przyszła płatność ➔ kupujemy proxy po **Ask**).")

    kierunek = st.selectbox("Jaką transakcję zabezpieczamy?",
                            ["Eksport — w przyszłości dostaniemy walutę (proxy SPRZEDAJEMY forward po Bid)",
                             "Import — w przyszłości zapłacimy walutą (proxy KUPUJEMY forward po Ask)"])
    is_eksport = kierunek.startswith("Eksport")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**1. Prawdziwa waluta z faktury (Target)**")
        waluta_cel = st.text_input("Nazwa waluty Target (np. NOK)", "NOK")
        kwota_cel = st.number_input("Kwota faktury / ekspozycji (w walucie Target)", value=4800000, step=10000)
        spot_cel = st.number_input("Kurs dzisiejszy (Spot) dla waluty Target", value=0.3830, format="%.4f", step=0.0001)

    with col2:
        st.markdown("**2. Waluta użyta do ochrony (Proxy)**")
        waluta_proxy = st.text_input("Nazwa waluty Proxy (np. EUR)", "EUR")
        spot_proxy = st.number_input("Kurs dzisiejszy (Spot) dla Proxy", value=4.3320, format="%.4f", step=0.0001)
        etykieta_fwd = "Kurs FORWARD Proxy — Bid (bo sprzedajemy proxy)" if is_eksport else "Kurs FORWARD Proxy — Ask (bo kupujemy proxy)"
        fwd_proxy = st.number_input(etykieta_fwd, value=4.3485, format="%.4f", step=0.0001)

    if st.button("Pokaż jak wyliczyć zabezpieczenie krzyżowe"):
        wartosc_pln = kwota_cel * spot_cel
        kwota_proxy = wartosc_pln / spot_proxy
        zablokowane_pln = kwota_proxy * fwd_proxy
        efektywny_kurs = zablokowane_pln / kwota_cel  # = spot_cel * fwd_proxy / spot_proxy

        akcja = "SPRZEDAĆ" if is_eksport else "KUPIĆ"
        st.success(f"**Krok 1 (dopasowanie wolumenu):** Aby wyrównać ekspozycję z waluty {waluta_cel}, firma musi {akcja} na rynku forward równowartość **{kwota_proxy:,.2f} {waluta_proxy}**.")
        st.success(f"**Krok 2 (wynik zabezpieczenia):** Kontrakt forward na proxy blokuje wartość **{zablokowane_pln:,.2f} PLN**, co odpowiada efektywnemu kursowi zabezpieczenia **{efektywny_kurs:.4f} PLN za 1 {waluta_cel}**.")
        st.caption("⚠️ Do komentarza: hedging krzyżowy działa tylko tak dobrze, jak korelacja między walutami — pozostaje ryzyko rezydualne (kursy Target i Proxy mogą się rozjechać). Dlatego w zadaniu podaje się współczynniki korelacji.")

        st.subheader("Dokładne rozpisanie na kolokwium:")
        st.latex(rf"\text{{Wolumen}}_{{{waluta_proxy}}} = \text{{Kwota}}_{{{waluta_cel}}} \times \frac{{\text{{Spot}}_{{{waluta_cel}/PLN}}}}{{\text{{Spot}}_{{{waluta_proxy}/PLN}}}} = {kwota_cel:,.0f} \times \frac{{{spot_cel:.4f}}}{{{spot_proxy:.4f}}} = {kwota_proxy:,.2f}")
        st.latex(rf"\text{{Wartosc zablokowana}} = {kwota_proxy:,.2f} \times {fwd_proxy:.4f} = {zablokowane_pln:,.2f}\ \text{{PLN}}")
        st.latex(rf"\text{{Efektywny kurs}}_{{{waluta_cel}/PLN}} = \frac{{{zablokowane_pln:,.2f}}}{{{kwota_cel:,.0f}}} = {efektywny_kurs:.4f}")

# --------------------------------------------------------------------------------
# MODUŁ 7: FORWARDY TOWAROWE
# --------------------------------------------------------------------------------
elif opcja == "7. Forwardy Towarowe i Ryzyko Bazy":
    st.header("🌾 Forwardy Towarowe (Ryzyko Bazy)")

    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "Czytasz treść o soi, rzepaku lub metalach. Problem: ceny na polskim, lokalnym rynku różnią się od cen referencyjnych kontraktu o jakiś procent.\n"
            "1. Jak firma skupuje surowiec (produkcja) ➔ zaznacz 'Kupuje'. Jak to rolnik/wydobywca ➔ zaznacz 'Sprzedaje'.\n"
            "2. Najważniejszy haczyk: w zadaniu jest np. *'lokalne ceny są zazwyczaj o 2,5% NIŻSZE'*. Skoro niższe ➔ w polu 'Ryzyko bazy' wpisz minus (`-2.5`). Jeśli WYŻSZE (jak przy soi +3,8%) ➔ wpisz na plusie.\n"
            "3. Termin kontraktu dobieraj jak najbliżej daty dostawy — jeśli idealny miesiąc nie jest kwotowany, wybierz najbliższy i zaznacz w odpowiedzi niedopasowanie terminu.")

    col1, col2 = st.columns(2)
    with col1:
        kierunek = st.selectbox("Krok 1: Co firma robi z towarem?",
                                ["Kupuje (Musi zabezpieczyć cenę zakupu - Ask)",
                                 "Sprzedaje (Musi uchronić zyski - Bid)"])
        wolumen = st.number_input("Ile kupują/sprzedają? (Np. 12000 ton)", value=12000.0, step=100.0)
    with col2:
        fwd_bid = st.number_input("Kurs giełdowy Niższy (Bid w EUR)", value=502.80, format="%.2f", step=0.1)
        fwd_ask = st.number_input("Kurs giełdowy Wyższy (Ask w EUR)", value=506.30, format="%.2f", step=0.1)

    st.markdown("---")

    col3, col4 = st.columns(2)
    with col3:
        ryzyko_bazy = st.number_input("Procent odchylenia lokalnego (Ryzyko bazy). PAMIĘTAJ O MINUSIE jeśli ceny lokalne są niższe!", value=-2.50, step=0.1)
    with col4:
        fx_fwd = st.number_input("Kurs forward wymiany waluty na PLN (FX Forward)", value=4.3705, format="%.4f", step=0.0001)
        st.caption("📌 Przy ZAKUPIE surowca firma kupuje też walutę ➔ użyj kursu **Ask** forward FX. Przy SPRZEDAŻY surowca wpływy wymienia po **Bid**.")

    if st.button("Oblicz Koszty całego Surowca"):
        is_zakup = "Kupuje" in kierunek
        typ_fwd = "KUPNO kontraktu (Bierzemy wyższą cenę Ask z giełdy)" if is_zakup else "SPRZEDAŻ kontraktu (Bierzemy niższą cenę Bid)"
        kurs_surowca = fwd_ask if is_zakup else fwd_bid

        st.success(f"**Co musisz napisać (Krok 1 - Surowiec):** Firma musi wejść w operację **{typ_fwd}**. Kurs referencyjny wynosi {kurs_surowca:.2f}.")

        korekta_bazy = ryzyko_bazy / 100
        efektywna_cena_waluta = kurs_surowca * (1 + korekta_bazy)
        calkowita_wartosc_waluta = wolumen * efektywna_cena_waluta
        calkowita_wartosc_pln = calkowita_wartosc_waluta * fx_fwd

        st.info(f"**Co musisz napisać (Krok 2 - Korekta bazy):** Po uwzględnieniu lokalnego odchylenia ({ryzyko_bazy:+.2f}%), efektywna cena wyniesie **{efektywna_cena_waluta:.2f}** za tonę.")
        st.success(f"**Wynik Końcowy:** Za całość towaru firma zapłaci / otrzyma **{calkowita_wartosc_pln:,.2f} PLN** (po wymianie waluty po kursie {fx_fwd:.4f}).")
        st.caption("⚠️ Do komentarza: baza jest tylko WARTOŚCIĄ HISTORYCZNĄ/PRZECIĘTNĄ — może się zmienić do dnia dostawy. To ryzyko bazy obniża skuteczność hedgingu; minimalizuje się je np. dopasowaniem terminów i lokalnymi kontraktami.")

        st.subheader("Wzory do przepisania na kolokwium:")
        st.latex(r"\text{Cena Efektywna} = \text{Forward}_{\text{Gielda}} \times (1 + \text{Ryzyko Bazy})")
        st.latex(rf"\text{{Cena Efektywna}} = {kurs_surowca:.2f} \times {1 + korekta_bazy:.4f} = {efektywna_cena_waluta:.2f}")
        st.latex(r"\text{Calosc PLN} = \text{Wolumen} \times \text{Cena Efektywna} \times \text{Kurs Walutowy}")
        st.latex(rf"\text{{Calosc PLN}} = {wolumen:,.0f} \times {efektywna_cena_waluta:.2f} \times {fx_fwd:.4f} = {calkowita_wartosc_pln:,.2f}")

# --------------------------------------------------------------------------------
# MODUŁ 8: STRATEGIA KORPORACYJNA (STRIP FRA)
# --------------------------------------------------------------------------------
elif opcja == "8. Emisja Obligacji i Lokaty (Strip FRA)":
    st.header("🏛️ Złożona Ekspozycja: Obligacje i Lokaty")

    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "Najtrudniejsze zadanie. Firma emituje obligacje (tworzy dług o zmiennym oprocentowaniu), a jednocześnie ma nadwyżki i robi lokaty.\n"
            "1. 'Strip FRA' = pocięcie długu na kawałki. Jeśli emisja rusza za 2 miesiące, a okres odsetkowy trwa 3 miesiące, zabezpieczamy serią: 2x5, 5x8, 8x11 itd. Program sam wygeneruje symbole.\n"
            "2. Niżej wpisz parametry poszczególnych lokat (jeśli lokat jest mniej niż 3 — wpisz kwotę 0).")

    st.subheader("1. Główny problem: Emisja Obligacji (Firma pożycza od inwestorów)")
    c1, c2, c3 = st.columns(3)
    with c1:
        kwota_obl = st.number_input("Ile milionów emitują?", value=100.0)
        marza_obl = st.number_input("Marża doliczana do WIBOR (z zadania, w %)", value=1.20, step=0.01)
    with c2:
        start_obl = st.number_input("Kiedy rusza emisja? (Za ile miesięcy)", value=2, step=1, min_value=0)
        okres_obl = st.number_input("Co ile miesięcy płacą odsetki?", value=3, step=1, min_value=1)
    with c3:
        liczba_okresow = st.number_input("Ile okresów odsetkowych zabezpieczasz?", value=3, step=1, min_value=1, max_value=8)

    st.markdown("---")
    st.subheader("2. Poboczne transakcje: LOKATY (Firma inwestuje nadwyżki)")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Lokata 1**")
        l1_kwota = st.number_input("L1: Ile Milionów", value=30.0)
        l1_start = st.number_input("L1: Start za (miesięcy)", value=1, step=1, min_value=0)
        l1_trwa = st.number_input("L1: Trwa ile (miesięcy)", value=3, step=1, min_value=1)
    with col2:
        st.markdown("**Lokata 2**")
        l2_kwota = st.number_input("L2: Ile Milionów", value=25.0)
        l2_start = st.number_input("L2: Start za (miesięcy)", value=4, step=1, min_value=0)
        l2_trwa = st.number_input("L2: Trwa ile (miesięcy)", value=3, step=1, min_value=1)
    with col3:
        st.markdown("**Lokata 3**")
        l3_kwota = st.number_input("L3: Ile Milionów", value=20.0)
        l3_start = st.number_input("L3: Start za (miesięcy)", value=7, step=1, min_value=0)
        l3_trwa = st.number_input("L3: Trwa ile (miesięcy)", value=3, step=1, min_value=1)

    if st.button("Generuj wynik końcowy na zaliczenie (Strip FRA)"):
        st.success("### Co napisać o Obligacjach? (Firma ucieka przed wzrostem stóp)")
        st.markdown("Ponieważ firma będzie PŁACIĆ odsetki od długu inwestorom, otwiera pozycję **DŁUGĄ (KUPNO FRA — bierze kursy wyższe ASK)**, pociętą na następujące części:")

        for i in range(int(liczba_okresow)):
            poczatek = start_obl + (i * okres_obl)
            koniec = poczatek + okres_obl
            kontrakt = f"{poczatek}X{koniec}"
            st.markdown(f"- **Rata/Okres nr {i + 1}:** Potrzebujemy kontraktu FRA **{kontrakt}** na nominał {kwota_obl:g} mln PLN. Bierzemy pozycję **KUPNO (Long)**.")
            st.latex(rf"\text{{Calkowity Koszt dla Okresu {i + 1}}} = \text{{Cena FRA (ASK)}}_{{{kontrakt}}} + {marza_obl:.2f}\%")

        st.caption("📌 Jeśli któregoś z powyższych symboli NIE MA w tabeli kwotowań (w klasycznym zadaniu brakuje np. 11X14) — napisz, że ostatni okres pozostaje niezabezpieczony albo wymaga innego instrumentu. Prowadzący sprawdza, czy to zauważysz!")

        st.info("### Co napisać o Lokatach? (Firma ucieka przed spadkiem stóp)")
        st.markdown("Przy lokatach firma chce uchronić przyszłe zyski odsetkowe, dlatego dla każdej z lokat otwiera pozycję **KRÓTKĄ (SPRZEDAŻ FRA — bierze kursy niższe BID)**.")

        lokaty = [
            (l1_start, l1_trwa, l1_kwota, "Lokata 1 z zadania"),
            (l2_start, l2_trwa, l2_kwota, "Lokata 2 z zadania"),
            (l3_start, l3_trwa, l3_kwota, "Lokata 3 z zadania"),
        ]

        for start, trwa, kwota, nazwa in lokaty:
            if kwota > 0:
                kontrakt = f"{start}X{start + trwa}"
                st.markdown(f"- **{nazwa}:** Potrzebny kontrakt **{kontrakt}** na {kwota:g} mln PLN. Zaznacz pozycję: **SPRZEDAŻ (Short)**.")
                st.latex(rf"\text{{Efektywny Przychod ({nazwa})}} = \text{{Cena FRA (BID)}}_{{{kontrakt}}}")

        st.caption("💬 Do komentarza końcowego: pozycje z obligacji (kupione FRA) i z lokat (sprzedane FRA) częściowo się znoszą w nakładających się okresach — można to wskazać jako naturalny hedging zmniejszający potrzebne nominały kontraktów.")

# --------------------------------------------------------------------------------
# MODUŁ 9: BAZA WIEDZY I TEORII
# --------------------------------------------------------------------------------
elif opcja == "9. Wyszukiwarka Teorii (Baza Wiedzy)":
    st.header("📚 Wyszukiwarka Pojęć i Teorii (Baza Wiedzy)")
    st.info("💡 **Instrukcja:** Wpisz słowo kluczowe (np. 'aprecjacja') lub CAŁE pytanie z kolokwium. System przeanalizuje bazę i wskaże najważniejsze informacje, pomijając nieistotne słowa.")

    # Baza wiedzy spisana własnymi słowami na podstawie materiałów wykładowych
    baza_wiedzy = {
        "Aprecjacja a Deprecjacja": "Aprecjacja oznacza wzrost wartości krajowego pieniądza (za waluty obce płacimy mniej). Skutkuje to tańszym importem, ale nasz eksport staje się droższy dla zagranicy. Deprecjacja to spadek wartości naszej waluty (obce waluty drożeją). Import staje się droższy (rośnie inflacja), lecz eksport zyskuje na opłacalności.",
        "Dewaluacja a Rewaluacja": "Są to pojęcia zbliżone do aprecjacji i deprecjacji, jednak wynikają z oficjalnych decyzji władz monetarnych (banku centralnego) w systemach kursu stałego, a nie z rynkowej gry popytu i podaży.",
        "Waluta Kwotowana i Bazowa": "Dla pary walutowej takiej jak USD/PLN, pierwsza z nich (USD) to waluta bazowa (jej wartość wynosi zawsze 1), natomiast druga (PLN) to waluta kwotowana (określa cenę jednej jednostki bazowej). Kurs kupna (Bid) to cena zakupu waluty bazowej przez bank, a Ask to cena jej sprzedaży.",
        "Hedging (Zabezpieczenie)": "Jest to strategia ochrony przed ryzykiem kursowym polegająca na zajęciu pozycji przeciwstawnej do posiadanej ekspozycji. Wyróżniamy metody wewnętrzne (np. fakturowanie we własnej walucie) oraz zewnętrzne (użycie instrumentów takich jak kontrakty forward, futures czy opcje).",
        "Spekulacja a Arbitraż": "Spekulant podejmuje ryzyko, otwierając pozycję z nadzieją na zysk dzięki trafnym prognozom przyszłych kursów. Arbitrażysta z kolei poszukuje zysku bez ponoszenia ryzyka, dokonując jednoczesnego zakupu i sprzedaży na różnych rynkach, aby wykorzystać chwilowe różnice w cenach.",
        "Rynek Kasowy (Spot) vs Terminowy": "Rynek Spot (kasowy) to transakcje realizowane po bieżącym kursie z dostawą środków natychmiast lub maksymalnie w ciągu dwóch dni roboczych. Rynek terminowy to umowy ustalające cenę dzisiaj, ale z fizyczną dostawą waluty w z góry określonym dniu w przyszłości.",
        "Pozycja Walutowa Długa i Krótka": "Pozycja długa (Long) występuje, gdy posiadamy więcej aktywów i należności w walucie obcej niż zobowiązań (boimy się wtedy spadku jej kursu). Pozycja krótka (Short) oznacza przewagę zobowiązań nad należnościami w walucie obcej (zagrożeniem jest wtedy wzrost jej kursu).",
        "Teoria Parytetu Siły Nabywczej (PPP)": "Bazuje na Prawie Jednej Ceny – te same dobra powinny kosztować tyle samo w różnych krajach po przeliczeniu walut. W ujęciu absolutnym kurs zależy od poziomu cen, a w ujęciu względnym zmiany kursu wynikają z różnic w stopach inflacji pomiędzy państwami.",
        "Efekt Fishera i Międzynarodowy Efekt Fishera": "Zgodnie z efektem Fishera stopa nominalna to suma stopy realnej i oczekiwanej inflacji. Wersja międzynarodowa zakłada, że różnice w stopach procentowych między krajami determinują zmiany kursu – waluta kraju o wyższej stopie procentowej (i wyższej inflacji) będzie ulegać osłabieniu.",
        "Teoria Parytetu Stóp Procentowych (IRP)": "Teoria wiążąca rynki spot i forward. Wskazuje, że waluta kraju z wyższymi stopami procentowymi będzie notowana z dyskontem na rynku terminowym w stosunku do waluty kraju o niższych stopach procentowych.",
        "Teoria Oczekiwań": "Zakłada, że dzisiejszy kurs terminowy (forward) odzwierciedla rynkowe przewidywania i jest najlepszym oszacowaniem przyszłego kursu natychmiastowego (spot) w dniu wygaśnięcia kontraktu.",
        "Czynniki Wpływające na Kurs Walutowy": "Wzmocnienie waluty następuje na skutek wzrostu PKB, wyższych stóp procentowych czy dodatniego salda bilansu płatniczego. Osłabienie waluty wywołuje wysoka inflacja, rosnące bezrobocie oraz ujemny bilans płatniczy.",
        "Kontrakty Forward vs Futures": "Forward to elastyczne umowy pozagiełdowe dopasowane do klienta, ale obarczone ryzykiem niewypłacalności drugiej strony. Futures to standaryzowane kontrakty giełdowe, w których bezpieczeństwo zapewnia izba rozliczeniowa poprzez system depozytów zabezpieczających.",
        "Depozyty i Rozliczenia na Giełdzie Futures": "Izba rozliczeniowa wymaga wniesienia depozytu początkowego (przy otwarciu pozycji) oraz utrzymania depozytu podtrzymującego. Codziennie następuje wycena rynkowa (marking-to-market), która polega na dopisywaniu zysków lub potrącaniu strat z rachunku inwestora.",
        "Opcje Walutowe (Call, Put, Wartość)": "Dają kupującemu prawo (nie obowiązek) do zawarcia transakcji w zamian za zapłaconą premię. Wystawca pobiera premię, ale jego ryzyko straty jest teoretycznie nieograniczone. Opcja Call to prawo kupna, a Put – prawo sprzedaży. Wartość opcji to suma wartości wewnętrznej oraz wartości w czasie.",
        "Swap Walutowy (FX Swap)": "Obejmuje jednoczesne zawarcie transakcji spot (np. kupno waluty) i transakcji terminowej (odsprzedaż tej samej waluty w przyszłości). Pozwala na krótkoterminowe pozyskanie waluty bez wystawiania się na ryzyko kursowe.",
        "Swap Stopy Procentowej (IRS)": "Transakcja bez fizycznej wymiany kapitału docelowego. Strony wymieniają się wyłącznie płatnościami odsetkowymi w tej samej walucie. Często wykorzystywana do zamiany oprocentowania zmiennego na stałe.",
        "Swap Walutowo-Procentowy (CIRS)": "Składa się z trzech kroków: początkowej wymiany nominałów w różnych walutach, cyklicznej wymiany płatności odsetkowych w tych walutach oraz zwrotu nominałów na koniec umowy. Pomaga firmom taniej pozyskiwać kapitał zagranicą.",
        "Międzynarodowy Fundusz Walutowy (MFW / IMF)": "Organizacja powstała w 1944 r. w Bretton Woods. Jej zadaniem jest nadzór nad globalnym systemem finansowym, promowanie współpracy i udzielanie pomocy kredytowej krajom borykającym się z kryzysami bilansu płatniczego. Jednostką rozliczeniową MFW jest SDR.",
        "Grupa Banku Światowego (WBG)": "W jej skład wchodzi m.in. Międzynarodowy Bank Odbudowy i Rozwoju (IBRD) oraz Międzynarodowe Stowarzyszenie Rozwoju (IDA), które udziela preferencyjnych, nieoprocentowanych kredytów dla najbiedniejszych krajów na świecie.",
        "Instytucje Banku Światowego dla Biznesu": "IFC wspiera prywatne przedsiębiorstwa udzielając im pożyczek bez gwarancji rządowych. MIGA oferuje ubezpieczenia dla inwestorów przed ryzykiem politycznym (np. wojną czy nacjonalizacją). ICSID pełni funkcję sądu arbitrażowego w sporach inwestycyjnych.",
        "System Izby Walutowej (Currency Board)": "To reżim bardzo sztywnego kursu walutowego, w którym państwo rezygnuje z niezależnej polityki pieniężnej na rzecz powiązania własnej waluty z obcą (np. z dolarem). Cała baza monetarna musi mieć pokrycie w rezerwach dewizowych.",
        "Waluta Międzynarodowa i Jej Funkcje": "Wybór waluty w transakcjach globalnych zależy od potęgi gospodarki i zaufania do emitenta. Pełni ona funkcje: waluty rezerwowej, waluty fakturowania (w rozliczeniach handlowych), waluty interwencyjnej (dla banków centralnych) i waluty transakcyjnej na Forexie.",
    }

    query = st.text_input("Wpisz pytanie lub słowo klucz (np. 'czym różni się forward od futures', 'efekt fishera', 'mfw')", "")

    if query:
        def normalize_text(text):
            replacements = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z'}
            text = text.lower()
            for k, v in replacements.items():
                text = text.replace(k, v)
            return text

        query_norm = normalize_text(query)
        words = re.findall(r'\w+', query_norm)

        # Odrzucamy słowa, które nic nie wnoszą do wyszukiwania
        stop_words = {"co", "to", "jest", "jak", "dlaczego", "kiedy", "gdzie", "wymien", "podaj", "czym", "sie",
                      "i", "oraz", "na", "w", "z", "o", "a", "od", "do"}
        keywords = [w for w in words if w not in stop_words and len(w) > 2]

        results = []
        for title, desc in baza_wiedzy.items():
            score = 0
            t_norm = normalize_text(title)
            d_norm = normalize_text(desc)

            # Punktacja za dokładne trafienie całej frazy (najcenniejsze)
            if query_norm in t_norm:
                score += 100
            if query_norm in d_norm:
                score += 50

            # Punktacja za poszczególne słowa kluczowe
            for kw in keywords:
                if kw in t_norm:
                    score += 10
                if kw in d_norm:
                    score += 3

            if score > 0:
                results.append((score, title, desc))

        results.sort(key=lambda x: x[0], reverse=True)

        if results:
            st.success(f"Znaleziono {len(results)} pasujących zagadnień na podstawie Twojego pytania:")
            for score, title, desc in results[:5]:  # ograniczamy do top 5 wyników
                st.markdown(f"### 📘 {title}")
                st.write(desc)
                st.markdown("---")
        else:
            st.warning("Nie znaleziono pasującego zagadnienia w bazie. Spróbuj użyć innego, pojedynczego słowa kluczowego (np. wpisz samo słowo 'opcje' zamiast całego zdania).")
    else:
        st.info("Baza danych załadowana z sukcesem. Czekam na Twoje zapytanie...")

        with st.expander("Przeglądaj wszystkie definicje (Alfabetycznie)"):
            for title, desc in sorted(baza_wiedzy.items()):
                st.markdown(f"**{title}** - {desc}")
