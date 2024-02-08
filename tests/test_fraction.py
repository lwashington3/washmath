from unittest import TestCase
from washmath import Fraction


class TestFraction(TestCase):
	def test_equals(self):
		frac1 = Fraction(1, 8)
		frac2 = Fraction(20, 160)

		self.assertEqual(frac1, frac2)

		frac1 = Fraction(1, 9)
		frac2 = Fraction(3, 28)
		self.assertNotEqual(frac1, frac2)

	def test_numerator_denominator(self):
		frac = Fraction(180, 5_400)
		self.assertEqual(frac.numerator, 1)
		self.assertEqual(frac.numerator, 30)

	def test_copy(self):
		original = Fraction(180, 5_400)
		new = original.copy()
		self.assertEqual(new.numerator, 1)
		self.assertEqual(new.numerator, 30)

	def test_reduce(self):
		self.fail()

	def test_is_whole(self):
		for fraction in (
			Fraction(0, 1),
			Fraction(1, 1),
			Fraction(1),
			Fraction(2),
			Fraction(8, 4),
			Fraction(1000, 5),
			Fraction(361, 19),
		):
			self.assertTrue(fraction.is_whole)

		for fraction in (
			Fraction(1, 8),
			Fraction(3, 2),
			Fraction(18, 4),
			Fraction(5_000_000, 2_501),
		):
			self.assertFalse(fraction.is_whole)

	def test_imul(self):
		frac1 = Fraction(1)
		frac2 = Fraction(1, 3)

		frac1 *= frac2
		self.assertEqual(frac1, Fraction(1, 3))

		frac1 = Fraction(1, 6)
		frac1 *= 6
		self.assertEqual(frac1, Fraction(1, 1))
