# encoding:utf-8
"""
    超级表1 equipmentstable
        表结构（动态，数据上传后不可修改） 时间戳-datetime、数据-data
        表结构（静态，数据后续还可修改） 设备id-tid、地址-address、key-tkey
        data-str   tid-str, address-str, tkey-str
        增:CREATE TABLE IF NOT EXISTS %s USING equipmentstable TAGS ('%s', '%s', '%s');
        删:drop table %s;
        改:(改标签,涉及到表名会复刻表到新表,然后删除旧表)alter table %s set tag %s='%s';
        查:select %s from equipmentstable %s='%s';
    子表: 设备id-tid
        增:insert into %s values (now, '%s');
        删:不允许删除数据
        改:不允许修改数据
        查:select * from %s;

    超级表2 accountstable
        表结构（动态，数据上传后不可修改） 时间戳-datetime、设备id-tid、设备状态-tidflag
        表结构（静态，数据后续还可修改） 用户id-mailbox、用户密码-password、权限-power、个人信息-information
        tid-str, tidflag-int   mailbox-str, password-str, power-str, information-str
        增:CREATE TABLE IF NOT EXISTS %s USING accountstable TAGS ('%s', '%s', '%s', '%s');
        删:drop table %s;
        改:(改标签,涉及到表名会复刻表到新表,然后删除旧表)alter table %s set tag %s='%s';
        查:select %s from accountstable %s='%s';
    子表:
        增:insert into %s values (now, '%s', '%s');
        删:不允许删除数据
        改:不允许修改数据
        查:select * from %s;
"""
import datetime
import taos
import time


# 连接数据库，返回连接器conn、游标td
def connect_tdengine():
    # conn = taos.connect(host="127.0.0.1", user="root", password="taosdata", config="C:\TDengine\cfg")
    conn = taos.connect(host="106.55.27.102", user="root", password="taosdata", config="/etc/taos")
    # conn = taos.connect(host="127.0.0.1", user="root", password="taosdata", config="/etc/taos")
    td = conn.cursor()
    data = []
    # 创建数据库
    try:
        if td.execute("show databases;") is not None:
            datalist = td.fetchall()
            for i in datalist:
                data.append(i[0])
            if 'air' in data:
                if td.execute("use air;") != 0:
                    return 0, 0
            else:
                if td.execute("create database air;") != 0:
                    return 0, 0
                else:
                    if td.execute("use air;") != 0:
                        return 0, 0
        if create_stable(conn, td) == 1:
            return conn, td
        else:
            return 0, 0
    except Exception as err:
        conn.close()
        raise err


# 创建超级表,成功则返回1，失败则返回0
def create_stable(conn, td):
    try:
        equipmentflag = td.execute("""CREATE STABLE IF NOT EXISTS equipmentstable(
                                        datetime timestamp,
                                        data binary(75))
                                        TAGS(
                                        tid binary(15),
                                        address nchar(15),
                                        tkey binary(10));""")
        accountflag = td.execute("""CREATE STABLE IF NOT EXISTS accountstable(
                                        datetime timestamp,
                                        tid binary(15),
                                        tidflag bool)
                                        TAGS(
                                        mailbox binary(30),
                                        password binary(20),
                                        power binary(10),
                                        information binary(100));""")
        if equipmentflag == 0 and accountflag == 0:
            return 1
        else:
            return 0
    except Exception as err:
        conn.close()
        raise err


# 增：创建用户子表，表名为stable+用户名，一个用户一张表记录全部设备,成功则返回1，失败则返回0。
def create_account_subtable(conn, td, mailbox, password, power="r-x", information=""):
    try:
        result = select_table(conn, td, 'account', mailbox)
        if result == 0:
            if td.execute("CREATE TABLE %s USING accountstable TAGS ('%s', '%s', '%s', '%s');" % (
                    'table' + mailbox.split('@')[0], mailbox, password, power, information)) != 0:
                return 0
            else:
                if insert_account_subtable(conn, td, mailbox, "original", 1) == 0:
                    return 0
                else:
                    return 1
        elif result is None:
            if insert_account_subtable(conn, td, mailbox, "original", 1) == 0:
                return 0
            else:
                return 1
        else:
            return 1
    except Exception as err:
        conn.close()
        raise err


# 增：用户子表插入数据,成功则返回1，失败则返回0
def insert_account_subtable(conn, td, mailbox, tid="", tidflag=1):
    try:
        if td.execute("insert into %s values (now, '%s', %s);" % ('table' + mailbox.split('@')[0], tid, tidflag)) != 1:
            return 0
        else:
            return 1
    except Exception as err:
        conn.close()
        raise err


# 增：创建设备子表，表名为设备名成功则返回1，失败则返回0。
def create_equipment_subtable(conn, td, tid, address, tkey):
    try:
        result = select_table(conn, td, 'equipment', tid)
        if result == 0:
            if td.execute("CREATE TABLE %s USING equipmentstable TAGS ('%s', '%s', '%s');" % (
                    tid, tid, address, tkey)) != 0:
                print("execute")
                return 0
            else:
                if insert_equipment_subtable(conn, td, tid, "original") == 0:
                    print("insert_equipment_subtable===0")
                    return 0
                else:
                    print("insert_equipment_subtable===1")
                    return 1
        elif result is None:
            if insert_equipment_subtable(conn, td, tid, "original") == 0:
                print("insert_equipment_subtable==0")
                return 0
            else:
                print("insert_equipment_subtable==1")
                return 1
        else:
            print("select_table==1")
            return 1
    except Exception as err:
        conn.close()
        raise err


# 增：设备子表插入数据,成功则返回1，失败则返回0
def insert_equipment_subtable(conn, td, tid, data):
    try:
        if td.execute("insert into %s values (now, '%s');" % (tid, data)) != 1:
            return 0
        else:
            return 1
    except Exception as err:
        conn.close()
        raise err


# 删：只能删除设备子表，用户不可改变
def drop_equipment_subtable(conn, td, tid):
    try:
        if td.execute("drop table %s;" % tid) != 0:
            return 0
        else:
            return 1
    except Exception as err:
        conn.close()
        raise err


# 改：修改accounttable的子表的password、power、information，成功则返回1，失败则返回0
def alter_accountstable(conn, td, mailbox, requirement, value):
    try:
        if requirement == "password":
            if td.execute("alter table %s set tag password='%s';" % ('table' + mailbox.split('@')[0], value)) != 0:
                return 0
            else:
                return 1
        if requirement == "power":
            if td.execute("alter table %s set tag power='%s';" % ('table' + mailbox.split('@')[0], value)) != 0:
                return 0
            else:
                return 1
        if requirement == "information":
            if td.execute("alter table %s set tag information='%s';" % ('table' + mailbox.split('@')[0], value)) != 0:
                return 0
            else:
                return 1
    except Exception as err:
        conn.close()
        raise err


# 改：修改equipmentstable的子表的tid、address、tkey，tid需要修改表名，可能需要移植表到新表，然后删除旧表，成功则返回1，失败则返回0
def alter_equipmentstable(conn, td, tid, requirement, value):
    try:
        if requirement == "tid":
            datalist = select_equipment(conn, td, "tid", tid)
            if td.execute("create table if not exists %s using equipmentstable tags ('%s', '%s', '%s');" % (
                    value, value, datalist[0][3], datalist[0][4])) != 0:
                return 0
            else:
                for data in datalist:
                    if td.execute("insert into %s values (%s, '%s')" % (value, time_change(1, data), data[1])) != 1:
                        return 0
                    else:
                        pass
                if td.execute("drop table %s;" % tid) != 0:
                    return 0
                else:
                    return 1
        if requirement == "address":
            if td.execute("alter table %s set tag address='%s';" % (tid, value)) != 0:
                return 0
            else:
                return 1
        if requirement == "tkey":
            if td.execute("alter table %s set tag tkey='%s';" % (tid, value)) != 0:
                return 0
            else:
                return 1
    except Exception as err:
        conn.close()
        raise err


# 查：查询用户表，需要什么列表就返回什么列表
def select_account(conn, td, requirement="", value=""):
    try:
        if requirement == "" and value == "":
            td.execute("select * from accountstable;")
            datalist = td.fetchall()
            return datalist
        else:
            td.execute("select * from accountstable where %s='%s';" % (requirement, value))
            datalist = td.fetchall()
            return datalist
    except Exception as err:
        conn.close()
        raise err


# 查：查询设备表，需要什么列表就返回什么列表，比如你查找相同tid返回相同tid数据
def select_equipment(conn, td, requirement="", value=""):
    try:
        if requirement == "" and value == "":
            td.execute("select * from equipmentstable;")
            datalist = td.fetchall()
            return datalist
        else:
            td.execute(
                "select * from equipmentstable where %s='%s' ORDER BY datetime DESC LIMIT 1;" % (requirement, value))
            datalist = td.fetchall()
            return datalist
    except Exception as err:
        conn.close()
        raise err


# 查：查询表内数据返回
def select_table(conn, td, requirement="", value=""):
    try:
        if requirement == 'account':
            td.execute("select * from %s;" % ('table' + value.split('@')[0]))
            datalist = td.fetchall()
        if requirement == 'equipmentday':
            # 一天5760 一周40320
            # td.execute("select * from %s;" % value)
            td.execute("select * from %s where datetime>NOW-1d" % value)
            datalist = td.fetchall()
        if requirement == 'equipmentweek':
            # 一天5760 一周40320
            # td.execute("select * from %s;" % value)
            td.execute("select * from %s where datetime>NOW-1w" % value)
            datalist = td.fetchall()
        return datalist
    except Exception as err:
        return 0
        # conn.close()
        # raise err


def select_table_Finaldata(conn, td, tid):
    try:
        # SELECT * FROM user LIMIT 1;  # 第一行数据
        # SELECT * FROM beiliulzx1 ORDER BY datetime DESC LIMIT 1;  # 最后一行数据
        td.execute("SELECT * FROM %s ORDER BY datetime DESC LIMIT 1;" % tid)
        data = td.fetchall()
        return data
    except Exception as err:
        conn.close()
        raise err


# 13位时间戳正反转
# 日期正转返回时间戳str（传进来列表list）   flag=1   (datetime.datetime(2021, 3, 6, 17, 40, 54, 727000), 'lkslkslks', 'lks', 'llks', '234567')
# 时间戳反转返回日期str（传进来时间戳datetime.datetime）   flag=0   datetime.datetime(2021, 3, 6, 17, 40, 54, 727000)
def time_change(flag, data):
    if flag == 1:
        dt = datetime.datetime.strptime(str(str(data[0]).split('.')[0]), '%Y-%m-%d %H:%M:%S')
        # 10位，时间点相当于从1.1开始的当年时间编号
        date_stamp = str(int(time.mktime(dt.timetuple())))
        # 3位，微秒
        data_microsecond = str("%06d" % dt.microsecond)[0:3]
        # date_stamp是个列表，将每个date_stamp逐个append到列表列表中再写入到数据库里，或者每个直接写入
        date_stamp = date_stamp + data_microsecond
        return date_stamp
    if flag == 0:
        return data.strftime("%Y-%m-%d %H:%M:%S")


# 设备数据显示处理
def data_change(datalist):
    dataresult = []
    for data in datalist:
        date = time_change(0, data[0])
        data = data[1].split(',')
        mp25 = int(data[3] + data[4], 16)
        temperature = int(data[5] + data[6], 16)
        humidity = int(data[7] + data[8], 16)
        hcho = int(data[9] + data[10], 16) / 1000
        tvoc = int(data[11] + data[12], 16) / 1000
        dataresult.append(
            {'date': date, 'pm25': mp25, 'temperature': temperature, 'humidity': humidity, 'hcho': hcho, 'tvoc': tvoc})
    return dataresult


# 折线图数据处理
def data_changelist(datalist):
    dataresult = {}
    datelist = []
    pm25list = []
    temperaturelist = []
    humiditylist = []
    hcholist = []
    tvoclist = []
    for data in datalist:
        date = time_change(0, data[0])
        data = data[1].split(',')
        pm25 = int(data[3] + data[4], 16)
        temperature = int(data[5] + data[6], 16)
        humidity = int(data[7] + data[8], 16)
        hcho = int(data[9] + data[10], 16) / 1000
        tvoc = int(data[11] + data[12], 16) / 1000

        datelist.append(date)
        pm25list.append(pm25)
        temperaturelist.append(temperature)
        humiditylist.append(humidity)
        hcholist.append(hcho)
        tvoclist.append(tvoc)

    dataresult['date'] = datelist
    dataresult['pm25'] = pm25list
    dataresult['temperature'] = temperaturelist
    dataresult['humidity'] = humiditylist
    dataresult['hcho'] = hcholist
    dataresult['tvoc'] = tvoclist
    return dataresult


# 地图标点
def mapaddress(address):
    maplist = []
    f = open("./mapcity.txt", 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        maplist.append(line.split())
    for data in maplist:
        if address in data[2]:
            return {'lng': float(data[3]), 'lat': float(data[4])}
    else:
        return {'lng': 0, 'lat': 0}


# conn, td = connect_tdengine()
# print(create_stable(conn, td))
# print(create_account_subtable(conn, td, '2550294419@qq.com', '123456789lzx', "r-x"))

# print(insert_account_subtable(conn, td, '2550294419@qq.com', "beiliulzx1"))

# print(create_equipment_subtable(conn, td, 'beiliulzx1', '玉林市', 'yulinlzx1'))

# print(insert_equipment_subtable(conn, td, 'beiliulzx1', "123234567uhgdssdfgb"))

# print(create_equipment_subtable(conn, td, 'beiliulzx2', '玉林市', 'yulinlzx1'))
# print(drop_equipment_subtable(conn, td, 'beiliulzx2'))

# print(alter_accountstable(conn, td, '2550294419@qq.com', 'password', '12345lzx'))

# print(alter_equipmentstable(conn, td, 'beiliulzx1', 'tid', 'beiliulzx2'))
# print(alter_equipmentstable(conn, td, 'beiliulzx1', 'address', '玉林'))

# print(select_account(conn, td))
'''
[(datetime.datetime(2021, 3, 25, 21, 6, 28, 691000), 'original', True, '578761295@qq.com', '19990720lks', 'r', ''), (datetime.datetime(2021, 3, 30, 21, 18, 38, 625000), 'original', True, '2550294419@qq.com', '12345lzx', 'r-x', ''), (datetime.datetime(2021, 3, 30, 21, 23, 21, 100000), 'beiliulzx1', True, '2550294419@qq.com', '12345lzx', 'r-x', '')]
'''
# print(select_account(conn, td, 'mailbox', '2550294419@qq.com'))
'''
[(datetime.datetime(2021, 3, 30, 21, 18, 38, 625000), 'original', True, '2550294419@qq.com', '12345lzx', 'r-x', ''), (datetime.datetime(2021, 3, 30, 21, 23, 21, 100000), 'beiliulzx1', True, '2550294419@qq.com', '12345lzx', 'r-x', '')]
'''

# print(select_equipment(conn, td))
'''
[(datetime.datetime(2021, 3, 30, 21, 26, 36), 'original', 'beiliulzx1', '玉林市', 'yulinlzx1'), (datetime.datetime(2021, 3, 30, 21, 29, 31), '123234567uhgdssdfgb', 'beiliulzx1', '玉林市', 'yulinlzx1')]
'''
# print(create_equipment_subtable(conn, td, 'beiliulzx2', '玉林市', 'yulinlzx1'))
# print(select_equipment(conn, td, 'tid', 'beiliulzx1'))
'''
[(datetime.datetime(2021, 3, 30, 21, 26, 36), 'original', 'beiliulzx1', '玉林市', 'yulinlzx1'), (datetime.datetime(2021, 3, 30, 21, 29, 31), '123234567uhgdssdfgb', 'beiliulzx1', '玉林市', 'yulinlzx1')]
'''
# print(select_table(conn, td, 'equipment', 'beiliulzx1'))
