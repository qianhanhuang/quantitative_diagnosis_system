from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import time
import random
import hashlib
import string
from flask import session
import mysql.connector


def encrypt(pwd):
    m = hashlib.md5()
    m.update(pwd.encode("utf8"))
    x = m.hexdigest()
    return x


def make_id(nums=5):
    time_code = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    random_code = ''.join(str(i) for i in random.sample(range(0, 9), nums))
    return time_code + random_code


def make_active_code():
    return ''.join(random.sample(string.ascii_letters + string.digits, 6))


def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def analysis_token():
    life_time = current_app.config.get("PERMANENT_SESSION_LIFETIME")
    s = Serializer(current_app.config.get("SECRET_KEY", "beornut@gmail.com"), expires_in=life_time)
    user_info = s.loads(session["user_id"])
    user_id = user_info["user_id"]
    return user_id


def get_unix_time():
    return int(round(time.time() * 1000))


def mysqlCon(argsdict, command):
    # print("db connecting")
    dbconn = mysql.connector.connect(host=argsdict['host'], database=argsdict['database'], user=argsdict['user'],
                                     password=argsdict['pwd'],
                                     port=argsdict['port'])
    cursor = dbconn.cursor()
    cursor.execute(command)
    datas = cursor.fetchall()
    cursor.close()
    dbconn.close()
    # print("db connect over")
    return datas
