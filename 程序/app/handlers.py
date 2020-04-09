import app.models as model
import xlrd
import os
import pymysql
import re


def confirmPassword(user_name, password):
    res = model.confirm(user_name, password)
    return res


def getUserInfoByID(id):
    res = model.getUserInfo(id)
    return res


def save_token(token_type, user_id, token, life_time):
    now = model.time.time()
    model.checkRepeatLogin(user_id)
    res = model.insertUserToken(token, model.time.strftime('%Y-%m-%d %H:%M:%S', model.time.localtime(now)), token_type,
                                user_id,
                                model.time.strftime('%Y-%m-%d %H:%M:%S', model.time.localtime(now + life_time)))
    return res


def load_token(key, token):
    try:
        s = model.Serializer(key)
        tk_content = s.loads(token)
    except:
        print("token had been modified")
        return None
    user = getUserInfoByID(tk_content["user_id"])
    if user:
        token_res = model.getToken(token)
        if token_res is not None:
            if str(token_res.expired_on) > model.time.strftime('%Y-%m-%d %H:%M:%S',
                                                               model.time.localtime(model.time.time())):
                return user
        else:
            return None
    return None


def expire_token(token):
    res = model.makeTokenExpire(token)
    return res


def filter(data):
    res = model.get_std_rcd(data['rcd_id'])
    if res:
        return {'main_sym': res.main_sym,
                'add_sym': res.add_sym,
                'tongue': res.tongue,
                'pulse': res.pulse,
                'syndrome': res.syndrome}
    res = model.get_raw_rcd(data['rcd_id'])
    res = model.filter(res.main_sym, res.add_sym, res.tongue, res.pulse, res.syndrome)
    return {'main_sym': ','.join(res[0]),
            'add_sym': ','.join(res[1]),
            'tongue': ','.join(res[2]),
            'pulse': ','.join(res[3]),
            'syndrome': ','.join(res[4])}


def get_clean_table(data):
    res, count = model.get_clean_table(data['index'])
    return {'res': res, 'count': count, 'index': data['index']}


def update_clean(data):
    return model.update_clean(data['rcd_id'], data['main_sym'], data['add_sym'], data['tongue'], data['pulse'],
                              data['syndrome'])


def delete_clean(data):
    return model.delete_clean(data['rcd_id'])


def get_pulse_table(data):
    res, count = model.get_pulse_table(data['index'])
    return {'res': res, 'count': count, 'index': data['index']}


def search_pulse(data):
    return model.search_pulse(data['abbr'])


def add_pulse(data):
    return model.add_pulse(data['pul_name'], data['abbr'], data['std_name'])


def update_pulse(data):
    return model.update_pulse(data['pul_id'], data['pul_name'], data['abbr'], data['std_name'])


def delete_pulse(data):
    return model.delete_pulse(data['pul_id'])


def get_tongue_table(data):
    res, count = model.get_tongue_table(data['index'])
    return {'res': res, 'count': count, 'index': data['index']}


def search_tongue(data):
    return model.search_tongue(data['abbr'])


def add_tongue(data):
    return model.add_tongue(data['ton_name'], data['abbr'], data['std_name'])


def update_tongue(data):
    return model.update_tongue(data['ton_id'], data['ton_name'], data['abbr'], data['std_name'])


def delete_tongue(data):
    return model.delete_tongue(data['ton_id'])


def get_symptom_table(data):
    res, count = model.get_symptom_table(data['index'])
    return {'res': res, 'count': count, 'index': data['index']}


def search_symptom(data):
    return model.search_symptom(data['abbr'])


def add_symptom(data):
    return model.add_symptom(data['sym_name'], data['abbr'], data['std_name'])


def update_symptom(data):
    return model.update_symptom(data['sym_id'], data['sym_name'], data['abbr'], data['std_name'])


def delete_symptom(data):
    return model.delete_symptom(data['sym_id'])


def get_syndrome_table(data):
    res, count = model.get_syndrome_table(data['index'])
    return {'res': res, 'count': count, 'index': data['index']}


def search_syndrome(data):
    return model.search_syndrome(data['abbr'])


def add_syndrome(data):
    return model.add_syndrome(data['syn_name'], data['abbr'], data['std_name'])


def update_syndrome(data):
    return model.update_syndrome(data['syn_id'], data['syn_name'], data['abbr'], data['std_name'])


def delete_syndrome(data):
    return model.delete_syndrome(data['syn_id'])


def add_form_rcd(data):
    return model.add_raw_rcd(data['main_sym'], data['add_sym'], data['tongue'], data['pulse'], data['syndrome'])


def add_text_rcd(data):
    try:
        text = data['text']
        for i in text.split('\n\n'):
            if i == '':
                continue
            lines = i.split('\n')
            res = model.add_raw_rcd(lines[0].split(':')[1], lines[1].split(':')[1], lines[2].split(':')[1],
                                    lines[3].split(':')[1], lines[4].split(':')[1])
            if res['code'] == -1:
                return res
        return {'code': 1}
    except Exception as e:
        return {'code': -1, 'message':'文本格式不对'}


def add_excel_rcd(data, file):
    filename = 'temp.' + file['file'].filename.split('.')[-1]
    file['file'].save(filename)
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)
    try:
        for i in range(int(data['first_row']) - 1, int(data['last_row'])):
            res = model.add_raw_rcd(sheet.row_values(i)[int(data['main_col']) - 1],
                                    sheet.row_values(i)[int(data['add_col']) - 1],
                                    sheet.row_values(i)[int(data['ton_col']) - 1],
                                    sheet.row_values(i)[int(data['pul_col']) - 1],
                                    sheet.row_values(i)[int(data['syn_col']) - 1],
                                    )
            if res['code'] == -1:
                os.remove(filename)
                return res
    except Exception as e:
        return {'code': -1, 'message':'表格内容错误！'}
    os.remove(filename)
    return {'code': 1}


def add_database_rcd(data):
    try:
        (user, password, host, port, database) = re.findall(r'(.+):(.+)@(.+):(.+)/(.+)', data['conn'])[0]
        conn = pymysql.connect(user=user, password=password, port=int(port), host=host, database=database)
        cur = conn.cursor()
        sql = 'select %s, %s, %s, %s, %s from %s' % (
            data['main'], data['add'], data['tongue'], data['pulse'], data['syndrome'], data['table'])
        cur.execute(sql)
        res = cur.fetchall()
        for i in res:
            if model.add_raw_rcd(i[0], i[1], i[2], i[3], i[4])['code'] == -1:
                return {'code': -1, 'message': '插入医案异常'}
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '数据库连接有误'}


def get_train_table(data):
    res, count = model.get_train_table(data['index'])
    return {'res': res, 'count': count, 'index': data['index']}


def add_train(data):
    return model.add_train(data['algo_name'], data['para'], data['indict'], float(data['accu']), data['time'])


def update_train(data):
    return model.update_train(data['train_id'], data['algo_name'], data['para'], data['indict'], float(data['accu']),
                              data['time'])


def delete_train(data):
    return model.delete_train(data['train_id'])


def get_accu():
    return model.get_accu()


def get_indict():
    return model.get_indict()


def get_data():
    return model.get_data()
