import sys

if __name__ == "__main__":
    par = int(sys.argv[1])
    num = 0
    print(par)
    if par == 0:
        for _ in range(10000000):
            p = [5, 5, 6, 4, 1, 5, 6, 5, 5, 1]
            for i in range(len(p)):
                num += 1
    elif par == 1:
        for _ in range(10000000):
            p = [5, 5, 6, 4, 1, 5, 6, 5, 5, 1]
            l = len(p)
            for i in range(l):
                num += 1
    elif par == 2:
        for _ in range(10000000):
            p = [5, 5, 6, 4, 1, 5, 6, 5, 5, 1]
            for i in range(10):
                num += 1

"""
For 0 (calling len)

python3 tests/len.py 0 : 6.34s user . 0.05s system . 100% cpu . 6.383 total
python3 tests/len.py 0 : 6.45s user . 0.07s system . 100% cpu . 6.505 total
python3 tests/len.py 0 : 6.44s user . 0.05s system . 100% cpu . 6.483 total
python3 tests/len.py 0 : 6.19s user . 0.06s system . 100% cpu . 6.237 total
python3 tests/len.py 0 : 6.20s user . 0.06s system . 100% cpu . 6.249 total
python3 tests/len.py 0 : 6.92s user . 0.08s system . 100% cpu . 6.992 total
python3 tests/len.py 0 : 6.38s user . 0.06s system . 100% cpu . 6.435 total
python3 tests/len.py 0 : 6.35s user . 0.07s system . 100% cpu . 6.418 total
python3 tests/len.py 0 : 6.69s user . 0.05s system . 100% cpu . 6.733 total
python3 tests/len.py 0 : 7.43s user . 0.07s system . 100% cpu . 7.487 total

For 1 (saved variable)

python3 tests/len.py 1 : 7.12s user . 0.05s system . 100% cpu . 7.167 total
python3 tests/len.py 1 : 6.58s user . 0.06s system . 100% cpu . 6.638 total
python3 tests/len.py 1 : 6.35s user . 0.07s system . 100% cpu . 6.410 total
python3 tests/len.py 1 : 6.72s user . 0.07s system . 100% cpu . 6.786 total
python3 tests/len.py 1 : 6.62s user . 0.06s system . 100% cpu . 6.674 total
python3 tests/len.py 1 : 7.56s user . 0.07s system . 100% cpu . 7.617 total
python3 tests/len.py 1 : 6.61s user . 0.05s system . 100% cpu . 6.656 total
python3 tests/len.py 1 : 6.83s user . 0.06s system . 100% cpu . 6.874 total
python3 tests/len.py 1 : 6.39s user . 0.06s system . 100% cpu . 6.438 total
python3 tests/len.py 1 : 6.67s user . 0.06s system . 100% cpu . 6.723 total

For 2 (fixed number)

python3 tests/len.py 2 : 6.04s user . 0.05s system . 100% cpu . 6.082 total
python3 tests/len.py 2 : 6.45s user . 0.07s system . 100% cpu . 6.509 total
python3 tests/len.py 2 : 6.19s user . 0.06s system . 100% cpu . 6.240 total
python3 tests/len.py 2 : 6.05s user . 0.07s system . 100% cpu . 6.114 total
python3 tests/len.py 2 : 6.25s user . 0.06s system . 100% cpu . 6.300 total
python3 tests/len.py 2 : 5.91s user . 0.06s system . 100% cpu . 5.966 total
python3 tests/len.py 2 : 5.84s user . 0.05s system . 100% cpu . 5.884 total
python3 tests/len.py 2 : 6.11s user . 0.06s system . 100% cpu . 6.160 total
python3 tests/len.py 2 : 6.16s user . 0.06s system . 100% cpu . 6.212 total
python3 tests/len.py 2 : 6.03s user . 0.06s system . 100% cpu . 6.086 total
"""