from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn.datasets import dump_svmlight_file


####3.1决策树回归####
from sklearn import tree
model_1 = tree.DecisionTreeRegressor()
####3.2线性回归####
from sklearn import linear_model
model_2 = linear_model.LinearRegression()
####3.3SVM回归####
from sklearn import svm
model_3 = svm.SVR()
####3.4KNN回归####
from sklearn import neighbors
model_4 = neighbors.KNeighborsRegressor()
####3.5随机森林回归####
from sklearn import ensemble
model_5 = ensemble.RandomForestRegressor(n_estimators=20) #这里使用20个决策树
####3.6Adaboost回归####
from sklearn import ensemble
model_6 = ensemble.AdaBoostRegressor(n_estimators=50) #这里使用50个决策树
####3.7GBRT回归####
from sklearn import ensemble
model_7 = ensemble.GradientBoostingRegressor(n_estimators=100) #这里使用100个决策树
####3.8Bagging回归####
from sklearn.ensemble import BaggingRegressor
model_8 = BaggingRegressor()
####3.9ExtraTree极端随机树回归####
from sklearn.tree import ExtraTreeRegressor
model_9 = ExtraTreeRegressor()

dict_models = {
    # "DT": model_1,
    # "LR": model_2,
    # "SVR": model_3,
    # "KNN": model_4,
    "RF": model_5,
    # "Adaboot": model_6,
    # "GBR": model_7,
    # "Bagging": model_8,
    # "ETR": model_9
}

def load(i):
    Y = []
    X = []

    for line in open('train_data.txt'):
        values = line.strip().split('\t')
        y = float(values[i])
        x = [float(v) for v in values[6:]]
        # print(y, x)
        if y < 35.25:
            y = -1
        elif y < 42.81:
            y = 0
        else:
            y = 1
        Y.append(y)
        X.append(x)
    return X, Y


def train(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(score)
    result = model.predict(X_test)
    print(result)
    return model


if __name__ == "__main__":
    for i in range(1, 6):
        print(' ------------------------', '-', '------------------------ ')
        print('|                        ', i, '                        |')
        print(' ------------------------', '-', '------------------------ ')
        X, Y = load(i)
        if i == 2:
            dump_svmlight_file(X, Y, "data-{}.txt".format(i))

        # X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=23)

        # for name, model in dict_models.items():
        #     print('---------------------- {} ----------------------'.format(name))
        #     m = train(model, X, X, Y, Y)
        #     joblib.dump(m, "train-{}.m".format(i))
        #     train(model, X_train, X_test, y_train, y_test)