import datetime
import json

from Tdengine import connect_tdengine, create_stable, create_account_subtable, insert_account_subtable, \
    create_equipment_subtable, insert_equipment_subtable, drop_equipment_subtable, alter_accountstable, \
    alter_equipmentstable, select_account, select_equipment, select_table, time_change, select_table_Finaldata, \
    data_change

# tid = 'lks'
# tidflag = 0
# data = '1234567890'
# address = '南宁'
# tkey = '123456'
# mailbox = '578761295@qq.com'
# password = 'lks990720'
# power = 'rwxrwxrwx'
# information = '12877579373'
# value = 'llks'
# datalist = [(datetime.datetime(2021, 3, 6, 17, 40, 54, 727000), 'lkslkslks', 'lks', 'llks', '234567')]
#
# data = "01,03,14,00,00,00,00,00,85,00,00,14,46,00,00,00,00,01,2c,00,00,00,00,0d,6a"
# place = "桂林"
# key = "123456"
# datadata = "桂林、01,03,14,00,4f,00,11,00,17,03,43,01,43,f0,5e、990720"
#
# dlist = {}
#
# datacount ={}
# result = [(datetime.datetime(2021, 3, 30, 21, 18, 38, 625000), 'original', True, '2550294419@qq.com', '12345lzx', 'r-x', ''),
#           (datetime.datetime(2021, 3, 30, 21, 23, 21, 100000), 'beiliulzx1', True, '2550294419@qq.com', '12345lzx', 'r-x', '')]
#
# for count in result:
#     print(count[1])
# print(datacount)

def mapaddress(address):
    maplist = []
    f = open("./mapcity.txt", 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        maplist.append(line.split())
    for list in maplist:
        if address in list[2]:
            return {'lng': float(list[3]), 'lat': float(list[4])}

print(mapaddress('南宁'))