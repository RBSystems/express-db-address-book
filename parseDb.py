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
import os
from os import listdir
from os.path import isfile, join
import string
import re

parser = argparse.ArgumentParser(description='Process a Roomview Express DB')
parser.add_argument('--db')
parser.add_argument('--output')

args = parser.parse_args()

mypath = os.getcwd()

hosts=[]

files = []

def removeDupes(l):
    dedupe = l
    return dedupe

def dedupe(seq):
    set = {}
    map(set.__setitem__, seq, [])
    return set.keys()

entries = ['[Entries]','_AAASerial on COM1=usb','_Generic Cresnet Device Override=_Serial on COM1:cresnet 03;device GenericCrensetDevice','_Remote Console To CNet ID 03=_Serial on COM1:cresnet 03','_Serial on COM1=rs232 1,0,n,8,1,n,y','_USB=usb']

entries2 = ['[Settings]','DefaultEntry=','[Comments]','_AAASerial on COM1=','_Generic Cresnet Device Override=','_Remote Console To CNet ID 03=','_Serial on COM1=','_USB=']

if args.db:
    files.append(args.db)
else:
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for fName in onlyfiles:
        if (fName.find(".rvd") > 0) and (fName.find("HD") > 0):
            files.append(fName)

if args.output:
    out = output
else:
    out = "ServiceCenterAddressBook.xadr"

for f in files:
    with open(f, "rb") as binary_file:
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

#fileName = f + "_addressBook.xadr"
for host in hosts:
    entries.append(host['bldg'] + " " + host['room'] + " " + host['roomType'] + "=tcp " + host['ip'] + "")

entries = removeDupes(entries)

for host in hosts:
    entries2.append(host['bldg'] + " " + host['room'] + " " + host['roomType'] + "=")

entries2 = removeDupes(entries2)

with open(out,'a') as addressBook:
    for entry in entries:
        addressBook.write(entry + '\n')
    for entry in entries2:
        addressBook.write(entry + '\n')
