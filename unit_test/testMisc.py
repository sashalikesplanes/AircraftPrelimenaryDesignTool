import unittest

from misc.constants import testMargin
from misc.unitConversions import *
from misc.ISA import *


class TestMisc(unittest.TestCase):
    def test_isa(self):
        pass

    def test_unit_conversion_1(self):
        self.assertAlmostEqual(lbs_to_kg(1), 0.453592, delta=0.453592*testMargin)
        self.assertAlmostEqual(kg_to_lbs(1), 2.20462, delta=2.20462*testMargin)
        self.assertAlmostEqual(K_to_C(1), -274.15, delta=274.15*testMargin)
        self.assertAlmostEqual(C_to_K(1), 274.15, delta=1*testMargin)
        self.assertAlmostEqual(pa_to_psi(1), 0.000145038, delta=0.000145038*testMargin)
        self.assertAlmostEqual(pa_to_psf(1), 0.020885, delta=0.020885*testMargin)
        self.assertAlmostEqual(bar_to_pa(1), 100000, delta=100000*testMargin)

    def test_unit_conversion_2(self):
        self.assertAlmostEqual(kts_to_ms(1), 1/1.94384, delta=1/1.94384*testMargin)
        self.assertAlmostEqual(ms_to_kts(1), 1.94384, delta=1.94384*testMargin)
        self.assertAlmostEqual(m_to_inch(1), 39.3701, delta=39.3701*testMargin)
        self.assertAlmostEqual(inch_to_m(1), 0.0254, delta=0.0254*testMargin)
        self.assertAlmostEqual(m3_to_ft3(1), 35.3147, delta=35.3147*testMargin)
        self.assertAlmostEqual(m2_to_ft2(1), 10.7639, delta=10.7639*testMargin)
        self.assertAlmostEqual(ft_to_m(1), 0.3048, delta=0.3048*testMargin)
