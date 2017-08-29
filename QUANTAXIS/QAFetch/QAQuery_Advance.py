# coding: utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import datetime

import numpy
import pandas as pd
from bson.objectid import ObjectId
from pandas import DataFrame
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_date_stamp,
                              QA_util_date_valid, QA_util_log_info,
                              QA_util_time_stamp)
from QUANTAXIS.QAData import QA_data_make_hfq,QA_data_make_qfq,QA_DataStruct_Stock_day
"""
按要求从数据库取数据，并转换成numpy结构

"""


def QA_fetch_stock_day_adv(code, __start, __end,collections=QA_Setting.client.quantaxis.stock_day):
    '获取股票日线'
    __start = str(__start)[0:10]
    __end = str(__end)[0:10]

    if QA_util_date_valid(__end) == True:
        __data = []
        for item in collections.find({
            'code': str(code)[0:6], "date_stamp": {
                "$lte": QA_util_date_stamp(__end),
                "$gte": QA_util_date_stamp(__start)}}):
            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['vol']), item['date']])
        __data = DataFrame(__data, columns=[
            'code', 'open', 'high', 'low', 'close', 'volume', 'date'])
        __data['date'] = pd.to_datetime(__data['date'])
        __data = __data.set_index('date', drop=False)
        return QA_DataStruct_Stock_day(__data)
    else:
        QA_util_log_info('something wrong with date')


def QA_fetch_index_day_adv(code, __start, __end, format_='numpy', collections=QA_Setting.client.quantaxis.stock_day):
    '获取指数日线'
    # print(datetime.datetime.now())
    __start = str(__start)[0:10]
    __end = str(__end)[0:10]

    if QA_util_date_valid(__end) == True:

        __data = []

        for item in collections.find({
            'code': str(code), "date_stamp": {
                "$lte": QA_util_date_stamp(__end),
                "$gte": QA_util_date_stamp(__start)
            }
        }):
            # print(item['code'])

            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['volume']), item['date']])
        if format_ in ['n', 'N', 'numpy']:
            __data = numpy.asarray(__data)
        elif format_ in ['list', 'l', 'L']:
            __data = __data
        elif format_ in ['P', 'p', 'pandas', 'pd']:
            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])
            __data['date'] = pd.to_datetime(__data['date'])
            __data = __data.set_index('date')

        return __data
    else:
        QA_util_log_info('something wrong with date')


def QA_fetch_stock_min_adv(code, startTime, endTime, format_='numpy', type_='1min', collections=QA_Setting.client.quantaxis.stock_min):
    '获取股票分钟线'
    if type_ in ['1min', '1m']:
        type_ = '1min'
    elif type_ in ['5min', '5m']:
        type_ = '5min'
    elif type_ in ['15min', '15m']:
        type_ = '15min'
    __data = []
    for item in collections.find({
        'code': str(code), "time_stamp": {
            "$gte": QA_util_time_stamp(startTime),
            "$lte": QA_util_time_stamp(endTime)
        },'type':type_
    }):

        __data.append([str(item['code']), float(item['open']), float(item['high']), float(
            item['low']), float(item['close']), float(item['vol']), item['datetime'], item['time_stamp'], item['date']])
    
    __data = DataFrame(__data, columns=[
        'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])
    
    __data['datetime'] = pd.to_datetime(__data['datetime'])
    __data = __data.set_index('datetime', drop=False)
    #res = QA_fetch_stock_to_fq(__data)
    if format_ in ['numpy', 'np', 'n']:
        return numpy.asarray(__data)
    elif format_ in ['list', 'l', 'L']:
        return numpy.asarray(__data).tolist()
    elif format_ in ['P', 'p', 'pandas', 'pd']:
        return __data


