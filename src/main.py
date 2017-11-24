from flask import Flask, redirect
from flask import request

import os
import json

import spotipy
from spotipy import oauth2

app = Flask(__name__)

client_id = os.environ['SPOTIPY_CLIENT_ID']
client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
redirect_uri = 'http://127.0.0.1:5000/auth/callback'
scope = 'user-read-private user-top-read'

sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
                                scope=scope, cache_path=None)

### API

@app.route('/toplist')
def toplist():
        token = request.args.get('token')
        sp = spotipy.Spotify(auth=token)
        data = sp.current_user_top_tracks(limit=50)
        toplist = []
        for item in data['items']:
                track_id = item['id']
                features = sp.audio_features([track_id])
                item['features'] = features
                toplist.append(item)
        return json.dumps(toplist)

### Autharization

@app.route('/auth/<username>')
def auth(username):
        cache_path = None or ".cache-" + username
        token_info = sp_oauth.get_cached_token()
        if not token_info:
                auth_url = sp_oauth.get_authorize_url()
                return redirect(auth_url)
        else:
                return token_info['access_token']

@app.route('/auth/callback')
def auth_callback():
        code = request.args.get('code')
        token_info = sp_oauth.get_access_token(code)
        return token_info['access_token']
