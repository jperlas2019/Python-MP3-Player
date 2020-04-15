from datetime import datetime
from sqlalchemy import Column, Text
from AudioFile import AudioFile

class Song(AudioFile):
    """Initialize a Song inherited by AudioFile, with album and genre

    With ORM
    """
    album = Column(Text, nullable=True)
    genre = Column(Text, nullable=True)

    def __init__(self, title: str = '-', artist: str = '-', runtime: str = '-', rating: int = 0, pathname: str = '-',
                 album: str = '-', genre: str = None) -> None:
        super().__init__(title, artist, runtime, rating, pathname)
        self.album = album
        self.genre = genre

        Song._validate_constructor(title, artist, runtime, rating, album, genre)
        # Song._split_string_genre(self, genre)

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


    # def _split_string_genre(self, genre) -> None:
    #     """Split genre string when creating object and append to genre list"""
    #     if genre is not None:
    #         genre_list = genre.split(', ')
    #         for thing in genre_list:
    #             self._genre.append(thing)

    def get_description(self) -> str:
        """Returns a string containing a description of the song"""
        if (len(self._genre) > 0) and (self._genre[0] is not None):
            song_description = '%s by %s from the album %s added on %s. Genres are %s. Runtime is %s. Last' \
                               ' played on %s. User rating is %s' % (self.title, self.artist, self.album,
                                                                     self.date_added, self.genre, self.runtime,
                                                                     self.last_played, self.user_rating)
        else:
            song_description = '%s by %s from the album %s added on %s. Runtime is %s. Last' \
                               ' played on %s. User rating is %s' % (self.title, self.artist,
                                                                     self.date_added, self.genre, self.runtime,
                                                                     self.last_played, self.user_rating)
        return song_description

    def meta_data(self) -> dict:
        """Returns a dict containing information about the song data"""
        print(self.genre + 'genre')
        #REMOVED "filename" AND "play_count"
        # if (len(self.genre) > 0) and (self.genre[0] is not None):
        if (self.genre is not None) and (self.genre != ''):
            song_dict = {'title': self.title, 'artist': self.artist, 'genre': self.genre,
                         'album': self.album, 'date_added': self.date_added,
                         'runtime': self.runtime, 'pathname': self.pathname,
                         'last_played': self.last_played,
                         'rating': self._user_rating}
        else:
            song_dict = {'title': self.title, 'artist': self.artist, 'album': self.album,
                         'date_added': self.date_added, 'runtime': self.runtime,
                         'pathname': self.pathname, 'last_played': self.last_played,
                         'rating': self._user_rating}
        return song_dict

    def get_location(self) -> str:
        return self._pathname

    #vvvvvvvvvvvvvvvvvv   New ORM functions  vvvvvvvvvvvvvvvvvvvvvvvvv

    def update(self, new_data: object):
        """ Copy all changes fields into the actual object (self). """
        if not isinstance(new_data, Song):
            raise TypeError("new_data must be a Song object")
        if new_data.runtime != self.runtime:
            raise ValueError("Runtime cannot be changed")
        self.title = new_data.title
        self.artist = new_data.artist
        self.album = new_data.album
        self.genre = new_data.genre
        self.rating = new_data.rating

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
        return f"<Song {self.title} by {self.artist} from the album " \
               f"({self.album})>"


    # #vvvvvvvvvvvvvvv   UsageStats data below vvvvvvvvvvvvvvvvvvvvvvv
    #
    # @property
    # def date_added(self):
    #     """ return the date the song or playlist was added to the library """
    #     return self._date_added.strftime("%Y-%m-%d")
    #
    # @property
    # def last_played(self):
    #     """ return the date the song or playlist was last played """
    #     if self._last_played is None:
    #         return None
    #     else:
    #         return self._last_played.strftime("%Y-%m-%d")
    #
    # @property
    # def play_count(self):
    #     """ return the number of times the song or playlist has been played """
    #     return self._play_count
    #
    # def increment_usage_stats(self):
    #     """ update the play count and last played time when a song is played """
    #     self._play_count += 1
    #     self._last_played = datetime.now()
    #
    # @classmethod
    # def __valid_datetime(cls, date):
    #     """ private method to validate the date is datetime object """
    #     if type(date) is not datetime:
    #         return False
    #     else:
    #         return True
    #
