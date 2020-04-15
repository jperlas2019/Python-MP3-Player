from datetime import datetime
from abc import abstractmethod
import os
from sqlalchemy import Column, Text, Integer
from base import Base


class AudioFile(Base):
    """Represent a song played on a music player

    Author: Jaguar Perlas
    ID: A01175812
    """

    __tablename__ = "collection"
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=True)
    artist = Column(Text, nullable=True)
    # album = Column(Text, nullable=True)
    runtime = Column(Text, nullable=False)
    # genre = Column(Text, nullable=True)
    rating = Column(Text, nullable=True)
    pathname = Column(Text, nullable=True)
    date_added = Column(Text, nullable=True)
    last_played = Column(Text, nullable=True)


    def __init__(self, title: str, artist: str, runtime: str, rating: int = 0, pathname: str = None) -> None:
        """Initialize a song with a title, artist, album, date added, runtime, pathname, filename,
        user rating, last played, and play count."""
        if type(self) == AudioFile:
            raise ValueError('Creation of super class not allowed')
        self.title = title
        self.artist = artist
        self.runtime = runtime
        self.rating = rating
        self.pathname = pathname
        self.filename = os.path.basename(pathname)
        self.user_rating = rating

        self.date_added = datetime.now()
        self.play_count = 0
        self.last_played = None

        # self._usage = UsageStats(datetime.now())
        AudioFile._validate_constructor(title, artist, runtime, rating, self.pathname)

    @staticmethod
    def _validate_constructor(title: str, artist: str, runtime: str, rating: int, pathname) -> None:
        """Validate the values passed into the constructor"""
        if not ((type(title) != str) or (type(artist) != str) or (type(runtime) != str) or
                (type(rating) != int)):
            if not os.path.exists(pathname):
                raise ValueError('Path does not exist.')
            pass
        else:
            raise ValueError('Values must be a string and "rating" must be an int.')

    @abstractmethod
    def get_description(self):
        """Return a string containing the description of the song"""
        song_description = '%s by %s from the album '' added on %s. Runtime is %s. Last' \
                           ' played on %s. User rating is %s' % (self.title, self._artist,
                                                                 self.date_added, self.runtime,
                                                                 self._last_played, self.user_rating)
        pass

    def song_location(self) -> str:
        """Return a string containing the path of the song file"""
        song_location = '%s is located at %s' % (self.filename, self.pathname)
        return song_location

    def play_song(self) -> None:
        """Plays the song"""
        self.increment_usage_stats()
        print('Now playing: %s by %s' % (self.title, self._artist))
        print('Play count is now %d' % self.play_count)

    @property
    def _user_rating(self) -> int:
        """Gets and returns the user rating"""
        return self.rating

    @_user_rating.setter
    def _user_rating(self, user_rating: int) -> None:
        """Sets the user rating to desired value"""
        if type(user_rating) != int:
            raise ValueError('Input must be a number')
        else:
            if (user_rating < 0) or (user_rating > 5):
                raise ValueError('Rating must be a number out of 10')
            else:
                self.user_rating = int(user_rating)

    @abstractmethod
    def meta_data(self):
        song_dict = {'title': self._title, 'artist': self._artist,
                     'date_added': self.date_added, 'runtime': self.runtime,
                     'pathname': self.pathname, 'filename': self.filename, 'play_count':
                         self.play_count, 'last_played': self._last_played,
                     'rating': self.user_rating}
        pass

    #UsageStats functions below vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    @property
    def _date_added(self):
        """ return the date the song or playlist was added to the library """
        return self._date_added.strftime("%Y-%m-%d")

    @property
    def _last_played(self):
        """ return the date the song or playlist was last played """
        if self.last_played is None:
            return None
        else:
            return self.last_played.strftime("%Y-%m-%d")

    @property
    def _play_count(self):
        """ return the number of times the song or playlist has been played """
        return self._play_count

    def increment_usage_stats(self):
        """ update the play count and last played time when a song is played """
        self.play_count += 1
        self.last_played = datetime.now()

    @classmethod
    def __valid_datetime(cls, date):
        """ private method to validate the date is datetime object """
        if type(date) is not datetime:
            return False
        else:
            return True
