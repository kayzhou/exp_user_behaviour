import numpy as np
from sklearn.externals import joblib
from feature_handler_v3 import extract_features

models = [joblib.load("model/train-{}.m".format(i)) for i in range(0, 6)]

def pred(in_name):
    '''
    预测大五人格
    :param in_name: 某用户的数据文件名
    :return: 外倾性分类（-1，0，1，-1 > 内向，0 > 中性，1 > 外向；
             大五人格分数（0-60，分数越高在该性格倾向上表现更强烈），分别为neuroticism，extraversion，openness，agreeableness，conscientiousness
    '''
    X = np.array(extract_features(in_name)).reshape((1, -1))
    y = {
        'ext_label': int(models[0].predict(X)),
        'neu_score': int(models[1].predict(X)),
        'ext_score': int(models[2].predict(X)),
        'ope_score': int(models[3].predict(X)),
        'agr_score': int(models[4].predict(X)),
        'con_score': int(models[5].predict(X))
    }
    return y



