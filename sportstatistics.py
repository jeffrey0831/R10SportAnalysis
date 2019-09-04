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
    # valueΪ�����ֵΪʱ���(����)���磺1332888820
    timestamp = time.localtime(timestamp)
    # ����localtimeת������
    # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # ����پ���strftime����ת��Ϊ�������ڸ�ʽ��
    str = time.strftime(format, timestamp)
    return str

def printDividingLine():
    "��ӡ�ָ���"
    print "*" * 40

def getUint32(str):
    "��ȡUINT32"
    val = (int(str[0], 16) << 4) + int(str[1], 16)
    val += (int(str[2], 16) << 4) + int(str[3], 16) << 8
    val += (int(str[4], 16) << 4) + int(str[5], 16) << 16
    val += (int(str[6], 16) << 4) + int(str[7], 16) << 24
    # print "u32:" + hex(val)
    return val

def getUint16(str):
    "��ȡUINT16"
    val = (int(str[0], 16) << 4) + int(str[1], 16)
    val += (int(str[2], 16) << 4) + int(str[3], 16) << 8
    # print "u16:" + hex(val)
    return val

def getUint8(str):
    "��ȡUINT8"
    val = (int(str[0], 16) << 4) + int(str[1], 16)
    # print "u8:" + hex(val)
    return val

def printStatisticsInfo():
    "��ӡͳ��������Ϣ"

    modeName = ["����", "������", "������", "����"]
    if (statisticsData[Statistics.MODE] < 4):
        print "�˶�����:\t" + hex(statisticsData[Statistics.MODE]) + "\t\t" + modeName[statisticsData[Statistics.MODE]]
    else:
        print "�˶�����:\t " + hex(statisticsData[Statistics.MODE]) + "\t\t�޷�ʶ��"

    print "ƽ������:\t" + str(statisticsData[Statistics.AVERAGEHR])
    print "�������:\t" + str(statisticsData[Statistics.MAXHR])
    print "ʱ��:\t\t" + str(statisticsData[Statistics.TIMEZONE])

    hrCount = 0
    for i in range(5):
        hrCount += statisticsData[Statistics.DISTRIBUTED1 + i]
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
    print "��ʼʱ���:\t" + str(statisticsData[Statistics.TIMESTAMP]) + "\t" + converUnixTimestamp(statisticsData[Statistics.TIMESTAMP])
    print "���ʱ��:\t" + str(statisticsData[Statistics.ACCOMPLISHTIME]) + "��\t\t" + converUnixTimestamp(statisticsData[Statistics.TIMESTAMP] + statisticsData[Statistics.ACCOMPLISHTIME])
    print "��ͣʱ��:\t" + str(statisticsData[Statistics.PAUSETIME]) + "��"
    print "����:\t\t" + str(statisticsData[Statistics.DISTANCE]) + "��"
    print "У׼����:\t" + str(statisticsData[Statistics.CALIDISTANCE]) + "��"
    print "����:\t\t" + str(statisticsData[Statistics.STEP]) + "��"

def analysisStatisticsV1003(buffer):
    "�˶�ͳ������V1003����"
    print "�˶�ͳ������Э��汾V1.0.03(" + hex(dataInfo[DataHead.VERSION]) + ")"

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
    "�˶�ʵʱ����V1004����"
    print "�˶�ͳ������Э��汾V1.0.04(" + hex(dataInfo[DataHead.VERSION]) + ")"

    # print "RAW����"
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
    #     print "�������:\t%d\t\t%d'%d\""%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 60, statisticsData[Statistics.BESTPACE] % 60)
    # else:
    #     print "����ٶ�:\t%d\t\t%d.%dkm/h"%(statisticsData[Statistics.BESTPACE], statisticsData[Statistics.BESTPACE] / 1000, (statisticsData[Statistics.BESTPACE] % 1000) / 100)
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
    "����ͷ��Ϣ����"

    # print "RAW����ͷ"
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
    # filename = raw_input("�������˶������ļ�����")
    filename = "data.txt"

    if len(filename) == 0:
        filename = "data.txt"

    print "�˶������ļ���: ", filename

    for i in range(DataHead.MAXITEM):
        i
        dataInfo.append(0)

    # ��һ���ļ�
    file = open(filename, "r")

    # ��ȡ����ͷ����
    buffer = file.read(12 * 2)

    # ��������ͷ��Ϣ
    analysisHeadInfo(buffer)

    # ��ȡ���ݾ�������
    buffer = file.read(dataInfo[DataHead.NODESIZE] * dataInfo[DataHead.NODENUM] * 2)

    if (str("S") == chr(dataInfo[DataHead.MODEL1])):
        # ͳ����Ϣ
        initStatisticsData()
        if (0x1003 == dataInfo[DataHead.VERSION]):
            analysisStatisticsV1003(buffer)
            printStatisticsInfo()
        else:
            print "�汾�޷�ʶ��" + hex(dataInfo[DataHead.VERSION])
    elif (str("R") == chr(dataInfo[DataHead.MODEL1])):
        # ʵʱ����
        initRealtimeData()
        analysisRealtimeV1004(buffer)
    else:
        print "�����޷�ʶ��" + hex(dataInfo[DataHead.MODEL1]) + " " + chr(dataInfo[DataHead.MODEL1])

    # �رմ򿪵��ļ�
    file.close()


process()