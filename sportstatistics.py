# coding=gbk

import time
import copy
import getuint

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

# // size: 12
# typedef struct FstorageHeadRegionTag
# {
#     uint32_t uuid;
#     uint8_t model1;
#     uint8_t model2; // reserve
#     uint16_t ver;
#     uint16_t nodeSize;
#     uint16_t nodeNum;
# } FstorageHeadRegion;

# // size: 68
# typedef struct _StoreStatisticData
# {
#     uint8_t mode;
#     uint8_t averageHr;
#     uint8_t maxHr;
#     int8_t timezone;                    // [-11, 12]
#     uint16_t distributed[5];
#     uint16_t maxCadence;                // unit: per min
#     uint32_t riseAtmosphericPressure;   // unit: pa
#     uint32_t dropAtmosphericPressure;   // unit: pa
#     uint32_t maxAtmosphericPressure;    // unit: pa
#     uint32_t minAtmosphericPressure;    // unit: pa
#     uint32_t atmosphericPressure;
#     uint32_t calorie;
#     uint32_t bestPace;                  // unit: sec per kilometer / meter per hour
#     uint32_t timestamp;
#     uint32_t accomplishTime;            // unit: sec
#     uint32_t pauseTime;                 // unit: sec
#     uint32_t distance;                  // unit: meter
#     uint32_t calibrateDistance;         // unit: meter
#     uint32_t step;
# } StoreStatisticsData;

# // size: 24
# typedef struct _StoreRealtimeData
# {
#     uint8_t pause;
#     uint8_t hr; // reserve
#     uint8_t longitude_ew;
#     uint8_t latitude_ns;
#     uint16_t cadence;
#     int16_t temperature;
#     uint32_t pace;
#     uint32_t latitude;
#     uint32_t longitude;
#     uint32_t atmosphericPressure;
# } StoreRealtimeData;

dataInfo = []
statisticsData = []
realtimeData = []
realtimeInfo = []

def converUnixTimestamp(timestamp):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    timestamp = time.localtime(timestamp)
    # 经过localtime转换后变成
    # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    str = time.strftime(format, timestamp)
    return str

def printDividingLine():
    "打印分割线"
    print "*" * 40

def getUint32(str):
    "获取UINT32"
    val = (int(str[0], 16) << 4) + int(str[1], 16)
    val += (int(str[2], 16) << 4) + int(str[3], 16) << 8
    val += (int(str[4], 16) << 4) + int(str[5], 16) << 16
    val += (int(str[6], 16) << 4) + int(str[7], 16) << 24
    # print "u32:" + hex(val)
    return val

def getUint16(str):
    "获取UINT16"
    val = (int(str[0], 16) << 4) + int(str[1], 16)
    val += (int(str[2], 16) << 4) + int(str[3], 16) << 8
    # print "u16:" + hex(val)
    return val

def getUint8(str):
    "获取UINT8"
    val = (int(str[0], 16) << 4) + int(str[1], 16)
    # print "u8:" + hex(val)
    return val

def printStatisticsInfo():
    "打印统计数据信息"

    modeName = ["健走", "户外跑", "室内跑", "骑行"]
    if (statisticsData[Statistics.MODE] < 4):
        print "运动类型:\t" + hex(statisticsData[Statistics.MODE]) + "\t\t" + modeName[statisticsData[Statistics.MODE]]
    else:
        print "运动类型:\t " + hex(statisticsData[Statistics.MODE]) + "\t\t无法识别"

    print "平均心率:\t" + str(statisticsData[Statistics.AVERAGEHR])
    print "最大心率:\t" + str(statisticsData[Statistics.MAXHR])
    print "时区:\t\t" + str(statisticsData[Statistics.TIMEZONE])

    hrCount = 0
    for i in range(5):
        hrCount += statisticsData[Statistics.DISTRIBUTED1 + i]
    for i in range(5):
        print "心率区间%d:\t%d\t\t%d%s"%(i + 1, statisticsData[Statistics.DISTRIBUTED1 + i], statisticsData[Statistics.DISTRIBUTED1 + i] * 100 / hrCount, "%")

    print "最大步频:\t" + str(statisticsData[Statistics.MAXCADENCE]) + "spm"
    print "上升大气压:\t" + str(statisticsData[Statistics.RISEATMOSPRESS]) + "帕"
    print "下降大气压:\t" + str(statisticsData[Statistics.DROPATMOSPRESS]) + "帕"
    print "最大大气压:\t" + str(statisticsData[Statistics.MAXATMOSPRESS]) + "帕"
    print "最小大气压:\t" + str(statisticsData[Statistics.MINATMOSPRESS]) + "帕"
    print "起始大气压:\t" + str(statisticsData[Statistics.ATMOSPRESS]) + "帕"
    print "卡路里消耗:\t" + str(statisticsData[Statistics.CALORIE]) + "卡"
    if SportMode.SPORT_RIDE != statisticsData[Statistics.MODE]:
        print "最佳配速:\t%d\t\t%d'%d\""%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 60, statisticsData[Statistics.BESTPACE] % 60)
    else:
        print "最佳速度:\t%d\t\t%d.%dkm/h"%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 1000, (statisticsData[Statistics.BESTPACE] % 1000) / 100)
    print "起始时间戳:\t" + str(statisticsData[Statistics.TIMESTAMP]) + "\t" + converUnixTimestamp(statisticsData[Statistics.TIMESTAMP])
    print "完成时间:\t" + str(statisticsData[Statistics.ACCOMPLISHTIME]) + "秒\t\t" + converUnixTimestamp(statisticsData[Statistics.TIMESTAMP] + statisticsData[Statistics.ACCOMPLISHTIME])
    print "暂停时间:\t" + str(statisticsData[Statistics.PAUSETIME]) + "秒"
    print "距离:\t\t" + str(statisticsData[Statistics.DISTANCE]) + "米"
    print "校准距离:\t" + str(statisticsData[Statistics.CALIDISTANCE]) + "米"
    print "步数:\t\t" + str(statisticsData[Statistics.STEP]) + "次"

def analysisStatisticsV1003(buffer):
    "运动统计数据V1003解析"
    print "运动统计数据协议版本V1.0.03(" + hex(dataInfo[DataHead.VERSION]) + ")"

    statisticsData[Statistics.MODE] = getUint8(buffer[0:2])
    statisticsData[Statistics.AVERAGEHR] = getUint8(buffer[2:4])
    statisticsData[Statistics.MAXHR] = getUint8(buffer[4:6])
    statisticsData[Statistics.TIMEZONE] = getUint8(buffer[6:8])
    statisticsData[Statistics.DISTRIBUTED1] = getUint16(buffer[8:12])
    statisticsData[Statistics.DISTRIBUTED2] = getUint16(buffer[12:16])
    statisticsData[Statistics.DISTRIBUTED3] = getUint16(buffer[16:20])
    statisticsData[Statistics.DISTRIBUTED4] = getUint16(buffer[20:24])
    statisticsData[Statistics.DISTRIBUTED5] = getUint16(buffer[24:28])
    statisticsData[Statistics.MAXCADENCE] = getUint16(buffer[28:32])
    statisticsData[Statistics.RISEATMOSPRESS] = getUint32(buffer[32:40])
    statisticsData[Statistics.DROPATMOSPRESS] = getUint32(buffer[40:48])
    statisticsData[Statistics.MAXATMOSPRESS] = getUint32(buffer[48:56])
    statisticsData[Statistics.MINATMOSPRESS] = getUint32(buffer[56:64])
    statisticsData[Statistics.ATMOSPRESS] = getUint32(buffer[64:72])
    statisticsData[Statistics.CALORIE] = getUint32(buffer[72:80])
    statisticsData[Statistics.BESTPACE] = getUint32(buffer[80:88])
    statisticsData[Statistics.TIMESTAMP] = getUint32(buffer[88:96])
    statisticsData[Statistics.ACCOMPLISHTIME] = getUint32(buffer[96:104])
    statisticsData[Statistics.PAUSETIME] = getUint32(buffer[104:112])
    statisticsData[Statistics.DISTANCE] = getUint32(buffer[112:120])
    statisticsData[Statistics.CALIDISTANCE] = getUint32(buffer[120:128])
    statisticsData[Statistics.STEP] = getUint32(buffer[128:136])

def initStatisticsData():
    for i in range(Statistics.MAXITEM):
        statisticsData.append(0)
        i

def analysisRealtimeV1004(buffer):
    "运动实时数据V1004解析"
    print "运动统计数据协议版本V1.0.04(" + hex(dataInfo[DataHead.VERSION]) + ")"

    # print "RAW数据"
    print buffer[:dataInfo[DataHead.NODESIZE] * 2]
    printDividingLine()

    offset = 0
    for i in range(2):
    # for i in range(dataInfo[DataHead.NODENUM]):
        realtimeInfo[RealtimeData.PAUSE] = getUint8(buffer[offset + 0:offset + 2])
        realtimeInfo[RealtimeData.HR] = getUint8(buffer[offset + 2:offset + 4])
        realtimeInfo[RealtimeData.LONGITUDE_EW] = getUint8(buffer[offset + 4:offset + 6])
        realtimeInfo[RealtimeData.LATITUDE_NS] = getUint8(buffer[offset + 6:offset + 8])
        realtimeInfo[RealtimeData.CADENCE] = getUint16(buffer[offset + 8:offset + 12])
        realtimeInfo[RealtimeData.TEMPERATURE] = getUint16(buffer[offset + 12:offset + 16])
        realtimeInfo[RealtimeData.PACE] = getUint32(buffer[offset + 16:offset + 24])
        realtimeInfo[RealtimeData.LATITUDE] = getUint32(buffer[offset + 24:offset + 32])
        realtimeInfo[RealtimeData.LONGITUDE] = getUint32(buffer[offset + 32:offset + 40])
        realtimeInfo[RealtimeData.ATMOSPRESS] = getUint32(buffer[offset + 40:offset + 48])
        offset += dataInfo[DataHead.NODESIZE] * 2
        i
        info = copy.copy(realtimeInfo)
        realtimeData.append(info)
        # print realtimeInfo

    print "pause:\t" + hex(realtimeInfo[RealtimeData.PAUSE])
    print "hr:\t\t" + hex(realtimeInfo[RealtimeData.HR])
    print "longitude_ew:\t" + chr(realtimeInfo[RealtimeData.LONGITUDE_EW])
    print "latitude_ns:\t" + chr(realtimeInfo[RealtimeData.LATITUDE_NS])
    print "cadence:\t" + str(realtimeInfo[RealtimeData.CADENCE])
    print "temperature:\t" + str(realtimeInfo[RealtimeData.TEMPERATURE])
    # print "pace:\t\t%d\t\t%d'%d\""%(realtimeInfo[RealtimeData.PACE], realtimeInfo[RealtimeData.PACE] / 60, realtimeInfo[RealtimeData.PACE] % 60)
    print "speed:\t\t%d\t\t%d.%dkm/h"%(realtimeInfo[RealtimeData.PACE], realtimeInfo[RealtimeData.PACE] / 1000, (realtimeInfo[RealtimeData.PACE] % 1000) / 100)
    # if SportMode.SPORT_RIDE != statisticsData[Statistics.MODE]:
    #     print "最佳配速:\t%d\t\t%d'%d\""%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 60, statisticsData[Statistics.BESTPACE] % 60)
    # else:
    #     print "最佳速度:\t%d\t\t%d.%dkm/h"%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 1000, (statisticsData[Statistics.BESTPACE] % 1000) / 100)
    # print "longitude:\t" + str(realtimeInfo[RealtimeData.LONGITUDE])[0:2] + "." + str(realtimeInfo[RealtimeData.LONGITUDE])[2:8]
    print "longitude:\t" + hex(realtimeInfo[RealtimeData.LONGITUDE]) + "\t\t" + str(realtimeInfo[RealtimeData.LONGITUDE])
    print "longitude:\t" + str(realtimeInfo[RealtimeData.LONGITUDE])[0:2]
    # print "latitude:\t" + str(realtimeInfo[RealtimeData.LATITUDE])[0:2] + "." + str(realtimeInfo[RealtimeData.LATITUDE])[2:8]
    print "latitude:\t" + hex(realtimeInfo[RealtimeData.LATITUDE]) + "\t\t" + str(realtimeInfo[RealtimeData.LATITUDE])
    print "latitude:\t" + str(realtimeInfo[RealtimeData.LATITUDE])[0:2]
    print "atmospress:\t" + hex(realtimeInfo[RealtimeData.ATMOSPRESS])
    printDividingLine()

    print realtimeData[0]
    print realtimeData[1]

    print "longitude_ew:\t" + chr(realtimeData[0][RealtimeData.LONGITUDE_EW])
    print "longitude_ew:\t" + chr(realtimeData[1][RealtimeData.LONGITUDE_EW])

def initRealtimeData():
    for i in range(RealtimeData.MAXITEM):
        realtimeInfo.append(0)
        i

def analysisHeadInfo(buffer):
    "数据头信息解析"

    # print "RAW数据头"
    # print buffer
    # printDividingLine()

    dataInfo[DataHead.UUID] = getUint32(buffer[0:8])
    dataInfo[DataHead.MODEL1] = getUint8(buffer[8:10])
    dataInfo[DataHead.MODEL2] = getUint8(buffer[10:12])
    dataInfo[DataHead.VERSION] = getUint16(buffer[12:16])
    dataInfo[DataHead.NODESIZE] = getUint16(buffer[16:20])
    dataInfo[DataHead.NODENUM] = getUint16(buffer[20:24])

    # print "uuid:" + hex(dataInfo[DataHead.UUID])
    # print "mode1:" + hex(dataInfo[DataHead.MODEL1]) + "\t" + chr(dataInfo[DataHead.MODEL1])
    # print "mode2:" + hex(dataInfo[DataHead.MODEL2])
    # print "version:" + hex(dataInfo[DataHead.VERSION])
    # print "nodesize:" + str(dataInfo[DataHead.NODESIZE])
    # print "nodenum:" + hex(dataInfo[DataHead.NODENUM])
    # printDividingLine()

def process():
    # filename = raw_input("请输入运动数据文件名：")
    filename = "data.txt"

    if len(filename) == 0:
        filename = "data.txt"

    print "运动数据文件名: ", filename

    for i in range(DataHead.MAXITEM):
        i
        dataInfo.append(0)

    # 打开一个文件
    file = open(filename, "r")

    # 读取数据头长度
    buffer = file.read(12 * 2)

    # 解析数据头信息
    analysisHeadInfo(buffer)

    # 读取数据具体内容
    buffer = file.read(dataInfo[DataHead.NODESIZE] * dataInfo[DataHead.NODENUM] * 2)

    if (str("S") == chr(dataInfo[DataHead.MODEL1])):
        # 统计信息
        initStatisticsData()
        if (0x1003 == dataInfo[DataHead.VERSION]):
            analysisStatisticsV1003(buffer)
            printStatisticsInfo()
        else:
            print "版本无法识别" + hex(dataInfo[DataHead.VERSION])
    elif (str("R") == chr(dataInfo[DataHead.MODEL1])):
        # 实时数据
        initRealtimeData()
        analysisRealtimeV1004(buffer)
    else:
        print "类型无法识别" + hex(dataInfo[DataHead.MODEL1]) + " " + chr(dataInfo[DataHead.MODEL1])

    # 关闭打开的文件
    file.close()


process()