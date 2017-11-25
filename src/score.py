sample_track_1 = {
  "danceability": 0.696,
  "energy": 0.905,
  "key": 2,
  "loudness": -2.743,
  "mode": 1,
  "speechiness": 0.103,
  "acousticness": 0.011,
  "instrumentalness": 0.000905,
  "liveness": 0.302,
  "valence": 0.625,
  "tempo": 114.944,
  "type": "audio_features",
  "id": "11dFghVXANMlKmJXsNCbNl",
  "uri": "spotify:track:11dFghVXANMlKmJXsNCbNl",
  "track_href": "https://api.spotify.com/v1/tracks/11dFghVXANMlKmJXsNCbNl",
  "analysis_url": "https://api.spotify.com/v1/audio-analysis/11dFghVXANMlKmJXsNCbNl",
  "duration_ms": 207960,
  "time_signature": 4
}

sample_track_2 = {
  "danceability": 0.5,
  "energy": 0.5,
  "key": 2,
  "loudness": -2.743,
  "mode": 1,
  "speechiness": 0.103,
  "acousticness": 0.011,
  "instrumentalness": 0.000905,
  "liveness": 0.302,
  "valence": 0.625,
  "tempo": 114.944,
  "type": "audio_features",
  "id": "a1dFghVXANMlKmJXsNCbNl",
  "uri": "spotify:track:11dFghVXANMlKmJXsNCbNl",
  "track_href": "https://api.spotify.com/v1/tracks/11dFghVXANMlKmJXsNCbNl",
  "analysis_url": "https://api.spotify.com/v1/audio-analysis/11dFghVXANMlKmJXsNCbNl",
  "duration_ms": 207960,
  "time_signature": 4
}

sample_track_3 = {
  "danceability": 0.5,
  "energy": 0.5,
  "key": 2,
  "loudness": -2.743,
  "mode": 1,
  "speechiness": 0.103,
  "acousticness": 0.011,
  "instrumentalness": 0.000905,
  "liveness": 0.302,
  "valence": 0.625,
  "tempo": 114.944,
  "type": "audio_features",
  "id": "c1dFghVXANMlKmJXsNCbNl",
  "uri": "spotify:track:11dFghVXANMlKmJXsNCbNl",
  "track_href": "https://api.spotify.com/v1/tracks/11dFghVXANMlKmJXsNCbNl",
  "analysis_url": "https://api.spotify.com/v1/audio-analysis/11dFghVXANMlKmJXsNCbNl",
  "duration_ms": 207960,
  "time_signature": 4
}

guest_playlists = list()

sample_playlist_1 = list()
sample_playlist_2 = list()

sample_playlist_1.append(sample_track_1)
sample_playlist_1.append(sample_track_2)


sample_playlist_2.append(sample_track_1)
sample_playlist_2.append(sample_track_3)
sample_playlist_2.append(sample_track_3)
sample_playlist_2.append(sample_track_3)

guest_playlists.append(sample_playlist_1)
guest_playlists.append(sample_playlist_2)


track_count = dict()

track_map = dict()

for playlist in guest_playlists:
    
    for track in playlist:
        track_id = track["id"]
        track_map[track_id] = track
        if(track_id in track_count): 
            track_count[track_id] += 1
        else: 
            track_count[track_id] = 1

track_count_sorted_list = sorted(track_count.items(), key=lambda tup : tup[1], reverse=True)

print(track_count_sorted_list)

def normalize(value, min, max):
    return (value - min) / (max - min)

def calculate_score(track):
    normalized_loudness = normalize(track["loudness"], -60, 0)
    normalized_tempo = normalize(track["loudness"], 10,200)

    score_danceability = abs(track["danceability"] - mean_danceability) * importance_danceability
    score_loudness = abs(normalized_loudness - mean_loudness) * importance_loudness
    score_tempo = abs(normalized_tempo - mean_tempo) * importance_tempo
    score_energy = abs(track["energy"] - mean_energy) * importance_energy

    return score_danceability + score_loudness + score_tempo + score_energy

mood = 0.5

mean_danceability = 0.5
mean_loudness = 0.5
mean_tempo = 0.5
mean_energy = 0.5


importance_danceability = 1 / mood
importance_loudness = 0.5
importance_tempo = 1 / mood
importance_energy = 1 / mood
importance_popularity = 0.1


guest_playlist = track_count_sorted_list

guest_playlist_scored = dict()

for track_tup in guest_playlist:
    track = track_map[track_tup[0]]
    guest_playlist_scored[track["id"]] = calculate_score(track)


print(guest_playlist_scored)






