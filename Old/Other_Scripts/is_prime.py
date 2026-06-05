__author__ = "Charles Engen"

# import cProfile
#
# def run_program(x):
#     a = []
#     for i in range(x):
#         b = is_prime(i, False)
#         if b:
#             a.append(b)
#
# cProfile.run("run_program(50000)")


def is_prime(get_number, display=False):

    prime = True

    _numbers_to_number = [number for number in range(2, get_number)]

    for number in _numbers_to_number:
        if get_number % number == 0:
            prime = False
            break

    if prime:
        if display:
            print("%s is a prime" % prime)
        return get_number
    elif not prime:
        if display:
            print("%s is not a Prime" % get_number)


def factors_to_1000():
    list_of_primes = []
    for i in range(1001):
        if True == is_prime(i):
            list_of_primes.append(i)
    return list_of_primes


class Divisible(BaseException):
    pass


def is_prime(number):
    primes_to_1000 = [
        1,
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
        101,
        103,
        107,
        109,
        113,
        127,
        131,
        137,
        139,
        149,
        151,
        157,
        163,
        167,
        173,
        179,
        181,
        191,
        193,
        197,
        199,
        211,
        223,
        227,
        229,
        233,
        239,
        241,
        251,
        257,
        263,
        269,
        271,
        277,
        281,
        283,
        293,
        307,
        311,
        313,
        317,
        331,
        337,
        347,
        349,
        353,
        359,
        367,
        373,
        379,
        383,
        389,
        397,
        401,
        409,
        419,
        421,
        431,
        433,
        439,
        443,
        449,
        457,
        461,
        463,
        467,
        479,
        487,
        491,
        499,
        503,
        509,
        521,
        523,
        541,
        547,
        557,
        563,
        569,
        571,
        577,
        587,
        593,
        599,
        601,
        607,
        613,
        617,
        619,
        631,
        641,
        643,
        647,
        653,
        659,
        661,
        673,
        677,
        683,
        691,
        701,
        709,
        719,
        727,
        733,
        739,
        743,
        751,
        757,
        761,
        769,
        773,
        787,
        797,
        809,
        811,
        821,
        823,
        827,
        829,
        839,
        853,
        857,
        859,
        863,
        877,
        881,
        883,
        887,
        907,
        911,
        919,
        929,
        937,
        941,
        947,
        953,
        967,
        971,
        977,
        983,
        991,
        997,
    ]

    def divide_by_primes_1000(number):
        for a_number in primes_to_1000:
            if number % a_number == 0:
                raise Divisible

    def factor_primes(factor):
        return [item ** factor for item in primes_to_1000]

    if number < 2:
        return False
    elif number < 1001:
        try:
            divide_by_primes_1000(number)
        except Divisible:
            return False
    else:
        try:
            if number in primes_to_1000:
                raise Divisible
            divide_by_primes_1000(number)
        except Divisible:
            return False
        else:
            try:
                hold_factors = [factor_primes(i) for i in primes_to_1000[:10]]
                if number in hold_factors:
                    raise Divisible
                for a_num in range(1001, number):
                    if number % a_num == 0:
                        raise Divisible
            except Divisible:
                return False
    return True
