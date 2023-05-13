# -*- coding: utf-8 -*-
import csv
import os

import pandas as pd
import statsmodels.api as sm
from scipy import interpolate


def capacity_management_algorithm_days(date, duration):
    if duration <= 1:
        duration += 1

    # 获取数据
    data = pd.read_excel('3_1.xlsx')

    time_data = []
    capacity_data = []
    for i in range(len(data['collect_time'])):
        if str(data['collect_time'][i])[5:10] == date:
            for j in range(duration):
                time_data.append(data['collect_time'][i])
                capacity_data.append(data['used_value'][i])
                i += 1
                if i >= len(data['collect_time']):
                    break

    # 创建一个新的数据框, 并将时间序列数据和容量数据添加到其中
    data_frame = pd.DataFrame(
        {
            'collect_time': time_data,
            'used_value': capacity_data
        }
    )

    # 创建 ARIMA 模型
    model = sm.tsa.ARIMA(data_frame['used_value'],
                         order=(2, 1, 1))

    # 训练 ARIMA 模型
    ARIMA_model = model.fit()

    # 预测容量需求
    predictions = ARIMA_model.predict(start=len(data_frame['used_value']),
                                      end=len(data_frame['used_value']) + duration - 1,
                                      dynamic=False
                                      )

    predictions = predictions.array
    if duration <= 2:
        duration -= 1
    return predictions[0: duration]


def capacity_management_algorithm_hours(date, duration):
    if duration <= 1:
        duration += 1

    # 获取数据
    data = pd.read_excel('3_1.xlsx')

    # 将数据分成时间序列数据和容量数据
    time_data = data['collect_time']
    capacity_data = data['used_value']

    # 将时间序列数据转换为时间戳格式
    time_data = pd.to_datetime(time_data,
                               format='%Y-%m-%d %H:%M:%S'
                               )

    # 对容量数据进行插值，得到每个小时的容量数据
    f = interpolate.interp1d(time_data.astype('int64'),
                             capacity_data,
                             kind='linear'
                             )
    hour_time = pd.date_range(start=time_data.min(),
                              end=time_data.max(),
                              freq='1H'
                              )
    hour_capacity = f(hour_time.astype('int64')).tolist()

    # 创建一个新的数据框，并将时间序列数据和插值后的容量数据添加到其中
    data_frame = pd.DataFrame({'collect_time': hour_time,
                               'used_value': hour_capacity}
                              )

    # 创建 ARIMA 模型
    model = sm.tsa.ARIMA(data_frame['used_value'],
                         order=(2, 1, 1))

    # 训练 ARIMA 模型
    ARIMA_model = model.fit()

    # 预测容量需求
    predictions = ARIMA_model.predict(start=len(data_frame['used_value']),
                                      end=len(data_frame['used_value']) + duration - 1,
                                      dynamic=False
                                      )

    predictions = predictions.array
    if duration <= 2:
        duration -= 1
    return predictions[0: duration]


days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

dates = []
for month in range(1, 13):
    for day in range(1, days_in_month[month - 1] + 1):
        date = "{:02d}-{:02d}".format(month, day)
        dates.append(date)

predictions = capacity_management_algorithm_days(dates[0], 730)

dates += dates

file_name = '3_1_predictions.csv'
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['date', 'prediction'])

    for i in range(len(dates)):
        writer.writerow([dates[i], predictions[i]])
