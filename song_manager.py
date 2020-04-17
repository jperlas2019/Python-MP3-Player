from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

from song import Song


class SongManager:

    def __init__(self, song_db):
        """Create Song object and map to the database"""

        if song_db is None or song_db == '':
            raise ValueError('Song database %s not found' % song_db)

        engine = create_engine('sqlite:///' + song_db)
        Base.metadata.bind = engine
        self._db_session = sessionmaker(bind=engine)

    def add_song(self, new_song: Song):
        """Add a new song to the song database"""

        if new_song is None or not isinstance(new_song, Song):
            raise ValueError('Invalid Song Object')

        session = self._db_session()
        session.add(new_song)

        session.commit()

        song_title = new_song.title
        session.close()

        return song_title

    def update_song(self, song):
        """Update existing song to match given, by title"""
        if song is None or not isinstance(song, Song):
            raise ValueError('Invalid Song Object')

        session = self._db_session()

        existing_song = session.query(Song).filter(Song.title == song.title).first()
        if existing_song is None:
            raise ValueError("Song %s does not exist" % song.title)

        existing_song.update(song)

        session.commit()
        session.close()

    def get_song(self, song_title):
        """Return song object matching title"""
        if song_title is None or type(song_title) != str:
            raise ValueError("Invalid Song Title")

        session = self._db_session()

        song = session.query(Song).filter(Song.title == song_title).first()

        session.close()

        return song

    def delete_song(self, song_title):
        """Delete a song from the database"""
        if song_title is None or type(song_title) != str:
            raise ValueError("Invalid Song Title")

        session = self._db_session()

        song = session.query(Song).filter(Song.title == song_title).first()
        if song is None:
            session.close()
            raise ValueError('Song does not exist.')

        session.delete(song)
        session.commit()

        session.close()

    def get_all_songs(self):
        """Return a list of all songs in the database"""
        session = self._db_session()

        all_songs = session.query(Song).all()

        session.close()

        return all_songs

    def delete_all_songs(self):
        """ Delete all students from the database """
        session = self._db_session()
        session.query(Song).delete()
        session.commit()
        session.close()




