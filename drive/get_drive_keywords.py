import os
import json
from collections import Counter

in_dir = '..'

lexicon = Counter()
keywords = ['交通', '开车', '车', '驾驶', '堵车', '高速']

# i = 0
# for in_name in os.listdir(in_dir):
#     i += 1
#     print(i)
#     for line in open(os.path.join(in_dir, in_name)):
#         words = line.strip().split(' ')
#         for w in words:
#             if w in keywords:
#                 for w_0 in words:
#                     lexicon[w_0] += 1
#                 break

# res = sorted(dict(lexicon).items(), lambda k: k[1], reverse=True)
# for r in res:
#     print(r)

for in_name in os.listdir(in_dir):
    _sum = 0
    tweet_count = 0
    count = [0] * len(keywords)
    for line in open(os.path.join(in_dir, in_name)):
        tweet_count += 1
        words = line.strip().split(' ')
        for w in words:
            for i in range(len(keywords)):
                if w == keywords[i]:
                    count[i] = 1
    _sum = sum(count)
    _pro = _sum / tweet_count 
    uid = in_name
    count.append(_sum)
    count.append(_pro)
    print(uid + ',' + ','.join([str(c) for c in count]))
        
