import time
import pyupbit
import datetime

access = ""          # 본인 값으로 변경
secret = ""          # 본인 값으로 변경

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


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
my_money = get_balance("KRW")

###############################################################
#최근 체결가
#print(pyupbit.get_current_price("KRW-BTC"))

#현재가
#print(pyupbit.get_current_price(["KRW-BTC", "KRW-XRP"]))

#get_ohlcv 함수는 고가/시가/저가/종가/거래량
#                           open        high         low       close      volume
#2021-04-30 22:45:00  65529000.0  65622000.0  65369000.0  65607000.0  178.252793
#df = pyupbit.get_ohlcv("KRW-BTC")
#print(df.tail())

#interval 파라미터는 조회단위를 지정합니다. 파라미터에는 다음 값을 지정할 수 있습니다.
#day/minute1/minute3/minute5/minute10/minute15/minute30/minute60/minute240/week/month
#print(pyupbit.get_ohlcv("KRW-BTC", interval="day")              # 일봉 데이터 (5일)
#print(pyupbit.get_ohlcv("KRW-BTC", interval="minute1"))         # 분봉 데이터
#print(pyupbit.get_ohlcv("KRW-BTC", interval="minute5"))         # 분봉 데이터
#print(pyupbit.get_ohlcv("KRW-BTC", interval="week"))            # 주봉 데이터

#df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=1)
#print(df.high[0])


#get_orderbook 함수는 매수/매도 호가 정보를 조회합니다.
# * market : 암호화폐 티커
# * timestamp : 조회시간 (단위 ms)
# * orderbook_units : 매도호가/매수호가 정보
#print(pyupbit.get_orderbook(tickers=["KRW-BTC", "KRW-XRP"]))
#[{'market': 'KRW-BTC', 'timestamp': 1619788491459, 'total_ask_size': 4.45776086, 'total_bid_size': 3.66528398, 'orderbook_units': {'ask_price': 64507000.0, 'bid_price': 64502000.0, 'ask_size': 3.53148249, 'bid_size': 0.0521755}

#매도
#원화 시장에 리플을 600원에 20개 매도
#print(upbit.sell_limit_order("KRW-XRP", 600, 20))

#매수
#리플을 613원에 10개 매수
#print(upbit.buy_limit_order("KRW-XRP", 613, 10))

#시장가 매수/매도
#주문한 10000원은 수수료가 포함된 금액
#print(upbit.buy_market_order("KRW-XRP", 10000))

#리플 30개를 시장가 매도
#print(upbit.sell_market_order("KRW-XRP", 30))
###############################################################

#매수할 종목은 거래량 전날보다 많은 애들 기준?
#3분봉으로 변동폭 1.1퍼 이상 3회 이상 매수
#-2퍼 손절
#+3퍼 익절
#반복


# 자동매매 시작
while True:
    try:
        #현재시간
        now = datetime.datetime.now()
        #시작시간 09:00
        start_time = get_start_time("KRW-BTC")
        #09:00 + 하루
        end_time = start_time + datetime.timedelta(days=1)
        # 9:00:00 < 현재 < 8:59:50
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5)
            current_price = get_current_price("KRW-BTC")
            avg_price = upbit.get_avg_buy_price("KRW-BTC")
            # 원화잔고
            current_krw = get_balance("KRW")
            
            if  current_krw > my_money * 0.7:
                if target_price < current_price:
                    krw = current_krw / 10
                    if krw > 5000:
                        upbit.buy_market_order("KRW-BTC", krw*0.9995) # 비트코인 매수
                        
            if avg_price != 0:
                if ((current_price / avg_price) - 1) * 100 > 4.0:
                    upbit.sell_market_order("KRW-BTC", btc*0.9995) # 비트코인 전량 매도
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995) # 비트코인 전량 매도
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)