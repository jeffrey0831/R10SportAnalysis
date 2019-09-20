# coding=gbk

import copy
import os
import shutil

import info
import util

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
    DELTAALTITUDE = 9
    DELTADISTANCE = 10
    MAXITEM = 11

realtimeData = []
realtimeInfo = []

def initInfo():
    "初始化实时数据列表"
    for i in range(RealtimeData.MAXITEM):
        realtimeInfo.append(0)
        i

def analysisInfo(buffer, buffersize, nodenum, nodesize):
    "运动实时数据V1005解析"
    print "运动实时数据协议版本V1.0.05"

    offset = 0
    leftsize = buffersize
    for i in range(nodenum):
        if (leftsize < nodesize * 2):
            print "运动实时数据不完整"
            print buffer[offset:]
            break
        else:
            leftsize -= nodesize * 2

        realtimeInfo[RealtimeData.PAUSE] = util.getUint8(buffer[offset + 0:offset + 2])
        realtimeInfo[RealtimeData.HR] = util.getUint8(buffer[offset + 2:offset + 4])
        realtimeInfo[RealtimeData.LONGITUDE_EW] = util.getUint8(buffer[offset + 4:offset + 6])
        realtimeInfo[RealtimeData.LATITUDE_NS] = util.getUint8(buffer[offset + 6:offset + 8])
        realtimeInfo[RealtimeData.CADENCE] = util.getUint16(buffer[offset + 8:offset + 12])
        realtimeInfo[RealtimeData.TEMPERATURE] = util.getUint16(buffer[offset + 12:offset + 16])
        realtimeInfo[RealtimeData.PACE] = util.getUint32(buffer[offset + 16:offset + 24])
        realtimeInfo[RealtimeData.LATITUDE] = util.getUint32(buffer[offset + 24:offset + 32])
        realtimeInfo[RealtimeData.LONGITUDE] = util.getUint32(buffer[offset + 32:offset + 40])
        realtimeInfo[RealtimeData.DELTAALTITUDE] = util.getUint8(buffer[offset + 40:offset + 42])
        realtimeInfo[RealtimeData.DELTADISTANCE] = util.getUint8(buffer[offset + 42:offset + 44])
        offset += nodesize * 2
        info = copy.copy(realtimeInfo)
        realtimeData.append(info)
    str(i)

def printInfo():
    "输出实时数据"

    samplingInterval = 5
    samplingCount = 168
    # 打开一个文件
    timestamp = info.uuid + info.dataindex * samplingInterval * samplingCount
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

        distance = util.computeDistanceByGnss(longitude, latitude, longitude_ew, latitude_ns)

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
        file.write("pace:\t" + str(realtimeData[i][RealtimeData.PACE]) + "\t\t")
        file.write("altitude:\t" + str(realtimeData[i][RealtimeData.DELTAALTITUDE]) + "\t\t")
        file.write("distance:\t" + str(realtimeData[i][RealtimeData.DELTADISTANCE]) + " cm" + "\t\t")
        file.write("offset:\t" + str(distance))
        file.write("\n")
    file.flush()
    file.close()
