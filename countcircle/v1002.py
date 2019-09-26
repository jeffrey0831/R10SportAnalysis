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
    LONGITUDE = 4
    LATITUDE = 5
    LONGITUDE_EW = 6
    LATITUDE_NS = 7
    MAXITEM = 9

countcircleData = []
countcircleInfo = []

def initInfo():
    for i in range(CountCircleInfo.MAXITEM):
        countcircleInfo.append(0)
    str(i)

def analysisInfo(buffer, buffersize, nodenum, nodesize):
    "�˶���Ȧ����V1002����"
    print "�˶���Ȧ����Э��汾V1.0.02"

    i = 0
    leftsize = buffersize
    offset = 0
    for i in range(nodenum):
        if (leftsize < nodesize * 2):
            print "�˶���Ȧ���ݲ�����"
            print buffer[offset:]
            break
        else:
            leftsize -= nodesize * 2

        countcircleInfo[CountCircleInfo.PACE] = util.getUint32(buffer[offset + 0:offset + 8])
        countcircleInfo[CountCircleInfo.ELAPSETIME] = util.getUint32(buffer[offset + 8:offset + 16])
        countcircleInfo[CountCircleInfo.PAUSETIME] = util.getUint32(buffer[offset + 16:offset + 24])
        countcircleInfo[CountCircleInfo.UNIT] = util.getUint32(buffer[offset + 24:offset + 32])
        countcircleInfo[CountCircleInfo.LONGITUDE] = util.getUint32(buffer[offset + 32:offset + 40])
        countcircleInfo[CountCircleInfo.LATITUDE] = util.getUint32(buffer[offset + 40:offset + 48])
        countcircleInfo[CountCircleInfo.LONGITUDE_EW] = util.getUint8(buffer[offset + 48:offset + 50])
        countcircleInfo[CountCircleInfo.LATITUDE_NS] = util.getUint8(buffer[offset + 50:offset + 52])
        offset += nodesize * 2
        info = copy.copy(countcircleInfo)
        countcircleData.append(info)
    str(i)

def printInfo():
    "����˶���Ȧ����V1002"
    
    i = 0
    # ��һ���ļ�
    file = open(info.outfile, "a")
    for i in range(len(countcircleData)):
        longitude = float(countcircleData[i][CountCircleInfo.LONGITUDE]) / 1000000
        latitude = float(countcircleData[i][CountCircleInfo.LATITUDE]) / 1000000
        longitude_ew = chr(countcircleData[i][CountCircleInfo.LONGITUDE_EW])
        latitude_ns = chr(countcircleData[i][CountCircleInfo.LATITUDE_NS])
        
        if 0xffffffff == countcircleData[i][CountCircleInfo.LONGITUDE]: longitude = 0
        if 0xffffffff == countcircleData[i][CountCircleInfo.LATITUDE]: latitude = 0
        if countcircleData[i][CountCircleInfo.LONGITUDE_EW] in (0, 0xff): longitude_ew = ""
        if countcircleData[i][CountCircleInfo.LATITUDE_NS] in (0, 0xff): latitude_ns = ""

        print "��Ȧ" +str(i + 1) + "��Ϣ:"
        if (info.SportMode.SPORT_RIDE != info.mode):
            print "pace:\t\t%s\t\t%d'%d\""%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 60, countcircleData[i][CountCircleInfo.PACE] % 60)
        else:
            print "speed:\t\t%s\t\t%d.%dkm/h"%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 1000, (countcircleData[i][CountCircleInfo.PACE] % 1000) / 100)
        print "elapsetime:\t" + hex(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "��"
        print "pause:\t\t" + hex(countcircleData[i][CountCircleInfo.PAUSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.PAUSETIME]) + "��"
        print "unit:\t\t" + hex(countcircleData[i][CountCircleInfo.UNIT]) + "\t\t" + str(countcircleData[i][CountCircleInfo.UNIT]) + "��"
        print "longitude:\t" + hex(countcircleData[i][CountCircleInfo.LONGITUDE]) + "\t" + str(longitude) + longitude_ew
        print "latitude:\t" + hex(countcircleData[i][CountCircleInfo.LATITUDE]) + "\t" + str(latitude) + latitude_ns

        file.write("��%d��%d�׼�Ȧ��Ϣ:\n"%(i + 1, countcircleData[i][CountCircleInfo.UNIT]))
        if (info.SportMode.SPORT_RIDE != info.mode):
            file.write("pace:\t\t%s\t\t%d'%d\""%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 60, countcircleData[i][CountCircleInfo.PACE] % 60) + "\n")
        else:
            file.write("speed:\t\t%s\t\t%d.%dkm/h"%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 1000, (countcircleData[i][CountCircleInfo.PACE] % 1000) / 100) + "\n")
        file.write("elapsetime:\t" + hex(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "��\n")
        file.write("pause:\t\t" + hex(countcircleData[i][CountCircleInfo.PAUSETIME]) + "\t\t\t" + str(countcircleData[i][CountCircleInfo.PAUSETIME]) + "��\n")
        file.write("unit:\t\t" + hex(countcircleData[i][CountCircleInfo.UNIT]) + "\t\t" + str(countcircleData[i][CountCircleInfo.UNIT]) + "��\n")
        file.write("longitude:\t" + hex(countcircleData[i][CountCircleInfo.LONGITUDE]) + "\t" + str(longitude) + longitude_ew + "\n")
        file.write("latitude:\t" + hex(countcircleData[i][CountCircleInfo.LATITUDE]) + "\t" + str(latitude) + latitude_ns + "\n")
        file.write("*" * 40 + "\n")
    file.flush()
    file.close()

