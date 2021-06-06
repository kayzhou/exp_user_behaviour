import numpy as np
from sklearn.externals import joblib
from feature_handler_v3 import extract_features


models = [joblib.load("model/train-{}.m".format(i)) for i in range(1, 6)]

def pred(in_name):
    '''
    预测大五人格
    :param in_name: 某用户的数据文件名
    :return: 大五人格分数，分别为neuroticism，extraversion，openness，agreeableness，conscientiousness
    '''
    X = np.array(extract_features(in_name)).reshape((1, -1))
    y = [int(m.predict(X)) for m in models]
    return y


print(pred("user_data.txt"))



