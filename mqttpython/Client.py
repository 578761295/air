# encoding:utf-8
import json
import paho.mqtt.client as mqtt
import time
from Virtualdata import virtualdata


# https://www.cnblogs.com/nuister/p/12942267.html
# https://blog.csdn.net/a1368783069/article/details/99676745
# https://www.jianshu.com/p/b76dbc675141
# https://blog.csdn.net/xxmonstor/article/details/80479851***最终版本***
# json跟request https://blog.csdn.net/luguanyou/article/details/107068551

# 连接MQTT服务器
def mqtt_connect():
    client.connect(host, port, 60)  # 连接
    client.loop_start()  # 以start方式运行，需要启动一个守护线程，让服务端运行，否则会随主线程死亡
    # client.loop_forever()  # 以forever方式阻塞运行。无限运行


# 订阅主题
def on_subscribe(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    print("Start server!")
    client.subscribe("air-monitor/download")  # 订阅主题
    client.on_message = on_message  # 消息处理函数


# 接收服务端发送的消息
def on_message(client, userdata, msg):
    """
    接收服务端发送的消息
    :param client: 连接信息
    :param userdata:
    :param msg: 服务端返回的消息(---主题(Topic)、负载(payload)---)
    :return:
    """
    payload = json.loads(msg.payload.decode('utf-8'))
    print(msg.topic, payload["msg"])


# 客户端发布消息
def on_publish(message: str):
    """
    客户端发布消息
    :param message: 消息主体
    :return:
    """
    payload = {"msg": "%s" % message}
    # publish(主题：Topic; 消息内容)
    client.publish("air-monitor/upload", json.dumps(payload, ensure_ascii=False))
    print("Successful send message:", message)


# 读取串口数据转码
def serialdata():
    # data = []
    # i = 0
    # ser = serial.Serial('COM10', 9600)
    #
    # while True:
    #     s = ser.read().hex()
    #     data.append(str(s))
    #     i += 1
    #     if i == 25:
    #         print(data)
    #         i = 0
    #         time.sleep(2)
    data = virtualdata()
    return clientid + '、' + place + '、' + str(data) + '、' + key


def main():
    client.on_connect = on_subscribe  # 启用订阅模式(补齐4个参数)
    mqtt_connect()  # 连接MQTT服务器
    while True:
        data = serialdata()
        on_publish(data)
        time.sleep(15)


if __name__ == '__main__':
    host = "106.55.27.102"
    port = 1883
    clientid = "guilinlks1"
    place = "桂林"
    key = "990720"
    client = mqtt.Client(client_id=clientid)
    # 启动监听
    main()
