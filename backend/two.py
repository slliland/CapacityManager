# -*- coding: utf-8 -*-
import pandas as pd
import statsmodels.api as sm
import numpy as np
import json


# 生成当前数据
def generate_current_data(capacity_data, duration):
    current = []
    for index in range(duration):
        current.append(capacity_data[index] * 1.00001)

    return current


# 容量管理算法
def capacity_management_algorithm_days(day, hour, duration):
    if duration <= 1:
        duration += 1

    time_data = []
    capacity_data = []

    def get_data(day, hour):
        # 获取数据
        # '32.csv' 与 two.py 文件在同一层级
        data = pd.read_csv('32.csv')

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

    data = get_data(day, hour)
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


# 获取预测结果
def get_predictions(day, hour, duration=10):
    return capacity_management_algorithm_days(day, hour, duration)


# 获取上界和下界
def get_upper_and_lower_bound(predictions):
    predictions = predictions[predictions > 0]
    return [np.max(predictions), np.min(predictions)]


# 获取预测值
def get_prediction(predictions):
    return predictions.mean()


days = []
for day in range(6, 21 + 1):
    days.append(str(day))

hours = []
for hour in range(0, 24):
    hours.append(str(hour))

# 日期
dates = []
# 预测上界
upper_bounds = []
# 预测下届
lower_bounds = []
# 预测值
predictions = []

# 遍历日期和小时
for day in days:
    for hour in hours:
        if day == '6' and int(hour) < 21:
            continue

        if day == '21' and int(hour) > 21:
            continue

        # 获取预测值
        p = get_predictions('2023/4/' + day, hour)
        # 存入日期
        dates.append('2023/4/' + day + ' ' + hour)
        # 获取界限
        bounds = get_upper_and_lower_bound(p)
        upper_bounds.append(float(bounds[0]))
        lower_bounds.append(float(bounds[1]))
        # 存入预测值
        predictions.append(float(get_prediction(p)))

# 读入数据
# '32.csv' 与 two.py 文件在同一层级
data = pd.read_csv('32.csv')
# 当前值
currents = generate_current_data(data['value'], len(data['date']))

warnings = []
for i in range(len(dates)):
    warning = '未超出界限'
    if currents[i] > upper_bounds[i]:
        warning = '超出上界'
    if currents[i] < lower_bounds[i]:
        warning = '超出下界'
    warnings.append(warning)

# 构造输出数据
data = {'xData': dates,
        'y1Data': upper_bounds,
        'y2Data': lower_bounds,
        'y3Data': predictions,
        'warn': warnings
        }

# 将数据保存为 JSON 文件
with open("3_2_predictions.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False)
