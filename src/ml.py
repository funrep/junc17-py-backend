import numpy as np
import sklearn
from sklearn.preprocessing import Normalizer
import json
  

def convert_to_array(track):
    energy = track["energy"]
    tempo = track["tempo"]
    danceability = track["danceability"]
    loudness = track["loudness"]
    return [energy, tempo, danceability, loudness]


def prepare_data_set(tracks):
    array = []
    for track in tracks:
        array.append(convert_to_array(track))

    final_array = np.array(array)    

    print(final_array)

    X_normalized = sklearn.preprocessing.normalize(final_array, norm='l2')

    print(X_normalized)    


prepare_data_set(json.load(open('lounge_data.json')))
prepare_data_set(json.load(open('club_data.json')))


