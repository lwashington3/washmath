class ANOVA(object):
    def __init__(self, groups, length, lst, pprint=True):
        self.lst = lst
        self.length = length  # Same as n
        self.groups = groups  # Same as k
        self.mean, self.items = self.mean(lst)

        self.SST = self.SST_cal(lst, self.mean)  # Sum of squares treatment
        self.SSE = self.SSE_cal(lst)  # Sum of squares error
        self.SS = self.SST + self.SSE  # Sum of squares total
        if pprint:
            print(f"SST = {self.SST}\nSSE = {self.SSE}\nSS Total = {self.SS}")

        self.DFT = self.groups - 1  # Degrees of Freedom Treatments
        self.DFE = self.length - self.groups  # Degrees of Freedom Error
        self.DF = self.length - 1  # Total Degrees of Freedom, equals DFT + DFE
        if pprint:
            print(f"DFT = {self.DFT}\nDFE = {self.DFE}\nDF Total = {self.DF}")

        self.MST = self.SST / self.DFT  # Mean Square Treatment
        self.MSE = self.SSE / self.DFE  # Mean Square Error, pooled variance
        self.F = self.MST / self.MSE
        if pprint:
            print(f"MST = {self.MST}\nMSE = {self.MSE}\nF Total = {self.F}")  # This gives independent weighted and unweighted accoding to vassarstats

    def getAnova(self):
        return self.F

    @staticmethod
    def mean(lst):
        mean = 0.0
        items = 0
        for li in lst:
            for i in li:
                mean += i
                items += i
        return mean, items

    @staticmethod
    def SST_cal(data, overall_mean):
        SST = 0
        for lst in data:
            lst_mean = 0
            ni = len(lst)  # Number of observations of ith group
            for i in lst:
                lst_mean += i
            lst_mean /= ni
            tmp = lst_mean - overall_mean
            tmp = ni * (tmp ** 2)
            SST += tmp
        return SST

    @staticmethod
    def SSE_cal(data):
        SSE = 0
        for lst in data:
            lst_mean = 0
            ni = len(lst)
            for i in lst:
                lst_mean += i
            lst_mean /= ni

            SDi = 0  # Standard Deviation for ith group
            for i in lst:
                x = (i - lst_mean) ** 2
                SDi += x
            SDi = SDi / (len(lst) - 1)
            SDi = abs(SDi)  # When finding the sample standard deviation, the final step is to take the square root, but for the formula we immediately square it, so taking the absolute value is a shortcut

            tmp = SDi * (ni - 1)
            SSE += tmp
        return SSE

    def __len__(self):
        return self.length

    def __str__(self):
        return f"The ANOVA returned an F value of {self.F}"

    def __float__(self):
        return self.F

    def __int__(self):
        return int(self.F)

    @classmethod
    def create(cls):
        k = int(input("How many groups are there? "))  # Number of groups
        n = 0  # Total number of observations
        data = []
        for i in range(k):
            tmp = []
            observ = 1
            while observ != 'q':
                observ = input(f"What is the data for group {i}? If completed with the group, eneter 'q'. ")
                if observ != 'q':
                    tmp.append(float(observ))
                    n += 1
                else:
                    data.append(tmp)
                    print("\n")
        return cls(k, n, data)


if __name__ == "__main__":
    anova = ANOVA.create()
