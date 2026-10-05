"""Research-model regressions, standard-library only. License: CC BY-SA 4.0."""
import sys
import unittest
from fractions import Fraction
from pathlib import Path
from random import Random

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import verify_model as model


class ModelTests(unittest.TestCase):
    def test_negacyclic_wrap(self):
        a, b = [0]*model.N, [0]*model.N
        a[-1], b[1] = 1, 1
        product = model.ring_mul(a,b)
        self.assertEqual(product, [model.Q-1]+[0]*(model.N-1))

    def test_exact_old_statistics(self):
        for modulus, values in ((512,(3,3,12041,Fraction(40084480,11082241))),
                                (1024,(2,2,3076,Fraction(10240000,11082241))),
                                (8,(208,208,48038016,Fraction(159918512000,11082241)))):
            with self.subTest(modulus=modulus):
                self.assertEqual(model.statistics(3329,modulus), values)

    def test_exact_new_statistics(self):
        self.assertEqual(model.statistics(model.Q,32768)[:3], (1,1,32769))
        self.assertEqual(model.statistics(model.Q,256)[:3], (128,128,357941248))

    def test_rounding_against_independent_rational_definition(self):
        for q,modulus in ((3329,512),(model.Q,256),(model.Q,32768)):
            for x in range(q):
                v = Fraction(modulus*x,q)+Fraction(1,2)
                expected = (v.numerator//v.denominator) % modulus
                self.assertEqual(model.round_to(x,q,modulus),expected)
            for z in range(modulus):
                v = Fraction(q*z,modulus)+Fraction(1,2)
                expected = (v.numerator//v.denominator) % q
                self.assertEqual(model.lift(z,q,modulus),expected)

    def test_decode_entire_proved_interval(self):
        self.assertEqual(model.BOUND,9346)
        self.assertLess(2*model.BOUND,model.D)
        for bit in (0,1):
            for noise in range(-model.BOUND,model.BOUND+1):
                self.assertEqual(model.decode(model.D*bit+noise),bit)

    def test_polynomial_encryption_identity_and_roundtrip(self):
        rng = Random(1947)
        for _ in range(4):
            model.trial(rng)

    def test_old_hint_disclosure(self):
        # Regression for the withdrawn design: each marked position exposes m.
        for bit in (0,1):
            for mask in (3,5):
                v = (mask+4*bit) % 8
                self.assertEqual(int(v in (1,7)),bit)

    def test_old_correction_is_modularly_inert(self):
        for v in range(8):
            for w in range(8):
                for shift in (-8,0,8):
                    self.assertEqual((v-w-shift) % 8,(v-w) % 8)


if __name__ == '__main__':
    unittest.main()
