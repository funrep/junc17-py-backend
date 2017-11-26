# Junction 17 - Partify

Queueing songs at a party is always a struggle. Our solution: generate a playlist automatically using machine learning based on the users favorite tracks and the mood of the party.

## How it works

We analyzed songs labelled by their playlists titles to determine what metadata parameters determines the mood and feel of a song, from calm (lounge) to intense (club). For this we used a Support Vector Machine model. 

react, spotify api, scikit/learn
Using the Spotify API and the library

The Backend is built using Python and Flask library. The tracks are classified with a Support Vector Machine with regularization in SciKit Learn. Frontend wise we’ve used React and Redux. All the data is fetched using the Spotify API.

## Setup

```
export SPOTIPY_CLIENT_ID='xxx'
export SPOTIPY_CLIENT_SECRET='yyy'
pip install flask sklearn spotipy # deps (see requirements.txt)
export FLASK_APP=src/main.py
flask run
````

## License

Copyright Team D-0x10

(TBA)
