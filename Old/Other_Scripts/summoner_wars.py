__author__ = "Charles Engen"

import time


class Summoner(object):
    def __init__(self):
        self.monsters_inventory = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.monsters_needed = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self._sacrifice_1_star_xp = {1: 493}
        self._sacrifice_2_star_xp = {1: 1760}
        self._sacrifice_3_star_xp = {1: 3200}
        self._cost_to_evolve_6 = 35200
        self._cost_to_evolve_5 = 22400
        self._cost_to_evolve_4 = 9600
        self._cost_to_evolve_3 = 4000
        self._cost_to_evolve_2 = 1600
        self._xp_needed = 0
        self._max_1_star = {
            1: 460,
            2: 516,
            3: 579,
            4: 650,
            5: 728,
            6: 818,
            7: 918,
            8: 1029,
            9: 1155,
            10: 1296,
            11: 1455,
            12: 1631,
            13: 1831,
            14: 2054,
            "max": 15120,
        }
        self._max_2_star = {
            1: 552,
            2: 619,
            3: 695,
            4: 779,
            5: 875,
            6: 981,
            7: 1102,
            8: 1235,
            9: 1386,
            10: 1555,
            11: 1745,
            12: 1958,
            13: 2197,
            14: 2465,
            15: 2765,
            16: 3103,
            17: 3481,
            18: 3906,
            19: 4423,
            "max": 35822,
        }
        self._max_3_star = {
            1: 662,
            2: 743,
            3: 834,
            4: 936,
            5: 1049,
            6: 1178,
            7: 1321,
            8: 1483,
            9: 1663,
            10: 1866,
            11: 2094,
            12: 2350,
            13: 2636,
            14: 2957,
            15: 3319,
            16: 3723,
            17: 4178,
            18: 4687,
            19: 5307,
            20: 6009,
            21: 6802,
            22: 7703,
            23: 8720,
            24: 9962,
            "max": 82182,
        }
        self._max_4_star = {
            1: 796,
            2: 892,
            3: 1002,
            4: 1124,
            5: 1261,
            6: 1415,
            7: 1587,
            8: 1781,
            9: 1998,
            10: 2243,
            11: 2515,
            12: 2823,
            13: 3167,
            14: 3553,
            15: 3987,
            16: 4473,
            17: 5019,
            18: 5631,
            19: 6376,
            20: 7219,
            21: 8172,
            22: 9254,
            23: 10476,
            24: 11969,
            25: 13673,
            26: 15619,
            27: 17844,
            28: 20386,
            29: 23495,
            "max": 189750,
        }
        self._max_5_star = {
            1: 952,
            2: 1068,
            3: 1199,
            4: 1344,
            5: 1509,
            6: 1693,
            7: 1899,
            8: 2131,
            9: 2392,
            10: 2682,
            11: 3010,
            12: 3378,
            13: 3789,
            14: 4252,
            15: 4770,
            16: 5352,
            17: 6006,
            18: 6738,
            19: 7628,
            20: 8638,
            21: 9779,
            22: 11072,
            23: 12535,
            24: 14321,
            25: 16360,
            26: 18690,
            27: 21350,
            28: 24392,
            29: 28113,
            30: 32404,
            31: 37348,
            32: 43048,
            33: 49617,
            34: 57188,
            "max": 446647,
        }
        self._max_6_star = {
            1: 1150,
            2: 1290,
            3: 1447,
            4: 1624,
            5: 1823,
            6: 2044,
            7: 2294,
            8: 2574,
            9: 2888,
            10: 3240,
            11: 3635,
            12: 4079,
            13: 4576,
            14: 5135,
            15: 5762,
            16: 6464,
            17: 7252,
            18: 8138,
            19: 9214,
            20: 10431,
            21: 11811,
            22: 13371,
            23: 15140,
            24: 17296,
            25: 19758,
            26: 22572,
            27: 25786,
            28: 29458,
            29: 33954,
            30: 39134,
            31: 45107,
            32: 51990,
            33: 59924,
            34: 69068,
            35: 76085,
            36: 83816,
            37: 92332,
            38: 101712,
            39: 112046,
            "max": 1005420,
        }

    # def _info_string_to_id_number(self, xp, level):
    #     return int(''.join([''.join([str(ord(letter)) for letter in time.ctime()]), str(level), str(xp)]))
    #
    # def add_to_inventory(self, current_star, current_level, current_xp):
    #     id_monster = self._info_string_to_id_number(level=current_level, xp=current_xp)
    #     self.monsters_inventory[current_star][id_monster] = {'level': current_level, 'xp': current_xp}
    #
    # def _adjust_inventory_monster(self, monster):
    #     if self.monsters_inventory[monster]:
    #         self.monsters_inventory[monster] -= 1
    #         return 1
    #     else:
    #         return 0
    def get_need_monsters(self, star):
        if star == 2:
            a = [
                (y, x, s, st, sta)
                for sta in range(1, star + 1)
                for st in range(1, sta + 1)
                for s in range(1, st + 1)
                for x in range(1, s + 1)
                for y in range(1, x + 1)
            ]
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        for sta in range(1, star + 1):
            a += 1
            for st in range(1, sta + 1):
                b += 1
                for s in range(1, st + 1):
                    c += 1
                    for x in range(1, s + 1):
                        d += 1
                        for y in range(1, x + 1):
                            e += 1
        print("A: %s, B: %s, C: %s, D:%s, E: %s" % (a, b, c, d, e))

    def return_monsters_needed(self):
        return (
            "You need %s 5*s, %s 4*s, %s 3*s, %s 2*s, %s 1*s. "
            "The total gold needed is %s"
            % (
                self.monsters_needed[5],
                self.monsters_needed[4],
                self.monsters_needed[3],
                self.monsters_needed[2],
                self.monsters_needed[1],
                (),
            )
        )
