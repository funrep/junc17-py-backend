from flask import Flask, redirect, json
from flask import request
from flask_cors import CORS, cross_origin

import os
# import json

import spotipy
from spotipy import oauth2

from hashids import Hashids

app = Flask(__name__)
CORS(app)

appname = 'AppName'

client_id = os.environ['SPOTIPY_CLIENT_ID']
client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
redirect_uri = 'http://127.0.0.1:5000/admin/callback'
scope = 'user-read-private user-top-read playlist-modify-private'

sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
                                scope=scope, cache_path=None)

### Database (lol)
# party_id -> [tokens]
# [(str, [int])]
database = {}
# [(str, [str])]
# party_id -> [track_ids]
playlists = {}

### Spotify helper functions

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
                playlists[party_id] = toplist

                sp = spotipy.Spotify(auth=token)
                user_info = sp.current_user()
                user_id = user_info['id']
                playlist_info = sp.user_playlist_create(user_id, appname, public=False)
                playlist_id = playlist_info['id']
                tracks_sorted = mood(playlists[party_id])
                trackid_list = []
                for track in tracks_sorted:
                        trackid_list.append(track['id'])
                sp.user_playlist_add_tracks(user_id, playlist_id, trackid_list)

                playlists['party_id'] = {'pl_id': playlist_id, 'user_id': user_id}

                tokens[token] = party_id

                return json.dumps({'partyId': party_id})
        else:
                return json.dumps({'partyId': tokens[token]})

@app.route('/add_guest/<party_id>')
def add_guest(party_id):
        token = request.args.get('token')

        toplist = get_toplist(token)
        
        sp = spotipy.Spotify(auth=token)
        user_id = playlists[party_id]['user_id']
        playlist_id = playlist[playlist_id]['pl_id']
        tracks_sorted = mood(toplist)
        trackid_list = []
        for track in tracks_sorted:
                trackid_list.append(track['id'])
        sp.user_playlist_add_tracks(user_id, playlist_id, trackid_list)
        return 'Added guest to ' + party_id

 

@app.route('/<party_id>/create')
def create(party_id):
        token = database[token]

        admin_token = database[party_id][0]
        sp = spotipy.Spotify(auth=admin_token)
        user_info = sp.current_user()
        user_id = user_info['id']
        playlist_info = user_playlist_create(user_id, 'temp', public=False)
        playlist_id = playlist_info['id']
        tracks_sorted = mood(playlists[party_id])
        trackid_list = []
        for track in tracks_sorted:
                trackid_list.append(track['id'])
        sp.user_playlist_add_tracks(user_id, playlist_id, trackid_list)

@app.route('/update/<party_id>/<guest_count>')
def update(party_id, guest_count):
        guest_tokens = database[party_id]
        curr_guest_count = len(guest_tokens)
        if curr_guest_count > guest_count:
                # new guests
                # retrieve playlists
                toplists = []
                for i in range(guest_count, curr_guest_count):
                        toplist = get_toplist(guest_tokens[i])
                        toplists.append(toplist)
                return json.dumps[toplists]
        else:
                return json.dumps([])

### Autharization

@app.route('/guest/<party_id>/<username>')
def add_guest2(party_id, username):
        cache_path = None or ".cache-" + username
        token_info = sp_oauth.get_cached_token()
        if not token_info:
                auth_url = sp_oauth.get_authorize_url()
                return redirect(auth_url)
        else:
                database[party_id] = token_info['access_token']
                toplist = get_toplist[token_info['access_token']]
                playlists[party_id].extend(toplist)
                return 'Successfully connected to ' + party_id + '.'

@app.route('/guest/callback')
def guest_callback():
        code = request.args.get('code')
        token_info = sp_oauth.get_access_token(code)
        database[party_id] = token_info['access_token']
        toplist = get_toplist[token_info['access_token']]
        playlists[party_id].extend(toplist)
        return 'Successfully connected to ' + party_id + '.'

@app.route('/admin/<username>')
def auth(username):
        cache_path = None or ".cache-" + username
        token_info = sp_oauth.get_cached_token()
        if not token_info:
                auth_url = sp_oauth.get_authorize_url()
                return redirect(auth_url)
        else:
                hashids = Hashids(salt=token_info['access_token'])
                party_id = hashids.encode(1, 2);
                database[party_id] = [token_info['access_token']]
                toplist = get_toplist[token_info['access_token']]
                playlists[party_id] = toplist
                return party_id

@app.route('/admin/callback')
def auth_callback():
        code = request.args.get('code')
        token_info = sp_oauth.get_access_token(code)
        hashids = Hashids(salt=token_info['access_token'])
        party_id = hashids.encode(1, 2);
        database[party_id] = [token_info['access_token']]
        toplist = get_toplist(token_info['access_token'])
        playlists[party_id] = toplist

        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_info = sp.current_user()
        user_id = user_info['id']
        playlist_info = sp.user_playlist_create(user_id, appname, public=False)
        playlist_id = playlist_info['id']
        tracks_sorted = mood(playlists[party_id])
        trackid_list = []
        for track in tracks_sorted:
                trackid_list.append(track['id'])
        sp.user_playlist_add_tracks(user_id, playlist_id, trackid_list)

        return party_id
