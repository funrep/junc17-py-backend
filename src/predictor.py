from sklearn.externals import joblib

clf = joblib.load('model.pkl') 


def predict(track):
    instrumentalness = track["instrumentalness"]
    acousticness = track["acousticness"]
    energy = track["energy"]
    danceability = track["danceability"]
    loudness = track["loudness"]
    res = clf.predict_proba([[energy, danceability, loudness, acousticness,
                              instrumentalness]])
    score = round(res[0][0] * 100)
    return score

