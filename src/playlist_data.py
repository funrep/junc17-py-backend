import spotipy
import spotipy.util as util
import json

import os
from json.decoder import JSONDecodeError


def get_track_ids(fname):
    tracks = list()
    data = json.load(open(fname))
    for element in data[0]['items']:
        #print(element['track']['id'])
        tracks.append(element['track']['id'])

    return tracks

username = "alex@mcserver.se"
track_ids = get_track_ids("club.json")

#Temp-fix cache bug
try:
    token = util.prompt_for_user_token(username)
except(AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)



if token:
    sp = spotipy.Spotify(auth=token)

    tracks_features = sp.audio_features(track_ids)
    filedata = json.dumps(tracks_features)

    f = open('data.json', 'w')
    f.write(filedata)
else:
        print ("Can't get token")
