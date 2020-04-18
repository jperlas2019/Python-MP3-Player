import os
from os import path


class Chooser:
    """
    Load student songs from a file so that students can be randomly selected
    to answer questions etc in class.

    Songs are by default stored in a file called __songs__.txt, or,
    a different file can be specified when the program is started. The file
    has one student song per line.
    """
    def __init__(self, filename):
        """ Create a new instance and load songs from a file. """
        self._filename = filename
        self._songlist = []
        self._load_songs_from_file()

    @property
    def filename(self):
        return self._filename

    @property
    def songlist(self):
        return self._songlist

    def add(self, song):
        """ Append a song to the songs file. """
        try:
            f = open(self.filename, "a")
            f.write(song+"\n")
            f.close()
        except FileNotFoundError:
            raise
        self._load_songs_from_file()

    def clear(self):
        """ Remove all songs and delete the songs file. """
        self._songlist = []
        if path.isfile(self.filename):
            os.remove(self.filename)

    def _load_songs_from_file(self):
        """ Load the contents of songs file into a list. """
        try:
            f = open(self.filename)
            self._songlist = f.readlines()
            f.close()
            self._songlist = [song.strip() for song in self._songlist]
        except FileNotFoundError:
            self._songlist = []

    def delete(self, song):
        """Deletes song from file"""
        try:
            f = open(self.filename, "r")
            lines = f.readlines()
            f = open(self.filename, "w")
            for line in lines:
                if line.strip("\n") != song:
                    f.write(line)
            f.close()
        except FileNotFoundError:
            raise
        self._load_songs_from_file()
