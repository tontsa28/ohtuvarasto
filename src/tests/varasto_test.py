import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 7)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)
    
    def test_laitetaan_liikaa_tavaraa(self):
        self.varasto.lisaa_varastoon(12)

        # varastossa ei pitäisi olla enää tilaa
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 0)
    
    def test_lisataan_negatiivisesti_tilaa(self):
        self.varasto.lisaa_varastoon(-1)
    
    def test_ota_negatiivinen_maara_tavaraa(self):
        self.varasto.ota_varastosta(-1)
    
    def test_ota_liikaa_tavaraa(self):
        self.varasto.ota_varastosta(20)

    def test_muunna_merkkijonoksi(self):
        str(self.varasto)
    
    def test_luo_negatiivisella_tilalla(self):
        Varasto(-1)
    
    def test_luo_negatiivisella_saldolla(self):
        Varasto(5, -1)
