# coding=gbk

import math
import time

class GnssInfo():
    LONGITUDE_EW = 0
    LONGITUDE = 1
    LATITUDE_NS = 2
    LATITUDE = 3
    MAXITEM = 4

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
    
    # 将角度转化为弧度
    radLog1 = rad(longitude1)
    radLat1 = rad(latitude1)
    radLog2 = rad(longitude2)
    radLat2 = rad(latitude2)

    # 纬度的差值
    a = radLat1 - radLat2
    # 经度差值
    b = radLog1 - radLog2
    # 弧度长度
    s = 2 * math.asin(math.sqrt(pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * pow(math.sin(b / 2), 2)));
    # 获取长度
    s = s * R;
    # 返回最接近参数的 long。结果将舍入为整数：加上 1/2
    s = round(s * 10000) / 10000;

    return s;

def printDividingLine():
    "打印分割线"
    print "*" * 40

def converUnixTimestamp(timestamp):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    timestamp = time.localtime(timestamp)
    # 经过localtime转换后变成
    # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    str = time.strftime(format, timestamp)
    return str

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
