from flask import current_app
from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Token(db.Model, UserMixin):
    # 表的名字:
    __tablename__ = 'token'

    # 表的结构:
    token_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer)
    created_on = db.Column(db.DateTime)
    token_type = db.Column(db.Integer)
    expired_on = db.Column(db.DateTime)


class User(db.Model, UserMixin):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255))
    user_name = db.Column(db.String(20))


    def verify_password(self, password):
        return check_password_hash(generate_password_hash(self.password), password)

    def get_id(self, life_time=None):
        if not life_time:
            life_time = current_app.config.get("PERMANENT_SESSION_LIFETIME")
        # browser_id = create_browser_id() # 浏览器检查
        s = Serializer(current_app.config.get("SECRET_KEY", "beornut@gmail.com"), expires_in=life_time)
        token = s.dumps({'user_id': self.user_id})
        return token.decode("utf-8")

class Diagnose(db.Model, UserMixin):
    __tablename__ = 'diagnose'

    rcd_id = db.Column(db.Integer, primary_key=True, nullable=False)
    train_id = db.Column(db.Integer, primary_key=True, nullable=False)
    syn = db.Column(db.String(255), nullable=False)


class Pulse(db.Model, UserMixin):
    __tablename__ = 'pulse'

    pul_id = db.Column(db.Integer, primary_key=True)
    pul_name = db.Column(db.String(255), nullable=False)
    abbr = db.Column(db.String(255), nullable=False)
    std_id = db.Column(db.Integer, nullable=False)
    num = db.Column(db.Integer, nullable=True)


class RawRecord(db.Model, UserMixin):
    __tablename__ = 'raw_record'

    rcd_id = db.Column(db.Integer, primary_key=True)
    main_sym = db.Column(db.String(255))
    add_sym = db.Column(db.String(255))
    tongue = db.Column(db.String(255))
    pulse = db.Column(db.String(255))
    syndrome = db.Column(db.String(255))


class StdRecord(db.Model, UserMixin):
    __tablename__ = 'std_record'

    rcd_id = db.Column(db.Integer, primary_key=True)
    main_sym = db.Column(db.String(255))
    add_sym = db.Column(db.String(255))
    tongue = db.Column(db.String(255))
    pulse = db.Column(db.String(255))
    syndrome = db.Column(db.String(255))



class Symptom(db.Model, UserMixin):
    __tablename__ = 'symptom'

    sym_id = db.Column(db.Integer, primary_key=True)
    sym_name = db.Column(db.String(255), nullable=False)
    abbr = db.Column(db.String(255), nullable=False)
    std_id = db.Column(db.Integer, nullable=False)
    num = db.Column(db.Integer, nullable=True)


class Syndrome(db.Model, UserMixin):
    __tablename__ = 'syndrome'

    syn_id = db.Column(db.Integer, primary_key=True)
    syn_name = db.Column(db.String(255), nullable=False)
    abbr = db.Column(db.String(255), nullable=False)
    std_id = db.Column(db.Integer, nullable=False)
    num = db.Column(db.Integer, nullable=True)


class Tongue(db.Model, UserMixin):
    __tablename__ = 'tongue'

    ton_id = db.Column(db.Integer, primary_key=True)
    ton_name = db.Column(db.String(255), nullable=False)
    abbr = db.Column(db.String(255), nullable=False)
    std_id = db.Column(db.Integer, nullable=False)
    num = db.Column(db.Integer, nullable=True)


class Train(db.Model, UserMixin):
    __tablename__ = 'train'

    train_id = db.Column(db.Integer, primary_key=True)
    algo_id = db.Column(db.Integer, nullable=False)
    para = db.Column(db.String(255))
    indict = db.Column(db.String(255))
    accu = db.Column(db.Float)
    path = db.Column(db.String(255))
    time = db.Column(db.DateTime)
