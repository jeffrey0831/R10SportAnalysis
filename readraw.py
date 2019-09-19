import copy
import os
import shutil


filename = "data.raw"
outfilename = "data.txt"

# digital = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

file = open(filename, "rb")
outfilename = open(outfilename, "w")

# magic_number = int(data[0:2].encode("hex"), 16)
# val = str(digital[magic_number / 0x10]) + str(digital[magic_number % 0x10])
while (True):
    data = file.read(1)
    if not data:
        break
    
    number = data[0:2].encode("hex")
    # print number
    outfilename.write(number)
    
file.close()
outfilename.close()