# -*- coding: utf-8 -*-
__author__ = 'Kay'

import numpy as np
from sklearn.datasets import load_svmlight_file
from sklearn.externals import joblib
from sklearn.metrics import f1_score
from sklearn.model_selection import (GridSearchCV, cross_val_score,
                                     train_test_split)
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

def ca_svm(in_name, out_model_name, C, gamma):
    print(in_name)
    X, y = load_svmlight_file(in_name)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=23)
    clf = SVC(C=C, gamma=gamma, probability=True)
    # clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    print('训练数据上的表现 =', clf.score(X_train, y_train))
    cvs = cross_val_score(clf, X_train, y_train, cv=5).mean()
    print('5次5折交叉检验 =', cvs)
    y_hat = clf.predict(X_test)
    print('预测结果 =', y_hat)
    print('实际结果 =', y_test)
    # print('F1 score =', f1_score(y, y_hat))
    print('F1 score =', f1_score(y_test, y_hat, average='macro'))

    clf = SVC(C=C, gamma=gamma, probability=True)
    clf.fit(X, y)
    joblib.dump(clf, out_model_name)


def ca_svm_grid(in_name):
    '''
    自动选择最好的参数
    :param in_name:
    :param out_model_name:
    :return:
    '''
    print(in_name)
    X, y = load_svmlight_file(in_name)
    param_grid = {'C': np.logspace(-10, 10, num=21, base=2),
                  'gamma': np.logspace(-10, 10, num=21, base=2)}
    # param_grid = {'C': np.logspace(-5, 5, num=11, base=2),
    #               'gamma': np.logspace(-5, 5, num=11, base=2)}
    clf = SVC(probability=True)
    # clf = GridSearchCV(clf, param_grid, scoring='f1', cv=5)
    # clf = GridSearchCV(clf, param_grid, scoring='log_loss', cv=5)
    clf = GridSearchCV(clf, param_grid, cv=5)
    clf.fit(X, y)
    print('最优交叉验证结果:', clf.best_score_)
    print('最优参数:', clf.best_params_)

    y_hat = clf.predict(X)
    print('预测结果 =', y_hat)
    # print('实际结果 =', y)
    # joblib.dump(clf, out_model_name)
    print('F1 score =', f1_score(y, y_hat, average='macro'))
    # print('F1 score =', f1_score(y, y_hat))
    print('训练数据上的表现 =', clf.score(X, y))


def svm_predict(in_name, model):
    clf = joblib.load(model)
    for line in open(in_name):
        X = np.array([[float(x) for x in line.strip()[11:].split(' ')]])
        y = clf.predict(X)
        # y_pro = clf.predict_proba(X)
        # print(line[:10], y, y_pro)
        # if y[0] == -1:
        #     print(line[:10], y_pro[0][0], y_pro[0][1], y_pro[0][2])
        if y[0] != 0:
            print(line[:10], y[0])


if __name__ == '__main__':

    # ca_svm_grid('data-2.txt')
    ca_svm('data-2.txt', 'model/train-0.m', 2.0, 0.0078125)
    # svm_predict('data/features/large_IGNORE_404.txt', 'model/svm_404_features_4.mod')
