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
    "�˶���Ȧ����V1001����"
    print "�˶���Ȧ����Э��汾V1.0.01"

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
        offset += nodesize * 2
        info = copy.copy(countcircleInfo)
        countcircleData.append(info)
    str(i)

def printInfo():
    "����˶���Ȧ����V1001"
    
    i = 0
    # ��һ���ļ�
    file = open(info.outfile, "a")
    for i in range(len(countcircleData)):
        print "��%d��%d�׼�Ȧ��Ϣ:"%(i + 1, countcircleData[i][CountCircleInfo.UNIT])
        if (info.SportMode.SPORT_RIDE != info.mode):
            print "����:\t\t%s\t\t%d'%d\""%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 60, countcircleData[i][CountCircleInfo.PACE] % 60)
        else:
            print "�ٶ�:\t\t%s\t\t%d.%dkm/h"%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 1000, (countcircleData[i][CountCircleInfo.PACE] % 1000) / 100)
        print "�˶�ʱ��:\t" + hex(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "��"
        print "��ͣʱ��:\t\t" + hex(countcircleData[i][CountCircleInfo.PAUSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.PAUSETIME]) + "��"
        print "����:\t\t" + hex(countcircleData[i][CountCircleInfo.UNIT]) + "\t\t" + str(countcircleData[i][CountCircleInfo.UNIT]) + "��"

        file.write("��%d��%d�׼�Ȧ��Ϣ:\n"%(i + 1, countcircleData[i][CountCircleInfo.UNIT]))
        if (info.SportMode.SPORT_RIDE != info.mode):
            file.write("����:\t\t%s\t\t%d'%d\""%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 60, countcircleData[i][CountCircleInfo.PACE] % 60) + "\n")
        else:
            file.write("�ٶ�:\t\t%s\t\t%d.%dkm/h"%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 1000, (countcircleData[i][CountCircleInfo.PACE] % 1000) / 100) + "\n")
        file.write("�˶�ʱ��:\t" + hex(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "��\n")
        file.write("��ͣʱ��:\t\t" + hex(countcircleData[i][CountCircleInfo.PAUSETIME]) + "\t\t\t" + str(countcircleData[i][CountCircleInfo.PAUSETIME]) + "��\n")
        file.write("����:\t\t" + hex(countcircleData[i][CountCircleInfo.UNIT]) + "\t\t" + str(countcircleData[i][CountCircleInfo.UNIT]) + "��\n")
        file.write("*" * 40 + "\n")
    file.flush()
    file.close()
