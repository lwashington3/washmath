from washmath import gcd


def test(n, r): # 25, 13
    numerators = [i for i in range(r+1, n+1)]
    denominators = [i for i in range(1, (n-r+1))]
    print(len(numerators), len(denominators))
    for i in range(len(denominators)):
        j = 0
        while denominators[i] != 1 and j != len(numerators):
            mult = gcd(denominators[i], numerators[j])
            if mult != 1 and mult != 0:
                denominators[i] //= mult
                numerators[j] //= mult
            j+=1
    total = 1
    for i in numerators:
        total *= i
    for i in denominators:
        total /= i
    return total


if __name__ == "__main__":
    print(f"{test(25,15):,}")
