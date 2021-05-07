import pyupbit
import sys

access = ""          # 본인 값으로 변경
secret = ""          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # KRW-BTC 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회


arguments = sys.argv[1]
print(arguments)
coin = "KRW-" + arguments
print(coin)
print(upbit.get_balance(coin))

count = 0
#print(arguments[1])
#print(upbit.get_balance(arguments[1]))
#print(pyupbit.get_ohlcv(arguments[1], interval="minute1", count=3))
# 자동매매 시작
while True:
    try:
        print(count)
        
        count = count + 1
        
        if count == 10:
            print("break")
            break
            
        sleep(2)
    
    except Exception as e:
        print(e)
        time.sleep(1)