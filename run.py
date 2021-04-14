# encoding:utf-8
import datetime
from functools import reduce
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from mailboxcode import mail
from Tdengine import connect_tdengine, create_stable, create_account_subtable, insert_account_subtable, \
    create_equipment_subtable, insert_equipment_subtable, drop_equipment_subtable, alter_accountstable, \
    alter_equipmentstable, select_account, select_equipment, select_table, time_change, data_change, \
    select_table_Finaldata, data_changelist, mapaddress

app = Flask(__name__)
# 实现跨域访问
cors = CORS(app, resources={r"*": {"origins": "*"}})


@app.route('/login', methods=['POST'])
def login():
    # {'requirement': xxx 'mailbox': '2550294419@qq.com', 'password': '123abc'}
    json_data = request.get_json()
    if json_data['requirement'] == 'registercode':
        if select_table(conn, td, "account", json_data['mailbox']) != 0:
            return json.dumps(False)
        else:
            coderesult = mail(json_data['mailbox'])
            return json.dumps(coderesult)
    if json_data['requirement'] == 'forgetcode':
        if select_table(conn, td, "account", json_data['mailbox']) != 0:
            coderesult = mail(json_data['mailbox'])
            return json.dumps(coderesult)
        else:
            return json.dumps(False)
    if json_data['requirement'] == 'register':
        if create_account_subtable(conn, td, json_data['mailbox'], json_data['password']) == 1:
            return json.dumps(True)
        else:
            return json.dumps(False)
    if json_data['requirement'] == 'forget':
        if alter_accountstable(conn, td, json_data['mailbox'], 'password', json_data['password']) == 1:
            return json.dumps(True)
        else:
            return json.dumps(False)
    if json_data['requirement'] == 'login':
        result = select_account(conn, td, 'mailbox', json_data['mailbox'])
        if not result:
            return json.dumps(False)
        else:
            if json_data['password'] == result[0][4]:
                if result[0][6] == "":
                    return json.dumps({'power': result[0][5], 'information': {}})
                else:
                    return json.dumps({'power': result[0][5], 'information': eval(result[0][6])})
            else:
                return json.dumps(False)


# 设备数据页
@app.route('/equipmentmap', methods=['POST'])
def equipmentmap():
    # {'mailbox': 'xxx'}
    json_data = request.get_json()
    # return json.dumps([{'name': '北流市', 'lng': 110.35, 'lat': 22.72}])
    datacount = {}
    data = []
    result = select_account(conn, td, 'mailbox', json_data['mailbox'])
    if not result:
        return json.dumps(False)
    else:
        for count in result:
            datacount[count[1]] = count[2]
        # {'original': True, 'beiliulzx1': True, 'guilinlzx1': False, 'guilinlzx2': False, 'guilinlzx3': False, 'guilin1': True, 'beijing': True, 'beijin1': False, 'beijin2': True, 'beiliu1': True, 'beiliulzx2': True, 'beiliulzx10': True, 'beijin': False, 'beijin3': False}
        for datacountdata in datacount:
            if not datacount[datacountdata]:
                pass
            else:
                result1 = select_equipment(conn, td, "tid", datacountdata)
                if result1:
                    result2 = mapaddress(result1[0][3])
                    data.append({'address': result1[0][3], 'tid': datacountdata, 'finalresponsetime': time_change(0, result1[0][0]), 'lng': result2['lng'], 'lat': result2['lat']})
                else:
                    pass
        return json.dumps(data)


# 设备数据页
@app.route('/equipmenthome', methods=['POST'])
def equipmenthome():
    # {'requirement':'onquery', 'tid': 'xxx'}
    json_data = request.get_json()
    if json_data['requirement'] == 'onquery':
        result = select_table_Finaldata(conn, td, json_data['tid'])
        if result is not None:
            result1 = select_equipment(conn, td, "tid", json_data['tid'])
            result1 = result1[0][3]
            data = data_change(result)[0]
            data['address'] = result1
            return json.dumps(data)
        else:
            return json.dumps(False)
    if json_data['requirement'] == 'ononeday':
        result = select_table(conn, td, 'equipmentday', json_data['tid'])
        datalist = []
        for i in range(0, len(result)):
            if i % 40 == 0:
                datalist.append(result[i])
        data = data_changelist(datalist)
        return json.dumps(data)
    if json_data['requirement'] == 'ononeweek':
        result = select_table(conn, td, 'equipmentweek', json_data['tid'])
        datalist = []
        for i in range(0, len(result)):
            if i % 240 == 0:
                datalist.append(result[i])
        data = data_changelist(datalist)
        return json.dumps(data)
    # if json_data['requirement'] == 'ononemonth':
    #     # result = select_table(conn, td, 'equipment', json_data['tid'])[-(240*7):0:240]
    #     result = [(datetime.datetime(2021, 4, 6, 17, 29, 44, 375000), '01,03,14,00,4a,00,14,00,2a,02,51,02,11,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 30, 44, 375000), '01,03,14,00,4b,00,20,00,2c,02,53,02,13,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 31, 44, 375000), '01,03,14,00,4c,00,16,00,2d,02,55,02,1c,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 32, 44, 375000), '01,03,14,00,41,00,18,00,2f,02,5c,02,1f,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 33, 44, 375000), '01,03,14,00,43,00,17,00,21,02,51,02,10,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 34, 44, 375000), '01,03,14,00,4a,00,19,00,25,02,5d,02,17,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 35, 44, 375000), '01,03,14,00,42,00,18,00,23,02,5c,02,14,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 36, 44, 375000), '01,03,14,00,4a,00,15,00,2a,02,5a,02,15,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 37, 44, 375000), '01,03,14,00,4d,00,14,00,27,02,5c,02,1a,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 38, 44, 375000), '01,03,14,00,4a,00,19,00,24,02,52,02,1d,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 39, 44, 375000), '01,03,14,00,46,00,20,00,21,02,55,02,14,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 40, 44, 375000), '01,03,14,00,41,00,19,00,2a,02,56,02,1c,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 41, 44, 375000), '01,03,14,00,42,00,19,00,23,02,57,02,1d,87,39'),
    #               (datetime.datetime(2021, 4, 6, 17, 42, 44, 375000), '01,03,14,00,41,00,15,00,2a,02,51,02,11,87,39')]
    #
    #     data = data_changelist(result)
    #     return json.dumps(data)


# 设备控制台
@app.route('/consoleequipment', methods=['POST'])
def consoleequipment():
    json_data = request.get_json()
    datacount = {}
    timerdata = {'total': 0, 'running': 0, 'stopped': 0}
    data = []
    if json_data['requirement'] == 'onquery':
        # {'requirement':'onquery', 'mailbox': '578761295@qq.com'}
        # result = [{'tid': 'beiliu1', 'status': 1, 'address': '北流', 'finalresponsetime': '2021-4-3'},]
        result = select_account(conn, td, 'mailbox', json_data['mailbox'])
        if not result:
            return json.dumps(False)
        else:
            for count in result:
                datacount[count[1]] = count[2]
            # {'original': True, 'beiliulzx1': True, 'guilinlzx1': False, 'guilinlzx2': False, 'guilinlzx3': False, 'guilin1': True, 'beijing': True, 'beijin1': False, 'beijin2': True, 'beiliu1': True, 'beiliulzx2': True, 'beiliulzx10': True, 'beijin': False, 'beijin3': False}
            for datacountdata in datacount:
                if not datacount[datacountdata]:
                    pass
                else:
                    result1 = select_equipment(conn, td, "tid", datacountdata)
                    if result1:
                        data.append({'tid': datacountdata, 'status': 1, 'address': result1[0][3],
                                     'finalresponsetime': time_change(0, result1[0][0])})
                    else:
                        data.append({'tid': datacountdata, 'status': 1, 'address': 'xxx',
                                     'finalresponsetime': 'xxxx-xx-xx xx:xx:xx'})
            return json.dumps(data)
    if json_data['requirement'] == 'timer':
        # {'requirement':'onquery', 'mailbox': '578761295@qq.com'}
        # result = [{'tid': 'beiliu1', 'status': 1, 'address': '北流', 'finalresponsetime': '2021-4-3'},]
        result = select_account(conn, td, 'mailbox', json_data['mailbox'])
        if not result:
            return json.dumps(False)
        else:
            for count in result:
                datacount[count[1]] = count[2]
            # {'original': True, 'beiliulzx1': True, 'guilinlzx1': False, 'guilinlzx2': False, 'guilinlzx3': False, 'guilin1': True, 'beijing': True, 'beijin1': False, 'beijin2': True, 'beiliu1': True, 'beiliulzx2': True, 'beiliulzx10': True, 'beijin': False, 'beijin3': False}
            for datacountdata in datacount:
                timerdata['total'] += 1
                if datacount[datacountdata]:
                    timerdata['running'] += 1
                else:
                    timerdata['stopped'] += 1
            return json.dumps(timerdata)
    if json_data['requirement'] == 'onchange':
        # {'requirement': 'onchange', 'tid': 'beiliu2', 'address': '桂林'}
        result = alter_equipmentstable(conn, td, json_data['tid'], 'address', json_data['address'])
        return json.dumps(result)


# 个人中心
@app.route('/consolepersonal', methods=['POST'])
def consolepersonal():
    json_data = request.get_json()
    result = alter_accountstable(conn, td, json_data['mailbox'], 'information', str(json_data['data']))
    return json.dumps(True)


# 管理员
@app.route('/useradministrator', methods=['POST'])
def useradministrator():
    json_data = request.get_json()
    datacount = {}
    data = []
    if json_data['requirement'] == 'onquery':
        # {'requirement':'onquery', 'mailbox': 'xxx', 'password':'xxx'}
        result = select_account(conn, td, 'mailbox', json_data['mailbox'])
        if not result:
            return json.dumps(False)
        else:
            if result[0][4] != json_data['password']:
                return json.dumps(False)
            else:
                for count in result:
                    datacount[count[1]] = count[2]
                for resultdata in result:
                    if not datacount[resultdata[1]]:
                        pass
                    else:
                        result1 = select_equipment(conn, td, "tid", resultdata[1])
                        if result1:
                            data.append({'tid': resultdata[1], 'address': result1[0][3], 'tkey': result1[0][4]})
                datas = lambda x, y: x if y in x else x + [y]
                return json.dumps(reduce(datas, [[], ] + data))
        # return json.dumps([{'tid': '123', 'address': '456', 'tkey': '789'}, {'tid': '987', 'address': '654', 'tkey': '321'}])
    if json_data['requirement'] == 'onadd':
        # {'requirement':'onadd', 'mailbox': 'xxx', 'tid':'xxx', 'address':'xxx', 'tkey':'xxx'}
        result = create_equipment_subtable(conn, td, json_data['tid'], json_data['address'], json_data['tkey'])
        result1 = insert_account_subtable(conn, td, json_data['mailbox'], json_data['tid'], 1)
        if result == 1 and result1 == 1:
            return json.dumps(True)
        else:
            return json.dumps(False)
    if json_data['requirement'] == 'deleteRow':
        # 删除设备等于在该用户的表里对该客户的tidflag取反
        # {'requirement':'onquery', 'mailbox': 'xxx', 'tid':'xxx'}
        result = insert_account_subtable(conn, td, json_data['mailbox'], json_data['tid'], 0)
        if result == 1:
            return json.dumps(True)
        else:
            return json.dumps(False)
    if json_data['requirement'] == 'ondel':
        # {'requirement': 'ondel', 'mailbox': 'xxx', 'data': [{'tid': '123', 'address': '456', 'tkey': '789'}, {'tid': '987', 'address': '654', 'tkey': '321'}]}
        # 删除设备等于在该用户的表里对该客户的tidflag取反
        for data in json_data['data']:
            result = insert_account_subtable(conn, td, json_data['mailbox'], data['tid'], 0)
            if result != 1:
                return json.dumps(False)
        return json.dumps(True)


# 超级管理员
@app.route('/superadministrator', methods=['POST'])
def superadministrator():
    json_data = request.get_json()
    if json_data['requirement'] == 'onquery':
        # {'requirement':'onquery', 'mailbox': '578761295@qq.com'}
        result = select_account(conn, td, 'mailbox', json_data['mailbox'])
        if not result:
            return json.dumps(False)
        else:
            data = {'mailbox': result[0][3], 'password': result[0][4], 'power': result[0][5]}
            return json.dumps(data)
    if json_data['requirement'] == 'onadddel':
        # {'requirement':'onadddel', 'mailbox': 'xxx','power':'xxx'}
        result = alter_accountstable(conn, td, json_data['mailbox'], 'power', json_data['power'])
        if result == 1:
            return json.dumps(True)
        else:
            return json.dumps(False)
    if json_data['requirement'] == 'onchange':
        # {'requirement':'onadddel', 'mailbox': 'xxx','password':'xxx'}
        result = alter_accountstable(conn, td, json_data['mailbox'], 'password', json_data['password'])
        if result == 1:
            return json.dumps(True)
        else:
            return json.dumps(False)


if __name__ == '__main__':
    conn, td = connect_tdengine()  # 连接数据库
    if conn == 0 and td == 0:
        exit(0)
    else:
        app.run(host='0.0.0.0', port=5000)
