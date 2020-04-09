from flask import request, redirect, abort, render_template, url_for, session, current_app, g, jsonify, make_response
from flask_login import login_user, logout_user
from app.algo.cnn import prediction as cp
from app.algo.SpectralClistering import prediction as sp
from app.algo.random_forest import prediction as rp
from app.algo.adaboost import prediction as ap
import app.handlers as handler


def login():
    token_type = 1
    if request.method == 'POST':
        result = handler.confirmPassword(request.form['username'], request.form['password'])
        if result is False:
            return render_template("login.html")
        else:
            login_user(result)
            g.user = result
            life_time = current_app.config.get("PERMANENT_SESSION_LIFETIME")
            token = result.get_id(life_time)
            handler.save_token(token_type, result.user_id, token, life_time)
            session["username"] = result.user_name
            session.permanent = True
            return redirect(url_for("home", token=token))
    else:
        return render_template("login.html")


def home():
    res = {"username": session["username"]}
    return render_template("index.html", res=res)


def logout():
    if session["user_id"] is not None:
        handler.expire_token(session["user_id"])
    logout_user()
    return render_template("login.html")


def filter():
    data = request.get_json('data')
    return jsonify(handler.filter(data))


def show_clean_content():
    if request.method == 'GET':
        res = handler.get_clean_table({'index': 1})
        return render_template('content/clean_content.html', res=res['res'], count=res['count'], index=res['index'])
    else:
        res = handler.get_clean_table(request.get_json('data'))
        return render_template('table/clean_table.html', res=res['res'], count=res['count'], index=res['index'])


def update_clean():
    data = request.get_json('data')
    return jsonify(handler.update_clean(data))


def delete_clean():
    data = request.get_json('data')
    return jsonify(handler.delete_clean(data))


def show_pulse_content():
    if request.method == 'GET':
        res = handler.get_pulse_table({'index': 1})
        return render_template('content/pulse_content.html', res=res['res'], count=res['count'], index=res['index'])
    else:
        res = handler.get_pulse_table(request.get_json('data'))
        return render_template('table/pulse_table.html', res=res['res'], count=res['count'], index=res['index'])


def search_pulse():
    data = request.get_json('data')
    return jsonify(handler.search_pulse(data))


def add_pulse():
    data = request.get_json('data')
    return jsonify(handler.add_pulse(data))


def update_pulse():
    data = request.get_json('data')
    return jsonify(handler.update_pulse(data))


def delete_pulse():
    data = request.get_json('data')
    return jsonify(handler.delete_pulse(data))


def show_tongue_content():
    if request.method == 'GET':
        res = handler.get_tongue_table({'index': 1})
        return render_template('content/tongue_content.html', res=res['res'], count=res['count'], index=res['index'])
    else:
        res = handler.get_tongue_table(request.get_json('data'))
        return render_template('table/tongue_table.html', res=res['res'], count=res['count'], index=res['index'])


def search_tongue():
    data = request.get_json('data')
    return jsonify(handler.search_tongue(data))


def add_tongue():
    data = request.get_json('data')
    return jsonify(handler.add_tongue(data))


def update_tongue():
    data = request.get_json('data')
    return jsonify(handler.update_tongue(data))


def delete_tongue():
    data = request.get_json('data')
    return jsonify(handler.delete_tongue(data))


def show_symptom_content():
    if request.method == 'GET':
        res = handler.get_symptom_table({'index': 1})
        return render_template('content/symptom_content.html', res=res['res'], count=res['count'], index=res['index'])
    else:
        res = handler.get_symptom_table(request.get_json('data'))
        return render_template('table/symptom_table.html', res=res['res'], count=res['count'], index=res['index'])


def search_symptom():
    data = request.get_json('data')
    return jsonify(handler.search_symptom(data))


def add_symptom():
    data = request.get_json('data')
    return jsonify(handler.add_symptom(data))


def update_symptom():
    data = request.get_json('data')
    return jsonify(handler.update_symptom(data))


def delete_symptom():
    data = request.get_json('data')
    return jsonify(handler.delete_symptom(data))


def show_syndrome_content():
    if request.method == 'GET':
        res = handler.get_syndrome_table({'index': 1})
        return render_template('content/syndrome_content.html', res=res['res'], count=res['count'], index=res['index'])
    else:
        res = handler.get_syndrome_table(request.get_json('data'))
        return render_template('table/syndrome_table.html', res=res['res'], count=res['count'], index=res['index'])


def search_syndrome():
    data = request.get_json('data')
    return jsonify(handler.search_syndrome(data))


def add_syndrome():
    data = request.get_json('data')
    return jsonify(handler.add_syndrome(data))


def update_syndrome():
    data = request.get_json('data')
    return jsonify(handler.update_syndrome(data))


def delete_syndrome():
    data = request.get_json('data')
    return jsonify(handler.delete_syndrome(data))


def show_input_content():
    return render_template('content/input_content.html')


def form_upload():
    return jsonify(handler.add_form_rcd(request.get_json('data')))


def text_upload():
    return jsonify(handler.add_text_rcd(request.get_json('data')))


def excel_upload():
    file = request.files.to_dict()
    data = request.form.to_dict()
    return jsonify(handler.add_excel_rcd(data, file))


def database_upload():
    return jsonify(handler.add_database_rcd(request.get_json('data')))


def show_diagnose_content():
    if request.method == 'GET':
        res = handler.get_clean_table({'index': 1})
        return render_template('content/diagnose_content.html', res=res['res'], count=res['count'], index=res['index'])
    else:
        res = handler.get_clean_table(request.get_json('data'))
        return render_template('table/diagnose_table.html', res=res['res'], count=res['count'], index=res['index'])


def show_result_content():
    return render_template('content/result_content.html')


def show_algorithm_content():
    res = handler.get_indict()
    return render_template('content/algorithm_content.html', ab=res[0], rf=res[1], cnn=res[2], sp=res[3])


def show_display_content():
    res = handler.get_accu()
    return render_template('content/display_content.html', time=res[0], ab=res[1], rf=res[2], cnn=res[3], sp=res[4])


def show_train_content():
    if request.method == 'GET':
        res = handler.get_train_table({'index': 1})
        return render_template('content/train_content.html', res=res['res'], count=res['count'], index=res['index'])
    else:
        res = handler.get_train_table(request.get_json('data'))
        return render_template('table/train_table.html', res=res['res'], count=res['count'], index=res['index'])


def add_train():
    data = request.get_json('data')
    return jsonify(handler.add_train(data))


def update_train():
    data = request.get_json('data')
    return jsonify(handler.update_train(data))


def delete_train():
    data = request.get_json('data')
    return jsonify(handler.delete_train(data))


def get_graph():
    return render_template('graph.gexf')


def get_data():
    return jsonify(handler.get_data())

def predict():
    data = request.get_json('data')
    res = []
    res.append(ap(data['main_sym'], data['add_sym'], data['ton'], data['pul']))
    res.append(rp(data['main_sym'], data['add_sym'], data['ton'], data['pul']))
    res.append(cp(data['main_sym'], data['add_sym'], data['ton'], data['pul']))
    res.append(sp(data['main_sym'], data['add_sym'], data['ton'], data['pul']))
    return jsonify(res)