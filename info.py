# coding=gbk

import time

class SportMode():
    SPORT_WALK = 0
    SPORT_RUN_OUT = 1
    SPORT_RUN_IN = 2
    SPORT_RIDE = 3
    SPORT_MAX = 4

outfile = "output.txt"
mode = 0
uuid = int(time.time())
dataindex = 0

