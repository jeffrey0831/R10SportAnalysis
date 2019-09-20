# coding=gbk

import copy
import os
import shutil

import info
import util

class Statistics():
    MODE = 0
    AVERAGEHR = 1
    MAXHR = 2
    TIMEZONE = 3
    DISTRIBUTED1 = 4
    DISTRIBUTED2 = 5
    DISTRIBUTED3 = 6
    DISTRIBUTED4 = 7
    DISTRIBUTED5 = 8
    MAXCADENCE = 9
    RISEATMOSPRESS = 10
    DROPATMOSPRESS = 11
    MAXATMOSPRESS = 12
    MINATMOSPRESS = 13
    ATMOSPRESS = 14
    CALORIE = 15
    BESTPACE = 16
    TIMESTAMP = 17
    ACCOMPLISHTIME = 18
    PAUSETIME = 19
    DISTANCE = 20
    CALIDISTANCE = 21
    STEP = 22
    MAXITEM = 23

statisticsData = []

def initInfo():
    "��ʼ��ͳ�������б�"
    for i in range(Statistics.MAXITEM):
        statisticsData.append(0)
        i

def analysisInfo(buffer, buffersize, nodenum, nodesize):
    "�˶�ͳ������V1004����"
    print "�˶�ͳ������Э��汾V1.0.04"

    if (buffersize < nodesize * 2):
        print "�˶�ͳ�����ݲ�����"
        print buffer
        return

    statisticsData[Statistics.MODE] = util.getUint8(buffer[0:2])
    statisticsData[Statistics.AVERAGEHR] = util.getUint8(buffer[2:4])
    statisticsData[Statistics.MAXHR] = util.getUint8(buffer[4:6])
    statisticsData[Statistics.TIMEZONE] = util.getUint8(buffer[6:8])
    statisticsData[Statistics.DISTRIBUTED1] = util.getUint16(buffer[8:12])
    statisticsData[Statistics.DISTRIBUTED2] = util.getUint16(buffer[12:16])
    statisticsData[Statistics.DISTRIBUTED3] = util.getUint16(buffer[16:20])
    statisticsData[Statistics.DISTRIBUTED4] = util.getUint16(buffer[20:24])
    statisticsData[Statistics.DISTRIBUTED5] = util.getUint16(buffer[24:28])
    statisticsData[Statistics.MAXCADENCE] = util.getUint16(buffer[28:32])
    statisticsData[Statistics.RISEATMOSPRESS] = util.getUint32(buffer[32:40])
    statisticsData[Statistics.DROPATMOSPRESS] = util.getUint32(buffer[40:48])
    statisticsData[Statistics.MAXATMOSPRESS] = util.getUint32(buffer[48:56])
    statisticsData[Statistics.MINATMOSPRESS] = util.getUint32(buffer[56:64])
    statisticsData[Statistics.ATMOSPRESS] = util.getUint32(buffer[64:72])
    statisticsData[Statistics.CALORIE] = util.getUint32(buffer[72:80])
    statisticsData[Statistics.BESTPACE] = util.getUint32(buffer[80:88])
    statisticsData[Statistics.TIMESTAMP] = util.getUint32(buffer[88:96])
    statisticsData[Statistics.ACCOMPLISHTIME] = util.getUint32(buffer[96:104])
    statisticsData[Statistics.PAUSETIME] = util.getUint32(buffer[104:112])
    statisticsData[Statistics.DISTANCE] = util.getUint32(buffer[112:120])
    statisticsData[Statistics.CALIDISTANCE] = util.getUint32(buffer[120:128])
    statisticsData[Statistics.STEP] = util.getUint32(buffer[128:136])

    info.mode = statisticsData[Statistics.MODE]
    info.uuid = statisticsData[Statistics.TIMESTAMP]

def printInfo():
    "��ӡͳ��������Ϣ"

    modeName = ["����", "������", "������", "����"]
    hrCount = 0
    for i in range(5):
        hrCount += statisticsData[Statistics.DISTRIBUTED1 + i]

    h = statisticsData[Statistics.ACCOMPLISHTIME] / 3600
    m = (statisticsData[Statistics.ACCOMPLISHTIME] - h * 3600) / 60
    s = statisticsData[Statistics.ACCOMPLISHTIME] % 60
    if (h > 0):
        accomplishtime = str(h) + "Сʱ" + str(m) + "��" + str(s) + "��"
    else:
        accomplishtime = str(m) + "��" + str(s) + "��"

    if (statisticsData[Statistics.MODE] < info.SportMode.SPORT_MAX):
        print "�˶�����:\t" + hex(statisticsData[Statistics.MODE]) + "\t\t" + modeName[statisticsData[Statistics.MODE]]
    else:
        print "�˶�����:\t " + hex(statisticsData[Statistics.MODE]) + "\t\t�޷�ʶ��"

    print "ƽ������:\t" + str(statisticsData[Statistics.AVERAGEHR])
    print "�������:\t" + str(statisticsData[Statistics.MAXHR])
    print "ʱ��:\t\t" + str(statisticsData[Statistics.TIMEZONE])

    for i in range(5):
        if 0 == hrCount:
            print "��������%d:\t%d\t\t%d%s"%(i + 1, statisticsData[Statistics.DISTRIBUTED1 + i], 0, "%")
        else:
            print "��������%d:\t%d\t\t%d%s"%(i + 1, statisticsData[Statistics.DISTRIBUTED1 + i], statisticsData[Statistics.DISTRIBUTED1 + i] * 100 / hrCount, "%")

    print "���Ƶ:\t" + str(statisticsData[Statistics.MAXCADENCE]) + "spm"
    print "��������ѹ:\t" + str(statisticsData[Statistics.RISEATMOSPRESS]) + "��"
    print "�½�����ѹ:\t" + str(statisticsData[Statistics.DROPATMOSPRESS]) + "��"
    print "������ѹ:\t" + str(statisticsData[Statistics.MAXATMOSPRESS]) + "��"
    print "��С����ѹ:\t" + str(statisticsData[Statistics.MINATMOSPRESS]) + "��"
    print "��ʼ����ѹ:\t" + str(statisticsData[Statistics.ATMOSPRESS]) + "��"
    print "��·������:\t" + str(statisticsData[Statistics.CALORIE]) + "��"
    if info.SportMode.SPORT_RIDE != info.mode:
        print "�������:\t%d\t\t%d'%d\""%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 60, statisticsData[Statistics.BESTPACE] % 60)
    else:
        print "����ٶ�:\t%d\t\t%d.%dkm/h"%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 1000, (statisticsData[Statistics.BESTPACE] % 1000) / 100)
    print "��ʼʱ���:\t" + str(statisticsData[Statistics.TIMESTAMP]) + "\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP])
    print "���ʱ��:\t" + str(accomplishtime) + "\t\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP] + statisticsData[Statistics.ACCOMPLISHTIME])
    print "��ͣʱ��:\t" + str(statisticsData[Statistics.PAUSETIME]) + "��"
    print "����:\t\t" + str(statisticsData[Statistics.DISTANCE]) + "��"
    print "У׼����:\t" + str(statisticsData[Statistics.CALIDISTANCE]) + "��"
    print "����:\t\t" + str(statisticsData[Statistics.STEP]) + "��"

    file = open(info.outfile, "a")
    if (statisticsData[Statistics.MODE] < info.SportMode.SPORT_MAX):
        file.write("�˶�����:\t" + hex(statisticsData[Statistics.MODE]) + "\t\t\t" + modeName[statisticsData[Statistics.MODE]] + "\n")
    else:
        file.write("�˶�����:\t " + hex(statisticsData[Statistics.MODE]) + "\t\t\t�޷�ʶ��\n")

    file.write("ƽ������:\t" + str(statisticsData[Statistics.AVERAGEHR]) + "\n")
    file.write("�������:\t" + str(statisticsData[Statistics.MAXHR]) + "\n")
    file.write("ʱ��:\t\t" + str(statisticsData[Statistics.TIMEZONE]) + "\n")

    for i in range(5):
        if 0 == hrCount:
            file.write("��������%d:\t%d\t\t\t%d%s"%(i + 1, statisticsData[Statistics.DISTRIBUTED1 + i], 0, "%") + "\n")
        else:
            file.write("��������%d:\t%d\t\t\t%d%s"%(i + 1, statisticsData[Statistics.DISTRIBUTED1 + i], statisticsData[Statistics.DISTRIBUTED1 + i] * 100 / hrCount, "%") + "\n")

    file.write("���Ƶ:\t" + str(statisticsData[Statistics.MAXCADENCE]) + " spm" + "\n")
    file.write("��������ѹ:\t" + str(statisticsData[Statistics.RISEATMOSPRESS]) + " pa" + "\n")
    file.write("�½�����ѹ:\t" + str(statisticsData[Statistics.DROPATMOSPRESS]) + " pa" + "\n")
    file.write("������ѹ:\t" + str(statisticsData[Statistics.MAXATMOSPRESS]) + " pa" + "\n")
    file.write("��С����ѹ:\t" + str(statisticsData[Statistics.MINATMOSPRESS]) + " pa" + "\n")
    file.write("��ʼ����ѹ:\t" + str(statisticsData[Statistics.ATMOSPRESS]) + " pa" + "\n")
    file.write("��·������:\t" + str(statisticsData[Statistics.CALORIE]) + " cal" + "\n")
    if info.SportMode.SPORT_RIDE != info.mode:
       file.write("�������:\t%d\t\t%d'%d\""%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 60, statisticsData[Statistics.BESTPACE] % 60) + "\n")
    else:
       file.write("����ٶ�:\t%d\t\t%d.%dkm/h"%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 1000, (statisticsData[Statistics.BESTPACE] % 1000) / 100) + "\n")
    file.write("��ʼʱ���:\t" + str(statisticsData[Statistics.TIMESTAMP]) + "\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP]) + "\n")
    file.write("���ʱ��:\t" + str(accomplishtime) + "\t\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP] + statisticsData[Statistics.ACCOMPLISHTIME]) + "\n")
    file.write("��ͣʱ��:\t" + str(statisticsData[Statistics.PAUSETIME]) + "��" + "\n")
    file.write("����:\t\t" + str(statisticsData[Statistics.DISTANCE]) + " m" + "\n")
    file.write("У׼����:\t" + str(statisticsData[Statistics.CALIDISTANCE]) + " m" + "\n")
    file.write("����:\t\t" + str(statisticsData[Statistics.STEP]) + "��" + "\n")
    file.write("*" * 40 + "\n")
    file.flush()
    file.close()
