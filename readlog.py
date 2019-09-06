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
        type = raw_input("��ѡ��1.�˶� 2.�Ʋ� 0:�˳�����")
        if type == "1":
            context = SPORT_RAW_DATA
            outfilename = "datasport.txt"
        elif type == "2":
            context = STEP_RAW_DATA
            outfilename = "datastep.txt"
        elif type == "0":
            break

    if len(context) == 0: return

    # filename = raw_input("�������ȡ��׿��־�ļ�����")
    filename = "2019-09-02_09-14-49.log"

    if len(filename) == 0 or 0 == os.path.exists(filename):
        filename = "data.log"

    print "��׿��־�ļ���: ", filename

    if (os.path.exists("data_out.txt")): os.remove("data_out.txt")

    outfilename = "datasport.txt"

    # ��һ���ļ�
    file = open(filename, "r")
    outfilename = open(outfilename, "w")

    start = len("2019-09-02 09:14:54")
    length = len(context)

    while (True):
        # ��ȡһ��
        buffer = file.readline()

        # �ж��Ƿ��ȡ������
        if not buffer:
            break

        if len(buffer) <= start + length: continue
        if buffer.find(context, start, start + length) < 0: continue
        if buffer.find("id=", start + length, start + length + 3) >= 0: continue
        
        # ÿ��ȡһ�е�ĩβ�Ѿ�����һ�� `\n`
        # print(buffer[start + length:-1], ends='')
        # print(buffer[start + length:-1])
        outfilename.write(buffer[start + length:-1])
        
    # �رմ򿪵��ļ�
    outfilename.close()
    file.close()


readlog()