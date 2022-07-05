import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import sqlite3

logging.basicConfig(level=logging.INFO)

def getdir_size(dir):
    """
    :param dir:文件路径
    :return:输出该文件路径下包含所有文件的大小（字节）
    """
    size = 0
    for root,dirs,file in os.walk(dir):
        # print(file)
        logging.debug(f'当前路径{root}')
        logging.debug(f'目录有{dirs}')
        logging.debug(f'文件有{file} \n')
        for i in range(len(file)):
            logging.debug(file[i])
            path = os.path.join(root,file[i])
            size_tmp = os.path.getsize(path)
            size = size + size_tmp
    print(size)
    return size

def write_txt(dir,mesg):
    with open(dir, mode='a') as note:
        note.write(mesg)
    print("write success")

def get_request():
    """
    :return: 发送get请求
    """
    url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
    res = requests.get(url)
    print(res.json()) #打印返回的json
    print(res.status_code)  #打印返回码
    print(res.raise_for_status())

def post_request():
    """
    :return:发送post请求
    """
    url = 'http://api.nnzhp.cn/api/user/gold_add'
    #入参
    data = {'stu_id':231,'gold':123}
    #添加header
    header = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}
    #添加cookie
    cookie = {'niuhanyang':'7e4c46e5790ca7d5165eb32d0a895ab1'}
    req = requests.post(url,json=data,headers=header,cookies=cookie)
    print(req.json())
    logging.debug(req.json()['msg'])

def send_mail(msg_text,sender,receivers):
    """
    :param msg_text: 要发送的信息
    :param sender: 发件人
    :param receivers: 收件人（列表，可多个）
    :return: 返回发送状态
    """
    smtpserver = 'smtp.qq.com'
    username = 'chengdgccc@qq.com'
    password = 'glgfdpxlnhiogaji'
    sender = sender  #发件人信息
    receivers = receivers #收件人信息，可写多个
    subject = 'Service check reminder' #标题
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    # msg['From'] = 'chengdegang@ezxr.com <chengdegang@ezxr.com>'
    msg['From'] = 'QA_ccc'
    msg['To'] = 'qa'
    # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
    msg['To'] = ";".join(receivers)

    text = f"Hi!\nHere is the link you wanted:\n{msg_text}"
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

    smtp = smtplib.SMTP_SSL(smtpserver)
    smtp.connect(smtpserver, '465')
    # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
    # smtp.set_debuglevel(1)
    smtp.login(username, password)
    smtp.sendmail(sender, receivers, msg.as_string())
    print("send success")
    smtp.quit()

def data_create():
    con = sqlite3.connect("data.db")
    # cursor = con.cursor()
    sql = """create table ccctest(
    id int,
    name text,
    gender text)"""
    con.execute(sql)
    # cursor.close()
    print("table created success")
    con.close()

def data_sql_insert():
    con = sqlite3.connect("data.db")
    sql = """insert into ccctest values(2,'name2','xx')
    """
    con.execute(sql)
    con.commit()
    print("sql excute success")
    con.close()

def data_sql_select():
    con = sqlite3.connect("data.db")
    sql = """select * from ccctest"""
    result = con.execute(sql)
    # print(type(result))
    for i in result:
        print(i)
    con.close()

if __name__ == '__main__':
    # getdir_size('/Users/degangcheng/Desktop/code/filecompare/testfile')
    # get_request()
    # send_mail('cesces','chengdgccc@qq.com',['18868890069@163.com'])
    # write_txt('data/ces.txt','ces666')
    data_sql_select()