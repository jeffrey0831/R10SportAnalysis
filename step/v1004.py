# coding=gbk

import copy
import os
import shutil

import info
import util

class StepInfo():
    TIMESTAMP = 0
    TIMEZONE = 1
    SEDENTARYCOUNT = 2
    REVERSE = 3
    CALORIEBMR = 4
    CALORIESPORT = 5
    STEPHOUR = 6
    DISTANCEHOUR = 7
    MAXITEM = 54

stepData = []
stepInfo = []

def initInfo():
    "初始化计步数据列表"
    for i in range(StepInfo.MAXITEM):
        stepInfo.append(0)
    str(i)

def analysisInfo(buffer, buffersize, nodenum, nodesize):
    "计步数据V1004解析"
    print "计步数据协议版本V1.0.04"

    i = 0
    offset = 0
    leftsize = buffersize
    for i in range(nodenum):
        if (leftsize < nodesize * 2):
            print "计步数据不完整"
            print buffer[offset:]
            break
        else:
            leftsize -= nodesize * 2

        stepInfo[StepInfo.TIMESTAMP] = util.getUint32(buffer[offset + 0:offset + 8])
        stepInfo[StepInfo.TIMEZONE] = util.getUint8(buffer[offset + 8:offset + 10])
        stepInfo[StepInfo.SEDENTARYCOUNT] = util.getUint8(buffer[offset + 10:offset + 12])
        stepInfo[StepInfo.REVERSE] = util.getUint16(buffer[offset + 12:offset + 16])
        stepInfo[StepInfo.CALORIEBMR] = util.getUint32(buffer[offset + 16:offset + 24])
        stepInfo[StepInfo.CALORIESPORT] = util.getUint32(buffer[offset + 24:offset + 32])
        for j in range(24):
            start = offset + 32 + 8 * j
            end = offset + 36 + 8 * j
            stepInfo[StepInfo.STEPHOUR + j * 2] = util.getUint16(buffer[start:end])
            stepInfo[StepInfo.DISTANCEHOUR + j * 2] = util.getUint16(buffer[end:end + 4])
        offset += nodesize * 2
        i
        info = copy.copy(stepInfo)
        stepData.append(info)
        print info

def printInfo():
    "输出计步数据"

    for i in range(len(stepData)):
        print str(i + 1) + "天计步信息:"
        print "当地时间:\t" + hex(stepData[i][StepInfo.TIMESTAMP]) + "\t\t" + util.converUnixTimestamp(stepData[i][StepInfo.TIMESTAMP])

        print "时区:\t\t" + hex(stepData[i][StepInfo.TIMEZONE]) + "\t\t\t" + str(stepData[i][StepInfo.TIMEZONE])
        print "久坐:\t\t" + hex(stepData[i][StepInfo.SEDENTARYCOUNT]) + "\t\t\t" + str(stepData[i][StepInfo.SEDENTARYCOUNT])
        print "静息卡路里:\t" + hex(stepData[i][StepInfo.CALORIEBMR]) + "\t\t\t" + str(stepData[i][StepInfo.CALORIEBMR])
        print "运动卡路里:\t" + hex(stepData[i][StepInfo.CALORIESPORT]) + "\t\t\t" + str(stepData[i][StepInfo.CALORIESPORT])
        for j in range(24):
            if j < 10:
                h = "0" + str(j)
            else:
                h = str(j) 
            print h + ":00 步数:\t" + hex(stepData[i][StepInfo.STEPHOUR + j * 2]) + "\t\t\t" + str(stepData[i][StepInfo.STEPHOUR + j * 2]) + "\t距离:\t" + hex(stepData[i][StepInfo.DISTANCEHOUR + j * 2]) + "\t\t\t" + str(stepData[i][StepInfo.DISTANCEHOUR + j * 2])
        util.printDividingLine()
