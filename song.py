from datetime import datetime
from sqlalchemy import Column, Text
from base import Base
from AudioFile import AudioFile

class Song(AudioFile, Base):
    """Initialize a Song inherited by AudioFile, with album and genre

    With ORM
    """
    __tablename__ = "collection"
    title = Column(Text, primary_key=True)
    artist = Column(Text, nullable=True)
    album = Column(Text, nullable=True)
    duration = Column(Text, nullable=False)
    genre = Column(Text, nullable=True)
    rating = Column(Text, nullable=True)
    pathname = Column(Text, nullable=True)

    def __init__(self, title: str = '-', artist: str = '-', runtime: str = '-', rating: int = 0, pathname: str = '-',
                 album: str = '-', genre: str = None) -> None:
        super().__init__(title, artist, runtime, rating, pathname)
        self._album = album
        self._genre = []

        Song._validate_constructor(title, artist, runtime, rating, album, genre)
        Song._split_string_genre(self, genre)

        #-----NOTE: runtime is treated the same as duration-----

    @staticmethod
    def _validate_constructor(title: str, artist: str, runtime: str, rating: int, album: str,
                              genre: str) -> None:
        """Validate the values passed into the constructor"""
        if not ((type(title) != str) or (type(artist) != str) or (type(runtime) != str) or
                (type(rating) != int) or (type(album) != str) or
                ((type(genre) != str) and type(genre) is None)):
            pass
        else:
            raise ValueError('Values must be a string and "rating" must be an int.')


    def _split_string_genre(self, genre) -> None:
        """Split genre string when creating object and append to genre list"""
        if genre is not None:
            genre_list = genre.split(', ')
            for thing in genre_list:
                self._genre.append(thing)

    def get_description(self) -> str:
        """Returns a string containing a description of the song"""
        if (len(self._genre) > 0) and (self._genre[0] is not None):
            song_description = '%s by %s from the album %s added on %s. Genres are %s. Runtime is %s. Last' \
                               ' played on %s. User rating is %s' % (self._title, self._artist, self._album,
                                                                     self.date_added, self._genre, self._runtime,
                                                                     self.last_played, self._user_rating)
        else:
            song_description = '%s by %s from the album %s added on %s. Runtime is %s. Last' \
                               ' played on %s. User rating is %s' % (self._title, self._artist,
                                                                     self.date_added, self._genre, self._runtime,
                                                                     self.last_played, self._user_rating)
        return song_description

    def meta_data(self) -> dict:
        """Returns a dict containing information about the song data"""
        if (len(self._genre) > 0) and (self._genre[0] is not None):
            song_dict = {'title': self._title, 'artist': self._artist, 'genre': ','.join(self._genre),
                         'album': self._album, 'date_added': self._usage.date_added,
                         'runtime': self._runtime, 'pathname': self._pathname, 'filename': self._filename,
                         'play_count': self.play_count, 'last_played': self.last_played,
                         'rating': self._user_rating}
        else:
            song_dict = {'title': self._title, 'artist': self._artist, 'album': self._album,
                         'date_added': self._usage.date_added, 'runtime': self._runtime,
                         'pathname': self._pathname, 'filename': self._filename, 'play_count':
                             self.play_count, 'last_played': self.last_played,
                         'rating': self._user_rating}
        return song_dict

    def get_location(self) -> str:
        return self._pathname

    #vvvvvvvvvvvvvvvvvv   New ORM functions  vvvvvvvvvvvvvvvvvvvvvvvvv

    def update(self, new_data: object):
        """ Copy all changes fields into the actual object (self). """
        if not isinstance(new_data, Song):
            raise TypeError("new_data must be a Song object")
        if new_data.runtime != self.duration:
            raise ValueError("Duration cannot be changed")
        self._title = new_data.title
        self._artist = new_data.artist
        self._album = new_data.album
        self._genre = new_data.genre
        self._rating = new_data.rating

    def to_dict(self):
        """ Returns dictionary of instance state """
        # output = []
        # output.append(self.meta_data())
        output = self.meta_data()
        return output

    @staticmethod
    def from_dict(d):
        """ Create and return instance from dictionary """
        for val in ("title", "artist", "album", "genre", "rating"):
            if val not in d.keys():
                raise ValueError("Invalid dict")

        instance = Song(title=d['title'], artist=d['artist'], album=d['album'],
                        genre=d['genre'], rating=d['rating'])

        return instance

    def __str__(self):
        return f"<Student {self.first_name} {self.last_name} " \
               f"({self.student_id})>"


    #vvvvvvvvvvvvvvv   UsageStats data below vvvvvvvvvvvvvvvvvvvvvvv

    @property
    def date_added(self):
        """ return the date the song or playlist was added to the library """
        return self._date_added.strftime("%Y-%m-%d")

    @property
    def last_played(self):
        """ return the date the song or playlist was last played """
        if self._last_played is None:
            return None
        else:
            return self._last_played.strftime("%Y-%m-%d")

    @property
    def play_count(self):
        """ return the number of times the song or playlist has been played """
        return self._play_count

    def increment_usage_stats(self):
        """ update the play count and last played time when a song is played """
        self._play_count += 1
        self._last_played = datetime.now()

    @classmethod
    def __valid_datetime(cls, date):
        """ private method to validate the date is datetime object """
        if type(date) is not datetime:
            return False
        else:
            return True

