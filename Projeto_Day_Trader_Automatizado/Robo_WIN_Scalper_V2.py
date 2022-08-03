""" Robo WIN Scalper V2 """

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time
import pytz
from datetime import datetime

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

timezone = pytz.timezone('ETC/UTC')

""" data_hoje = datetime.today().strftime('%Y-%m-%d')
data_hoje_pregao = data_hoje + "-09:00:00"
duracao_pregao = datetime.today() - pd.Timestamp(data_hoje_pregao) """

horario_inicio_mercado = pd.Timestamp(datetime.today().strftime("%Y-%m-%d") + "-09:05:00")
horario_fechamento_mercado = pd.Timestamp(datetime.today().strftime("%Y-%m-%d") + "-17:30:00")

mt5.initialize()

ativo = 'WINM22'
quantidade = 1
stop_loss = 250
take_profit = 50
 
def ordem_compra(ativo, quantidade, preco):
    print("ORDEM DE COMPRA ENVIADA")
    lot = float(quantidade)
    symbol = ativo
    point = mt5.symbol_info(symbol).point
    price = preco
    deviation = 0

    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY_LIMIT,
        "double price": price,
        "sl": price - stop_loss * point,
        "tp": price + take_profit * point,
        "deviation": deviation,
        "magic": 30101983, 
        "comment": "Ordem de Compra Enviada",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }

    resultado = mt5.order_send(request)
    return resultado

def ordem_venda(ativo, quantidade, preco):
    print("ORDEM DE VENDA ENVIADA")
    lot = float(quantidade)
    symbol = ativo
    point = mt5.symbol_info(symbol).point
    price = preco
    deviation = 0

    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL_LIMIT,
        "double price": price, 
        "sl": price + stop_loss * point,
        "tp": price - take_profit * point,
        "deviation": deviation,
        "magic": 30101983, 
        "comment": "Ordem de Venda Enviada",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }

    resultado = mt5.order_send(request)
    return resultado

def alterar_ordem_compra(ativo, magic_number, quantidade, preco):

    print("ALTERAÇÃO DE ORDEM ENVIADA")
    lot = float(quantidade)
    symbol = ativo
    point = mt5.symbol_info(symbol).point
    price = preco
    deviation = 0

    request = {
        "action": mt5.TRADE_ACTION_MODIFY,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY_LIMIT,
        "double price": price,
        "sl": price - stop_loss * point,
        "tp": price + take_profit * point,
        "deviation": deviation,
        "magic": magic_number, 
        "comment": "Ordem de Compra Alterada",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    
    resultado = mt5.order_send(request)
    return

def alterar_ordem_venda(ativo, magic_number, quantidade, preco):

    print("ALTERAÇÃO DE ORDEM ENVIADA")
    lot = float(quantidade)
    symbol = ativo
    point = mt5.symbol_info(symbol).point
    price = preco
    deviation = 0

    request = {
        "action": mt5.TRADE_ACTION_MODIFY,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL_LIMIT,
        "double price": price,
        "sl": price + stop_loss * point,
        "tp": price - take_profit * point,
        "deviation": deviation,
        "magic": magic_number, 
        "comment": "Ordem de Compra Alterada",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    
    resultado = mt5.order_send(request)
    return


hora_atual = pd.Timestamp(datetime.today().strftime('%H:%M'))
if hora_atual >= horario_inicio_mercado and hora_atual <= horario_fechamento_mercado:
    minutos = 5
    quant_barras = 3
    barras = mt5.copy_rates_from(ativo, mt5.TIMEFRAME_M5, datetime.today(), quant_barras)
    barras_frame = pd.DataFrame(barras)
    barras_frame['time'] = pd.to_datetime(barras_frame['time'], unit='s')

    data = barras_frame[['time', 'open','high','low','close']]
    data.dropna(inplace = True)
    data = data.assign(operacao = '')
    data.reset_index(inplace=True)
    data.drop(columns='index', inplace=True)

    for n in range(2, len(data)):
        if data.close[n-1] > data.high[n-2]:
            data.operacao[n] = 'Comprado'
        elif data.close[n-1] < data.low[n-2]: 
            data.operacao[n] = 'Vendido'
        ordens_abertas = mt5.orders_total()
        posicoes_abertas = mt5.positions_total()
        valor_ordem_aberta = mt5.ORDER_STATE_PLACED #verificar
        magic_number = 30101983 

    while posicoes_abertas == 0:
        while data.operacao[n] == 'Comprado':
            if ordens_abertas == 0:
                if data.close[n] >= ((data.high[n-1]+data.low[n-1])/2):
                    valor_medio = (data.high[n-1]+data.low[n-1])/2
                    preco = float(str(valor_medio)[:-3]+'0')
                    ordem_compra(ativo, quantidade, preco)
                    print(f'Ordem de COMPRA a {preco}')
                elif data.close[n] < ((data.high[n-1]+data.low[n-1])/2):
                    preco = data.close[n]
                    ordem_compra(ativo, quantidade, preco)
                    print(f'Ordem de COMPRA a {preco}')
            else:
                if data.close[n] > valor_ordem_aberta:
                    valor_medio = (data.high[n-1]+data.low[n-1])/2
                    preco = float(str(valor_medio)[:-3]+'0')
                    tipo = 'Compra'
                    magic_number = magic_number
                    alterar_ordem_compra(ativo, magic_number, quantidade, preco)
                    print(f'Ordem de COMPRA a {preco}')
                    time.sleep(1)

        while data.operacao[n] == 'Vendido':
            if ordens_abertas == 0:
                if data.close[n] <= ((data.high[n-1]+data.low[n-1])/2):
                    valor_medio = (data.high[n-1]+data.low[n-1])/2
                    preco = float(str(valor_medio)[:-3]+'0')
                    ordem_venda(ativo, quantidade, preco)
                    print(f'Ordem de VENDA a {preco}')
                elif data.close[n] > ((data.high[n-1]+data.low[n-1])/2):
                    preco = data.close[n]
                    ordem_venda(ativo, quantidade, preco)
                    print(f'Ordem de VENDA a {preco}')
            else:
                if data.close[n] < valor_ordem_aberta:
                    valor_medio = (data.high[n-1]+data.low[n-1])/2
                    preco = float(str(valor_medio)[:-3]+'0')
                    tipo = 'Venda'
                    magic_number = magic_number
                    alterar_ordem_venda(ativo, magic_number, quantidade, preco)
                    print(f'Ordem de VENDA  a {preco}') 
                    time.sleep(1)

    time.sleep(1) 

    print(data)




