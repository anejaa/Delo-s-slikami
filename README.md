# Detekcija kože v videoposnetkih

#### Ta projekt je namenjen detekciji kože v realnem času v videoposnetkih. Program omogoča zaznavanje kožnih območij na podlagi določene barve kože.

## Funkcionalnosti

Zmanjšanje velikosti slike: Funkcija zmanjsaj_sliko zmanjša velikost vhodne slike na želeno velikost.

Obdelava slike s skatlami: Funkcija obdelaj_sliko_s_skatlami identificira skatle na sliki in prešteje število pikslov z barvo kože v vsaki skatli.

Iskanje maske barve kože v HSV prostoru: Funkcija najdi_masko_hsv določi masko barve kože v sliki v barvnem prostoru HSV.

Prestej piksle z barvo kože: Funkcija prestej_piksle_z_barvo_koze prešteje število pikslov v sliki, ki spadajo v območje barve kože.

Določi barvo kože: Funkcija doloci_barvo_koze določi minimalno in maksimalno vrednost barve kože na podlagi izbranega območja na sliki.

Filtriranje skatl po barvi kože: Funkcija filtriraj_skatle_po_barvi_koze filtrira skatle glede na število pikslov z barvo kože.

Združevanje sosednjih skatle: Funkcija zdruzi_sosednje_skatle združi sosednje skatle v eno skatlo, če so dovolj blizu.

Ostale pomožne funkcije: V projektu so tudi druge pomožne funkcije, kot so funkcije za izračun razdalje med skatlami in druge.

## Uporaba

Program omogoča zajem videoposnetka v realnem času s spletne kamere ali drugega vhoda ter nato detekcijo kože v videoposnetku. Uporabnik lahko določi območje kože na sliki, na podlagi katerega se določi barva kože. Nato program samodejno detektira in označi skatle na videoposnetku, ki vsebujejo kožna območja.

## Navodila za uporabo

Začnite z izvedbo programa.
Na začetni sliki izberite območje, ki vsebuje barvo kože, s klikom in povlekom miške.
Po izbiri območja kože se bo program samodejno premaknil v način detekcije obraza v realnem času.
Pritisnite tipko 'n' za začetek zajema videoposnetka.
Program bo samodejno detektiral in označil skatle na videoposnetku, ki vsebujejo kožna območja.
Za izhod iz programa pritisnite tipko 'q'.

## Zahteve

    Python 3.x
    OpenCV
    NumPy
