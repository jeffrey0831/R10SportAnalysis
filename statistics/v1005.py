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
    RISEALTITUDE = 10
    DROPALTITUDE = 11
    MAXALTITUDE = 12
    MINALTITUDE = 13
    ALTITUDE = 14
    CALORIE = 15
    BESTPACE = 16
    TIMESTAMP = 17
    ACCOMPLISHTIME = 18
    PAUSETIME = 19
    DISTANCE = 20
    CALIDISTANCE = 21
    STEP = 22
    OLONGITUDE = 23
    OLATITUDE = 24
    TLONGITUDE = 25
    TLATITUDE = 26
    OLONGITUDE_EW = 27
    OLATITUDE_NS = 28
    TLONGITUDE_EW = 29
    TLATITUDE_NS = 30
    UNITTYPE = 31
    WEATHER = 32
    TEMPERATURE = 33
    MAXOXYGENUPTAKE = 34
    MAXITEM = 35

statisticsData = []

def initInfo():
    "初始化统计数据列表"
    for i in range(Statistics.MAXITEM):
        statisticsData.append(0)
    str(i)

def analysisInfo(buffer, buffersize, nodenum, nodesize):
    "运动统计数据V1005解析"
    print "运动统计数据协议版本V1.0.05"

    if (buffersize < nodesize * 2):
        print "运动统计数据不完整"
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
    statisticsData[Statistics.RISEALTITUDE] = util.getUint32(buffer[32:40])
    statisticsData[Statistics.DROPALTITUDE] = util.getUint32(buffer[40:48])
    statisticsData[Statistics.MAXALTITUDE] = util.getUint32(buffer[48:56])
    statisticsData[Statistics.MINALTITUDE] = util.getUint32(buffer[56:64])
    statisticsData[Statistics.ALTITUDE] = util.getUint32(buffer[64:72])
    statisticsData[Statistics.CALORIE] = util.getUint32(buffer[72:80])
    statisticsData[Statistics.BESTPACE] = util.getUint32(buffer[80:88])
    statisticsData[Statistics.TIMESTAMP] = util.getUint32(buffer[88:96])
    statisticsData[Statistics.ACCOMPLISHTIME] = util.getUint32(buffer[96:104])
    statisticsData[Statistics.PAUSETIME] = util.getUint32(buffer[104:112])
    statisticsData[Statistics.DISTANCE] = util.getUint32(buffer[112:120])
    statisticsData[Statistics.CALIDISTANCE] = util.getUint32(buffer[120:128])
    statisticsData[Statistics.STEP] = util.getUint32(buffer[128:136])
    statisticsData[Statistics.OLONGITUDE] = util.getUint32(buffer[136:144])
    statisticsData[Statistics.OLATITUDE] = util.getUint32(buffer[144:152])
    statisticsData[Statistics.TLONGITUDE] = util.getUint32(buffer[152:160])
    statisticsData[Statistics.TLATITUDE] = util.getUint32(buffer[160:168])
    statisticsData[Statistics.OLONGITUDE_EW] = util.getUint8(buffer[168:170])
    statisticsData[Statistics.OLATITUDE_NS] = util.getUint8(buffer[170:172])
    statisticsData[Statistics.TLONGITUDE_EW] = util.getUint8(buffer[172:174])
    statisticsData[Statistics.TLATITUDE_NS] = util.getUint8(buffer[174:176])
    statisticsData[Statistics.UNITTYPE] = util.getUint8(buffer[176:178])
    statisticsData[Statistics.WEATHER] = util.getUint8(buffer[178:180])
    statisticsData[Statistics.TEMPERATURE] = util.getUint16(buffer[180:184])
    statisticsData[Statistics.MAXOXYGENUPTAKE] = util.getUint16(buffer[184:188])

    info.mode = statisticsData[Statistics.MODE]
    info.uuid = statisticsData[Statistics.TIMESTAMP]

def printInfo():
    "打印统计数据信息"

    modeName = ["健走", "户外跑", "室内跑", "骑行"]
    hrCount = 0
    for i in range(5):
        hrCount += statisticsData[Statistics.DISTRIBUTED1 + i]

    olongitude = float(statisticsData[Statistics.OLONGITUDE]) / 1000000
    olatitude = float(statisticsData[Statistics.OLATITUDE]) / 1000000
    olongitude_ew = chr(statisticsData[Statistics.OLONGITUDE_EW])
    olatitude_ns = chr(statisticsData[Statistics.OLATITUDE_NS])
    
    if 0xffffffff == statisticsData[Statistics.OLONGITUDE]: olongitude = 0
    if 0xffffffff == statisticsData[Statistics.OLATITUDE]: olatitude = 0
    if statisticsData[Statistics.OLONGITUDE_EW] in (0, 0xff): olongitude_ew = ""
    if statisticsData[Statistics.OLATITUDE_NS] in (0, 0xff): olatitude_ns = ""

    tlongitude = float(statisticsData[Statistics.TLONGITUDE]) / 1000000
    tlatitude = float(statisticsData[Statistics.TLATITUDE]) / 1000000
    tlongitude_ew = chr(statisticsData[Statistics.TLONGITUDE_EW])
    tlatitude_ns = chr(statisticsData[Statistics.TLATITUDE_NS])
    
    if 0xffffffff == statisticsData[Statistics.TLONGITUDE]: tlongitude = 0
    if 0xffffffff == statisticsData[Statistics.TLATITUDE]: tlatitude = 0
    if statisticsData[Statistics.TLONGITUDE_EW] in (0, 0xff): tlongitude_ew = ""
    if statisticsData[Statistics.TLATITUDE_NS] in (0, 0xff): tlatitude_ns = ""
    
    h = statisticsData[Statistics.ACCOMPLISHTIME] / 3600
    m = (statisticsData[Statistics.ACCOMPLISHTIME] - h * 3600) / 60
    s = statisticsData[Statistics.ACCOMPLISHTIME] % 60
    if (h > 0):
        accomplishtime = str(h) + "小时" + str(m) + "分" + str(s) + "秒"
    else:
        accomplishtime = str(m) + "分" + str(s) + "秒"

    if (statisticsData[Statistics.MODE] < info.SportMode.SPORT_MAX):
        print "运动类型:\t" + hex(statisticsData[Statistics.MODE]) + "\t\t" + modeName[statisticsData[Statistics.MODE]]
    else:
        print "运动类型:\t " + hex(statisticsData[Statistics.MODE]) + "\t\t无法识别"

    print "平均心率:\t" + str(statisticsData[Statistics.AVERAGEHR])
    print "最大心率:\t" + str(statisticsData[Statistics.MAXHR])
    print "时区:\t\t" + str(statisticsData[Statistics.TIMEZONE])

    for i in range(5):
        if 0 == hrCount:
            print "心率区间%d:\t%d\t\t%d%s"%(i + 1, statisticsData[Statistics.DISTRIBUTED1 + i], 0, "%")
        else:
            print "心率区间%d:\t%d\t\t%d%s"%(i + 1, statisticsData[Statistics.DISTRIBUTED1 + i], statisticsData[Statistics.DISTRIBUTED1 + i] * 100 / hrCount, "%")

    print "最大步频:\t" + str(statisticsData[Statistics.MAXCADENCE]) + "spm"
    print "累计上升:\t" + str(statisticsData[Statistics.RISEALTITUDE]) + "米"
    print "累计下降:\t" + str(statisticsData[Statistics.DROPALTITUDE]) + "米"
    print "最大高度:\t" + str(statisticsData[Statistics.MAXALTITUDE]) + "米"
    print "最低高度:\t" + str(statisticsData[Statistics.MINALTITUDE]) + "米"
    print "起始高度:\t" + str(statisticsData[Statistics.ALTITUDE]) + "米"
    print "卡路里消耗:\t" + str(statisticsData[Statistics.CALORIE]) + "卡"
    if info.SportMode.SPORT_RIDE != info.mode:
        print "最佳配速:\t%d\t\t%d'%d\""%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 60, statisticsData[Statistics.BESTPACE] % 60)
    else:
        print "最佳速度:\t%d\t\t%d.%dkm/h"%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 1000, (statisticsData[Statistics.BESTPACE] % 1000) / 100)
    print "起始时间戳:\t" + str(statisticsData[Statistics.TIMESTAMP]) + "\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP])
    print "完成时间:\t" + str(accomplishtime) + "\t\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP] + statisticsData[Statistics.ACCOMPLISHTIME])
    print "暂停时间:\t" + str(statisticsData[Statistics.PAUSETIME]) + "秒"
    print "距离:\t\t" + str(statisticsData[Statistics.DISTANCE]) + "米"
    print "校准距离:\t" + str(statisticsData[Statistics.CALIDISTANCE]) + "米"
    print "步数:\t\t" + str(statisticsData[Statistics.STEP]) + "次"
    print "起始经度:\t" + hex(statisticsData[Statistics.OLONGITUDE]) + "\t" + str(olongitude) + olongitude_ew
    print "起始纬度:\t" + hex(statisticsData[Statistics.OLATITUDE]) + "\t" + str(olatitude) + olatitude_ns
    print "结束经度:\t" + hex(statisticsData[Statistics.TLONGITUDE]) + "\t" + str(tlongitude) + tlongitude_ew
    print "结束纬度:\t" + hex(statisticsData[Statistics.TLATITUDE]) + "\t" + str(tlatitude) + tlatitude_ns
    print "最大摄氧量:\t" + str(statisticsData[Statistics.MAXOXYGENUPTAKE])

    file = open(info.outfile, "a")
    if (statisticsData[Statistics.MODE] < info.SportMode.SPORT_MAX):
        file.write("运动类型:\t" + hex(statisticsData[Statistics.MODE]) + "\t\t\t" + modeName[statisticsData[Statistics.MODE]] + "\n")
    else:
        file.write("运动类型:\t " + hex(statisticsData[Statistics.MODE]) + "\t\t\t无法识别\n")

    file.write("平均心率:\t" + str(statisticsData[Statistics.AVERAGEHR]) + "\n")
    file.write("最大心率:\t" + str(statisticsData[Statistics.MAXHR]) + "\n")
    file.write("时区:\t\t" + str(statisticsData[Statistics.TIMEZONE]) + "\n")

    for i in range(5):
        if 0 == hrCount:
            file.write("心率区间%d:\t%d\t\t\t%d%s"%(i + 1, statisticsData[Statistics.DISTRIBUTED1 + i], 0, "%") + "\n")
        else:
            file.write("心率区间%d:\t%d\t\t\t%d%s"%(i + 1, statisticsData[Statistics.DISTRIBUTED1 + i], statisticsData[Statistics.DISTRIBUTED1 + i] * 100 / hrCount, "%") + "\n")

    file.write("最大步频:\t" + str(statisticsData[Statistics.MAXCADENCE]) + " spm" + "\n")
    file.write("累计上升:\t" + str(statisticsData[Statistics.RISEALTITUDE]) + " 米" + "\n")
    file.write("累计下降:\t" + str(statisticsData[Statistics.DROPALTITUDE]) + " 米" + "\n")
    file.write("最大高度:\t" + str(statisticsData[Statistics.MAXALTITUDE]) + " 米" + "\n")
    file.write("最低高度:\t" + str(statisticsData[Statistics.MINALTITUDE]) + " 米" + "\n")
    file.write("起始高度:\t" + str(statisticsData[Statistics.ALTITUDE]) + " 米" + "\n")
    file.write("卡路里消耗:\t" + str(statisticsData[Statistics.CALORIE]) + " cal" + "\n")
    if info.SportMode.SPORT_RIDE != info.mode:
       file.write("最佳配速:\t%d\t\t%d'%d\""%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 60, statisticsData[Statistics.BESTPACE] % 60) + "\n")
    else:
       file.write("最佳速度:\t%d\t\t%d.%dkm/h"%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 1000, (statisticsData[Statistics.BESTPACE] % 1000) / 100) + "\n")
    file.write("起始时间戳:\t" + str(statisticsData[Statistics.TIMESTAMP]) + "\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP]) + "\n")
    file.write("完成时间:\t" + str(accomplishtime) + "\t\t" + util.converUnixTimestamp(statisticsData[Statistics.TIMESTAMP] + statisticsData[Statistics.ACCOMPLISHTIME]) + "\n")
    file.write("暂停时间:\t" + str(statisticsData[Statistics.PAUSETIME]) + "秒" + "\n")
    file.write("距离:\t\t" + str(statisticsData[Statistics.DISTANCE]) + " m" + "\n")
    file.write("校准距离:\t" + str(statisticsData[Statistics.CALIDISTANCE]) + " m" + "\n")
    file.write("步数:\t\t" + str(statisticsData[Statistics.STEP]) + "次" + "\n")
    file.write("起始经度:\t" + str(olongitude) + olongitude_ew + "\n")
    file.write("起始纬度:\t" + str(olatitude) + olatitude_ns + "\n")
    file.write("结束经度:\t" + str(tlongitude) + tlongitude_ew + "\n")
    file.write("结束纬度:\t" + str(tlatitude) + tlatitude_ns + "\n")
    file.write("最大摄氧量:\t" + str(statisticsData[Statistics.MAXOXYGENUPTAKE]) + "\n")
    file.write("*" * 40 + "\n")
    file.flush()
    file.close()
