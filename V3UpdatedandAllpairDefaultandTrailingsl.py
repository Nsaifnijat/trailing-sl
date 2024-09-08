
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 20:46:18 2021

@author: Nsaifnijat
"""

# import libraries
import MetaTrader5 as mt5
import time
import sys
import decimal

# connect Python to MetaTrader5
mt5.initialize()
#optional: #you dont need this if you have already logged into your account in the mt5 platform
#login = account.login
#password = password
#server = account_server
#mt.login(login,password,server)

def update(ticket,new_sl,new_tp):
     request = {
                'action': mt5.TRADE_ACTION_SLTP,
                'position': ticket,
                'sl': float(new_sl),
                'tp':float(new_tp),
                    }
    
     result = mt5.order_send(request)
     return result

def TrailFunc():
    MAX_DIST_SL = 20  # Max distance between current price and SL, otherwise SL will update
    TRAIL_AMOUNT =10  # Amount by how much SL updates
    DEFAULT_SL =10  # If position has no SL, set a default SL
    INDEX_DEFAULT_SL=10
    INDEX_TRAIL_AMOUNT=11
    INDEX_MAX_DIST_SL=20


    indices=['US30','SPX','S&P500','AUS200','SPY','US500','DE30','FR40','HK50','STOXX50','USTEC']
    five_digit_pairs=['EURUSD','GBPUSD','EURGBP','USDCAD','NZDUSD','AUDUSD','AUDCAD','AUDCHF','AUDGBP','AUDNZD','NZDCAD',
                  'CADCHF','EURCAD','EURCHF','EURAUD','GBPAUD','GBPNZD','GBPCAD','USDCHF','GBPCHF','NZDCHF',
                  'EURNZD']
    three_digit_pairs=['AUDJPY','GBPJPY','CADJPY','CHFJPY','EURJPY','NZDJPY','USDJPY']
    while True:
        tposition=mt5.positions_get()
        for position in tposition:
            open_price=position.price_open
            curr_price=position.price_current
            ticket=position.ticket
            print(ticket)
            if position.type==0:        
                OPEN_CUR_PRICE_DIST=curr_price-open_price
                SL_CUR_PRICE_DIST=curr_price-position.sl
            else:
                OPEN_CUR_PRICE_DIST=open_price-curr_price
                SL_CUR_PRICE_DIST=position.sl-curr_price
    
            if position.symbol in indices:
                #giving default sl to indices
                if position.sl==0.0:
                    if position.type==0:
                        new_sl=open_price-INDEX_DEFAULT_SL
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                    else:
                        new_sl=open_price+INDEX_DEFAULT_SL
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                else:
                    #trail stop loss
                    if OPEN_CUR_PRICE_DIST>INDEX_DEFAULT_SL and SL_CUR_PRICE_DIST>INDEX_MAX_DIST_SL:
                        if SL_CUR_PRICE_DIST>INDEX_DEFAULT_SL:
                            if position.type==0:
                                new_sl=position.sl+INDEX_TRAIL_AMOUNT
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                                new_sl=position.sl-INDEX_TRAIL_AMOUNT
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                           
                        else:
                            if position.type==0:
                                new_sl=open_price+1
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                                new_sl=open_price-1
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                    
            elif position.symbol=='XAUUSD':
                #giving default sl to indices
                if position.sl==0.0:
                    if position.type==0:
                        new_sl=open_price-abs(round(DEFAULT_SL/5))
                        print(new_sl)
                        print(open_price)
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                    else:
                        new_sl=open_price+abs(round(DEFAULT_SL/5))
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                else:
                     if OPEN_CUR_PRICE_DIST>abs(round(DEFAULT_SL/5)) and SL_CUR_PRICE_DIST>abs(round(MAX_DIST_SL/5)):
                        if SL_CUR_PRICE_DIST>abs(round(DEFAULT_SL/5)):
                            if position.type==0:
                                new_sl=position.sl+abs(round(TRAIL_AMOUNT/5))
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                               new_sl=position.sl-abs(round(TRAIL_AMOUNT/5))
                               new_tp=position.tp
                               update(ticket,new_sl, new_tp)
                            
                        else:
                            if position.type==0:
                                new_sl=open_price+0.2
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                                new_sl=open_price-0.2
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
               
            elif position.symbol in five_digit_pairs:
                if position.sl==0.0:
                          multiplier=0.0001
                          if position.type==0:
                              new_sl=open_price-(DEFAULT_SL*multiplier)
                              new_tp=position.tp
                              update(ticket,new_sl, new_tp)
                          else:
                                new_sl=open_price+(DEFAULT_SL*multiplier)
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                else:
                    multiplier=0.0001
                    if OPEN_CUR_PRICE_DIST>(DEFAULT_SL*multiplier) and SL_CUR_PRICE_DIST>(MAX_DIST_SL*multiplier):
                        if SL_CUR_PRICE_DIST>(DEFAULT_SL*multiplier):    
                            if position.type==0:
                               new_sl=position.sl+(TRAIL_AMOUNT*multiplier)
                               new_tp=position.tp
                               update(ticket,new_sl, new_tp)
                            else:
                               new_sl=position.sl-(TRAIL_AMOUNT*multiplier)
                               new_tp=position.tp
                               update(ticket,new_sl, new_tp)
                        else:
                            if position.type==0:
                                new_sl=open_price+0.00007
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                                new_sl=open_price-0.00007
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
            elif position.symbol in three_digit_pairs:
                multiplier=0.01
                if position.sl==0.0:
                    if position.type==0:
                        new_sl=open_price-(DEFAULT_SL*multiplier)
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                    else:
                        new_sl=open_price+(DEFAULT_SL*multiplier)
                        new_tp=position.tp
                        update(ticket,new_sl, new_tp)
                       
                else:
                    multiplier=0.01
                    if OPEN_CUR_PRICE_DIST>(DEFAULT_SL*multiplier) and SL_CUR_PRICE_DIST>(MAX_DIST_SL*multiplier):
                        if SL_CUR_PRICE_DIST>(DEFAULT_SL*multiplier):    
                            if position.type==0:
                               new_sl=position.sl+(TRAIL_AMOUNT*multiplier)
                               new_tp=position.tp
                               update(ticket,new_sl, new_tp)
                            else:
                               new_sl=position.sl-(TRAIL_AMOUNT*multiplier)
                               new_tp=position.tp
                               update(ticket,new_sl, new_tp)
                        else:
                            if position.type==0:
                                new_sl=open_price+0.007
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                            else:
                                new_sl=open_price-0.007
                                new_tp=position.tp
                                update(ticket,new_sl, new_tp)
                        
                        
        time.sleep(1)
                    
                    
TrailFunc()              
                    
                    
                    
                    
                    
                    

