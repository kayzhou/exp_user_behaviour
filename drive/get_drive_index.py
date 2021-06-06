# -*- coding: UTF-8 -*-
__author__ = 'Kay Zhou'

import os
import json

keywords = ['交通', '开车', '车', '驾驶', '堵车', '高速']


def uid_2_drive_index(in_dir, uids, label):
    '''
    计算用户的驾驶因子
    :param in_dir:
    :param uids:
    :param label:
    :return:
    '''
    for in_name in uids:
        tweet_count = 0
        count = [0] * len(keywords)
        for line in open(os.path.join(in_dir, in_name)):
            words = json.loads(line)['seg']
            tweet_count += 1
            for w in words:
                for i in range(len(keywords)):
                    if w == keywords[i]:
                        count[i] = 1

        _sum = sum(count)
        _pro = '{:.6f}'.format(_sum / tweet_count)
        uid = in_name
        count.append(_sum)
        count.append(_pro)
        count.append(tweet_count)
        print(uid + ',' + label + ',' + ','.join([str(c) for c in count]))


uid_1 = [line.strip() for line in open('uid/uid_+1.txt')]
uid_0 = [line.strip() for line in open('uid/uid_-1.txt')]
in_dir = '/home/kayzhou/exp/come_on_data/get_weibo_users/data/weibo_0320'

uid_2_drive_index(in_dir, uid_1, '1')
uid_2_drive_index(in_dir, uid_0, '0')
