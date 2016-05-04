#####
#
# Title: parseDb.py
# Author: Dan Clegg
# Copyright: 2016, Dan Clegg
# LICENSE: Apache 2.0
#
#####

import sys
import binascii
import argparse
import string
import re

parser = argparse.ArgumentParser(description='Process a Roomview Express DB')
parser.add_argument('--db')

args = parser.parse_args()

hosts=[]

with open(args.db, "rb") as binary_file:
    # Read the whole file at once
    data = binary_file.read()
    a_data = binascii.rledecode_hqx(data)
    for line in iter(a_data.splitlines()):
        host = {}
        if (line.find('10.') >= 0):
            arr = re.split(' ',line)
            for item in arr:
                room = ""
                bldg = ""
                if (item.find('10.') >= 0):
                    room = arr[arr.index(item) - 1]
                    bldg = arr[arr.index(item) - 2]
                    ip = ""
                    roomType = ""

                    printable = set(string.printable)

                    bldg = ''.join([i if ord(i) < 128 else ' ' for i in bldg])
                    bldg = re.sub(' +',' ',bldg)
                    innerArr = bldg.split(' ')
                    bldg = innerArr[-1]
                    bldg = filter(lambda x: x in printable, bldg)

                    item = re.sub("0.0.0.0"," ",item)
                    innerarr = re.split(' ',item)
                    for inneritem in innerarr:
                        if (inneritem.find('10.') >= 0):
                            inneritem = re.sub('HDMMC','HDMMC ',inneritem)
                            inneritem = re.sub('HDTEC','HDTEC ',inneritem)
                            inneritem = re.sub('.*ite','TECLite ',inneritem)
                            innerItemSplit = inneritem.split(' ')
                            for subElement in innerItemSplit:
                                if (subElement.find('10.') >= 0):
                                    ip = subElement
                                else:
                                    roomType = subElement

                    host['bldg'] = bldg
                    host['room'] = room
                    host['roomType'] = roomType
                    host['ip'] = ip
                    hosts.append(host)

fileName = args.db + "_addressBook.xadr"

with open(fileName,'a') as addressBook:
    addressBook.write('[Entries]\n')
    addressBook.write('_AAASerial on COM1=usb\n')
    addressBook.write('_Generic Cresnet Device Override=_Serial on COM1:cresnet 03;device GenericCrensetDevice\n')
    addressBook.write('_Remote Console To CNet ID 03=_Serial on COM1:cresnet 03\n')
    addressBook.write('_Serial on COM1=rs232 1,0,n,8,1,n,y\n')
    addressBook.write('_USB=usb\n')
    for host in hosts:
        addressBook.write(host['bldg'] + " " + host['room'] + " " + host['roomType'] + "=tcp " + host['ip'] + "\n")

    addressBook.write('[Settings]\n')
    addressBook.write('DefaultEntry=\n')

    addressBook.write('[Comments]\n')
    addressBook.write('_AAASerial on COM1=\n')
    addressBook.write('_Generic Cresnet Device Override=\n')
    addressBook.write('_Remote Console To CNet ID 03=\n')
    addressBook.write('_Serial on COM1=\n')
    addressBook.write('_USB=\n')

    for host in hosts:
        addressBook.write(host['bldg'] + " " + host['room'] + " " + host['roomType'] + "=\n")
