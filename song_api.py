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


@app.route('/song/<string:song_id>', methods=['GET'])
def get_song(song_id):
    """ Get a song from the database """
    try:
        song = song_mgr.get_song(song_id)
        if song is None:
            raise ValueError(f"Song {song_id} does not exist")

        response = app.response_class(
                status=200,
                response=json.dumps(song.to_dict()),
                mimetype='application/json'
        )
        return response
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=404
        )
        return response


@app.route('/song/all', methods=['GET'])
def get_all_songs():
    """Get all the songs in the database"""
    content = request.json
    songs = song_mgr.get_all_songs()
    response = app.response_class(status=200, response=json.dumps([s.to_dict() for s in songs]),
                                  mimetype='application/json')
    return response


@app.route('/song/all', methods=['DELETE'])
def delete_all_songs():
    """ Delete a song from the DB   """
    try:
        song_mgr.delete_all_songs()
        response = app.response_class(status=200)
    except ValueError as e:
        response = app.response_class(response=str(e), status=404)
    return response


@app.route('/song/<string:song_id>', methods=['PUT'])
def update_song(song_id):
    """ Update the song information  """
    content = request.json

    try:
        song = song_mgr.get_song(song_id)
        song.title = content['title']
        song.artist = content['artist']
        song.album = content['album']
        song.genre = content['genre']
        song.rating = content['rating']
        song_mgr.update_song(song)
        response = app.response_class(
                status=200
        )
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=400
        )

    return response


if __name__ == "__main__":
    app.run(debug=True)