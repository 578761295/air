# encoding:utf-8
# 发送纯文本
import smtplib
# 发送标题
from email.header import Header
# 邮件正文
from email.mime.text import MIMEText
import random


# https://www.jianshu.com/p/129101b726b6?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation

def mail_code():
    code = ""
    x = random.randint(3, 12)
    y = x - 3
    while x != y:
        if x % 3 == 0:
            code += str(random.randint(0, 9))
            code += str(random.randint(0, 9))
        if x % 3 == 1:
            code += str(chr(random.randint(65, 90)))
            code += str(chr(random.randint(65, 90)))
        if x % 3 == 2:
            code += str(chr(random.randint(97, 122)))
            code += str(chr(random.randint(97, 122)))
        x -= 1
    return code


def sendmail(user, pwd, sender, receiver, content, title):
    """
    说明：此函数实现发送邮件功能。
    :param user: 用户名
    :param pwd: 授权码
    :param sender: 发送方
    :param receiver: 接收方
    :param content: 邮件的正文
    :param title: 邮件的标题
    :return:
    """
    mail_host = "smtp.qq.com"  # qq的SMTP服务器
    # 第一部分：准备工作
    # 1.将邮件的信息打包成一个对象
    message = MIMEText(content, "plain", "utf-8")  # 内容，格式，编码
    # 2.设置邮件的发送者
    message["From"] = sender
    # 3.设置邮件的接收方
    message["To"] = receiver
    # join():通过字符串调用，参数为一个列表
    # message["To"] = ",".join(receiver)
    # 4.设置邮件的标题
    message["Subject"] = title

    # 第二部分：发送邮件
    try:
        # 1.启用服务器发送邮件
        # 参数：服务器，端口号
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        # 2.登录邮箱进行验证
        # 参数：用户名，授权码
        smtpObj.login(user, pwd)
        # 3.发送邮件
        # 参数：发送方，接收方，邮件信息
        smtpObj.sendmail(sender, receiver, message.as_string())
        # 发送成功
        return 1
    except:
        return 0


def mail(mail_receiver):
    code = mail_code()
    mail_user = "2550294419@qq.com"  # 用户名
    # gmvmqdzrtpibdiei
    # urqkdaxwmtwodjfa
    # vvxwbtglbogmeaaa
    # ajlboyitewxjdidd
    mail_pass = "aqtiapkmuowneagh"  # 发件人邮箱授权码
    mail_sender = "2550294419@qq.com"  # 发送方
    mail_receiver = mail_receiver  # 接收方
    email_content = "本次登录的验证码是：%s" % code  # 正文
    email_title = "基于web的户外环境监测可视化平台"  # 标题
    if sendmail(mail_user, mail_pass, mail_sender, mail_receiver, email_content, email_title) == 1:
        return str(code)
    else:
        return "False"
