# coding=gbk

import copy
import os
import shutil

SPORT_RAW_DATA = ":SyncService syncSportData onReceiveData: "
STEP_RAW_DATA = ":SyncService syncHistoryStepData onReceiveData: "

def readlog():
    context = ""
    outfilename = ""
    while (len(outfilename) == 0):
        type = raw_input("请选择（1.运动 2.计步 0:退出）：")
        if type == "1":
            context = SPORT_RAW_DATA
            outfilename = "datasport.txt"
        elif type == "2":
            context = STEP_RAW_DATA
            outfilename = "datastep.txt"
        elif type == "0":
            break

    if len(context) == 0: return

    # filename = raw_input("请输入读取安卓日志文件名：")
    filename = "2019-09-02_09-14-49.log"

    if len(filename) == 0 or 0 == os.path.exists(filename):
        filename = "data.log"

    print "安卓日志文件名: ", filename

    if (os.path.exists("data_out.txt")): os.remove("data_out.txt")

    outfilename = "datasport.txt"

    # 打开一个文件
    file = open(filename, "r")
    outfilename = open(outfilename, "w")

    start = len("2019-09-02 09:14:54")
    length = len(context)

    while (True):
        # 读取一行
        buffer = file.readline()

        # 判断是否读取到内容
        if not buffer:
            break

        if len(buffer) <= start + length: continue
        if buffer.find(context, start, start + length) < 0: continue
        if buffer.find("id=", start + length, start + length + 3) >= 0: continue
        
        # 每读取一行的末尾已经有了一个 `\n`
        # print(buffer[start + length:-1], ends='')
        # print(buffer[start + length:-1])
        outfilename.write(buffer[start + length:-1])
        
    # 关闭打开的文件
    outfilename.close()
    file.close()


readlog()