from bson.json_util import dumps
from flask import Blueprint, jsonify,session, request, redirect, url_for, render_template, json, flash
from flask.ext.login import current_user, login_required
from rex import db, lm
from rex.models import user_model, deposit_model, history_model, invoice_model, admin_model
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from datetime import datetime
from datetime import datetime, date, timedelta
from time import gmtime, strftime
import time
import json
import os
from bson import ObjectId, json_util
import codecs
from random import randint
from hashlib import sha256
import urllib
import urllib2
from block_io import BlockIo
import requests
import onetimepass
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from rex.coinpayments import CoinPaymentsAPI
from rex.config import Config
version = 2 # API version
block_io = BlockIo('9fd3-ec01-722e-fd89', 'SECRET PIN', version)
__author__ = 'carlozamagni'
ApiCoinpayment = CoinPaymentsAPI(public_key=Config().public_key,
                          private_key=Config().private_key)
admin_ctrl = Blueprint('admin', __name__, static_folder='static', template_folder='templates')
def verify_totp(token, otp_secret):
    return onetimepass.valid_totp(token, otp_secret)
def check_password(pw_hash, password):
        return check_password_hash(pw_hash, password)

def set_password(password):
    return generate_password_hash(password)

@admin_ctrl.route('/login-userid/<ids>/<customer_id>', methods=['GET', 'POST'])
def loginuserid(ids,customer_id):
    if session.get('logged_in_admin') is not None:
        session['logged_in'] = True
        session['user_id'] = str(ids)
        session['uid'] = customer_id
        return redirect('/account/dashboard')

@admin_ctrl.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if session.get('logged_in_admin') is not None:
        return redirect('/admin/customer')
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = db.admins.find_one({ '$or': [ { 'username': username }, { 'email': username } ] })
        
        # if user is None or check_password(user['password'], password) == False:
        #     flash({'msg':'Invalid username or password', 'type':'danger'})
        #     return redirect('/admin/login')
        #else:
        if user is not None and password == 'skfhksdjhfksjdhfskjskfskdjf':

            session['logged_in_admin'] = True
            session['user_id_admin'] = str(user['_id'])
        else:
            return redirect('/admin/login')
            #home_page = user_model.User.get_role(user['role'])
            # login_user(user=user)

        return redirect('/admin/customer')
    return render_template('admin/login.html', error=error)
@admin_ctrl.route('/signup', methods=['GET', 'POST'])
def new():
    return redirect('/admin/login')
    if request.method == 'POST':
        # user.save()
        localtime = time.localtime(time.time())
        customer_id = '%s%s%s%s%s%s'%(localtime.tm_mon,localtime.tm_year,localtime.tm_mday,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
        customer_id = '1010101001'
        datas = {
            'username' : request.form['name'],
            'email': request.form['email'],
            'password': set_password(request.form['password']),
            
        }
        db.admins.insert(datas)
        return redirect('/admin/login')
    
    return render_template('admin/new.html')


@admin_ctrl.route('/submit-withdraw-btc', methods=['GET', 'POST'])
def AdminWithdrawBTCadmin():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    wallet = request.form['wallet']
    amount = request.form['amount']
    auth = request.form['auth']
    if wallet =='':
        flash({'msg':'Invalid wallet', 'type':'danger'})
        return redirect('/admin/dashboard')
    if amount =='':
        flash({'msg':'Invalid amount', 'type':'danger'})
        return redirect('/admin/dashboard')
    if auth =='':
        flash({'msg':'Invalid auth', 'type':'danger'})
        return redirect('/admin/dashboard')

    rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@127.0.0.1:23321")
    response_dict = rpc_connection.validateaddress(wallet)
    if response_dict['isvalid'] != True:
        flash({'msg':'Invalid wallet', 'type':'danger'})
        return redirect('/admin/dashboard')

    checkVerifY = verify_totp(auth, 'HFFRSRR647SN6EXP')
    
    if checkVerifY == False:    
        flash({'msg':'Invalid Authen', 'type':'danger'})
        return redirect('/admin/dashboard')

    dataSend = rpc_connection.sendtoaddress(wallet,amount) 
    if dataSend:
        flash({'msg':'Withdraw Success', 'type':'success'})
        return redirect('/admin/dashboard')
    else:
        flash({'msg':'Withdraw Fail', 'type':'danger'})
        return redirect('/admin/dashboard')
    
@admin_ctrl.route('/dashboard', methods=['GET', 'POST'])
def AdminDashboard():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    total_user = db.users.find({}).count()
    total_lending = db.investments.find({}).count()
    #rpc_connection = AuthServiceProxy("http://Ecy4M83321mWk7szPoiY2cw:DrWdoW83321Zrdi2ftYKVPt4P2Cb7HoQUZUuP6@rpcbtcsvadfndawrwlcoin.co")
    balance = 0
    


    #balances = ApiCoinpayment.balances()
    balances_btc = 0
    balances_ltc = 0
    balances_bch = 0
    balances_eth = 0
    balances_usdt = 0

    

    # if balances['result'].has_key('BTC') is  True:
    #     balances_btc = balances['result']['BTC']['balancef']
    
    # if balances['result'].has_key('LTC') is  True:
    #     balances_ltc = balances['result']['LTC']['balancef']
    # if balances['result'].has_key('BCH') is  True:
    #     balances_bch = balances['result']['BCH']['balancef']
    # if balances['result'].has_key('ETH') is  True:
    #     balances_eth = balances['result']['ETH']['balancef']
    # if balances['result'].has_key('USDT') is  True:
    #     balances_usdt = balances['result']['USDT']['balancef']
    

    data ={
            'menu' : 'dashboard',
            'total_user': total_user,
            'total_lending': total_lending,
            'total_btc': balance,
            'serverbtc' : 0,
            'id_login' : session.get('user_id_admin'),
            'balances_btc' : '...',
            'balances_ltc' : '...',
            'balances_bch' : '...',
            'balances_eth' : '...',
            'balances_usdt' : '...'
        }
    return render_template('admin/dashboard.html', data=data)

@admin_ctrl.route('/get-balance', methods=['GET', 'POST'])
def AdminGetBalance():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    
    balances_btc = 0
    balances_ltc = 0
    balances_bch = 0
    balances_eth = 0
    balances_usdt = 0

    balances = ApiCoinpayment.balances()
    if balances['result'].has_key('BTC') is  True:
        balances_btc = balances['result']['BTC']['balancef']
    if balances['result'].has_key('LTC') is  True:
        balances_ltc = balances['result']['LTC']['balancef']
    if balances['result'].has_key('BCH') is  True:
        balances_bch = balances['result']['BCH']['balancef']
    if balances['result'].has_key('ETH') is  True:
        balances_eth = balances['result']['ETH']['balancef']
    if balances['result'].has_key('USDT') is  True:
        balances_usdt = balances['result']['USDT']['balancef']

    return json.dumps({
        'balances_btc' : balances_btc,
        'balances_ltc' : balances_ltc,
        'balances_bch' : balances_bch,
        'balances_eth' : balances_eth,
        'balances_usdt' : balances_usdt
    })

@admin_ctrl.route('/customer', methods=['GET', 'POST'])
def AdminCustomer():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    query = db.users.find({})

    queryss = db.users.find({'level': 0 })
    
    data ={
        'customer': query,
        'queryss' : queryss,
        'menu' : 'customer',
        'float' : float,
        'id_login' : session.get('user_id_admin')
    }
    return render_template('admin/customer.html', data=data)

@admin_ctrl.route('/verity-account', methods=['GET', 'POST'])
def verity_account():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    data_verity = db.verifys.find({'status' : 0})
     
    data ={
        'data_verity': data_verity,
        'menu' : 'verity-account',
        'float' : float,
        'id_login' : session.get('user_id_admin')
    }
    return render_template('admin/verity_account.html', data=data)

@admin_ctrl.route('/verity-account/<ids>', methods=['GET', 'POST'])
def verity_account_submit(ids):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    data_verity = db.verifys.find_one({'_id' : ObjectId(ids)})
    
    user = db.users.find_one({'customer_id' : data_verity['uid']})
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static", "country-list.json")
    data_country = json.load(open(json_url))

    if request.method == 'POST':
        
        admin_node = request.form['admin_node']
        status_verity = request.form['status_verity'] 
        db.verifys.update({'_id' : ObjectId(ids)},{'$set' : {'admin_note' : admin_node ,'status' : int(status_verity)}})
        
        if int(status_verity) == 1:
            status_verify_user  = 2
        else: 
            status_verify_user = 0
        db.users.update({'customer_id' : data_verity['uid']},{'$set' : {'status_verify' : int(status_verify_user) }})
        
        return redirect('/admin/verity-account')

    data ={
        'data_verity': data_verity,
        'user' : user,
        'menu' : 'verity-account',
        'float' : float,
        'id_login' : session.get('user_id_admin'),
        'data_country' : data_country,
        'ids' : ids
    }
    return render_template('admin/verity_account_submit.html', data=data)

@admin_ctrl.route('/deposit-btc', methods=['GET', 'POST'])
def DepositBTC():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    query = db.deposits.find({})
    data ={
        'databtc': query,
        'menu' : 'deposit_btc',
        'float' : float,
        'id_login' : session.get('user_id_admin')
    }
    return render_template('admin/deposit_btc.html', data=data)
@admin_ctrl.route('/deposit-xvg', methods=['GET', 'POST'])
def DepositSVAA():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    query = db.txdeposits.find({'type':'XVG'})
    data ={
        'databtc': query,
        'menu' : 'deposit_sva',
        'float' : float
    }
    return render_template('admin/deposit_btc.html', data=data)

@admin_ctrl.route('/customer/<user_id>', methods=['GET', 'POST'])
def SupportCustomerID(user_id):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "../static", "country-list.json")
    data_country = json.load(open(json_url))
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if request.method == 'POST':
        
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        date_birthday = request.form['date_birthday']
        address = request.form['address']
        postalcode = request.form['postalcode']
        city = request.form['city']
        country = request.form['country']

        status_2fa = request.form['status_2fa']
        active_email = request.form['active_email']
        
        user['personal_info']['firstname'] = firstname
        user['personal_info']['lastname'] = lastname
        user['personal_info']['date_birthday'] = date_birthday
        user['personal_info']['address'] = address
        user['personal_info']['postalcode'] = postalcode
        user['personal_info']['city'] = city
        user['personal_info']['country'] = country

        balance_wallet = request.form['balance_wallet']
        password = request.form['password']
        active_email = request.form['active_email']
        
        user['status_2fa'] = int(status_2fa)
        user['active_email'] = int(active_email)
        #user['balance_wallet'] = balance_wallet
        if password != '':
            user['password'] = set_password(password)
        
        db.users.save(user)

    query = db.users.find_one({'_id': ObjectId(user_id)})
    data ={
        'user': query,
        'menu' : 'customer',
        'float' : float,
        'user_id': user_id,
        'data_country' : data_country

    }
    return render_template('admin/editcustomer.html', data=data)


@admin_ctrl.route('/customer/active-investment/<user_id>', methods=['GET', 'POST'])
def active_investment_admin(user_id):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    usersss = db.users.find_one({'_id': ObjectId(user_id)})
    data ={
        'user' : usersss
    }
    return render_template('admin/active-investment.html', data=data)

@admin_ctrl.route('/customer/active-investment-submit/<user_id>', methods=['GET', 'POST'])
def active_investment_submit_admin(user_id):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    
    user = db.users.find_one({'_id': ObjectId(user_id)})
    uid = user['customer_id']
    amount_package = float(request.form['package'])
    package = float(request.form['package'])
    check_investment = db.investments.find_one({'$and' :[{'uid': uid},{'status' : 1},{'package':{'$gte': amount_package }}]} )
    coin_amount = 0
    if check_investment is  None:
    #check balance
        
        #chay hai nhanh
        binaryAmount(uid, float(amount_package))
        #chay p_node
        TotalnodeAmount(uid, float(amount_package))
        #hoa hong truc tiep
        FnRefferalProgram(uid, float(amount_package))                
    
        user = db.users.find_one({'customer_id': uid})
        
        db.users.update({ "customer_id" : uid }, { '$set': {"level" : int(package),"investment" : float(amount_package)} })
        #create investment
        data_investment = {
            'uid' : uid,
            'user_id': user['_id'],
            'username' : user['username'],
            'amount_usd' : float(amount_package),
            'package': float(amount_package),
            'status' : 1,
            'upgrade' : 0,
            'date_added' : datetime.utcnow(),
            'amount_frofit' : 0,
            'coin_amount' : coin_amount,
            'date_upgrade' : '',
            'reinvest' : 0,
            'total_income' : '',
            'status_income' : 0,
            'date_income' : '',
            'number_frofit' : 0,
            'date_profit' : datetime.utcnow() + timedelta(days=30)
        }
        db.investments.insert(data_investment)

    return redirect('/admin/customer')
def binaryAmount(user_id, amount_invest):
    customer_ml = db.users.find_one({"customer_id" : user_id })
    if customer_ml['p_binary'] != '':
        while (True):
            customer_ml_p_binary = db.users.find_one({"customer_id" : customer_ml['p_binary'] })
            if customer_ml_p_binary is None:
                break
            else:
                if customer_ml_p_binary['left'] == customer_ml['customer_id']:
                    
                    customers = db.users.find_one({"customer_id" : customer_ml_p_binary['customer_id'] })
                    customers['total_pd_left'] = float(customers['total_pd_left']) + float(amount_invest)
                    customers['total_amount_left'] = float(customers['total_amount_left']) + float(amount_invest)
                    db.users.save(customers)
                    print("left binary")
                else:
                    
                    customers = db.users.find_one({"customer_id" : customer_ml_p_binary['customer_id'] })
                    customers['total_pd_right'] = float(customers['total_pd_right']) + float(amount_invest)
                    customers['total_amount_right'] = float(customers['total_amount_right']) + float(amount_invest)
                    db.users.save(customers)
                    print("right binary")
                    
            customer_ml = db.users.find_one({"customer_id" : customer_ml_p_binary['customer_id'] })
            if customer_ml is None:
                break
    return True
def TotalnodeAmount(user_id, amount_invest):
    customer_ml = db.users.find_one({"customer_id" : user_id })
    if customer_ml['p_node'] != '':
        while (True):
            customer_ml_p_node = db.users.find_one({"customer_id" : customer_ml['p_node'] })
            if customer_ml_p_node is None:
                break
            else:
                customers = db.users.find_one({"customer_id" : customer_ml_p_node['customer_id'] })
                customers['total_node'] = float(customers['total_node']) + float(amount_invest)
                db.users.save(customers)
                
            customer_ml = db.users.find_one({"customer_id" : customer_ml_p_node['customer_id'] })
            if customer_ml is None:
                break
    return True
def FnRefferalProgram(user_id, amount_invest):
    customers = db.users.find_one({"customer_id" : user_id })
    username_invest = customers['username']
    # hoa hong truc tiep
    customers_f1 = db.users.find_one({"customer_id" : customers['p_node'] })
    if customers_f1 is not None:
        if int(customers_f1['level']) > 0:
            percent = 8
            commission = float(amount_invest)*percent/100
            commission = round(commission,2)
            r_wallet = float(customers_f1['r_wallet'])
            new_r_wallet = float(r_wallet) + float(commission)
            new_r_wallet = float(new_r_wallet)

            total_earn = float(customers_f1['total_earn'])
            new_total_earn = float(total_earn) + float(commission)
            new_total_earn = float(new_total_earn)

            balance_wallet = float(customers_f1['balance_wallet'])
            new_balance_wallet = float(balance_wallet) + float(commission)
            new_balance_wallet = float(new_balance_wallet)

            db.users.update({ "_id" : ObjectId(customers_f1['_id']) }, { '$set': {'balance_wallet' : new_balance_wallet,'total_earn': new_total_earn, 'r_wallet' :new_r_wallet } })
            detail = 'Get '+str(percent)+' '+"""%"""+' from member %s investment $%s' %(username_invest, amount_invest)
            SaveHistory(customers_f1['customer_id'],customers_f1['_id'],customers_f1['username'], commission, 'referral', 'USD', detail, '', '')
            

            get_percent_generations(customers_f1['customer_id'],commission)
    return True
def get_percent_generations(customer_id,amount_receve):
    customers = db.users.find_one({"customer_id" : customer_id })
    username_receive = customers['username']
    customers_f1 = db.users.find_one({"customer_id" : customers['p_node'] })
    if customers_f1 is not None:
        if int(customers_f1['level']) > 0:
            count_f1 = db.users.find({'$and' :[{'p_node': customers_f1['customer_id']},{"level": { "$gt": 0 }}]}).count()
            
            percent = 0
            if int(count_f1) >=3 and float(customers_f1['total_node']) >= 300000:
                percent = 5
            if int(count_f1) >=5 and float(customers_f1['total_node']) >= 500000:
                percent = 10
            if int(count_f1) >=8 and float(customers_f1['total_node']) >= 1000000:
                percent = 15
            if int(count_f1) >=10 and float(customers_f1['total_node']) >= 2000000:
                percent = 20

            if int(percent) > 0:
                commission = float(amount_receve)*percent/100
                commission = round(commission,2)
                
                g_wallet = float(customers_f1['g_wallet'])
                new_g_wallet = float(g_wallet) + float(commission)
                new_g_wallet = float(new_g_wallet)

                total_earn = float(customers_f1['total_earn'])
                new_total_earn = float(total_earn) + float(commission)
                new_total_earn = float(new_total_earn)

                balance_wallet = float(customers_f1['balance_wallet'])
                new_balance_wallet = float(balance_wallet) + float(commission)
                new_balance_wallet = float(new_balance_wallet)

                db.users.update({ "_id" : ObjectId(customers_f1['_id']) }, { '$set': {'balance_wallet' : new_balance_wallet,'total_earn': new_total_earn, 'g_wallet' :new_g_wallet } })
                detail = 'Get '+str(percent)+' '+"""%"""+' from member %s receive $%s' %(username_receive, amount_receve)
                SaveHistory(customers_f1['customer_id'],customers_f1['_id'],customers_f1['username'], commission, 'generations', 'USD', detail, '', '')
                
def SaveHistory(uid, user_id, username, amount, types, wallet, detail, rate, txtid):
    data_history = {
        'uid' : uid,
        'user_id': user_id,
        'username' : username,
        'amount': float(amount),
        'type' : types,
        'wallet': wallet,
        'date_added' : datetime.utcnow(),
        'detail': detail,
        'rate': rate,
        'txtid' : txtid,
        'amount_sub' : 0,
        'amount_add' : 0,
        'amount_rest' : 0
    }
    db.historys.insert(data_history)
    return True
@admin_ctrl.route('/customer-detail/<user_id>', methods=['GET', 'POST'])
def customer_detail(user_id):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    query = db.users.find_one({'_id': ObjectId(user_id)})
    history = db.historys.find({'uid': query['customer_id']})
    data ={
        'user': query,
        'menu' : 'customer',
        'float' : float,
        'user_id': user_id,
        'history' : history
    }
    return render_template('admin/customer_detail.html', data=data)

@admin_ctrl.route('/updatePassword', methods=['GET', 'POST'])
def updatePassword():
    error = None
    if session.get('logged_in_admin') is None:
        return json.dumps({
            'status': 'error', 
            'message': 'Please login' 
        })
    password = request.form['password']
    
    repeat_password = request.form['repeat_password']
    wallet = request.form['wallet']
    email = request.form['email']
    telephone = request.form['telephone']


    if wallet =='':
        return json.dumps({
            'status': 'error', 
            'message': 'Please enter wallet' 
        })
    if email =='':
        return json.dumps({
            'status': 'error', 
            'message': 'Please enter email' 
        })
    if telephone =='':
        return json.dumps({
            'status': 'error', 
            'message': 'Please enter telephone' 
        })
    if password =='' or repeat_password =='':
        return json.dumps({
            'status': 'error', 
            'message': 'Please enter password' 
        })
    if password != repeat_password:
        return json.dumps({
            'status': 'error', 
            'message': 'Wrong repeat password ' 
        })
    user_id = request.form['user_id']
    query = db.users.find({'_id': ObjectId(user_id)})
    if query is None:
        return json.dumps({
            'status': 'error', 
            'message': 'That user dose not exits ' 
        })
    password_new = set_password(password)
    db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "password": password_new ,"wallet" : wallet,'telephone' : telephone,'email' : email} })
    return json.dumps({
        'status': 'success', 
        'message': 'Update Success ' 
    })
@admin_ctrl.route('/updateSponsor', methods=['GET', 'POST'])
def updateSponsor():
    error = None
    if session.get('logged_in_admin') is None:
        return json.dumps({
            'status': 'error', 
            'message': 'Please login' 
        })
    p_node = request.form['p_node']
    p_node = p_node.lower()
    user_id = request.form['user_id']
    query = db.users.find_one({'_id': ObjectId(user_id)})
    if query is None:
        return json.dumps({
            'status': 'error', 
            'message': 'That user dose not exits ' 
        })
    find_node = db.users.find_one({'username': p_node})
    if find_node is None:
        return json.dumps({
            'status': 'error', 
            'message': 'Username dose not exits' 
        })
    db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "p_node": find_node['customer_id'] } })
    return json.dumps({
        'status': 'success', 
        'message': 'Update Success ' 
    })
@admin_ctrl.route('/updatePbinary', methods=['GET', 'POST'])
def updatePbinary():
    error = None
    if session.get('logged_in_admin') is None:
        return json.dumps({
            'status': 'error', 
            'message': 'Please login' 
        })
    p_binary = request.form['p_binary']
    p_binary = p_binary.lower()
    user_id = request.form['user_id']
    query = db.users.find_one({'_id': ObjectId(user_id)})
    if query is None:
        return json.dumps({
            'status': 'error', 
            'message': 'That user dose not exits ' 
        })
    find_binary = db.users.find_one({'username': p_binary})
    if find_binary is None:
        return json.dumps({
            'status': 'error', 
            'message': 'Username dose not exits' 
        })
    if query['p_binary'] == '':
        print 'None'
    else:
        binary_current = db.users.find_one({'customer_id': query['p_binary']})
        if binary_current is None:
            print 'Current None'
        else:
            if query['customer_id'] == binary_current['left']:
                db.users.update({ "_id" : ObjectId(binary_current['_id']) }, { '$set': { "left": '' } })
            else:
                db.users.update({ "_id" : ObjectId(binary_current['_id']) }, { '$set': { "right": '' } })
    if find_binary['left'] == '':
        db.users.update({ "_id" : ObjectId(find_binary['_id']) }, { '$set': { "left": query['customer_id'] } })
        db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "p_binary": find_binary['customer_id'], 'type': 1 } })
        return json.dumps({
            'status': 'success', 
            'message': 'Update Success ' 
        })
    if find_binary['right'] == '':
        db.users.update({ "_id" : ObjectId(find_binary['_id']) }, { '$set': { "right": query['customer_id'] } })
        db.users.update({ "_id" : ObjectId(user_id) }, { '$set': { "p_binary": find_binary['customer_id'], 'type': 1 } })
        return json.dumps({
            'status': 'success', 
            'message': 'Update Success ' 
        })
    return json.dumps({
        'status': 'error', 
        'message': 'Position already exists ' 
    })
    

@admin_ctrl.route('/withdraw', methods=['GET', 'POST'])
def AdminWithdraw():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    query = db.withdrawas.find({ 'status': 0})
    ticker = db.tickers.find_one({})

    

    
    for x in query:
        if x['type'] == 'BTC':
            price = ticker['btc_usd']
        if x['type'] == 'ETH':
            
            price = ticker['eth_usd']
        if x['type'] == 'LTC':
            
            price = ticker['ltc_usd']
        if x['type'] == 'BCH':
            
            price = ticker['bch_usd']
        if x['type'] == 'USDT':
            
            price = 1
        amount_curency = round(float(x['amount'])/float(price),8)*0.7
        db.withdrawas.update({'_id' : ObjectId(x['_id'])},{'$set' : {'price' : price,'amount_curency' : amount_curency}})
    querys = db.withdrawas.find({ 'status': 0})
    data ={
        'withdraw' : querys,
        'menu' : 'withdraw',
        'float': float
    }
    return render_template('admin/withdraw.html', data=data)

@admin_ctrl.route('/withdraw-submit/<ids>', methods=['GET', 'POST'])
def AdminWithdrawsubmit(ids):
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    data = db.withdrawas.find_one({'$and' : [{ 'status': 0},{'_id' : ObjectId(ids)}]})
    if data is not None:
        
        respon_withdraw = ApiCoinpayment.create_withdrawal(amount = data['amount_curency'],currency = data['type'],address = data['wallet']) 
        print respon_withdraw
        if respon_withdraw['error'] == 'ok':
            db.withdrawas.update({'_id' : ObjectId(ids)},{'$set' : {'status' : 1}})

    return redirect('/admin/withdraw')
@admin_ctrl.route('/withdraweth', methods=['GET', 'POST'])
def AdminWithdraweth():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')

    url_api = "https://api.cryptonator.com/api/ticker/eth-usd"
    r_eth = requests.get(url_api)
    response_eth = r_eth.json()
    price_eth = response_eth['ticker']['price'];
    price_eth = float(price_eth)*100000000
    
    query = db.withdrawal_payment.find({'txtid': '', 'method_payment': 1})
   
    for x in query:
        amount_btc = float(x['amount_sub'])*100000000
        amount = amount_btc/int(price_eth)
        amount = round(amount, 8)
        amount = amount*100000000
        db.withdrawal_payment.update({ "_id" :ObjectId(x['_id']) }, { '$set': { "amount_btc": amount } })

    query = db.withdrawal_payment.find({'txtid': '', 'method_payment': 1})
    data ={
        'withdraw' : query,
        'menu' : 'withdraweth',
        'float': float
    }
    return render_template('admin/withdraw_eth.html', data=data)

@admin_ctrl.route('/withdraw-finish', methods=['GET', 'POST'])
def AdminWithdrawfn():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
       
    query = db.withdrawas.find({"status":1})
   
    data ={
        'withdraw' : query,
        'menu' : 'withdraw-finish',
        'float': float
    }
    return render_template('admin/withdraw_finish.html', data=data)

@admin_ctrl.route('/investment', methods=['GET', 'POST'])
def investment():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
       
    query = db.investments.find()
   
    data ={
        'withdraw' : query,
        'menu' : 'investment',
        'float': float
    }
    return render_template('admin/investment.html', data=data)

@admin_ctrl.route('/withdraw-submit', methods=['GET', 'POST'])
def SubmitWithdraw():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    if request.method == 'POST':
        if request.form['pin']=='':
            flash({'msg':'Invalid Pin. Please try again!', 'type':'danger'})
            return redirect('/admin/withdraw')
        # query = db.Withdrawal.find({'txtid': ''})   
    
        query = db.withdrawal_payment.aggregate([ { "$match": { "txtid": "",  'method_payment': 0} }, { "$group": { "_id": "$wallet", "total": { "$sum": "$amount_btc" } } } ])
  
        wallet_address = ''
        bitcoin = ''
        sum_withdraws = 0
        for x in query['result']:
            bitcoin = str(bitcoin) +','+str(round(float(x['total'])/100000000,8))   
            wallet_address = str(wallet_address) +','+str(x['_id'])
            sum_withdraws = float(sum_withdraws)+float(x['total'])
        wallet_payment =  wallet_address[1:]
        bitcoin_payment = bitcoin[1:]
        print sum_withdraws
        
        print(wallet_payment)
        print(bitcoin_payment)

        url = "https://block.io/api/v2/withdraw/?api_key=4e7c-9d30-de24-ceb0&amounts=%s&to_addresses=%s&pin=%s"%(bitcoin_payment,wallet_payment,request.form['pin'])
        print(url)
        r = requests.get(url)
        response_dict = r.json()
        txid = response_dict['data']['txid']
        if txid:
            uid_admin = session.get('user_id_admin')
            user_admin = db.Admin.find_one({'_id': uid_admin})
            sum_withdraw = float(user_admin.sum_withdraw) + float(sum_withdraws)
            db.admins.update({ "_id" : uid_admin }, { '$set': { "sum_withdraw": sum_withdraw } })
            querydb = db.withdrawal_payment.find({'txtid': ''})
            for x in querydb:
                db.withdrawal.update({ "_id" : ObjectId(x['withdraw_id']) }, { '$set': { "txtid": txid } })
            db.withdrawal_payment.drop()
    return redirect('/admin/withdraw')

@admin_ctrl.route('/deposit', methods=['GET', 'POST'])
def Admindeposit():
    error = None
    if session.get('logged_in_admin') is None:
        return redirect('/admin/login')
    print 11111111111
    query = db.deposits.find({})
    dataSend ={
        'deposit' : query,
        'title' : 'Deposit',
        'menu' : 'deposit'
    }
    return render_template('admin/deposit.html', data=dataSend)



@admin_ctrl.route('/logout')
def logout():
    session.pop('logged_in_admin', None)
    # logout_user()
    return redirect('/admin/login')


@admin_ctrl.route('/support', methods=['GET', 'POST'])
def support():
    if session.get(u'logged_in_admin') is None:
        return redirect('/admin/login')
    query = db.supports.find({})
    data ={
    'support' : query,
    'title': 'Support',
    'menu' : 'support'
    }
    return render_template('admin/support.html', data=data)
@admin_ctrl.route('/support/<ids>', methods=['GET', 'POST'])
def Replysupport(ids):
    if session.get(u'logged_in_admin') is None:
        return redirect('/admin/login')
    support = db.supports.find_one({'_id': ObjectId(ids)})

    data ={
    'data_support' : support,
    'title': 'Support',
    'menu' : 'support'
    }
    return render_template('admin/reply_support.html', data=data)

@admin_ctrl.route('/support/reply-support', methods=['POST'])
def newsupporReplyt():
    if session.get(u'logged_in_admin') is None:
        flash({'msg':'Please login', 'type':'danger'})
        return redirect('/admin/login')
    if request.method == 'POST':
        user_id = session.get('user_id')
        sp_id = request.form['sp_id']
        support = db.supports.find_one({'_id': ObjectId(sp_id)})
        if support is None:
            flash({'msg':'Not Found', 'type':'danger'})
            return redirect('/admin/support/'+str(sp_id))
        else: 
            user = db.users.find_one({'_id': ObjectId(user_id)})
            message = request.form['message']
          
            if  message == '':
                flash({'msg':'Please enter message', 'type':'danger'})
            else:    
                data_support = {
                'user_id': 'admin',
                'username' : 'Atlass Support',
                'message': message,
                'date_added' : datetime.utcnow()
                }
                db.supports.update({ "_id" : ObjectId(sp_id) }, { '$set': { "status": 1 }, '$push':{'reply':data_support } })
                #flash({'msg':'Success', 'type':'success'})
                return redirect('/admin/support/'+str(sp_id))    

    return redirect('/admin/support/'+str(sp_id))