from flask import Flask, redirect, json
from flask import request
from flask_cors import CORS, cross_origin
from sklearn.externals import joblib

import os
import pprint
pp = pprint.PrettyPrinter()
# import json

import spotipy
from spotipy import oauth2

from hashids import Hashids

app = Flask(__name__)
CORS(app)

clf = joblib.load('src/model.pkl')

appname = 'AppName'

client_id = os.environ['SPOTIPY_CLIENT_ID']
client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
redirect_uri = 'http://127.0.0.1:5000/admin/callback'
scope = 'user-read-private user-top-read playlist-modify-private user-modify-playback-state'

sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
                                scope=scope, cache_path=None)

### Database (lol)
# party_id -> [tokens]
# [(str, [int])]
database = {}
# [(str, [str])]
# party_id -> [track_ids]
playlists = {}

db = {}

### Spotify helper functions


def mod_playlist(party_id, user_id, pl_id, token, mood):
        # remove tracks
        data = sp.user_playlist(user=user_id, playlist_id=pl_id)
        track_ids = []
        for item in data['items']:
                track_ids.append(item['id'])
        sp.user_playlist_remove_specific_occurrences_of_tracks(user_id, pl_id, track_ids)

        # sort
        all_tracks = db[party_id]
        for track in all_tracks:
                score = predict_track(track)
                track['mood'] = abs(score - mood)
        
        result = sorted(all_tracks, key=lambda x: x['mood'])

        trackids = []
        for track in resut[:50]:
                trackids.append(track['id'])

        sp.user_playlist_add_tracks(user_id, pl_id, trackids)


def predict_track(track):
        instrumentalness = track["instrumentalness"]
        acousticness = track["acousticness"]
        energy = track["energy"]
        danceability = track["danceability"]
        loudness = track["loudness"]
        res = clf.predict_proba([[energy, danceability, loudness, acousticness,
                                  instrumentalness]])
        score = round(res[0][0] * 100)
        return score




def get_toplist(token):
        sp = spotipy.Spotify(auth=token)
        data = sp.current_user_top_tracks(limit=50)
        track_id_list = []
        toplist = []
        for item in data['items']:
                track_id = item['id']
                track_id_list.append(track_id)
                toplist.append(item)
        features_list = sp.audio_features(track_id_list)
        for i in range(0, len(data['items'])):
                toplist[i]['features'] = features_list[i]
        return toplist

def add_features(track_ids, token):
        sp = spotipy.Spotify(auth=token)
        features_list = sp.audio_features(track_ids)
        for i in range(0, len(data['items'])):
                toplist[i]['features'] = features_list[i]
        return toplist

### Mood

def mood(tracks):
        if len(tracks) > 50:
                return tracks[:50]
        return tracks

### API

# Play
# Pause
# Skip

# @app.route('/<party_id>/pause')
# @app.route('/<party_id>/skip')

tokens = {}

@app.route('/host_party')
def host_party():
        token = request.args.get('token')
        if token not in tokens:
                hashids = Hashids(salt=token)
                party_id = hashids.encode(1, 2).upper();
                database[party_id] = token
                toplist = get_toplist(token)
                db[party_id] = toplist

                sp = spotipy.Spotify(auth=token)
                user_info = sp.current_user()
                user_id = user_info['id']
                playlist_info = sp.user_playlist_create(user_id, appname, public=False)
                playlist_id = playlist_info['id']
                tracks_sorted = mood(toplist)
                for track in tracks_sorted:
                        trackid_list.append(track['id'])
                sp.user_playlist_add_tracks(user_id, playlist_id, trackid_list)

                playlists[party_id] = {'pl_id': playlist_id, 'user_id': user_id, 'guests': []}
                pp.pprint(playlists)

                tokens[party_id] = token

                return json.dumps({'partyId': party_id})
        else:
                return json.dumps({'partyId': tokens[token]})

@app.route('/join_party/<party_id>')
def join_party(party_id):
        token = request.args.get('token')

        if token in playlists[party_id]['guests']:
                return 'Already in party'
        else:
                toplist = get_toplist(token)
                db[party_id] = toplist

                playlists[party_id]['guests'].append(token)

                admin_token = tokens[party_id]
                sp = spotipy.Spotify(auth=admin_token)
                user_id = playlists[party_id]['user_id']
                playlist_id = playlists[party_id]['pl_id']
                tracks_sorted = mood(toplist)
                trackid_list = []
                for track in tracks_sorted:
                        trackid_list.append(track['id'])

                sp.user_playlist_add_tracks(user_id, playlist_id, trackid_list)
                return 'Success'

@app.route('/test')
def test():
        sample = {
                "acousticness": 0.0861,
                "analysis_url": "https://api.spotify.com/v1/audio-analysis/1JI70l1lE5IF2tgJm5TnMD",
                "danceability": 0.509,
                "duration_ms": 162440,
                "energy": 0.897,
                "id": "1JI70l1lE5IF2tgJm5TnMD",
                "instrumentalness": 0.000634,
                "key": 8,
                "liveness": 0.0625,
                "loudness": -3.418,
                "mode": 0,
                "speechiness": 0.0454,
                "tempo": 149.864,
                "time_signature": 4,
                "track_href": "https://api.spotify.com/v1/tracks/1JI70l1lE5IF2tgJm5TnMD",
                "type": "audio_features",
                "uri": "spotify:track:1JI70l1lE5IF2tgJm5TnMD",
                "valence": 0.283
        }

        return str(predict_track(sample))


@app.route('/playlistid/<party_id>', methods=['GET','POST'])
def play(party_id):
        # token = request.args.get('token')
        # sp = spotipy.Spotify(auth=token)
        # user_id = playlists[party_id]['user_id']
        # playlist_id = playlists[party_id]['pl_id']
        # context = 'spotify:user:spotify:playlist:' + playlist_id
        # sp.start_playback(context_uri=context)
        # return 'Success'
        return playlists[party_id]['pl_id'] 

@app.route('/mood/<party_id>/<level>')
def set_mood(party_id, level):
        token = request.args.get('token')
        sp = spotipy.Spotify(auth=token)
        user_id = playlists[party_id]['user_id']
        pl = sp.user_playlist()
