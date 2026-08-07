import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("SquareAndMultiply-Python.py")
SPEC = importlib.util.spec_from_file_location("square_and_multiply_module", MODULE_PATH)
square_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(square_module)


class SquareAndMultiplyTests(unittest.TestCase):
    def test_matches_builtin_pow(self):
        cases = [
            (3, 5, 11),
            (5, 32, 7),
            (2, 0, 5),
            (10, 12, 1),
            (123, 456, 789),
        ]

        for base, exponent, modulus in cases:
            with self.subTest(base=base, exponent=exponent, modulus=modulus):
                self.assertEqual(
                    square_module.square_and_multiply(base, exponent, modulus),
                    pow(base, exponent, modulus),
                )

    def test_negative_exponent_is_rejected(self):
        with self.assertRaises(ValueError):
            square_module.square_and_multiply(2, -1, 5)

    def test_openssl_matches_builtin_pow_when_available(self):
        try:
            result = square_module.openssl_mod_exp(5, 32, 7)
        except RuntimeError as error:
            self.skipTest(str(error))

        self.assertEqual(result, pow(5, 32, 7))


if __name__ == "__main__":
    unittest.main()
