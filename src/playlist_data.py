import spotipy
import json

token = util.prompt_for_user_token(username, scope)
track_ids = None # json.loads(FILE HERE)

if token:
    sp = spotipy.Spotify(auth=token)
    song_list = []
    for track_id in track_ids:
        track_info = sp.track(track_id)
        track_features = sp.audio_features(track_id)
        track = { 'id': track_id, 'info': track_info, 'features': track_features }
        song_list.append(track)
    filedata = json.dumps(song_list)
    f = open('filename', 'w')
    f.write(filedata)
else:
        print "Can't get token for", username
