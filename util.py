# coding=gbk

import time

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
