import numpy as np
import sklearn
from sklearn.preprocessing import Normalizer
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from random import shuffle
import json
  

def convert_to_array(track):
    energy = track["energy"]
    danceability = track["danceability"]
    loudness = track["loudness"]
    return [energy, danceability, loudness]


def prepare_data_set(tracks):
    array = []
    for track in tracks:
        array.append(convert_to_array(track))

    final_array = np.array(array)    
    normalized = sklearn.preprocessing.normalize(final_array, norm='l2')

    return normalized    


norm_lounge = prepare_data_set(json.load(open('lounge_data.json')))
norm_club = prepare_data_set(json.load(open('club_data.json')))

print("Lounge: " + str(len(norm_lounge)))
print("Club: " + str(len(norm_club)))

X = np.concatenate((norm_lounge, norm_club), axis=0)

Y = list()

for i in range(0, len(norm_lounge)):
    Y.append(0)

for i in range(0, len(norm_club)):
    Y.append(1)


XY_shuffled = list(zip(X, Y))
shuffle(XY_shuffled)

samples_count = 100

samples_train = XY_shuffled[0: len(XY_shuffled) - samples_count]
samples_eval = XY_shuffled[len(XY_shuffled) - samples_count: len(XY_shuffled)]

X_train = [x[0] for x in samples_train]
X_eval = [x[0] for x in samples_eval]
Y_train = [x[1] for x in samples_train]
Y_eval = [x[1] for x in samples_eval]


clf = SGDClassifier(loss="hinge", penalty="l2")
clf.fit(X_train, Y_train)
SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
              eta0=0.0, fit_intercept=True, l1_ratio=0.15,
              learning_rate='optimal', loss='hinge', max_iter=4, n_iter=None,
              n_jobs=1, penalty='l2', power_t=0.5, random_state=None,
              shuffle=True, tol=None, verbose=0, warm_start=False)

predicted = clf.predict(X_eval)
decided = clf.decision_function(X_eval)
expected = Y_eval

print("Samples: " + str(len(X_train)))

print("Predicted: " + metrics.classification_report(expected, predicted))

