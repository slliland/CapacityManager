# -*- coding: utf-8 -*-
import random
import pandas as pd
import statsmodels.api as sm
from scipy import interpolate

# 默认集群
cluster = 1
# 当前值
currents = []


def get_dates_from_duration(start_date, duration):
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # 解析起始日期
    start_month, start_day = map(int, start_date.split('-'))
    current_month = start_month
    current_day = start_day

    # 存储结果的列表
    result_dates = []

    # 循环添加日期
    for _ in range(duration):
        # 格式化当前日期并添加到结果列表中
        current_date = "{:02d}-{:02d}".format(current_month, current_day)
        result_dates.append(current_date)

        # 增加一天
        current_day += 1

        # 如果当前日期超过了当前月份的天数，则进入下一个月
        if current_day > days_in_month[current_month - 1]:
            current_month += 1
            current_day = 1

            # 如果当前月份超过12，则进入下一年的1月份
            if current_month > 12:
                current_month = 1

    return result_dates


# 生成当前数据
def generate_current_data(capacity_data, duration):
    current = []
    capacity_data_length = len(capacity_data)
    # 随机生成开始点位
    random_start = random.randint(0, capacity_data_length)

    if (random_start + 100) in range(capacity_data_length - 200, capacity_data_length):
        random_start /= 10
        random_start = int(random_start)

    if duration == 0:
        index = capacity_data[random.uniform(0, 100)]
        current.append(capacity_data[index])
    else:
        for i in range(random_start, random_start + duration):
            # 随机选择正常/放大/缩小
            random_option = random.randint(-1, 1)
            index = i
            # 正常范围
            if random_option == 0:
                current.append(capacity_data[index])
            # 放大
            elif random_option == 1:
                current.append(capacity_data[index] * 10000)
            # 缩小
            elif random_option == -1:
                current.append(capacity_data[index] * 0.000000001)
    return current


# 容量管理算法
def capacity_management_algorithm_days(date, duration):
    if duration <= 1:
        duration += 1

    # 获取数据
    # 为方便，固定路径
    path = r"D:\Downloads\CapacityManager-main1\backend\31\0{}.xlsx".format(cluster)
    data = pd.read_excel(path)

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

    # 获取当前值
    global currents
    currents = generate_current_data(data['used_value'], duration)

    if len(time_data) <= 2:
        time_data += time_data
        capacity_data += capacity_data

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


# 容量管理算法 小时级
def capacity_management_algorithm_hours(date, duration):
    if duration <= 1:
        duration += 1

    # 获取数据
    # 为方便，固定路径
    path = r"D:\Downloads\CapacityManager-main1\backend\31\0{}.xlsx".format(cluster)
    data = pd.read_excel(path)

    # 将数据分成时间序列数据和容量数据
    time_data = []
    capacity_data = []

    for i in range(len(data['collect_time'])):
        if str(data['collect_time'][i])[5:10] == date:
            for j in range(7):
                time_data.append(data['collect_time'][i])
                capacity_data.append(data['used_value'][i])
                i += 1
                if i >= len(data['collect_time']):
                    break

    # 获取当前值
    global currents
    currents = generate_current_data(data['used_value'], duration)

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

    start_index = len(data_frame['used_value']) - 1
    end_index = start_index + duration

    # 预测容量需求
    predictions = ARIMA_model.predict(start=start_index, end=end_index, dynamic=False)

    predictions = predictions.array
    if duration <= 2:
        duration -= 1
    return predictions[0: duration]


# 接收输入
def get_input(date, range_value, cluster_value):
    # 预测时长
    duration = range_value
    # 集群
    global cluster
    cluster = cluster_value

    if range_value == 0:
        # 小时级预测
        values = capacity_management_algorithm_hours(date, 1).to_numpy()
    else:
        # 日月天级预测
        values = capacity_management_algorithm_days(date, duration).to_numpy()

    # 预测
    predictions = []
    # 告警
    warnings = []

    for i in range(duration):
        predictions.append(round(float(values[i] * random.uniform(0.01, 100)), 3))
        if currents[i] > predictions[i]:
            warnings.append('超出预测值')
        else:
            warnings.append('未超出预测值')

    if duration != 0:
        dates = get_dates_from_duration(date, duration)
    else:
        dates = [date]
        predictions.append(round(float(values[0]), 3))

        if currents[0] > predictions[0]:
            warnings.append('超出预测值')
        else:
            warnings.append('未超出预测值')

    result = {
        'dateArray': dates,  # 从1到10的数组
        'valueArray': predictions,  # 从10到20的数组
        'warnArray': warnings
    }
    return result
