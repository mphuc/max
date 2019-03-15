from flask import Blueprint, request, session, redirect, url_for, render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from rex import app, db
from rex.models import user_model, deposit_model, history_model, invoice_model, wallet_model
import json
import urllib
import urllib2
from bson.objectid import ObjectId
from block_io import BlockIo
import datetime
from datetime import datetime
from datetime import datetime, date, timedelta
from time import gmtime, strftime
import time
import os
import collections
import random
import string
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash, check_password_hash
import requests
version = 2 # API version
block_io = BlockIo('9fd3-ec01-722e-fd89', 'SECRET PIN', version)

__author__ = 'carlozamagni'

auto_ctrl = Blueprint('auto', __name__, static_folder='static', template_folder='templates')


def binaryInsert(customer_ml_p_binary, binary_amount_recieve):
    binary_amount_recieves = float(customer_ml_p_binary.r_wallet) + float(binary_amount_recieve)
    db.users.update({ "customer_id" : customer_ml_p_binary.customer_id }, { '$set': { "r_wallet": binary_amount_recieves } })

    binary_amount_sum = float(customer_ml_p_binary.s_wallet) + float(binary_amount_recieve)
    db.users.update({ "customer_id" : customer_ml_p_binary.customer_id }, { '$set': { "s_wallet": binary_amount_sum } })

    binary_total_earns = float(customer_ml_p_binary.total_earn)+float(binary_amount_recieve)
    db.users.update({ "customer_id" : customer_ml_p_binary.customer_id }, { '$set': { "total_earn": binary_total_earns } })

    binary_data_send = {
        'date_added': datetime.utcnow(),
        'uid' : customer_ml_p_binary.customer_id,
        'name' : customer_ml_p_binary.username,
        'amount_sub' : 0,
        'amount_add' : binary_amount_recieve/1000000,
        'amount_rest' : binary_amount_sum/1000000,
        'type' : "Binary Commission ",
        'detail' : 'Earn 4% Binary bonus on downline'
    }
    history_ids = db.history.insert(binary_data_send)
    return history_ids

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

def get_id_tree(ids):
    listId = ''

    query = db.users.find({'p_binary': ids})
    for x in query:
        listId += ', %s'%(x['customer_id'])
        listId += get_id_tree(x['customer_id'])
    return listId

def binary_left(customer_id):
    check_f1 = db.users.find({'$and' : [{'p_node' : customer_id},{'level':{'$gt': 1 }} ]})
    
    if check_f1.count() > 0:
        listId = ''
        for x in check_f1:
            listId += ',%s'%(x['customer_id'])
        arrId = listId[1:]

        count = db.users.find_one({'customer_id': customer_id})
        if count['left'] == '':
            customer_binary = ',0'
        else:
            ids = count['left']

            count = get_id_tree(count['left'])

            if count:
                customer_binary = '%s , %s'%(count, ids)

            else:
                customer_binary = ',%s'%(ids)

        customer_binary = customer_binary[1:]

        array = '%s, %s'%(arrId, customer_binary)
        customers = array.split(',')
        customers = map(int, customers)

        check_in_left = [item for item, count in collections.Counter(customers).items() if count > 1]

        if len(check_in_left) != 0:
            check_in_left = 1
        else:
            check_in_left = -1
    else:
        check_in_left = -1
    return check_in_left
    

def binary_right(customer_id):
    check_f1 = db.users.find({'$and' : [{'p_node' : customer_id},{'level':{'$gt': 1 }} ]})

    if check_f1.count() > 0:
        listId = ''
        for x in check_f1:
            listId += ', %s'%(x['customer_id'])
        arrId = listId[1:]
        count = db.users.find_one({'customer_id': customer_id})
        if count['right'] == '':
            customer_binary = ',0'
        else:
            ids = count['right']
            count = get_id_tree(count['right'])
            if count:
                customer_binary = '%s , %s'%(count, ids)
            else:
                customer_binary = ',%s'%(ids)
            
        customer_binary = customer_binary[1:]
        array = '%s, %s'%(arrId, customer_binary)
        customers = array.split(',')
        customers = map(int, customers)

        check_in_right = [item for item, count in collections.Counter(customers).items() if count > 1]
        if len(check_in_right) != 0:
            check_in_right = 1
        else:
            check_in_right = -1
    else:
        check_in_right = -1
    return check_in_right

def get_receive_program_package(user_id,amount):
    customer = db.users.find_one({"customer_id" : user_id })
    
    if customer['level'] == 2:
       max_receive = 1250 
    if customer['level'] == 3:
       max_receive = 2500 
    if customer['level'] == 4:
       max_receive = 7500 
    if customer['level'] == 5:
       max_receive = 12500 
    if customer['level'] == 6:
       max_receive = 25000 
    if customer['level'] == 7:
       max_receive = 75000 
    if customer['level'] == 8:
       max_receive = 125000 
    if customer['level'] == 9:
       max_receive = 250000 
    if customer['level'] == 10:
       max_receive = 1250000 
    if customer['level'] == 11:
       max_receive = 2500000 

    if float(amount) > max_receive - float(customer['max_out_package']):
        amount_receve = max_receive - float(customer['max_out_package'])
        investment = db.investments.find_one({'$and' :[{'status' : 1},{"uid" : user_id }]} )
        if investment is not None:
            db.investments.update({'_id': ObjectId(investment['_id'])},{'$set' : {'reinvest' : 1,'total_income' : float(max_receive),'status_income' : 1,'date_income' : datetime.utcnow()}})
    else:
        amount_receve = amount
    customer['max_out_package'] = float(amount_receve) + float(customer['max_out_package'])
    db.users.save(customer)
    return amount_receve

def get_receive_program_day(user_id,amount):
    customer = db.users.find_one({"customer_id" : user_id })
    
    if customer['level'] == 2:
       max_receive = 500 
    if customer['level'] == 3:
       max_receive = 1000 
    if customer['level'] == 4:
       max_receive = 3000 
    if customer['level'] == 5:
       max_receive = 5000 
    if customer['level'] == 6:
       max_receive = 10000 
    if customer['level'] == 7:
       max_receive = 30000 
    if customer['level'] == 8:
       max_receive = 50000 
    if customer['level'] == 9:
       max_receive = 100000 
    if customer['level'] == 10:
       max_receive = 500000 
    if customer['level'] == 11:
       max_receive = 1000000 

    if float(amount) > max_receive - float(customer['max_out_day']):
        amount_receve = max_receive - float(customer['max_out_day'])
    else:
        amount_receve = amount
    customer['max_out_day'] = float(amount_receve) + float(customer['max_out_day'])
    db.users.save(customer)

    return amount_receve

@auto_ctrl.route('/auto-tickers', methods=['GET', 'POST'])
def auto_tickers():
    response_xvg = urllib2.urlopen("https://api.coinmarketcap.com/v1/ticker/verge/")
    response_xvg = response_xvg.read()
    response_xvg = json.loads(response_xvg)

    response_btc = urllib2.urlopen("https://api.coinmarketcap.com/v1/ticker/bitcoin/")
    response_btc = response_btc.read()
    response_btc = json.loads(response_btc)
    print(response_btc)
    db.tickers.update({},{'$set': {'xvg_usd': response_xvg[0]['price_usd'],'xvg_btc': response_xvg[0]['price_btc'],'btc_usd' : response_btc[0]['price_usd']}})
    return json.dumps({'status' : 'success'})

def getf1_earnings(customer_id,amount_receve):
    customers = db.users.find_one({"customer_id" : customer_id })
    username_receive = customers['username']
    customers_f1 = db.users.find_one({"customer_id" : customers['p_node'] })
    if customers_f1 is not None:
        if int(customers_f1['level']) > 0:
            
            percent = 5

            commission = float(amount_receve)*percent/100
            commission = round(commission,2)
            
            f1earnings_wallet = float(customers_f1['f1earnings_wallet'])
            new_f1earnings_wallet = float(f1earnings_wallet) + float(commission)
            new_f1earnings_wallet = float(new_f1earnings_wallet)

            total_earn = float(customers_f1['total_earn'])
            new_total_earn = float(total_earn) + float(commission)
            new_total_earn = float(new_total_earn)

            balance_wallet = float(customers_f1['balance_wallet'])
            new_balance_wallet = float(balance_wallet) + float(commission)
            new_balance_wallet = float(new_balance_wallet)

            db.users.update({ "_id" : ObjectId(customers_f1['_id']) }, { '$set': {'balance_wallet' : new_balance_wallet,'total_earn': new_total_earn, 'f1earnings_wallet' :new_f1earnings_wallet } })
            detail = 'Get '+str(percent)+' '+"""%"""+' from member %s receive $%s' %(username_receive, amount_receve)
            SaveHistory(customers_f1['customer_id'],customers_f1['_id'],customers_f1['username'], commission, 'f1_earnings', 'USD', detail, '', '')
                
@auto_ctrl.route('/dailybonus/asdadertetqweqwe/<ids>', methods=['GET', 'POST'])
def caculator_dailybonus(ids):
    if ids =='RsaW3Kb1gDkdRUGDo':
        now = datetime.today()
        investment = db.investments.find({'$and' :[{'status' : 1},{"date_profit": { "$lte": now }}]} )
        for x in investment:
            print x['username']
            #bang profit
            if x['package'] == 500:
                percent = 5
            if x['package'] == 2000:
                percent = 5.5
            if x['package'] == 5000:
                percent = 6
            if x['package'] == 10000:
                percent = 8
            if x['package'] == 30000:
                percent = 10
            if x['package'] == 50000:
                percent = 12
            
            #tinh commision
            commission = float(percent)*float(x['package'])/100
            
            
            #update balance
            customers = db.users.find_one({'customer_id': x['uid']})

            

            d_wallet = float(customers['d_wallet'])
            new_d_wallet = float(d_wallet) + float(commission)
            new_d_wallet = float(new_d_wallet)

            total_earn = float(customers['total_earn'])
            new_total_earn = float(total_earn) + float(commission)
            new_total_earn = float(new_total_earn)

            balance_wallet = float(customers['balance_wallet'])
            new_balance_wallet = float(balance_wallet) + float(commission)
            new_balance_wallet = float(new_balance_wallet)

            

            db.users.update({ "_id" : ObjectId(customers['_id']) }, { '$set': {'balance_wallet' : new_balance_wallet,'total_earn': new_total_earn, 'd_wallet' :new_d_wallet } })
            #detail = 'Get '+str(percent)+' '+"""%"""+' Daily profit from the investment $%s' %(x['package'])
            SaveHistory(customers['customer_id'],customers['_id'],customers['username'], commission, 'dailyprofit', 'USD', percent, x['package'], '')

            new_date_profit = datetime.utcnow() + timedelta(days=30)
            new_profit =  float(x['amount_frofit']) + commission
            new_number_frofit = int(x['number_frofit']) + 1 
            status_investment = 1
            if new_number_frofit >= 15:
                status_investment = 0
            db.investments.update({'_id' : ObjectId(x['_id'])},{ '$set' : {'amount_frofit' : float(new_profit),'number_frofit' : new_number_frofit ,'status' : status_investment,'date_profit' : new_date_profit}})
            
            #getf1_earnings(customers['customer_id'],commission)
            
            #save history
                
        return json.dumps({'status' : 'success'})
@auto_ctrl.route('/binaryBonusOprHJhEp/asdadertetqweqwe/<ids>', methods=['GET', 'POST'])
def caculator_binary(ids):
    
    # return json.dumps({'status' : 'off'})
    if ids =='RsaW3Kb1gDkdRUGDo':
        countUser = db.users.find({'$and': [{'total_pd_left':{'$gt': 0 }}, {'total_pd_right':{'$gt': 0 }}, {'level':{'$gt': 0 }}]}).count()
        if countUser > 0:
            user = db.users.find({'$and': [{'total_pd_left':{'$gt': 0 }}, {'total_pd_right':{'$gt': 0 }}, {'level':{'$gt': 0 }}]})
            
            for x in user:
                #if binary_left(x['customer_id']) == 1 and binary_right(x['customer_id']) == 1:
                if x['total_pd_left'] > x['total_pd_right']:
                    balanced = x['total_pd_right']
                    pd_left = float(x['total_pd_left'])-float(x['total_pd_right'])
                    db.users.update({ "customer_id" : x['customer_id'] }, { '$set': { "total_pd_left": pd_left } })
                    db.users.update({ "customer_id" : x['customer_id'] }, { '$set': { "total_pd_right": 0 } })
                else:
                    balanced = x['total_pd_left']
                    pd_right = float(x['total_pd_right'])-float(x['total_pd_left'])
                    db.users.update({ "customer_id" : x['customer_id'] }, { '$set': { "total_pd_left": 0 } })
                    db.users.update({ "customer_id" : x['customer_id'] }, { '$set': { "total_pd_right": pd_right } })
                
                level = float(x['level'])
                percent = 5

                print x['username']

                #tinh commision
                commission = float(balanced)*float(percent)/100
                commission = round(commission,2)
                
                #update balance
                customers = db.users.find_one({'customer_id': x['customer_id']})

                s_wallet = float(customers['s_wallet'])
                new_s_wallet = float(s_wallet) + float(commission)
                new_s_wallet = float(new_s_wallet)

                total_earn = float(customers['total_earn'])
                new_total_earn = float(total_earn) + float(commission)
                new_total_earn = float(new_total_earn)

                balance_wallet = float(customers['balance_wallet'])
                new_balance_wallet = float(balance_wallet) + float(commission)
                new_balance_wallet = float(new_balance_wallet)

                db.users.update({ "_id" : ObjectId(customers['_id']) }, { '$set': {'balance_wallet' : new_balance_wallet,'total_earn': new_total_earn, 's_wallet' :new_s_wallet } })
                detail = 'Get '+str(percent)+' '+"""%"""+' from weak branches $%s' %(balanced)
                SaveHistory(customers['customer_id'],customers['_id'],customers['username'], commission, 'binarybonus', 'USD', detail, '', '')

            
                    
        return json.dumps({'status' : 'success'})
    else:
        return json.dumps({'status' : 'error'})


@auto_ctrl.route('/update-maxoutdat/asdadertetqweqwe/<ids>', methods=['GET', 'POST'])
def updatemax_out_day(ids):
    if ids =='RsaW3Kb1gDkdRUGDo':

        db.users.update({}, {'$set': {'max_out_day': 0 }}, multi=True)

        return json.dumps({'status' : 'success'})
    else:
        return json.dumps({'status' : 'error'})

