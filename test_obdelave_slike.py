import unittest
import cv2 as cv
import numpy as np
from naloga1 import zmanjsaj_sliko, najdi_masko_hsv, prestej_piksle_z_barvo_koze, doloci_barvo_koze

# Definiramo razred za testiranje, ki razširja unittest.TestCase
class TestObdelaveSlike(unittest.TestCase):

    # Testna metoda za preverjanje funkcije zmanjševanja slik
    def test_zmanjsaj_sliko(self):
        test_slika = cv.imread('slike/test_slika.jpg')  # Naložimo testno sliko
        rezultat = zmanjsaj_sliko(test_slika, 100, 100)  # Zmanjšamo sliko
        self.assertEqual(rezultat.shape, (100, 100, 3))  # Preverimo, ali ima zmanjšana slika prave dimenzije

    # Testna metoda za preverjanje iskanja maske na podlagi barve kože v HSV prostoru
    def test_najdi_masko_hsv(self):
        test_slika = cv.imread('slike/test_slika.jpg')  # Naložimo testno sliko
        barva_koze = (np.array([0, 48, 80]), np.array([20, 255, 255]))  # Določimo obseg barv za kožo
        maska = najdi_masko_hsv(test_slika, barva_koze)  # Najdemo masko
        self.assertTrue(maska is not None)  # Preverimo, ali smo dobili masko
        self.assertEqual(maska.shape, test_slika.shape[:2])  # Preverimo, ali je maska pravilnih dimenzij

    # Testna metoda za preštevanje pikslov z barvo kože
    def test_prestej_piksle_z_barvo_koze(self):
        test_slika = cv.imread('slike/test_slika.jpg')  # Naložimo testno sliko
        barva_koze = (np.array([0, 48, 80]), np.array([20, 255, 255]))  # Določimo obseg barv za kožo
        število = prestej_piksle_z_barvo_koze(test_slika, barva_koze)  # Preštejemo piksle
        self.assertIsInstance(število, int)  # Preverimo, ali je rezultat tipa int
        self.assertTrue(število >= 0)  # Preverimo, ali je število pikslov nenegativno

    # Testna metoda za določanje barve kože
    def test_doloci_barvo_koze(self):
        test_slika = cv.imread('slike/test_slika.jpg')  # Naložimo testno sliko
        levo_zgoraj = (50, 50)  # Koordinate za levi zgornji kot
        desno_spodaj = (100, 100)  # Koordinate za desni spodnji kot
        min_barva, max_barva = doloci_barvo_koze(test_slika, levo_zgoraj, desno_spodaj)  # Določimo obseg barve kože
        self.assertTrue(min_barva is not None and max_barva is not None)  # Preverimo, ali sta obe barvi določeni
        self.assertEqual(len(min_barva), 3)  # Preverimo, ali barva vsebuje 3 komponente (HSV)
        self.assertEqual(len(max_barva), 3)  # Enako za drugo barvo

# Če skripto zaženemo neposredno, se izvedejo testi
if __name__ == '__main__':
    unittest.main()
