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


#고가 저가 종가 평균
avg_HLC   = numpy.zeros((50))
sum_avg_HLC = numpy.zeros((50))
sum_avg_cal = numpy.zeros((50))
avg_sum_avg_cal = numpy.zeros((50))
cci_price = numpy.zeros((50))




df = pyupbit.get_ohlcv("KRW-DOGE", interval="minute1", count=50)
print(df)         # 분봉 데이터
df.to_excel("test_cci.xlsx")

#CCI 계산 방법
#   M = ( H + L + C ) / 3       (H : 고가, L : 저가, C : 종가, M : 평균가격(mean price))
#   SM = M의 n일 합계 / n       (단, N은 일반적으로 20일을 기본값으로 제공함.)
#   D = ( M – SM )의 N일 합계 / N
#   M : 평균가격, SM : n기간 단순 이동평균, D : 평균편차(mean deviation)
#   CCI = ( M – SM ) / (0.015 * D )
#   단, 0.015란 값은 Lambert가 사용한 상수로서 CCI값이 ±100에서 크게 벗어나지 않도록 하기 위해 주어지 제수(constant divisor)이다


for i in range(0,50):
    avg_HLC[i] = ((df.high[i] + df.low[i] + df.close[i] ) / 3)
    print("avg_HLC : %f" % avg_HLC[i])

    if i > 12:
        for j in range(0,14):
            #print("avg_HLC[i - j] : %f" % avg_HLC[i - j])
            sum_avg_HLC[i] += avg_HLC[i - j]
        
    sum_avg_HLC[i] = (sum_avg_HLC[i] / 14)
    #print("sum_avg_HLC : %f" % sum_avg_HLC[i])
    sum_avg_cal[i] = (avg_HLC[i] - sum_avg_HLC[i])
    if sum_avg_cal[i] < 0:
        sum_avg_cal[i] = (sum_avg_cal[i] * -1)
    #print("sum_avg_cal : %f" % sum_avg_cal[i])
    
    if i > 26:
        for j in range(0,14):
            #print("avg_HLC[i - j] : %f" % avg_HLC[i - j])
            avg_sum_avg_cal[i] += sum_avg_cal[i - j]
    
    avg_sum_avg_cal[i] = (avg_sum_avg_cal[i] / 14)
    print("avg_sum_avg_cal : %f" % avg_sum_avg_cal[i])


    if i > 26:
        cci_price[i] = ((avg_HLC[i] - sum_avg_HLC[i])/(avg_sum_avg_cal[i] * 0.015))
    print("cci_price : %f" % cci_price[i])
    
