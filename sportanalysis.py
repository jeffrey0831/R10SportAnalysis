# coding=gbk

import copy
import math
import os
import shutil
import util

class SportMode():
    SPORT_WALK = 0
    SPORT_RUN_OUT = 1
    SPORT_RUN_IN = 2
    SPORT_RIDE = 3
    SPORT_MAX = 4

class DataHead():
    UUID = 0
    MODEL1 = 1
    MODEL2 = 2
    VERSION = 3
    NODESIZE = 4
    NODENUM = 5
    MAXITEM = 6

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

class RealtimeData():
    PAUSE = 0
    HR = 1
    LONGITUDE_EW = 2
    LATITUDE_NS = 3
    CADENCE = 4
    TEMPERATURE = 5
    PACE = 6
    LATITUDE = 7
    LONGITUDE = 8
    ATMOSPRESS = 9
    MAXITEM = 10

class CountCircleInfo():
    PACE = 0
    ELAPSETIME = 1
    PAUSETIME = 2
    UNIT = 3
    MAXITEM = 4

class GnssInfo():
    LONGITUDE_EW = 0
    LONGITUDE = 1
    LATITUDE_NS = 2
    LATITUDE = 3
    MAXITEM = 4

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

dataInfo = []
statisticsData = []
realtimeData = []
realtimeInfo = []
countcircleData = []
countcircleInfo = []
stepData = []
stepInfo = []
gnssInfo = [ "", 0.0, "", 0.0 ]

def rad(d):
    PI = 3.1415926535898;
    return d * PI / 180.0;

def computeDistanceByGnss(longitude, latitude, longitude_ew, latitude_ns):
    R = 6378137.0;

    if 0 == longitude or 0 == latitude or 0 == gnssInfo[GnssInfo.LONGITUDE] or 0 == gnssInfo[GnssInfo.LATITUDE]:
        gnssInfo[GnssInfo.LONGITUDE] = longitude
        gnssInfo[GnssInfo.LATITUDE] = latitude
        gnssInfo[GnssInfo.LONGITUDE_EW] = longitude_ew
        gnssInfo[GnssInfo.LATITUDE_NS] = latitude_ns
        return 0

    longitude1 = longitude
    latitude1 = latitude
    longitude2 = gnssInfo[GnssInfo.LONGITUDE]
    latitude2 = gnssInfo[GnssInfo.LATITUDE]
    
    if 'W' == longitude_ew: longitude1 = longitude1 * (-1.0)
    if 'S' == latitude_ns: latitude1 = latitude1 * (-1.0)
    if 'W' == gnssInfo[GnssInfo.LONGITUDE_EW]: longitude2 = longitude2 * (-1.0)
    if 'S' == gnssInfo[GnssInfo.LATITUDE_NS]: latitude2 = latitude2 * (-1.0)

    gnssInfo[GnssInfo.LONGITUDE] = longitude
    gnssInfo[GnssInfo.LATITUDE] = latitude
    gnssInfo[GnssInfo.LONGITUDE_EW] = longitude_ew
    gnssInfo[GnssInfo.LATITUDE_NS] = latitude_ns
    
    # ���Ƕ�ת��Ϊ����
    radLog1 = rad(longitude1)
    radLat1 = rad(latitude1)
    radLog2 = rad(longitude2)
    radLat2 = rad(latitude2)

    # γ�ȵĲ�ֵ
    a = radLat1 - radLat2
    # ���Ȳ�ֵ
    b = radLog1 - radLog2
    # ���ȳ���
    s = 2 * math.asin(math.sqrt(pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * pow(math.sin(b / 2), 2)));
    # ��ȡ����
    s = s * R;
    # ������ӽ������� long�����������Ϊ���������� 1/2
    s = round(s * 10000) / 10000;

    return s;

def printStatisticsInfo():
    "��ӡͳ��������Ϣ"

    modeName = ["����", "������", "������", "����"]
    hrCount = 0
    for i in range(5):
        hrCount += statisticsData[Statistics.DISTRIBUTED1 + i]

    if (statisticsData[Statistics.MODE] < 4):
        print "�˶�����:\t" + hex(statisticsData[Statistics.MODE]) + "\t\t" + modeName[statisticsData[Statistics.MODE]]
    else:
        print "�˶�����:\t " + hex(statisticsData[Statistics.MODE]) + "\t\t�޷�ʶ��"

    print "ƽ������:\t" + str(statisticsData[Statistics.AVERAGEHR])
    print "�������:\t" + str(statisticsData[Statistics.MAXHR])
    print "ʱ��:\t\t" + str(statisticsData[Statistics.TIMEZONE])

    for i in range(5):
        print "��������%d:\t%d\t\t%d%s"%(i + 1, statisticsData[Statistics.DISTRIBUTED1 + i], statisticsData[Statistics.DISTRIBUTED1 + i] * 100 / hrCount, "%")

    print "���Ƶ:\t" + str(statisticsData[Statistics.MAXCADENCE]) + "spm"
    print "��������ѹ:\t" + str(statisticsData[Statistics.RISEATMOSPRESS]) + "��"
    print "�½�����ѹ:\t" + str(statisticsData[Statistics.DROPATMOSPRESS]) + "��"
    print "������ѹ:\t" + str(statisticsData[Statistics.MAXATMOSPRESS]) + "��"
    print "��С����ѹ:\t" + str(statisticsData[Statistics.MINATMOSPRESS]) + "��"
    print "��ʼ����ѹ:\t" + str(statisticsData[Statistics.ATMOSPRESS]) + "��"
    print "��·������:\t" + str(statisticsData[Statistics.CALORIE]) + "��"
    if SportMode.SPORT_RIDE != statisticsData[Statistics.MODE]:
        print "�������:\t%d\t\t%d'%d\""%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 60, statisticsData[Statistics.BESTPACE] % 60)
    else:
        print "����ٶ�:\t%d\t\t%d.%dkm/h"%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 1000, (statisticsData[Statistics.BESTPACE] % 1000) / 100)
    print "��ʼʱ���:\t" + str(statisticsData[Statistics.TIMESTAMP]) + "\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP])
    print "���ʱ��:\t" + str(statisticsData[Statistics.ACCOMPLISHTIME]) + "��\t\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP] + statisticsData[Statistics.ACCOMPLISHTIME])
    print "��ͣʱ��:\t" + str(statisticsData[Statistics.PAUSETIME]) + "��"
    print "����:\t\t" + str(statisticsData[Statistics.DISTANCE]) + "��"
    print "У׼����:\t" + str(statisticsData[Statistics.CALIDISTANCE]) + "��"
    print "����:\t\t" + str(statisticsData[Statistics.STEP]) + "��"

    file = open("output.txt", "a")
    if (statisticsData[Statistics.MODE] < 4):
        file.write("�˶�����:\t" + hex(statisticsData[Statistics.MODE]) + "\t\t\t" + modeName[statisticsData[Statistics.MODE]] + "\n")
    else:
        file.write("�˶�����:\t " + hex(statisticsData[Statistics.MODE]) + "\t\t\t�޷�ʶ��\n")

    file.write("ƽ������:\t" + str(statisticsData[Statistics.AVERAGEHR]) + "\n")
    file.write("�������:\t" + str(statisticsData[Statistics.MAXHR]) + "\n")
    file.write("ʱ��:\t\t" + str(statisticsData[Statistics.TIMEZONE]) + "\n")

    for i in range(5):
       file.write("��������%d:\t%d\t\t\t%d%s"%(i + 1, statisticsData[Statistics.DISTRIBUTED1 + i], statisticsData[Statistics.DISTRIBUTED1 + i] * 100 / hrCount, "%") + "\n")

    file.write("���Ƶ:\t" + str(statisticsData[Statistics.MAXCADENCE]) + " spm" + "\n")
    file.write("��������ѹ:\t" + str(statisticsData[Statistics.RISEATMOSPRESS]) + " pa" + "\n")
    file.write("�½�����ѹ:\t" + str(statisticsData[Statistics.DROPATMOSPRESS]) + " pa" + "\n")
    file.write("������ѹ:\t" + str(statisticsData[Statistics.MAXATMOSPRESS]) + " pa" + "\n")
    file.write("��С����ѹ:\t" + str(statisticsData[Statistics.MINATMOSPRESS]) + " pa" + "\n")
    file.write("��ʼ����ѹ:\t" + str(statisticsData[Statistics.ATMOSPRESS]) + " pa" + "\n")
    file.write("��·������:\t" + str(statisticsData[Statistics.CALORIE]) + " cal" + "\n")
    if SportMode.SPORT_RIDE != statisticsData[Statistics.MODE]:
       file.write("�������:\t%d\t\t%d'%d\""%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 60, statisticsData[Statistics.BESTPACE] % 60) + "\n")
    else:
       file.write("����ٶ�:\t%d\t\t%d.%dkm/h"%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 1000, (statisticsData[Statistics.BESTPACE] % 1000) / 100) + "\n")
    file.write("��ʼʱ���:\t" + str(statisticsData[Statistics.TIMESTAMP]) + "\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP]) + "\n")
    file.write("���ʱ��:\t" + str(statisticsData[Statistics.ACCOMPLISHTIME]) + "��\t\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP] + statisticsData[Statistics.ACCOMPLISHTIME]) + "\n")
    file.write("��ͣʱ��:\t" + str(statisticsData[Statistics.PAUSETIME]) + "��" + "\n")
    file.write("����:\t\t" + str(statisticsData[Statistics.DISTANCE]) + " m" + "\n")
    file.write("У׼����:\t" + str(statisticsData[Statistics.CALIDISTANCE]) + " m" + "\n")
    file.write("����:\t\t" + str(statisticsData[Statistics.STEP]) + "��" + "\n")
    file.write("*" * 40 + "\n")
    file.flush()
    file.close()

def analysisStatisticsV1003(buffer):
    "�˶�ͳ������V1003����"
    print "�˶�ͳ������Э��汾V1.0.03(" + hex(dataInfo[DataHead.VERSION]) + ")"

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

def initStatisticsData():
    "��ʼ��ͳ�������б�"
    for i in range(Statistics.MAXITEM):
        statisticsData.append(0)
        i

def printRealtimeInfo():
    "���ʵʱ����"
    # ��һ���ļ�
    timestamp = statisticsData[Statistics.TIMESTAMP] + (dataInfo[DataHead.MODEL2] - 1) * 5 * 168
    file = open("output.txt", "a")
    for i in range(len(realtimeData)):
        timestamp = timestamp + 5
        timestring = util.converUnixTimestamp(timestamp)

        longitude = float(realtimeData[i][RealtimeData.LONGITUDE]) / 1000000
        latitude = float(realtimeData[i][RealtimeData.LATITUDE]) / 1000000
        longitude_ew = chr(realtimeData[i][RealtimeData.LONGITUDE_EW])
        latitude_ns = chr(realtimeData[i][RealtimeData.LATITUDE_NS])
        
        if 0xffffffff == realtimeData[i][RealtimeData.LONGITUDE]: longitude = 0
        if 0xffffffff == realtimeData[i][RealtimeData.LATITUDE]: latitude = 0
        if realtimeData[i][RealtimeData.LONGITUDE_EW] in (0, 0xff): longitude_ew = ""
        if realtimeData[i][RealtimeData.LATITUDE_NS] in (0, 0xff): latitude_ns = ""

        distance = computeDistanceByGnss(longitude, latitude, longitude_ew, latitude_ns)

        print timestring + "\t\tcadence:\t" + hex(realtimeInfo[RealtimeData.CADENCE]) + "\t\t" + str(realtimeInfo[RealtimeData.CADENCE])
        # print timestring + "\t\tlongitude:\t" + hex(realtimeData[i][RealtimeData.LONGITUDE]) + "\t" + str(longitude) + longitude_ew\
        #     + "\t" + "latitude:\t" + hex(realtimeData[i][RealtimeData.LATITUDE]) + "\t" + str(latitude) + latitude_ns\
        #     + "\t" + str(distance)

        file.write(timestring + "\t\t")
        file.write("longitude:\t" + str(longitude) + longitude_ew)
        if 0.0 == longitude:
            file.write("\t\t\t\t")
        else:
            file.write("\t\t")
        file.write("latitude:\t" + str(latitude) + latitude_ns)
        if 0.0 == latitude:
            file.write("\t\t\t\t")
        else:
            file.write("\t\t")
        file.write("distance:\t" + str(distance))
        file.write("\n")
    file.flush()
    file.close()

def analysisRealtimeV1004(buffer):
    "�˶�ʵʱ����V1004����"
    print "�˶�ʵʱ����Э��汾V1.0.04(" + hex(dataInfo[DataHead.VERSION]) + ")"

    offset = 0
    for i in range(dataInfo[DataHead.NODENUM]):
        realtimeInfo[RealtimeData.PAUSE] = util.getUint8(buffer[offset + 0:offset + 2])
        realtimeInfo[RealtimeData.HR] = util.getUint8(buffer[offset + 2:offset + 4])
        realtimeInfo[RealtimeData.LONGITUDE_EW] = util.getUint8(buffer[offset + 4:offset + 6])
        realtimeInfo[RealtimeData.LATITUDE_NS] = util.getUint8(buffer[offset + 6:offset + 8])
        realtimeInfo[RealtimeData.CADENCE] = util.getUint16(buffer[offset + 8:offset + 12])
        realtimeInfo[RealtimeData.TEMPERATURE] = util.getUint16(buffer[offset + 12:offset + 16])
        realtimeInfo[RealtimeData.PACE] = util.getUint32(buffer[offset + 16:offset + 24])
        realtimeInfo[RealtimeData.LATITUDE] = util.getUint32(buffer[offset + 24:offset + 32])
        realtimeInfo[RealtimeData.LONGITUDE] = util.getUint32(buffer[offset + 32:offset + 40])
        realtimeInfo[RealtimeData.ATMOSPRESS] = util.getUint32(buffer[offset + 40:offset + 48])
        offset += dataInfo[DataHead.NODESIZE] * 2
        i
        info = copy.copy(realtimeInfo)
        realtimeData.append(info)
        # print realtimeInfo

    # print "pause:\t\t" + hex(realtimeInfo[RealtimeData.PAUSE]) + "\t\t" + str(realtimeInfo[RealtimeData.PAUSE])
    # print "hr:\t\t" + hex(realtimeInfo[RealtimeData.HR]) + "\t\t" + str(realtimeInfo[RealtimeData.HR])
    # print "longitude_ew:\t" + hex(realtimeInfo[RealtimeData.LONGITUDE_EW]) + "\t\t" + chr(realtimeInfo[RealtimeData.LONGITUDE_EW])
    # print "latitude_ns:\t" + hex(realtimeInfo[RealtimeData.LATITUDE_NS]) + "\t\t" + chr(realtimeInfo[RealtimeData.LATITUDE_NS])
    # print "cadence:\t" + hex(realtimeInfo[RealtimeData.CADENCE]) + "\t\t" + str(realtimeInfo[RealtimeData.CADENCE])
    # print "temperature:\t" + hex(realtimeInfo[RealtimeData.TEMPERATURE]) + "\t\t" + str(realtimeInfo[RealtimeData.TEMPERATURE])
    # if (statisticsData[Statistics.MODE] != SportMode.SPORT_RIDE):
    #     print "pace:\t\t%s\t\t%d'%d\""%(hex(realtimeInfo[RealtimeData.PACE]), realtimeInfo[RealtimeData.PACE] / 60, realtimeInfo[RealtimeData.PACE] % 60)
    # else:
    #     print "speed:\t\t%s\t\t%d.%dkm/h"%(hex(realtimeInfo[RealtimeData.PACE]), realtimeInfo[RealtimeData.PACE] / 1000, (realtimeInfo[RealtimeData.PACE] % 1000) / 100)
    # print "longitude:\t" + hex(realtimeData[0][RealtimeData.LONGITUDE]) + "\t" + str(float(realtimeData[0][RealtimeData.LONGITUDE]) / 1000000)
    # print "longitude:\t" + hex(realtimeData[0][RealtimeData.LONGITUDE]) + "\t" + str(realtimeData[0][RealtimeData.LONGITUDE] / 1000000) + "." + str(realtimeData[0][RealtimeData.LONGITUDE] % 1000000)
    # print "latitude:\t" + hex(realtimeInfo[RealtimeData.LATITUDE]) + "\t" + str(realtimeInfo[RealtimeData.LATITUDE] / 1000000) + "." + str(realtimeInfo[RealtimeData.LATITUDE] % 1000000)
    # print "atmospress:\t" + hex(realtimeInfo[RealtimeData.ATMOSPRESS]) + "\t\t" + str(realtimeInfo[RealtimeData.ATMOSPRESS])

def initRealtimeInfo():
    for i in range(RealtimeData.MAXITEM):
        realtimeInfo.append(0)
        i

def printCountCircleInfo():
    "����˶���Ȧ����"
    
    # ��һ���ļ�
    file = open("output.txt", "a")
    for i in range(len(countcircleData)):
        print str(i + 1) + "d��Ȧ��Ϣ:"
        if (statisticsData[Statistics.MODE] != SportMode.SPORT_RIDE):
            print "pace:\t\t%s\t\t%d'%d\""%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 60, countcircleData[i][CountCircleInfo.PACE] % 60)
        else:
            print "speed:\t\t%s\t\t%d.%dkm/h"%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 1000, (countcircleData[i][CountCircleInfo.PACE] % 1000) / 100)
        print "elapsetime:\t" + hex(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.ELAPSETIME])
        print "pause:\t\t" + hex(countcircleData[i][CountCircleInfo.PAUSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.PAUSETIME])
        print "unit:\t\t" + hex(countcircleData[i][CountCircleInfo.UNIT]) + "\t\t" + str(countcircleData[i][CountCircleInfo.UNIT])

        file.write("��%d��%d�׼�Ȧ��Ϣ:\n"%(i + 1, countcircleData[i][CountCircleInfo.UNIT]))
        if (statisticsData[Statistics.MODE] != SportMode.SPORT_RIDE):
            file.write("pace:\t\t%s\t\t%d'%d\""%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 60, countcircleData[i][CountCircleInfo.PACE] % 60) + "\n")
        else:
            file.write("speed:\t\t%s\t\t%d.%dkm/h"%(hex(countcircleData[i][CountCircleInfo.PACE]), countcircleData[i][CountCircleInfo.PACE] / 1000, (countcircleData[i][CountCircleInfo.PACE] % 1000) / 100) + "\n")
        file.write("elapsetime:\t" + hex(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "\t\t" + str(countcircleData[i][CountCircleInfo.ELAPSETIME]) + "\n")
        file.write("pause:\t\t" + hex(countcircleData[i][CountCircleInfo.PAUSETIME]) + "\t\t\t" + str(countcircleData[i][CountCircleInfo.PAUSETIME]) + "\n")
        file.write("unit:\t\t" + hex(countcircleData[i][CountCircleInfo.UNIT]) + "\t\t" + str(countcircleData[i][CountCircleInfo.UNIT]) + "\n")
        file.write("*" * 40 + "\n")
    file.flush()
    file.close()

def analysisCountCircleV1001(buffer):
    "�˶���Ȧ����V1001����"
    print "�˶���Ȧ����Э��汾V1.0.01(" + hex(dataInfo[DataHead.VERSION]) + ")"

    offset = 0
    for i in range(dataInfo[DataHead.NODENUM]):
        countcircleInfo[CountCircleInfo.PACE] = util.getUint32(buffer[offset + 0:offset + 8])
        countcircleInfo[CountCircleInfo.ELAPSETIME] = util.getUint32(buffer[offset + 8:offset + 16])
        countcircleInfo[CountCircleInfo.PAUSETIME] = util.getUint32(buffer[offset + 16:offset + 24])
        countcircleInfo[CountCircleInfo.UNIT] = util.getUint32(buffer[offset + 24:offset + 32])
        offset += dataInfo[DataHead.NODESIZE] * 2
        i
        info = copy.copy(countcircleInfo)
        countcircleData.append(info)
        # print countcircleInfo

    if (statisticsData[Statistics.MODE] != SportMode.SPORT_RIDE):
        print "pace:\t\t%s\t\t%d'%d\""%(hex(countcircleData[0][CountCircleInfo.PACE]), countcircleData[0][CountCircleInfo.PACE] / 60, countcircleData[0][CountCircleInfo.PACE] % 60)
    else:
        print "speed:\t\t%s\t\t%d.%dkm/h"%(hex(countcircleData[0][CountCircleInfo.PACE]), countcircleData[0][CountCircleInfo.PACE] / 1000, (countcircleData[0][CountCircleInfo.PACE] % 1000) / 100)
    print "elapsetime:\t" + hex(countcircleData[0][CountCircleInfo.ELAPSETIME]) + "\t\t" + str(countcircleData[0][CountCircleInfo.ELAPSETIME])
    print "pause:\t\t" + hex(countcircleData[0][CountCircleInfo.PAUSETIME]) + "\t\t" + str(countcircleData[0][CountCircleInfo.PAUSETIME])
    print "unit:\t\t" + hex(countcircleData[0][CountCircleInfo.UNIT]) + "\t\t" + str(countcircleData[0][CountCircleInfo.UNIT])

def initCountCircleInfo():
    for i in range(CountCircleInfo.MAXITEM):
        countcircleInfo.append(0)
        i

def printStepInfo():
    "����Ʋ�����"

    for i in range(len(stepData)):
        print str(i + 1) + "d�Ʋ���Ϣ:"
        print "����ʱ��:\t" + hex(stepData[i][StepInfo.TIMESTAMP]) + "\t\t" + util.converUnixTimestamp(stepData[0][StepInfo.TIMESTAMP])

        print "ʱ��:\t\t" + hex(stepData[i][StepInfo.TIMEZONE]) + "\t\t\t" + str(stepData[0][StepInfo.TIMEZONE])
        print "����:\t\t" + hex(stepData[i][StepInfo.SEDENTARYCOUNT]) + "\t\t\t" + str(stepData[0][StepInfo.SEDENTARYCOUNT])
        print "��Ϣ��·��:\t" + hex(stepData[i][StepInfo.CALORIEBMR]) + "\t\t\t" + str(stepData[0][StepInfo.CALORIEBMR])
        print "�˶���·��:\t" + hex(stepData[i][StepInfo.CALORIESPORT]) + "\t\t\t" + str(stepData[0][StepInfo.CALORIESPORT])
        for j in range(24):
            h = str(j) 
            if j < 10: h = "0" + str(j)
            print h + ":00 ����:\t" + hex(stepData[i][StepInfo.STEPHOUR + j * 2]) + "\t\t\t" + str(stepData[i][StepInfo.STEPHOUR + j * 2])
            print h + ":00 ����:\t" + hex(stepData[i][StepInfo.DISTANCEHOUR + j * 2]) + "\t\t\t" + str(stepData[i][StepInfo.DISTANCEHOUR + j * 2])

def analysisStepV1004(buffer):
    "�Ʋ�����V1004����"
    print "�Ʋ�����Э��汾V1.0.04(" + hex(dataInfo[DataHead.VERSION]) + ")"

    offset = 0
    for i in range(dataInfo[DataHead.NODENUM]):
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
        offset += dataInfo[DataHead.NODESIZE] * 2
        i
        info = copy.copy(stepInfo)
        stepData.append(info)
        print info

def initStepInfo():
    for i in range(StepInfo.MAXITEM):
        stepInfo.append(0)
        i

def printHeadInfo():
    print "uuid:\t\t" + hex(dataInfo[DataHead.UUID])
    print "mode1:\t\t" + hex(dataInfo[DataHead.MODEL1]) + "\t" + chr(dataInfo[DataHead.MODEL1])
    print "mode2:\t\t" + hex(dataInfo[DataHead.MODEL2])
    print "version:\t" + hex(dataInfo[DataHead.VERSION])
    print "nodesize:\t" + str(dataInfo[DataHead.NODESIZE])
    print "nodenum:\t" + hex(dataInfo[DataHead.NODENUM])

def analysisHeadInfo(buffer):
    "����ͷ��Ϣ����"

    # print "RAW����ͷ"
    # print buffer
    # util.printDividingLine()

    dataInfo[DataHead.UUID] = util.getUint32(buffer[0:8])
    dataInfo[DataHead.MODEL1] = util.getUint8(buffer[8:10])
    dataInfo[DataHead.MODEL2] = util.getUint8(buffer[10:12])
    dataInfo[DataHead.VERSION] = util.getUint16(buffer[12:16])
    dataInfo[DataHead.NODESIZE] = util.getUint16(buffer[16:20])
    dataInfo[DataHead.NODENUM] = util.getUint16(buffer[20:24])

def initHeadInfo():
    for i in range(DataHead.MAXITEM):
        dataInfo.append(0)
        i

def process():
    # filename = raw_input("�������˶������ļ�����")
    filename = "data.txt"

    if len(filename) == 0 or 0 != os.path.exists(filename):
        filename = "data.txt"

    print "�˶������ļ���: ", filename

    if (os.path.exists("output.txt")): os.remove("output.txt")

    # ��ʼ���б�
    initHeadInfo()
    initStatisticsData()
    initRealtimeInfo()
    initCountCircleInfo()
    
    
    filesize = os.path.getsize(filename)
    # print "filesize:" + str(filesize)

    # ��һ���ļ�
    file = open(filename, "r")
    
    offset = 0
    leftsize = filesize
    util.printDividingLine()
    while (leftsize > 0):
        # print "offset:" + str(offset) + "\tleftsize:" + str(leftsize)
        file.seek(offset)
        readsize = 12 * 2
        if readsize > leftsize:
            readsize = leftsize
            buffer = file.read(readsize)
            leftsize = leftsize - readsize
            offset = offset + readsize
            print "����ͷ��Ϣ���Ȳ�������" + buffer
            continue
        
        # ��ȡ����ͷ��Ϣ
        buffer = file.read(readsize)
        leftsize = leftsize - readsize
        offset = offset + readsize
        
        # ��������ͷ��Ϣ
        analysisHeadInfo(buffer)
        # printHeadInfo()
        
        # ��ȡ���ݾ�������
        readsize = dataInfo[DataHead.NODESIZE] * dataInfo[DataHead.NODENUM] * 2
        if readsize > leftsize: readsize = leftsize
        file.seek(offset)
        buffer = file.read(readsize)
        leftsize = leftsize - readsize
        offset = offset + readsize

        if (str("S") == chr(dataInfo[DataHead.MODEL1])):
            # ͳ����Ϣ
            show = 1
            if (0x1003 == dataInfo[DataHead.VERSION]):
                analysisStatisticsV1003(buffer)
            else:
                show = 0
                print "�汾�޷�ʶ��" + hex(dataInfo[DataHead.VERSION])
            if (1 == show):
                printStatisticsInfo()
        elif (str("R") == chr(dataInfo[DataHead.MODEL1])):
            # ʵʱ����
            show = 1
            if (0x1004 == dataInfo[DataHead.VERSION]):
                analysisRealtimeV1004(buffer)
            else:
                show = 0
                print "�汾�޷�ʶ��" + hex(dataInfo[DataHead.VERSION])
            if (1 == show):
                printRealtimeInfo()
        elif (str("K") == chr(dataInfo[DataHead.MODEL1])):
            show = 1
            if (0x1001 == dataInfo[DataHead.VERSION]):
                analysisCountCircleV1001(buffer)
            else:
                show = 0
                print "�汾�޷�ʶ��" + hex(dataInfo[DataHead.VERSION])
            if (1 == show):
                printCountCircleInfo()
        elif (str("F") == chr(dataInfo[DataHead.MODEL1]) and str("S") == chr(dataInfo[DataHead.MODEL2])):
            initStepInfo()
            show = 1
            if (0x1004 == dataInfo[DataHead.VERSION]):
                analysisStepV1004(buffer)
            else:
                show = 0
                print "�汾�޷�ʶ��" + hex(dataInfo[DataHead.VERSION])
            if (1 == show):
                printStepInfo()
        else:
            print "�����޷�ʶ��" + hex(dataInfo[DataHead.MODEL1]) + "\t\t" + chr(dataInfo[DataHead.MODEL1])
            printHeadInfo()
        util.printDividingLine()

    # �رմ򿪵��ļ�
    file.close()

    if (0 != statisticsData[Statistics.TIMESTAMP]):
        outputfile = "output_" + str(statisticsData[Statistics.TIMESTAMP]) + ".txt"
        if (os.path.exists(outputfile)): os.remove(outputfile)
        shutil.copyfile("output.txt", outputfile)

process()