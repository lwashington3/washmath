from .statlist import StatList
from ..classes import Fraction


__ALL__ = ["ANOVA"]


def calculate_sst(statlists:list[StatList]) -> tuple[Fraction, Fraction]:
	mean = Fraction(0)

	for statlist in statlists:
		mean += statlist.mean

	mean /= len(statlists)

	lst_total = sum([(statlist.mean - mean)**2 * len(statlist) for statlist in statlists], start=Fraction(0))

	return lst_total, mean


def calculate_sse(statlists:list[StatList]) -> Fraction:
	return sum([statlist.variance * (len(statlist)-1) for statlist in statlists], start=Fraction(0))


class ANOVA(object):
	def __init__(self, *lsts, pprint=True):
		lsts = list(lsts)
		for i, lst in enumerate(lsts):
			if not isinstance(lst, StatList):
				lsts[i] = StatList(lst)
		self.statlists = lsts

		self.n = sum([len(statlist) for statlist in self.statlists])  # Same as n
		self.k = len(self.statlists)

		self.SST, self.mean = calculate_sst(self.statlists)  # Sum of squares treatment
		self.SSE = calculate_sse(self.statlists)  # Sum of squares error
		self.SS = self.SST + self.SSE  # Sum of squares total
		if pprint:
			print(f"SST = {self.SST}\nSSE = {self.SSE}\nSS Total = {self.SS}")

		self.DFT = self.k - 1  # Degrees of Freedom Treatments
		self.DFE = self.n - self.k  # Degrees of Freedom Error
		self.DF = self.n - 1  # Total Degrees of Freedom, equals DFT + DFE
		if pprint:
			print(f"DFT = {self.DFT}\nDFE = {self.DFE}\nDF Total = {self.DF}")

		self.MST = self.SST / self.DFT  # Mean Square Treatment
		self.MSE = self.SSE / self.DFE  # Mean Square Error, pooled variance
		self.F = self.MST / self.MSE
		if pprint:
			print(f"MST = {self.MST}\nMSE = {self.MSE}\nF Total = {self.F}")  # This gives independent weighted and unweighted accoding to vassarstats

	def __len__(self):
		return self.n

	def __str__(self):
		return f"The ANOVA returned an F value of {self.F}"

	def __float__(self):
		return self.F

	def __int__(self):
		return int(self.F)

	def __call__(self, *args, **kwargs):
		return float(self)

	@property
	def n(self) -> int:
		"""Total number of items"""
		return self._n

	@n.setter
	def n(self, n:int):
		if not isinstance(n, int):
			n = int(n)
		self._n = n

	@classmethod
	def create(cls):
		k = int(input("How many k are there? "))  # Number of k
		n = 0  # Total number of observations
		data = []
		for i in range(k):
			tmp = []
			observ = 1
			while observ != 'q':
				observ = input(f"What is the data for group {i}? If completed with the group, enter 'q'. ")
				if observ != 'q':
					tmp.append(float(observ))
					n += 1
				else:
					data.append(StatList(tmp))
					print("\n")
		return cls(k, n, data)


if __name__ == "__main__":
	anova = ANOVA.create()
