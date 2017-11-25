import numpy as np
import sklearn
from sklearn import svm
from sklearn.externals import joblib
from random import shuffle
import json
  

def convert_to_array(track):
    instrumentalness = track["instrumentalness"]
    acousticness = track["acousticness"]
    energy = track["energy"]
    danceability = track["danceability"]
    loudness = track["loudness"]
    return [energy, danceability, loudness, acousticness, 
            instrumentalness]


def prepare_data_set(tracks):
    array = []
    for track in tracks:
        array.append(convert_to_array(track))

    final_array = np.array(array)    

    return final_array    


norm_lounge = prepare_data_set(json.load(open('data/lounge_data.json')))
norm_club = prepare_data_set(json.load(open('data/club_data.json')))

print("Amount of Lounge tracks: " + str(len(norm_lounge)))
print("Amount of Club tracks: " + str(len(norm_club)))

X = np.concatenate((norm_lounge, norm_club), axis=0)

Y = list()

for i in range(0, len(norm_lounge)):
    Y.append('lounge')

for i in range(0, len(norm_club)):
    Y.append('club')


XY_shuffled = list(zip(X, Y))
shuffle(XY_shuffled)

samples_count = 100

samples_train = XY_shuffled[0: len(XY_shuffled) - samples_count]
samples_eval = XY_shuffled[len(XY_shuffled) - samples_count: len(XY_shuffled)]

X_train = [x[0] for x in samples_train]
X_eval = [x[0] for x in samples_eval]
Y_train = [x[1] for x in samples_train]
Y_eval = [x[1] for x in samples_eval]


clf = svm.SVC(C=1.0, cache_size=200, class_weight="balanced", coef0=0.0,
              decision_function_shape='ovo', degree=3, gamma='auto', kernel='rbf',
              max_iter=-1, probability=True, random_state=None, shrinking=True,
              tol=0.001, verbose=False)
clf.fit(X_train, Y_train)

predicted = clf.predict_proba(X_eval)
score = clf.score(X_eval, Y_eval)
decided = clf.decision_function(X_eval)
expected = Y_eval

joblib.dump(clf, 'model.pkl')

print("Samples: " + str(len(X_train)))

print(score)

