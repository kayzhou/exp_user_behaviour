import pandas as pd
import pendulum
import json

score = pd.read_csv('data/psy_test.txt', sep='\t')
df = pd.read_excel('data/weibo_uids.xlsx', sheet_name='weibo_uids')
df = df.fillna(0)
# print(df.head())


uids = score['uid']
u_data = {}
for _id in uids:
    u_data[str(_id)] = []

for row in df.iterrows():
    d = dict(row[1])
    uid = d['uid'][1:]
    del d['uid']
    del d['阅读数']
    del d['转发量']
    # print(d)
    u_data[uid].append(d)

for k, v in u_data.items():
    if len(v) < 50:
        continue
    with open('data/user_data/{}.txt'.format(k), 'a') as f:
        # print(k)
        for line in v:
            f.write(json.dumps(line, ensure_ascii=False) + '\n')
    # fol = row[2]
    # print(uid)



