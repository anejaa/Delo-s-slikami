import unittest
import cv2 as cv
import numpy as np
from naloga1 import zmanjsaj_sliko, najdi_masko_hsv, prestej_piksle_z_barvo_koze, doloci_barvo_koze

class TestObdelaveSlike(unittest.TestCase):

    def test_zmanjsaj_sliko(self):
        test_slika = cv.imread('slike/test_slika.jpg')
        rezultat = zmanjsaj_sliko(test_slika, 100, 100)
        self.assertEqual(rezultat.shape, (100, 100, 3))

    def test_najdi_masko_hsv(self):
        test_slika = cv.imread('slike/test_slika.jpg')
        barva_koze = (np.array([0, 48, 80]), np.array([20, 255, 255]))
        maska = najdi_masko_hsv(test_slika, barva_koze)
        self.assertTrue(maska is not None)
        self.assertEqual(maska.shape, test_slika.shape[:2])

    def test_prestej_piksle_z_barvo_koze(self):
        test_slika = cv.imread('slike/test_slika.jpg')
        barva_koze = (np.array([0, 48, 80]), np.array([20, 255, 255]))
        število = prestej_piksle_z_barvo_koze(test_slika, barva_koze)
        self.assertIsInstance(število, int)
        self.assertTrue(število >= 0)

    def test_doloci_barvo_koze(self):
        test_slika = cv.imread('slike/test_slika.jpg')
        levo_zgoraj = (50, 50)
        desno_spodaj = (100, 100)
        min_barva, max_barva = doloci_barvo_koze(test_slika, levo_zgoraj, desno_spodaj)
        self.assertTrue(min_barva is not None and max_barva is not None)
        self.assertEqual(len(min_barva), 3)
        self.assertEqual(len(max_barva), 3)

if __name__ == '__main__':
    unittest.main()
