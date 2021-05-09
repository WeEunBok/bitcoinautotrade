import time
import pyupbit
import datetime
import sys
import numpy

access = "ar3zJIbdK9Ng3d1ViD1hV89xbxlgUCeQz0cpxBdB"          # 본인 값으로 변경
secret = "QvxWjnGcqSpGy0WSlSrbVvwC5MiE7wQHQy6X7Cny"          # 본인 값으로 변경

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    #2일치 데이터 조회
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    #df.iloc[0]['close'] : 다음날 싯가
    #(df.iloc[0]['high'] - df.iloc[0]['low']) * k : 변동폭
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


#로그인
upbit = pyupbit.Upbit(access, secret)
#INPUT 값 받기
coin = sys.argv[1]
file_name = "log-"+coin+".txt"
file = open(file_name, 'w')
file.write("autotrade start \n")
file.flush()


my_money = get_balance("KRW")
buy_money = 0
krw = 0
data = "coin : %s \n" % coin
file.write(data)
file.flush()

KRW_coin = "KRW-"+coin
data = "KRW_coin : %s \n" % KRW_coin
file.write(KRW_coin)
file.flush()


#2차원 배열 선얼 [14][30]
#당일 - 전일 상승분 배열
up_arr   = numpy.zeros((30, 14))
#당일 - 전일 하락분 배열
down_arr = numpy.zeros((30, 14))
#1차 배열
#상승분 평균
avg_up   = numpy.zeros((30))
#하락분 평균
avg_down = numpy.zeros((30))
#rsi 상승분 기초데이터
rsi_base_up   = numpy.zeros((30))
#rsi 하락분 기초데이터
rsi_base_down = numpy.zeros((30))
#rsi 계산 최종 데이터
rsi_arr = numpy.zeros(30)

# 자동매매 시작
while True:
    try:
        # 현재가
        current_price = get_current_price(KRW_coin)
        # 평균단가
        avg_price = upbit.get_avg_buy_price(KRW_coin)
        # 원화잔고
        current_krw = get_balance("KRW")
        #1분봉 43개 가지고오기
        minute_ohlcv = pyupbit.get_ohlcv(KRW_coin, interval="minute1", count=43)
        
        i = 0
        j = 0
        
        for i in range(0,30):

            sum_up = 0
            sum_down = 0

            for j in range(0,14):
                #print(minute_ohlcv.close[j])
                
                #data = "i      : %d \n" % i
                #file.write(data)
                #file.flush()
                #data = "j      : %d \n" % j
                #file.write(data)
                #file.flush()
                
                if i == 0 and j == 0:
                    #file.write("첫번째\n")
                    #file.flush()
                    up_arr[0][0]   = 0
                    down_arr[0][0] = 0
                else:
                    #등락 계산(T분 종가- T-1분 종가) 배열에 저장
                    if (minute_ohlcv.close[i+j] - minute_ohlcv.close[i+j-1]) >= 0:
                        up_arr[i][j]   =  (minute_ohlcv.close[i+j] - minute_ohlcv.close[i+j-1])
                        down_arr[i][j] = 0
                    else:   
                        up_arr[i][j]   = 0
                        down_arr[i][j] = ((minute_ohlcv.close[i+j] - minute_ohlcv.close[i+j-1]) * -1)
                
#                data = "up_arr       : %.10s \n" % up_arr[i][j]
#                file.write(data)
#                file.flush()
#                data = "down_arr     : %.10s \n" % down_arr[i][j]
#                file.write(data)
#                file.flush()
            
                sum_up   += up_arr[i][j]
                sum_down += down_arr[i][j]
            #for k in range(0,14):
                #등락 SUM
                #sum_up   += up_arr[i][k]
                #sum_down += down_arr[i][k]

            #등락 평균
            avg_up[i]    = (sum_up / 14)
#            data = "avg_up       : %.10s \n" % avg_up[i]
#            file.write(data)
#            file.flush()
            avg_down[i]  = (sum_down / 14)
#            data = "avg_down     : %.10s \n" % avg_down[i]
#            file.write(data)
#            file.flush()
#            file.write("--------------------------------------------------\n")
#            file.flush()

        for i in range(0,30):
            if i == 0:
                rsi_base_up[i]   = avg_up[i]
                rsi_base_down[i] = avg_down[i]
            else:
                rsi_base_up[i]   = (((rsi_base_up[i-1] * 13  ) + up_arr[i][13]  ) / 14)
                rsi_base_down[i] = (((rsi_base_down[i-1] * 13) + down_arr[i][13]) / 14)

            #RSI = 상승폭 총합 / (상승폭 총합 + 하락폭 총합)
            rsi_arr[i] = (100 * rsi_base_up[i]) /(rsi_base_up[i] + rsi_base_down[i])

        #print(up_arr)
        #print(down_arr)
        #print(avg_up)
        #print(avg_down)
        #print(rsi_base_up)
        #print(rsi_base_down)
        #print(rsi_arr)
        #print(rsi_arr[29])
        
        #data = "now_date[29] : %s" % datetime.datetime.now()
        #file.write(data)
        #file.flush()
        #data = "rsi_price = : %s" % rsi_arr[29]
        #file.write(data)
        #file.flush()
        
        if krw == 0:
            #rsi 30미만(과매도시) 매수
            if rsi_arr[29] < 30:
                krw = current_krw
                buy_money = current_price
                if krw > 5000:
                    #upbit.buy_market_order(KRW_coin, krw*0.9995) # 비트코인 매수
                    data = "BUY_COIN!  : %f \n" % current_price
                    file.write(data)
                    file.flush()
                    data = "now_date[29] : %s" % datetime.datetime.now()
                    file.write(data)
                    file.flush()
                    data = "rsi_price = : %s" % rsi_arr[29]
                    file.write(data)
                    file.flush()

        if krw != 0:
            #rsi 65이상(과매수시) 매도
            if rsi_arr[29] >= 65:
                coin_price = get_balance(coin)
                #upbit.sell_market_order(KRW_coin, coin_price) # 비트코인 전량 매도
                data = "SELL_COIN! : %f \n" % current_price
                file.write(data)
                file.flush()
                data = "now_date[29] : %s" % datetime.datetime.now()
                file.write(data)
                file.flush()
                data = "rsi_price = : %s" % rsi_arr[29]
                file.write(data)
                file.flush()
                buy_money = 0
                krw = 0

        time.sleep(5)
    except Exception as e:
        print(e)
        file.close()
        time.sleep(5)
