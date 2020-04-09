from app.MySQLconnect import *
from app.utils import *
from sqlalchemy import desc
import math
import json


def confirm(user_name, password):
    user = User.query.filter_by(user_name=user_name).first()
    if user is not None and user.verify_password(encrypt(password)):
        return user
    else:
        return False


def getUserInfo(id):
    user = User.query.filter_by(user_id=id).first()
    if user is not None:
        return user


def checkRepeatLogin(user_id):
    res = db.session.execute(
        "select * from token where user_id='" + str(user_id) + "' and expired_on>sysdate()").fetchall()
    for i in res:
        makeTokenExpire(i[0])


def insertUserToken(token, now, token_type, user_id, expired_time):
    tk = Token()
    tk.token_id = token
    tk.created_on = now
    tk.token_type = token_type
    tk.user_id = user_id
    tk.expired_on = expired_time
    db.session.add(tk)
    db.session.commit()


def getToken(token):
    tk = Token.query.filter_by(token_id=token).first()
    if tk:
        return tk
    return None


def makeTokenExpire(token):
    res = Token.query.filter_by(token_id=token).update(
        {Token.expired_on: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))})
    db.session.commit()
    return res


def get_std_rcd(rcd_id):
    res = StdRecord.query.filter_by(rcd_id=rcd_id).first()
    if not res:
        return None
    else:
        return res


def get_raw_rcd(rcd_id):
    res = RawRecord.query.filter_by(rcd_id=rcd_id).first()
    if not res:
        return None
    else:
        return res


def filter(main_sym, add_sym, tongue, pulse, syndrome):
    res = [[], [], [], [], []]
    sym = Symptom.query.all()
    ton = Tongue.query.all()
    pul = Pulse.query.all()
    syn = Syndrome.query.all()
    syms = dict(zip([i.sym_name for i in sym], sym))
    tons = dict(zip([i.ton_name for i in ton], ton))
    puls = dict(zip([i.pul_name for i in pul], pul))
    syns = dict(zip([i.syn_name for i in syn], syn))
    if main_sym:
        for i in main_sym.split(','):
            if i in syms:
                std = i if syms[i].std_id == 0 else Symptom.query.filter(sym_id=syms[i].std_id).first().sym_name
                if std not in res[0]:
                    res[0].append(std)
    if add_sym:
        for i in add_sym.split(','):
            if i in syms and i not in res[0]:
                std = i if syms[i].std_id == 0 else Symptom.query.filter_by(sym_id=syms[i].std_id).first().sym_name
                if std not in res[0]:
                    res[1].append(std)
    if tongue:
        for i in tongue.split(','):
            if i in tons:
                std = i if tons[i].std_id == 0 else Tongue.query.filter_by(ton_id=tons[i].std_id).first().ton_name
                if std not in res[0]:
                    res[2].append(std)
    if pulse:
        for i in pulse.split(','):
            if i in puls:
                std = i if puls[i].std_id == 0 else Pulse.query.filter_by(pul_id=puls[i].std_id).first().pul_name
                if std not in res[0]:
                    res[3].append(std)
    if syndrome:
        for i in syndrome.split(','):
            if i in syns:
                std = i if syns[i].std_id == 0 else Syndrome.query.filter_by(syn_id=syns[i].std_id).first().syn_name
                if std not in res[0]:
                    res[4].append(std)
    return res


def get_clean_table(index):
    res = RawRecord.query.order_by(desc(RawRecord.rcd_id)).all()
    count = len(res)
    page_num = math.ceil(count / 10)
    data = []
    if page_num < index:
        return {}, count
    elif page_num == index:
        for i in res[index * 10 - 10:]:
            obj = {}
            obj['rcd_id'] = i.rcd_id
            obj['main_sym'] = i.main_sym if i.main_sym is not None else ''
            obj['add_sym'] = i.add_sym if i.add_sym is not None else ''
            obj['tongue'] = i.tongue if i.tongue is not None else ''
            obj['pulse'] = i.pulse if i.pulse is not None else ''
            obj['syndrome'] = i.syndrome if i.syndrome is not None else ''
            data.append(obj)
        return data, count
    else:
        for i in res[index * 10 - 10: index * 10]:
            obj = {}
            obj['rcd_id'] = i.rcd_id
            obj['main_sym'] = i.main_sym if i.main_sym is not None else ''
            obj['add_sym'] = i.add_sym if i.add_sym is not None else ''
            obj['tongue'] = i.tongue if i.tongue is not None else ''
            obj['pulse'] = i.pulse if i.pulse is not None else ''
            obj['syndrome'] = i.syndrome if i.syndrome is not None else ''
            data.append(obj)
        return data, count


def update_clean(rcd_id, main_sym, add_sym, tongue, pulse, syndrome):
    try:
        std = StdRecord.query.filter_by(rcd_id=rcd_id).first()
        if not std:
            std = StdRecord()
            std.rcd_id = rcd_id
            std.main_sym = main_sym
            std.add_sym = add_sym
            std.tongue = tongue
            std.pulse = pulse
            std.syndrome = syndrome
            db.session.add(std)
            db.session.commit()
            return {'code': 1}
        std.main_sym = main_sym
        std.add_sym = add_sym
        std.tongue = tongue
        std.pulse = pulse
        std.syndrome = syndrome
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def delete_clean(rcd_id):
    try:
        raw = RawRecord.query.filter_by(rcd_id=rcd_id).first()
        if not raw:
            return {'code': -1, 'message': '不存在'}
        std = StdRecord.query.filter_by(rcd_id=rcd_id).first()
        if std:
            db.session.delete(std)
        db.session.delete(raw)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def get_pulse_table(index):
    res = Pulse.query.order_by(desc(Pulse.pul_id)).all()
    count = len(res)
    page_num = math.ceil(count / 10)
    data = []
    if page_num < index:
        return {}, count
    elif page_num == index:
        for i in res[index * 10 - 10:]:
            obj = {}
            obj['pul_id'] = i.pul_id
            obj['pul_name'] = i.pul_name
            obj['abbr'] = i.abbr
            obj['std_name'] = Pulse.query.filter_by(pul_id=i.std_id).first().pul_name if i.std_id != 0 else i.pul_name
            data.append(obj)
        return data, count
    else:
        for i in res[index * 10 - 10: index * 10]:
            obj = {}
            obj['pul_id'] = i.pul_id
            obj['pul_name'] = i.pul_name
            obj['abbr'] = i.abbr
            obj['std_name'] = Pulse.query.filter_by(pul_id=i.std_id).first().pul_name if i.std_id != 0 else i.pul_name
            data.append(obj)
        return data, count


def search_pulse(abbr):
    try:
        res = db.session.query(Pulse.pul_name).filter(Pulse.abbr.like('%' + abbr.replace("'", "") + '%'),
                                                      Pulse.std_id == 0).all()
        data = [i.pul_name for i in res]
        return data
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def add_pulse(pul_name, abbr, std_name):
    try:
        pulse = Pulse()
        if Pulse.query.filter_by(pul_name=pul_name).first():
            return {'code': -1, 'message': '已存在'}
        pulse.pul_name = pul_name
        pulse.abbr = abbr
        pulse.std_id = Pulse.query.filter_by(
            pul_name=std_name.split(',')[0]).first().pul_id if std_name != pul_name else 0
        pulse.num = 0
        db.session.add(pulse)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def update_pulse(pul_id, pul_name, abbr, std_name):
    try:
        pulse = Pulse.query.filter_by(pul_id=pul_id).first()
        if not pulse:
            return {'code': -1, 'message': '不存在'}
        if Pulse.query.filter(Pulse.pul_name==pul_name, Pulse.pul_id!=pul_id).first():
            return {'code': -1, 'message': '同名'}
        pulse.pul_name = pul_name
        pulse.abbr = abbr
        pulse.std_id = Pulse.query.filter_by(
            pul_name=std_name.split(',')[0]).first().pul_id if std_name != pul_name else 0
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def delete_pulse(pul_id):
    try:
        pulse = Pulse.query.filter_by(pul_id=pul_id).first()
        if not pulse:
            return {'code': -1, 'message': '不存在'}
        db.session.delete(pulse)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def get_tongue_table(index):
    res = Tongue.query.order_by(desc(Tongue.ton_id)).all()
    count = len(res)
    page_num = math.ceil(count / 10)
    data = []
    if page_num < index:
        return {}, count
    elif page_num == index:
        for i in res[index * 10 - 10:]:
            obj = {}
            obj['ton_id'] = i.ton_id
            obj['ton_name'] = i.ton_name
            obj['abbr'] = i.abbr
            obj['std_name'] = Tongue.query.filter_by(ton_id=i.std_id).first().ton_name if i.std_id != 0 else i.ton_name
            data.append(obj)
        return data, count
    else:
        for i in res[index * 10 - 10: index * 10]:
            obj = {}
            obj['ton_id'] = i.ton_id
            obj['ton_name'] = i.ton_name
            obj['abbr'] = i.abbr
            obj['std_name'] = Tongue.query.filter_by(ton_id=i.std_id).first().ton_name if i.std_id != 0 else i.ton_name
            data.append(obj)
        return data, count


def search_tongue(abbr):
    try:
        res = db.session.query(Tongue.ton_name).filter(Tongue.abbr.like('%' + abbr.replace("'", "") + '%'),
                                                       Tongue.std_id == 0).all()
        data = [i.ton_name for i in res]
        return data
    except Exception as e:
        print(e)
        return {'code': -1}


def add_tongue(ton_name, abbr, std_name):
    try:
        tongue = Tongue()
        if Tongue.query.filter_by(ton_name=ton_name).first():
            return {'code': -1, 'message': '已存在'}
        tongue.ton_name = ton_name
        tongue.abbr = abbr
        tongue.std_id = Tongue.query.filter_by(
            ton_name=std_name.split(',')[0]).first().ton_id if std_name != ton_name else 0
        tongue.num = 0
        db.session.add(tongue)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def update_tongue(ton_id, ton_name, abbr, std_name):
    try:
        tongue = Tongue.query.filter_by(ton_id=ton_id).first()
        if not tongue:
            return {'code': -1, 'message': '不存在'}
        if Tongue.query.filter(Tongue.ton_name==ton_name, Tongue.ton_id!=ton_id).first():
            return {'code': -1, 'message': '同名'}
        tongue.ton_name = ton_name
        tongue.abbr = abbr
        tongue.std_id = Tongue.query.filter_by(
            ton_name=std_name.split(',')[0]).first().ton_id if std_name != ton_name else 0
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def delete_tongue(ton_id):
    try:
        tongue = Tongue.query.filter_by(ton_id=ton_id).first()
        if not tongue:
            return {'code': -1, 'message': '不存在'}
        db.session.delete(tongue)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def get_symptom_table(index):
    res = Symptom.query.order_by(desc(Symptom.sym_id)).all()
    count = len(res)
    page_num = math.ceil(count / 10)
    data = []
    if page_num < index:
        return {}, count
    elif page_num == index:
        for i in res[index * 10 - 10:]:
            obj = {}
            obj['sym_id'] = i.sym_id
            obj['sym_name'] = i.sym_name
            obj['abbr'] = i.abbr
            obj['std_name'] = Symptom.query.filter_by(sym_id=i.std_id).first().sym_name if i.std_id != 0 else i.sym_name
            data.append(obj)
        return data, count
    else:
        for i in res[index * 10 - 10: index * 10]:
            obj = {}
            obj['sym_id'] = i.sym_id
            obj['sym_name'] = i.sym_name
            obj['abbr'] = i.abbr
            obj['std_name'] = Symptom.query.filter_by(sym_id=i.std_id).first().sym_name if i.std_id != 0 else i.sym_name
            data.append(obj)
        return data, count


def search_symptom(abbr):
    try:
        res = db.session.query(Symptom.sym_name).filter(Symptom.abbr.like('%' + abbr.replace("'", "") + '%'),
                                                        Symptom.std_id == 0).all()
        data = [i.sym_name for i in res]
        return data
    except Exception as e:
        print(e)
        return {'code': -1}


def add_symptom(sym_name, abbr, std_name):
    try:
        symptom = Symptom()
        if symptom.query.filter_by(sym_name=sym_name).first():
            return {'code': -1, 'message': '已存在'}
        symptom.sym_name = sym_name
        symptom.abbr = abbr
        symptom.std_id = symptom.query.filter_by(
            sym_name=std_name.split(',')[0]).first().sym_id if std_name != sym_name else 0
        symptom.num = 0
        db.session.add(symptom)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def update_symptom(sym_id, sym_name, abbr, std_name):
    try:
        symptom = Symptom.query.filter_by(sym_id=sym_id).first()
        if not symptom:
            return {'code': -1, 'message': '不存在'}
        if Symptom.query.filter(Symptom.sym_name==sym_name, Symptom.sym_id!=sym_id).first():
            return {'code': -1, 'message': '同名'}
        symptom.sym_name = sym_name
        symptom.abbr = abbr
        symptom.std_id = symptom.query.filter_by(
            sym_name=std_name.split(',')[0]).first().sym_id if std_name != sym_name else 0
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def delete_symptom(sym_id):
    try:
        symptom = Symptom.query.filter_by(sym_id=sym_id).first()
        if not symptom:
            return {'code': -1, 'message': '不存在'}
        db.session.delete(symptom)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def get_syndrome_table(index):
    res = Syndrome.query.order_by(desc(Syndrome.syn_id)).all()
    count = len(res)
    page_num = math.ceil(count / 10)
    data = []
    if page_num < index:
        return {}, count
    elif page_num == index:
        for i in res[index * 10 - 10:]:
            obj = {}
            obj['syn_id'] = i.syn_id
            obj['syn_name'] = i.syn_name
            obj['abbr'] = i.abbr
            obj['std_name'] = Syndrome.query.filter_by(
                syn_id=i.std_id).first().syn_name if i.std_id != 0 else i.syn_name
            data.append(obj)
        return data, count
    else:
        for i in res[index * 10 - 10: index * 10]:
            obj = {}
            obj['syn_id'] = i.syn_id
            obj['syn_name'] = i.syn_name
            obj['abbr'] = i.abbr
            obj['std_name'] = Syndrome.query.filter_by(
                syn_id=i.std_id).first().syn_name if i.std_id != 0 else i.syn_name
            data.append(obj)
        return data, count


def search_syndrome(abbr):
    try:
        res = db.session.query(Syndrome.syn_name).filter(Syndrome.abbr.like('%' + abbr.replace("'", "") + '%'),
                                                         Syndrome.std_id == 0).all()
        data = [i.syn_name for i in res]
        return data
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def add_syndrome(syn_name, abbr, std_name):
    try:
        syndrome = Syndrome()
        if syndrome.query.filter_by(syn_name=syn_name).first():
            return {'code': -1, 'message': '已存在'}
        syndrome.syn_name = syn_name
        syndrome.abbr = abbr
        syndrome.std_id = syndrome.query.filter_by(
            syn_name=std_name.split(',')[0]).first().syn_id if std_name != syn_name else 0
        syndrome.num = 0
        db.session.add(syndrome)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def update_syndrome(syn_id, syn_name, abbr, std_name):
    try:
        syndrome = Syndrome.query.filter_by(syn_id=syn_id).first()
        if not syndrome:
            return {'code': -1, 'message': '不存在'}
        if Syndrome.query.filter(Syndrome.syn_name==syn_name, Syndrome.syn_id!=syn_id).first():
            return {'code': -1, 'message': '同名'}
        syndrome.syn_name = syn_name
        syndrome.abbr = abbr
        syndrome.std_id = syndrome.query.filter_by(
            syn_name=std_name.split(',')[0]).first().syn_id if std_name != syn_name else 0
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def delete_syndrome(syn_id):
    try:
        syndrome = Syndrome.query.filter_by(syn_id=syn_id).first()
        if not syndrome:
            return {'code': -1, 'message': '不存在'}
        db.session.delete(syndrome)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def add_raw_rcd(main_sym, add_sym, tongue, pulse, syndrome):
    try:
        rcd = RawRecord()
        rcd.main_sym = main_sym
        rcd.add_sym = add_sym
        rcd.tongue = tongue
        rcd.pulse = pulse
        rcd.syndrome = syndrome
        db.session.add(rcd)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


algo_dict = {'AdaBoost': 0, '随机森林': 1, 'CNN': 2, '谱聚类': 3}
algo_list = ['AdaBoost', '随机森林', 'CNN', '谱聚类']


def get_train_table(index):
    res = Train.query.order_by(desc(Train.train_id)).all()
    count = len(res)
    page_num = math.ceil(count / 10)
    data = []
    if page_num < index:
        return {}, count
    elif page_num == index:
        for i in res[index * 10 - 10:]:
            obj = {}
            obj['train_id'] = i.train_id
            obj['algo_name'] = algo_list[i.algo_id] if i.algo_id is not None else ''
            obj['para'] = i.para if i.para is not None else ''
            obj['indict'] = i.indict if i.indict is not None else ''
            obj['accu'] = i.accu if i.accu is not None else ''
            obj['time'] = str(i.time)[0:-3] if i.time is not None else ''
            data.append(obj)
        return data, count
    else:
        for i in res[index * 10 - 10: index * 10]:
            obj = {}
            obj['train_id'] = i.train_id
            obj['algo_name'] = algo_list[i.algo_id] if i.algo_id is not None else ''
            obj['para'] = i.para if i.para is not None else ''
            obj['indict'] = i.indict if i.indict is not None else ''
            obj['accu'] = i.accu if i.accu is not None else ''
            obj['time'] = str(i.time)[0:-3] if i.time is not None else ''
            data.append(obj)
        return data, count


def add_train(algo_name, para, indict, accu, time):
    try:
        train = Train()
        train.algo_id = algo_dict[algo_name]
        train.para = para
        train.indict = indict
        train.accu = accu
        train.time = time
        db.session.add(train)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def update_train(train_id, algo_name, para, indict, accu, time):
    try:
        train = Train.query.filter_by(train_id=train_id).first()
        train.algo_id = algo_dict[algo_name]
        train.para = para
        train.indict = indict
        train.accu = accu
        train.time = time
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def delete_train(train_id):
    try:
        train = Train.query.filter_by(train_id=train_id).first()
        if not train:
            return {'code': -1, 'message': '不存在'}
        db.session.delete(train)
        db.session.commit()
        return {'code': 1}
    except Exception as e:
        print(e)
        return {'code': -1, 'message': '异常'}


def get_accu():
    AdaBoost = Train.query.filter_by(algo_id=0).order_by(Train.time).all()
    RandomForest = Train.query.filter_by(algo_id=1).order_by(Train.time).all()
    CNN = Train.query.filter_by(algo_id=2).order_by(Train.time).all()
    SpectralClustering = Train.query.filter_by(algo_id=3).order_by(Train.time).all()
    time = [str(i.time)[0:-3] for i in AdaBoost]
    ab_accu = [i.accu for i in AdaBoost]
    rf_accu = [i.accu for i in RandomForest]
    cnn_accu = [i.accu for i in CNN]
    sp_accu = [i.accu for i in SpectralClustering]
    return [time, str(ab_accu), str(rf_accu), str(cnn_accu), str(sp_accu)]


def get_indict():
    AdaBoost = Train.query.filter_by(algo_id=0).order_by(Train.time).all()
    RandomForest = Train.query.filter_by(algo_id=1).order_by(Train.time).all()
    CNN = Train.query.filter_by(algo_id=2).order_by(Train.time).all()
    SpectralClustering = Train.query.filter_by(algo_id=3).order_by(Train.time).all()
    ab = [[j for j in json.loads(i.indict).values()] for i in AdaBoost]
    rf = [[j for j in json.loads(i.indict).values()] for i in RandomForest]
    cnn = [[j for j in json.loads(i.indict).values()] for i in CNN]
    sp = [[j for j in json.loads(i.indict).values()] for i in SpectralClustering]
    return [str(ab), str(rf), str(cnn), str(sp)]


def get_data():
    legend = []
    series = []
    select = {}
    bar_data = [['score', 'num', 'name']]
    sym = Symptom.query.order_by(desc(Symptom.num)).limit(10).all()
    ton = Tongue.query.order_by(desc(Tongue.num)).limit(10).all()
    pul = Pulse.query.order_by(desc(Pulse.num)).limit(10).all()
    syn = Syndrome.query.order_by(desc(Syndrome.num)).limit(10).all()
    for i in sym:
        legend.append(i.sym_name)
        series.append({'name': i.sym_name, 'value': i.num})
        select[i.sym_name] = True if i.num > 1000 else False
        if i.num > 100:
            bar_data.append([i.num, i.num, i.sym_name])
    for i in ton:
        legend.append(i.ton_name)
        series.append({'name': i.ton_name, 'value': i.num})
        select[i.ton_name] = True if i.num > 1000 else False
        if i.num > 100:
            bar_data.append([i.num, i.num, i.ton_name])
    for i in pul:
        legend.append(i.pul_name)
        series.append({'name': i.pul_name, 'value': i.num})
        select[i.pul_name] = True if i.num > 1000 else False
        if i.num > 100:
            bar_data.append([i.num, i.num, i.pul_name])
    for i in syn:
        legend.append(i.syn_name)
        series.append({'name': i.syn_name, 'value': i.num})
        select[i.syn_name] = True if i.num > 1000 else False
        if i.num > 100:
            bar_data.append([i.num, i.num, i.syn_name])
    pie_data = {'legend': legend, 'series': series, 'select':select}
    return {'pie_data': pie_data, 'bar_data': bar_data}
