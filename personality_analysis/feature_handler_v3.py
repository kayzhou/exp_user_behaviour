# -*- coding: utf-8 -*-
__author__ = 'Kay'

import datetime
import json
import os
import re

import numpy as np
import pandas as pd
import pendulum

keywords = [w.strip() for w in open("data/keywords.txt")]


def load_user_data(in_name):
    '''
    载入用户全部数据
    :param in_name:
    :return:
    '''
    user_data = []
    for line in open(in_name):
        line = line.strip()
        user_data.append(json.loads(line))
    return user_data


def static_features(in_name):

    x = []
    for line in open(in_name):
        user = json.loads(line.strip())

    # 最后一行
    if user['gender'] == 'f':
        x.append(1)
    else:
        x.append(2)
    x.append(np.log(float(user['followers_count']) + 1))
    return x


def str2datetime(s):
    return pendulum.parse(s)


def extract_day_series(dts):
    '''
    动态特征, 统计每天时间序列
    :param dts:
    :return:
    '''
    day_series = np.array([0] * 24)
    for dt in dts:
        day_series[dt.hour] += 1
    return day_series


def extract_week_series(dts):
    '''
    动态特征, 统计每周时间序列
    :param dts:
    :return:
    '''
    week_series = np.array([0] * 7)
    for dt in dts:
        week_series[dt.weekday()] += 1
    return week_series


def extract_series_feature(se, cnt):
    '''
    动态特征, 最大值所在, 最大值, 最小值所在, 最小值, 方差
    :param se:
    :return:
    '''
    # 均值, 最大所在, 最大平均, 最小所在, ¡¡¡¡¡平均的方差
    return [se.sum() / cnt, se.argmax(), se.max() / cnt, se.argmin(), (se / cnt).var()]


def extract_tweet_datetime(in_name, action='tweet', output_type='dt'):
    '''
    提取行为日期
    :param in_name:
    :param out_name:
    :return:
    '''
    user_data = load_user_data(in_name)
    if action == 'tweet':
        if output_type == 'dt':
            return [str2datetime(user['publish_dt']) for user in user_data]
        elif output_type == 'str':
            return [str2datetime(user['publish_dt']).strftime('%Y-%m-%d,%H:%M:%S') for user in user_data]

    elif action == 'retweet':
        return [str2datetime(user['publish_dt']) for user in user_data if "//" in str(user["text"])]

    elif action == "at":
        return [str2datetime(user['publish_dt']) for user in user_data if "@" in str(user["text"])]


def extract_how_many_weeks_days(dts):
    '''
    这段时间序列中有几天, 有几周
    :param dts:
    :return:
    '''
    def toMonday(dt):
        # 转成周一
        ndt = dt - datetime.timedelta(days=dt.weekday())
        return datetime.datetime(ndt.year, ndt.month, ndt.day)

    weeks = set()
    days = set()
    for dt in dts:
        weeks.add(toMonday(dt))
        days.add(datetime.datetime(dt.year, dt.month, dt.day))

    return len(weeks), len(days)


def extract_tweet_ave_length(in_name):
    '''
    获取微博的长度
    :param in_name:
    :return:
    '''
    user_data = load_user_data(in_name)
    tweet_length = []

    def remove_retweet(tweet):
        return tweet[:tweet.find("//")]

    def remove_at(tweet):
        del_at = r'@.*?:|@.*?\s|@.*?$'
        tweet = re.sub(del_at, '', tweet)
        return tweet

    def remove_share(tweet):
        tweet = re.sub(r'\(分享自.*?\)', '', tweet)
        return re.sub(r'（分享自.*?）', '', tweet)

    def remove_emoticon(tweet):
        del_emo = r'\[.*?\]'
        return re.sub(del_emo, '', tweet)

    def remove_url(tweet):
        url_pattern = r'http://t.cn/\w+'
        tweet = re.sub(url_pattern, '', tweet)
        return tweet

    def filter(tweet):
        return remove_url(remove_at(remove_share(remove_retweet(tweet))))

    for user in user_data:
        tweet_length.append(len(filter(str(user['text']))))

    tweet_length = np.array(tweet_length)
    # print(tweet_length.mean())
    # print(tweet_length.max())
    # print(tweet_length.argmax())
    # print(tweet_length.min())
    # print(tweet_length.__len__())

    return tweet_length.mean()


def dynamic_features(in_name):
    dts = extract_tweet_datetime(in_name)
    # print(in_name, len(dts))

    # 多少周发送微博, 多少天发送微博 (该周或天发送一条即可)
    cnt_weeks, cnt_days = extract_how_many_weeks_days(dts)
    X = extract_series_feature(extract_day_series(dts), cnt_days) \
        + extract_series_feature(extract_week_series(dts), cnt_weeks)

    # 获取转发的日期时间
    retweet_dts = extract_tweet_datetime(in_name, action='retweet')
    X += (extract_series_feature(extract_day_series(retweet_dts), cnt_days)
          + extract_series_feature(extract_week_series(retweet_dts), cnt_weeks))

    # 获取@的日期时间
    at_dts = extract_tweet_datetime(in_name, action='at')
    X += (extract_series_feature(extract_day_series(at_dts), cnt_days)
          + extract_series_feature(extract_week_series(at_dts), cnt_weeks))

    # 转发比例
    X.append(len(retweet_dts) / (len(dts) + 1))
    # @比例
    X.append(len(at_dts) / (len(dts) + 1))
    # 微博平均长度
    X.append(extract_tweet_ave_length(in_name))
    return X


def text_features(in_name):
    X = [0] * len(keywords)
    users = load_user_data(in_name)
    for u in users:
        line = u["text"]
        for i, kw in enumerate(keywords):
            # print(i, kw)
            pat = re.compile(kw)
            X[i] += len(pat.findall(str(line)))
    return X


def extract_features(in_name):
    X = static_features(in_name)
    X.extend(dynamic_features(in_name))
    X.extend(text_features(in_name))
    return X


def dump_train_data():
    uids = [u[:-4] for u in os.listdir("data/user_data")]
    print(uids)
    psy_data = pd.read_csv("data/psy_test.txt", sep="\t")

    with open('train_data.txt', 'w') as f:
        for row in psy_data.iterrows():
            if str(row[1]['uid']) in uids:
                d = row[1]
                X = [d['uid'], d['neu'], d['ext'], d['ope'], d['agr'], d['con'], d['gender']]
                X.extend(extract_features("data/user_data/{}.txt".format(d['uid'])))
                print(X)
                f.write("\t".join([str(x) for x in X]) + '\n')


if __name__ == "__main__":
    # print(extract_features("data/user_data/1178008717.txt"))
    dump_train_data()
