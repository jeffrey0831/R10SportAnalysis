# coding=gbk

import os
import shutil

import info
import util
import countcircle.v1001
import countcircle.v1002
import statistics.v1003
import statistics.v1004
import statistics.v1005
import realtime.v1004
import realtime.v1005
import step.v1004

class DataHead():
    UUID = 0
    MODEL1 = 1
    MODEL2 = 2
    VERSION = 3
    NODESIZE = 4
    NODENUM = 5
    MAXITEM = 6

dataInfo = [0, 0, 0, 0, 0, 0]

def printHeadInfo():
    print "uuid:\t\t" + hex(dataInfo[DataHead.UUID])
    print "mode1:\t\t" + hex(dataInfo[DataHead.MODEL1]) + "\t" + chr(dataInfo[DataHead.MODEL1])
    print "mode2:\t\t" + hex(dataInfo[DataHead.MODEL2])
    print "version:\t" + hex(dataInfo[DataHead.VERSION])
    print "nodesize:\t" + str(dataInfo[DataHead.NODESIZE])
    print "nodenum:\t" + hex(dataInfo[DataHead.NODENUM])

def analysisHeadInfo(buffer):
    "数据头信息解析"

    # print "RAW数据头"
    # print buffer
    # util.printDividingLine()

    dataInfo[DataHead.UUID] = util.getUint32(buffer[0:8])
    dataInfo[DataHead.MODEL1] = util.getUint8(buffer[8:10])
    dataInfo[DataHead.MODEL2] = util.getUint8(buffer[10:12])
    dataInfo[DataHead.VERSION] = util.getUint16(buffer[12:16])
    dataInfo[DataHead.NODESIZE] = util.getUint16(buffer[16:20])
    dataInfo[DataHead.NODENUM] = util.getUint16(buffer[20:24])

def process():
    filename = raw_input("请输入运动数据文件名：")
    # filename = "data.txt"

    if len(filename) == 0 or 0 == os.path.exists(filename):
        filename = "data.txt"

    print "运动数据文件名: ", filename

    if (os.path.exists("output.txt")): os.remove("output.txt")

    filesize = os.path.getsize(filename)
    # print "filesize:" + str(filesize)

    # 打开一个文件
    file = open(filename, "r")
    
    rename = 0
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
            print "数据头信息长度不完整：" + buffer
            continue
        
        # 读取数据头信息
        buffer = file.read(readsize)
        leftsize = leftsize - readsize
        offset = offset + readsize
        
        # 解析数据头信息
        analysisHeadInfo(buffer)
        # printHeadInfo()
        if (0xFFFFFFFF == dataInfo[DataHead.UUID]): break
        
        # 读取数据具体内容
        readsize = dataInfo[DataHead.NODESIZE] * dataInfo[DataHead.NODENUM] * 2
        if readsize > leftsize: readsize = leftsize
        file.seek(offset)
        buffer = file.read(readsize)
        leftsize = leftsize - readsize
        offset = offset + readsize

        if (str("S") == chr(dataInfo[DataHead.MODEL1])):
            # 统计信息
            rename = 1
            if (0x1003 == dataInfo[DataHead.VERSION]):
                statistics.v1003.initInfo()
                statistics.v1003.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                statistics.v1003.printInfo()
            elif (0x1004 == dataInfo[DataHead.VERSION]):
                statistics.v1004.initInfo()
                statistics.v1004.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                statistics.v1004.printInfo()
            elif (0x1005 == dataInfo[DataHead.VERSION]):
                statistics.v1005.initInfo()
                statistics.v1005.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                statistics.v1005.printInfo()
            else:
                print "统计数据版本无法识别" + hex(dataInfo[DataHead.VERSION])
                statistics.v1004.initInfo()
                statistics.v1004.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                statistics.v1004.printInfo()
        elif (str("R") == chr(dataInfo[DataHead.MODEL1])):
            # 实时数据
            info.dataindex = dataInfo[DataHead.MODEL2] - 1
            if (0x1004 == dataInfo[DataHead.VERSION]):
                realtime.v1004.initInfo()
                realtime.v1004.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                realtime.v1004.printInfo()
            elif (0x1005 == dataInfo[DataHead.VERSION]):
                realtime.v1005.initInfo()
                realtime.v1005.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                realtime.v1005.printInfo()
            else:
                print "实时数据版本无法识别" + hex(dataInfo[DataHead.VERSION])
                realtime.v1005.initInfo()
                realtime.v1005.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                realtime.v1005.printInfo()
        elif (str("K") == chr(dataInfo[DataHead.MODEL1])):
            if (0x1001 == dataInfo[DataHead.VERSION]):
                countcircle.v1001.initInfo()
                countcircle.v1001.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                countcircle.v1002.printInfo()
            elif (0x1002 == dataInfo[DataHead.VERSION]):
                countcircle.v1002.initInfo()
                countcircle.v1002.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                countcircle.v1002.printInfo()
            else:
                print "计圈数据版本无法识别" + hex(dataInfo[DataHead.VERSION])
                countcircle.v1002.initInfo()
                countcircle.v1002.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                countcircle.v1002.printInfo()
        elif (str("F") == chr(dataInfo[DataHead.MODEL1]) and str("S") == chr(dataInfo[DataHead.MODEL2])):
            if (0x1004 == dataInfo[DataHead.VERSION]):
                step.v1004.initInfo()
                step.v1004.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                step.v1004.printInfo()
            else:
                print "计步数据版本无法识别" + hex(dataInfo[DataHead.VERSION])
                step.v1004.initInfo()
                step.v1004.analysisInfo(buffer, readsize, dataInfo[DataHead.NODENUM], dataInfo[DataHead.NODESIZE])
                step.v1004.printInfo()
        else:
            util.printDividingLine()
            print "数据类型无法识别" + hex(dataInfo[DataHead.MODEL1]) + "\t\t" + chr(dataInfo[DataHead.MODEL1])
            printHeadInfo()
        util.printDividingLine()

    # 关闭打开的文件
    file.close()

    if (0 != rename):
        outputfile = "output_" + str(info.uuid) + ".txt"
        if (os.path.exists(outputfile)): os.remove(outputfile)
        shutil.copyfile("output.txt", outputfile)

process()