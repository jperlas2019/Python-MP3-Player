from flask import Flask, request
from song_manager import SongManager
from song import Song
import json

app = Flask(__name__)

song_mgr = SongManager('song_db.sqlite')


@app.route('/song', methods=['POST'])
def add_song():
    """Add song to the database/collection"""
    content = request.json
    try:
        song = Song(content['title'], content['artist'], content['runtime'], content['rating'],
                    content['pathname'], content['album'], content['genre'])
        song_mgr.add_song(song)
        response = app.response_class(status=200)
    except ValueError as e:
        response = app.response_class(response=str(e), status=400)
    return response


@app.route('/song/all', methods=['GET'])
def get_all_songs():
    """Get all the songs in the database"""
    content = request.json
    songs = song_mgr.get_all_songs()
    response = app.response_class(status=200, response=json.dumps([s.to_dict() for s in songs]),
                                  mimetype='application/json')
    return response


if __name__ == "__main__":
    app.run(debug=True)