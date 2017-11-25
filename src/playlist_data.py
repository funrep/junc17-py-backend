import spotipy
import spotipy.util as util
import json

import os
from json.decoder import JSONDecodeError

current_file = input()


def get_track_ids(fname):
    tracks = list()
    data = json.load(open(fname))
    for d in data:
        for element in d['items']:
            #print(element['track']['id'])
            tracks.append(element['track']['id'])

    return tracks

username = "alex@mcserver.se"
track_ids = get_track_ids(current_file + ".json")
track_ids_lounge = get_track_ids
 
#Temp-fix cache bug
try:
    token = util.prompt_for_user_token(username)
except(AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)



if token:
    sp = spotipy.Spotify(auth=token)

    tracks_features = list()

    steps = len(track_ids) / 40
    for i in range(0, len(track_ids), 40):
        tracks_features += sp.audio_features(track_ids[i : max(i, i + 40)])

    filedata = json.dumps(tracks_features)

    f = open(current_file + '_data.json', 'w')
    f.write(filedata)
    print("Saved file!")
else:
        print ("Can't get token")
