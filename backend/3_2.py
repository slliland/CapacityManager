# -*- coding: utf-8 -*-
import json

import pandas as pd
import statsmodels.api as sm
import numpy as np
import csv


def capacity_management_algorithm_days(day, hour, duration):
    if duration <= 1:
        duration += 1

    time_data = []
    capacity_data = []

    def get_data(file_number, day, hour):
        file_name = '3_2_' + str(file_number) + '.csv'
        # 获取数据
        data = pd.read_csv(file_name)

        time = []
        capacity = []
        for i in range(len(data['date'])):
            date = str(data['date'][i]).split(':')[0]
            d = date.split(' ')[0]
            h = date.split(' ')[1]
            if d == day and h == hour:
                while date.split(' ')[1] == hour:
                    time_data.append(date)
                    capacity_data.append(data['value'][i])
                    i += 1
                    if i < len(data['date']):
                        date = str(data['date'][i]).split(':')[0]
                    else:
                        break
                break
        return time, capacity

    for i in range(5):
        data = get_data(i + 1, day, hour)
        time_data += data[0]
        capacity_data += data[1]

    # 创建一个新的数据框, 并将时间序列数据和容量数据添加到其中
    data_frame = pd.DataFrame(
        {
            'date': time_data,
            'value': capacity_data
        }
    )

    # 创建 ARIMA 模型
    model = sm.tsa.ARIMA(data_frame['value'],
                         order=(2, 1, 1))

    # 训练 ARIMA 模型
    ARIMA_model = model.fit()

    # 预测容量需求
    predictions = ARIMA_model.predict(start=len(data_frame['value']),
                                      end=len(data_frame['value']) + duration - 1,
                                      dynamic=False
                                      )

    predictions = predictions.array
    if duration <= 2:
        duration -= 1
    return predictions[0: duration]


def get_predictions(day, hour, duration=10):
    return capacity_management_algorithm_days(day, hour, duration)


def get_upper_and_lower_bound(predictions):
    predictions = predictions[predictions > 0]
    return [np.max(predictions), np.min(predictions)]


def get_prediction(predictions):
    return predictions.mean()


days = []
for day in range(6, 21 + 1):
    days.append(str(day))

hours = []
for hour in range(0, 24):
    hours.append(str(hour))

dates = []
upper_bounds = []
lower_bounds = []
predictions = []

for day in days:
    for hour in hours:
        if day == '6' and int(hour) < 21:
            continue

        if day == '21' and int(hour) > 21:
            continue

        p = get_predictions('2023/4/' + day, hour)
        dates.append('2023/4/' + day + ' ' + hour)
        bounds = get_upper_and_lower_bound(p)
        upper_bounds.append(float(bounds[0]))
        lower_bounds.append(float(bounds[1]))
        predictions.append(float(get_prediction(p)))
        print('2023/4/' + day + ' ' + hour, 'success.')

print('Begin to generate json file...')

data = {'date': dates,
        'upper_bound': upper_bounds,
        'lower_bound': lower_bounds,
        'prediction': predictions
        }

with open('3_2_predictions.json', 'w') as file:
    json.dump(data, file)
