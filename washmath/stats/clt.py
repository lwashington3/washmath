__author__ = "Len Washington III"
# January 23, 2021


from . import Z, StatList
    

class CentralLimitTheorem(object):
    def __init__(self, sample_size:int, actual_mean:float, sample_mean:float, standard_deviation:float):
        self.sample_size = sample_size
        self.actual_mean = actual_mean
        self.sample_mean = sample_mean
        self.standard_deviation = standard_deviation

        ans = (self.sample_mean - self.actual_mean) / (self.standard_deviation / self.sample_size ** 0.5)
        self.z = Z(ans)
        self.CLT = 1 - self.z.getZScore()

    def __str__(self) -> str:
        return f"{self.CLT*100:.4}% of all possible means (of n={self.sample_size}) is higher than {self.actual_mean} which {self.sample_mean} is."

    def __float__(self) -> float:
        return self.CLT

    @classmethod
    def fromStatList(cls, sample_size:int, sl:StatList):
        return cls(sample_size, sl.getMean(), sl.getStandardDeviation())


if __name__ == "__main__":
    # clt = CentralLimitTheorem(36, 98.2, 98.6, .6)
    clt = CentralLimitTheorem(36, 98.2, 98.04, .6)

    print(1 - clt.CLT)
