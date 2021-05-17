import time
import pyupbit
import datetime
import sys
import numpy

access = "ar3zJIbdK9Ng3d1ViD1hV89xbxlgUCeQz0cpxBdB"          # 본인 값으로 변경
secret = "QvxWjnGcqSpGy0WSlSrbVvwC5MiE7wQHQy6X7Cny"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

file_name = "test.txt"
file = open(file_name, 'w')
file.write("autotrade start \n")
file.flush()


print(upbit.get_balance("KRW-DOGE"))     # KRW-BTC 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회


avg_12day   = numpy.zeros((50))
avg_26day   = numpy.zeros((50))
dnag_jang   = numpy.zeros((50))
signal9     = numpy.zeros((50))
macd_signal = numpy.zeros((50))

df = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=50)
print(df)         # 분봉 데이터
df.to_excel("test_cci.xlsx")

for i in range(0,50):
    
    if i > 11:
        for j in range(0,12):
            avg_12day[i] += df.close[i - j]
        
    avg_12day[i] = (avg_12day[i] / 12)
    print("avg_12day[i] : %f" % avg_12day[i])


    if i > 25:
        for j in range(0,26):
            avg_26day[i] += df.close[i - j]
        
    avg_26day[i] = (avg_26day[i] / 26)
    print("avg_26day[i] : %f" % avg_26day[i])


    dnag_jang[i] = avg_12day[i] - avg_26day[i]
    print("dnag_jang[i] : %f" % dnag_jang[i])

    if i > 33:
        for j in range(0,9):
            signal9[i] += dnag_jang[i - j]
    
    signal9[i] = (signal9[i] / 9)
    print("signal9[i] : %f" % signal9[i])

    macd_signal[i] = dnag_jang[i] - signal9[i]
    print("macd_signal[i] : %f" % macd_signal[i])
