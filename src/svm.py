import numpy as np

from sklearn.linear_model import SGDClassifier

X = [[0., 0.], [1., 1.]]
y = [0, 1]

clf = SGDClassifier(loss="hinge", penalty="l2")
clf.fit(X, y)
SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
       eta0=0.0, fit_intercept=True, l1_ratio=0.15,
       learning_rate='optimal', loss='hinge', max_iter=10, n_iter=None,
       n_jobs=1, penalty='l2', power_t=0.5, random_state=None,
       shuffle=True, tol=None, verbose=0, warm_start=False)

print(clf.predict([[2., 2.]]))