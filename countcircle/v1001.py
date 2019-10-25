# coding=gbk

import copy
import os
import shutil

import info
import util

class CountCircleInfo():
    PACE = 0
    ELAPSETIME = 1
    PAUSETIME = 2
    UNIT = 3
    MAXITEM = 4

countcircleData = []
countcircleInfo = []

def initInfo():
    for i in range(CountCircleInfo.MAXITEM):
        countcircleInfo.append(0)
    str(i)

def analysisInfo(buffer, buffersize, nodenum, nodesize):
    "运动计圈数据V1001解析"
    print "运动计圈数据协议版本V1.0.01"

    leftsize = buffersize
    offset = 0
    for i in range(nodenum):
        if (leftsize < nodesize * 2):
            print "运动计圈数据不完整"
            print buffer[offset:]
            break
        else:
            leftsize -= nodesize * 2

        countcircleInfo[CountCircleInfo.PACE] = util.getUint32(buffer[offset + 0:offset + 8])
        countcircleInfo[CountCircleInfo.ELAPSETIME] = util.getUint32(buffer[offset + 8:offset + 16])
        countcircleInfo[CountCircleInfo.PAUSETIME] = util.getUint32(buffer[offset + 16:offset + 24])
        countcircleInfo[CountCircleInfo.UNIT] = util.getUint32(buffer[offset + 24:offset + 32])
        offset += nodesize * 2
        info = copy.copy(countcircleInfo)
        countcircleData.append(info)
    str(i)

def printInfo():
    "输出运动计圈数据V1001"
    
    i = 0
    # 打开一个文件
    file = open(info.outfile, "a")
    for i in range(len(countcircleData)):
        print "第%d个%d米计圈信息:"%(i + 1, countcircleData[i][CountCircleInfo.UNIT])
        if (info.SportMode.SPORT_RIDE != info.mode):
            print "配速:\t\t%s\t\t%d'%d\""%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 60, countcircleData[i][CountCircleInfo.PACE] % 60)
        else:
            print "速度:\t\t%s\t\t%d.%dkm/h"%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 1000, (countcircleData[i][CountCircleInfo.PACE] % 1000) / 100)
        print "运动时间:\t" + hex(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "秒"
        print "暂停时间:\t\t" + hex(countcircleData[i][CountCircleInfo.PAUSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.PAUSETIME]) + "秒"
        print "距离:\t\t" + hex(countcircleData[i][CountCircleInfo.UNIT]) + "\t\t" + str(countcircleData[i][CountCircleInfo.UNIT]) + "米"

        file.write("第%d个%d米计圈信息:\n"%(i + 1, countcircleData[i][CountCircleInfo.UNIT]))
        if (info.SportMode.SPORT_RIDE != info.mode):
            file.write("配速:\t\t%s\t\t%d'%d\""%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 60, countcircleData[i][CountCircleInfo.PACE] % 60) + "\n")
        else:
            file.write("速度:\t\t%s\t\t%d.%dkm/h"%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 1000, (countcircleData[i][CountCircleInfo.PACE] % 1000) / 100) + "\n")
        file.write("运动时间:\t" + hex(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "秒\n")
        file.write("暂停时间:\t\t" + hex(countcircleData[i][CountCircleInfo.PAUSETIME]) + "\t\t\t" + str(countcircleData[i][CountCircleInfo.PAUSETIME]) + "秒\n")
        file.write("距离:\t\t" + hex(countcircleData[i][CountCircleInfo.UNIT]) + "\t\t" + str(countcircleData[i][CountCircleInfo.UNIT]) + "米\n")
        file.write("*" * 40 + "\n")
    file.flush()
    file.close()
