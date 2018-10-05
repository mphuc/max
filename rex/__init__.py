from json import dumps
import json
from flask import Flask, send_from_directory, send_file, Blueprint, jsonify,session, request, redirect, url_for, render_template, json, flash, send_file
from flask.ext.login import login_required, LoginManager, current_user
from flask.ext.mongokit import MongoKit
from flask.templating import render_template
import os
import settings
from random import randint
from hashlib import sha256
import string
import random
from datetime import datetime
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO
import requests
import json
from flask_socketio import emit
from bson.objectid import ObjectId
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# from flask_recaptcha import ReCaptcha
__author__ = 'carlozamagni'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(settings)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO()
socketio.init_app(app)

db = MongoKit(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = '/auth/login'

from rex.controllers import user_controller
app.register_blueprint(blueprint=user_controller.user_ctrl, url_prefix='/user')

from rex.controllers import auth_controller
app.register_blueprint(blueprint=auth_controller.auth_ctrl, url_prefix='/auth')

from rex.controllers import dashboard_controller
app.register_blueprint(blueprint=dashboard_controller.dashboard_ctrl, url_prefix='/account')

from rex.controllers import ico_controller
app.register_blueprint(blueprint=ico_controller.ico_ctrl, url_prefix='/account')

from rex.controllers import deposit_controller
app.register_blueprint(blueprint=deposit_controller.deposit_ctrl, url_prefix='/account')

from rex.controllers import refferal_controller
app.register_blueprint(blueprint=refferal_controller.refferal_ctrl, url_prefix='/account')
from rex.controllers import support_controller
app.register_blueprint(blueprint=support_controller.support_ctrl, url_prefix='/account')

from rex.controllers import personal_controller
app.register_blueprint(blueprint=personal_controller.personal_ctrl, url_prefix='/account')

from rex.controllers import history_controller
app.register_blueprint(blueprint=history_controller.history_ctrl, url_prefix='/account')

from rex.controllers import withdrawal_controller
app.register_blueprint(blueprint=withdrawal_controller.withdrawal_ctrl, url_prefix='/account')

from rex.controllers import wallet_controller
app.register_blueprint(blueprint=wallet_controller.wallet_ctrl, url_prefix='/account')

from rex.controllers import auto_controller
app.register_blueprint(blueprint=auto_controller.auto_ctrl, url_prefix='/auto')

from rex.controllers import admin_controller
app.register_blueprint(blueprint=admin_controller.admin_ctrl, url_prefix='/admin')
from rex.controllers import admin
app.register_blueprint(blueprint=admin.admin1_ctrl, url_prefix='/admin')

@app.route('/testsendmail', methods = ['GET', 'POST'])
def downlqweroad():
    username = 'no-reply@smartfva.co'
    password = 'rbdlnsmxqpswyfdv'
    msg = MIMEMultipart('mixed')
    mailServer = smtplib.SMTP('smtp.gmail.com', 587) # 8025, 587 and 25 can also be used. 
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    sender = 'no-reply@smartfva.co'
    recipient = 'belindatbeach@gmail.com'

    msg['Subject'] = 'Congratulations. Your account is now active111!'
    msg['From'] = sender
    msg['To'] = recipient
    html = """\
    <div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center">
    <div class="adM">
    </div>
    <table style="table-layout:fixed;width:90%;max-width:600px;margin:0 auto;background-color:#f9f9f9">
    <tbody>
     <tr>
        <td style="padding:20px 10px 10px 0px;text-align:left">
           <a href="https://smartfva.co/" title="SmartFVA" target="_blank" >
           <img src="https://i.imgur.com/tyjTbng.png" alt="SmartFVA" class="CToWUd" style=" width: 100px; ">
           </a>
        </td>
        <td style="padding:0px 0px 0px 10px;text-align:right">
        </td>
     </tr>
    </tbody>
    </table>
    </div>
    <div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center">
    <table style="table-layout:fixed;width:90%;max-width:600px;margin:0 auto;background:#fff;font-size:14px;border:2px solid #e8e8e8;text-align:left;table-layout:fixed">
    <tbody>
     <tr>
        <td style="padding:10px 30px;line-height:1.8">Congratulations, Your account on the <a href="https://smartfva.co/" target="_blank">SmartFVA</a> is now registered and active.</td>
     </tr>
     <tr>
        <td style="border-bottom:3px solid #efefef;width:90%;display:block;margin:0 auto;padding-top:30px"></td>
     </tr>
     <tr>
        <td style="padding:30px 30px 30px 30px;line-height:1.3">Best regards,<br> SmartFVA Team<br>  <a href="https://www.smartfva.co/" target="_blank" >www.smartfva.co</a></td>
     </tr>
    </tbody>
    </table>
    </div>
    <div style="font-family:Arial,sans-serif;background-color:#f9f9f9;color:#424242;text-align:center;padding-bottom:10px;     height: 50px;">

    </div>
    """
    html_message = MIMEText(html, 'html')

    msg.attach(html_message)
    mailServer.sendmail(sender, recipient, msg.as_string())
    mailServer.close()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/whitepaper.pdf', methods = ['GET', 'POST'])
def download():
    return send_from_directory(os.path.join(app.root_path, 'static/uploads'), 'whitepaper.pdf', as_attachment=False, attachment_filename=None)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')
# @app.route("/robots.txt")
# def robots_txt():
#     print 11111111111111111111111111
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')
@app.route('/api/update-price') 
def function():
    

    url = 'https://min-api.cryptocompare.com/data/price?fsym=USD&tsyms=BTC,ETH,LTC,BCH'
    r = requests.get(url)
    response_dict = r.json()

     
    data_ticker = db.tickers.find_one({})
    data_ticker['btc_usd'] = round(1/float(response_dict['BTC']),2)
    data_ticker['bch_usd'] = round(1/float(response_dict['BCH']),2)
    data_ticker['ltc_usd'] = round(1/float(response_dict['LTC']),2)
    data_ticker['eth_usd'] = round(1/float(response_dict['ETH']),2)
   
    db.tickers.save(data_ticker)
    return json.dumps({'status': 'success'})


@app.route('/getInfo')
def getInfo(): # date = datetime object.
    
    return ''


@app.route('/info-ico', methods=['GET', 'POST'])
def countIco():
    ico = db.icosums.find_one({})
    percent = ico['percent']
    percent = float(percent)/1000000
    percent = float(percent)*100
    data = {
        'percent': round(percent, 2)
    }
    return json.dumps(data)

@app.template_filter()
def format_int(value): # date = datetime object.
    return int(value)

@app.template_filter()
def format_date(date): # date = datetime object.
    return date.strftime('%Y-%m-%d %H:%M:%S')
@app.template_filter()
def format_only_date(date): # date = datetime object.
    return date.strftime('%Y-%m-%d')
@app.template_filter()
def find_username(uid): # date = datetime object.
    if uid:
        uid = uid
    else:
        uid ='1111111'
    user = db.User.find_one({'customer_id': uid})
    if user is None:
        return ''
    else:
        return user.username

@app.template_filter()
def find_user_usd(uid): # date = datetime object.
    if uid:
        uid = str(uid)
    else:
        uid ='1111111'
    user = db.users.find_one({'_id': ObjectId(uid)})
    if user is None:
        return ''
    else:
        return user['usd_balance']

@app.template_filter()
def find_user_sva(uid): # date = datetime object.
    if uid:
        uid = uid
    else:
        uid ='1111111'
    user = db.users.find_one({'_id': ObjectId(uid)})
    if user is None:
        return ''
    else:
        return user['sva_balance']

@app.template_filter()
def to_string(value):
    
    return str(value)
@app.template_filter()
def number_format(value, tsep=',', dsep='.'):
    s = unicode(value)
    cnt = 0
    numchars = dsep + '0123456789'
    ls = len(s)
    while cnt < ls and s[cnt] not in numchars:
        cnt += 1

    lhs = s[:cnt]
    s = s[cnt:]
    if not dsep:
        cnt = -1
    else:
        cnt = s.rfind(dsep)
    if cnt > 0:
        rhs = dsep + s[cnt+1:]
        s = s[:cnt]
    else:
        rhs = ''

    splt = ''
    while s != '':
        splt = s[-3:] + tsep + splt
        s = s[:-3]

    return lhs + splt[:-1] + rhs
@app.template_filter()
def format_round(value):
    value = float(value)
    return '{:20,.8f}'.format(value)
@app.template_filter()
def format_usd(value):
    value = float(value)
    return '{:20,.2f}'.format(value)

@app.template_filter()
def format_satoshi(value):
    value = float(value)
    return '{:.8f}'.format(value)

@app.template_filter()
def format_btc_usd(value):
    data_ticker = db.tickers.find_one({})
    btc_usd = data_ticker['btc_usd']
    value = float(value)*float(btc_usd)
    return '{:20,.2f}'.format(value)

@app.template_filter()
def format_xvg_usd(value):
    data_ticker = db.tickers.find_one({})
    xvg_usd = data_ticker['xvg_usd']
    value = float(value)*0.8
    return '{:20,.2f}'.format(value)


@app.template_filter()
def format_usds(value):
    value = float(value)
    return '{:20,.0f}'.format(value)

@app.template_filter()
def format_html(html):
    return html



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def set_password(password):
    return generate_password_hash(password)
@app.route('/setup')
def setup():
    inserted = []
    #return json.dumps({'status' : 'error'})
    profit = [{"_id" : "5995a569587b3b15a14174e0",
        '500': 0.1,
        '1000':  0.2,
        '3000' : 0.3,
        '5000' : 0.4,
        '10000' : 0.5,
        '30000' : 0.6,
        '50000': 0.7,
        '100000':  0.8,
        '500000' : 0.9,
        '1000000' : 1
    }]
    db['profits'].drop()
    db['profits'].insert(profit)
    
    # users = [{"_id" : "5995a569587b3b15a14174e0",
    # "roi" : 100920,
    # "right" : "",
    # "p_binary" : "",
    # "m_wallet" : 600000000,
    # "creation" : datetime.utcnow(),
    # "telephone" : "000000000",
    # "password_transaction" : set_password('12345'),
    # "total_amount_right" : int("0"),
    # "total_pd_right" : int("0"),
    # "btc_wallet" : "19WpQavvcEcy4MmWk7szPoiY2cwvi8jt9E",
    # "p_node" : "",
    # "r_wallet" : 600000000,
    # "password_custom" : set_password('12345'),
    # "total_pd_left" : 9700,
    # "customer_id" : "1010101001",
    # "email" : "meccafunds@meccafund.org",
    # "total_amount_left" : 10500,
    # "username" : "root",
    # "s_wallet" : 1000000000,
    # "total_invest" : 100000,
    # "password" : set_password('12345'),
    # "img_profile" : "",
    # "max_out" : 500000,
    # "max_binary" : 500000,
    # "name" : "MECCAFUND",
    # "level" : int("3"),
    # "country" : "French Southern territories",
    # "wallet" : "",
    # "status" : 1,
    # "total_earn" : 10000,
    # "position" : "",
    # 'sva_balance': 0,
    # 'sva_address': '',
    # 'btc_balance': 0,
    # 'btc_address': '',
    # 'usd_balance': 0,
    # 'total_max_out': 0,
    # 'total_capital_back': 0,
    # 'total_commission': 0,
    # 'secret_2fa':'',
    # 'status_2fa': 0,
    # "left" : "",
    # 's_left': 0,
    # 's_right': 0,
    # 's_p_node': 0,
    # 's_p_binary': 0,
    # 's_token': 0,
    # 's_id': 0
    # }]
    # db['users'].drop()
    # db['users'].insert(users)
    # inserted.append(users)

    # admin = [{
    #     "_id" : "1175a9437u2b3b15a14174e0",
    #     'username':  'admin',
    #     'email' :  'admin@admin.com',
    #     'password': set_password('12345'),
    #     'sum_withdraw': 0,
    #     'sum_invest' : 0
    # }]
    # db['admins'].drop()
    # db['admins'].insert(admin)
    # inserted.append(admin)

    # ticker = [{
    #     'btc_usd' : 7500,
    #     'sva_btc' : 0.00013333,
    #     'sva_usd' : 1
    # }]
    # db['tickers'].drop()
    # db['tickers'].insert(ticker)

    return json.dumps(inserted)
   


@app.route('/')
def home_page():
    data ={
    'menu' : 'home'
    }
    return render_template('home/index.html', data=data)

@app.route('/stock-index')
def stock_index():
    data ={
    'menu' : 'stock-index'
    }
    return render_template('home/stock_index.html', data=data)

@app.route('/product')
def home_product():
    data ={
    'menu' : 'product'
    }
    return render_template('home/product.html', data=data)

@app.route('/product/foreign-exchange')
def home_foreign_exchange():
    data ={
    'menu' : 'foreign-exchange'
    }
    return render_template('home/foreign_exchange.html', data=data)

@app.route('/product/trading-rule')
def home_trading_rule():
    data ={
    'menu' : 'trading-rule'
    }
    return render_template('home/trading_rule.html', data=data)

@app.route('/platform')
def home_platform():
    data ={
    'menu' : 'platform'
    }
    return render_template('home/platform.html', data=data)

@app.route('/client-area')
def home_client_area():
    data ={
    'menu' : 'client-area'
    }
    return render_template('home/client_area.html', data=data)

@app.route('/contact-us')
def home_contact_us():
    data ={
    'menu' : 'contact-us'
    }
    return render_template('home/contact_us.html', data=data)

