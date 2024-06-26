import cv2 as cv
import numpy as np
import time

def zmanjsaj_sliko(slika, sirina, visina):
    return cv.resize(slika, (sirina, visina), interpolation=cv.INTER_AREA)


def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    visina, sirina, _ = slika.shape
    skatle = []
    for y in range(0, visina - visina_skatle + 1, visina_skatle):
        for x in range(0, sirina - sirina_skatle + 1, sirina_skatle):
            pod_slika = slika[y:y + visina_skatle, x:x + sirina_skatle]
            st_pikslov = prestej_piksle_z_barvo_koze(pod_slika, barva_koze)
            skatle.append(((x, y, sirina_skatle, visina_skatle), st_pikslov))
    return skatle


def najdi_masko_hsv(slika, barva_koze):
    slika_hsv = cv.cvtColor(slika, cv.COLOR_BGR2HSV)
    maska = cv.inRange(slika_hsv, barva_koze[0], barva_koze[1])
    return maska


def prestej_piksle_z_barvo_koze(slika, barva_koze):
    maska_koze = najdi_masko_hsv(slika, barva_koze)
    return cv.countNonZero(maska_koze)


def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) -> tuple:
    obmocje_koze = slika[levo_zgoraj[1]:desno_spodaj[1],
                   levo_zgoraj[0]:desno_spodaj[0]]  # določimo y:visina in x:širina območja koze
    obmocje_koze_hsv = cv.cvtColor(obmocje_koze, cv.COLOR_BGR2HSV)
    min_barva = np.min(obmocje_koze_hsv, axis=(0, 1))  # iščemo minimalne vrednost po x in y
    max_barva = np.max(obmocje_koze_hsv, axis=(0, 1))
    return min_barva, max_barva

def filtriraj_skatle_po_barvi_koze(skatle, prag=50):
    filtrirane_skatle = []
    for skatla in skatle:
        if skatla[1] > prag:
            filtrirane_skatle.append(skatla)
    return filtrirane_skatle


def zdruzi_sosednje_skatle(skatle, max_razdalja=70):
    if not skatle:
        return []
    zdruzeni = [skatle[0]]
    for trenutna in skatle[1:]:
        zdruzeno = False
        for i, z in enumerate(zdruzeni): # hkrati dostop do indexa in vrednosti
            if so_sosednje(trenutna[0], z[0], max_razdalja):
                nova_skatla = zdruzi([trenutna, z])
                zdruzeni[i] = (nova_skatla, 0)
                zdruzeno = True
                break
        if not zdruzeno:
            zdruzeni.append(trenutna)
    return zdruzeni

# izračuna razdaljo med lokacijami začetnih točk (zgornji levi kot) obeh škatel
def so_sosednje(skatla1, skatla2, max_razdalja):
    x1, y1, _, _ = skatla1
    x2, y2, _, _ = skatla2
    razdalja = max(abs(x1-x2), abs(y1-y2))
    return razdalja <= max_razdalja

def zdruzi(skatli):
    x_coords = [skatla[0][0] for skatla in skatli]  # x koordinata vseh škatel v seznamu
    y_coords = [skatla[0][1] for skatla in skatli]  # x koordinata vseh škatel v seznamu

    widths = [skatla[0][2] for skatla in skatli]
    heights = [skatla[0][3] for skatla in skatli]  # širine in višine škatel

    x_min = min(x_coords)  # najdem minimume in maximume
    y_min = min(y_coords)

    x_max = max(x_coords) + max(widths)
    y_max = max(y_coords) + max(heights)
    return x_min, y_min, x_max - x_min, y_max - y_min


if __name__ == '__main__':
    start_time = time.time()
    frame_count = 0
    barva_koze_dolocena = False
    barva_koze = None
    sirina = 340
    visina = 220

    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()  # ret je boolean vrne true če je bil zajem slike uspešen
        if not ret:
            print("Napaka pri zajemu slike.")
            break

        frame = zmanjsaj_sliko(frame, sirina, visina)

        cv.imshow('Zacetna slika', frame)

        if cv.waitKey(1) & 0xFF == ord('n'):  # pritisni 'n' za naslednji korak
            break

    cv.destroyAllWindows()

    r = cv.selectROI("Izberi obmocje koze", frame)  # enter

    levo_zgoraj = (int(r[0]), int(r[1]))
    desno_spodaj = (int(r[0] + r[2]), int(r[1] + r[3]))
    cv.destroyWindow("Izberi obmocje koze")

    if r[2] > 0 and r[3] > 0:  # preverjanje da ixor ni prazen
        barva_koze = doloci_barvo_koze(frame, levo_zgoraj, desno_spodaj)
        barva_koze_dolocena = True

    if not barva_koze_dolocena:
        print("Barva kože ni bila določena. Zapiram program.")
        cap.release()
        cv.destroyAllWindows()
        exit()

    # Zajem in obdelava videoposnetka v realnem času
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = zmanjsaj_sliko(frame, sirina, visina)

        if barva_koze_dolocena:
            skatle = obdelaj_sliko_s_skatlami(frame, int(sirina * 0.1), int(visina * 0.3), barva_koze)

            filtrirane_skatle = filtriraj_skatle_po_barvi_koze(skatle)

            zdruzene_skatle = zdruzi_sosednje_skatle(filtrirane_skatle)

            for skatla in zdruzene_skatle:
                cv.rectangle(frame, (skatla[0][0], skatla[0][1]),
                             (skatla[0][0] + skatla[0][2], skatla[0][1] + skatla[0][3]), (0, 0, 255), 2)
        frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > 1:
            fps = frame_count / elapsed_time
            cv.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            start_time = current_time
            frame_count = 0

        cv.imshow('Detekcija obraza', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):  # Pritisnite 'q' za izhod
            break

    cap.release()
    cv.destroyAllWindows()