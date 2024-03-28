import cv2 as cv
import numpy as np


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


if __name__ == '__main__':
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

    # Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
    # Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
    # Vprašanje 2: Kako prešteti število ljudi?

    # Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
    # in ne pozabite, da ni nujno da je škatla kvadratna.
    pass