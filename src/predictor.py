from sklearn.externals import joblib
import sklearn

clf = joblib.load('model.pkl') 

sample_track = {
  "danceability": 0.574,
  "energy": 0.968,
  "key": 7,
  "loudness": -2.741,
  "mode": 1,
  "speechiness": 0.262,
  "acousticness": 0.0112,
  "instrumentalness": 0.245,
  "liveness": 0.371,
  "valence": 0.164,
  "tempo": 174.047,
  "type": "audio_features",
  "id": "5n6V83Uc992A8NTdiX4uqy",
  "uri": "spotify:track:5n6V83Uc992A8NTdiX4uqy",
  "track_href": "https://api.spotify.com/v1/tracks/5n6V83Uc992A8NTdiX4uqy",
  "analysis_url": "https://api.spotify.com/v1/audio-analysis/5n6V83Uc992A8NTdiX4uqy",
  "duration_ms": 321379,
  "time_signature": 4
  }


def predict(mood, track):
    time_signature = track["time_signature"]
    instrumentalness = track["instrumentalness"]
    acousticness = track["acousticness"]
    energy = track["energy"]
    danceability = track["danceability"]
    loudness = track["loudness"]
    res = clf.predict_proba([[energy, danceability, loudness, acousticness,
                              instrumentalness, time_signature]])
    score = round(res[0][0] * 100)
    print(score)
    return score

score_prediction = predict(0, sample_track)

