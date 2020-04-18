import tkinter as tk
from tkinter.filedialog import askopenfilename
import requests
from tkinter import messagebox
from player_window import PlayerWindow
from update_window import UpdateWindow
import eyed3
import vlc


class MainAppController(tk.Frame):
    """Contains callback functions"""

    def __init__(self, parent):
        """Create the views"""
        tk.Frame.__init__(self, parent)
        self._root_win = tk.Toplevel()
        self._player = PlayerWindow(self._root_win, self)
        self.list_songs()
        self._vlc_instance = vlc.Instance()
        self._vlc_player = self._vlc_instance.media_player_new()
        self.queue_path = []
        self.queue_name = []

    def clear_callback(self):
        """ Remove all songs names from system. """
        response = requests.delete("http://localhost:5000/song/all")
        if response.status_code == 200:
            msg_str = f'All names removed from the database'
            messagebox.showinfo(title='Delete All', message=msg_str)
        else:
            messagebox.showerror(title='Delete All', message="Something went wrong")

    def quit_callback(self):
        """ Exit the application. """
        self.master.quit()

    def openfile(self):
        """Load all the names from the file"""
        selected_file = askopenfilename(initialdir='.')
        print(selected_file)
        mp3_file = eyed3.load(selected_file)
        duration = mp3_file.info.time_secs
        mins = int(duration // 60)
        secs = int(duration % 60)
        duration = '%d:%d' % (mins, secs)
        tags = ['title', 'artist', 'album']
        genre = (str(getattr(mp3_file.tag, 'genre')).split(')'))[1]
        song_object = []
        for tag in tags:
            value = getattr(mp3_file.tag, tag)
            song_object.append(value)
        data = {'title': song_object[0],
                'artist': song_object[1],
                'runtime': duration,
                'rating': 0,
                'pathname': selected_file,
                'album': song_object[2],
                'genre': genre}
        response = requests.post("http://localhost:5000/song", json=data)
        print(response)
        if response.status_code == 200:
            msg_str = "Song %s has been added." % song_object[0]
            messagebox.showinfo(title='Add Song', message=msg_str)
            self.list_songs()
        else:
            messagebox.showinfo(title='Add Song', message='Uh oh! Something went wrong.')

    def delete_callback(self):
        """Deletes highlighted song in listbox"""
        title, index = self._player.selected_song()
        index = int(index) + 1
        response = requests.delete("http://localhost:5000/song/" + title)
        if response.status_code == 200:
            msg_str = "Song %s has been deleted." % title
            messagebox.showinfo(title='Delete Song', message=msg_str)
            self.list_songs()
        else:
            messagebox.showinfo(title='Delete Song', message='Uh oh! Something went wrong.')

    def update_popup(self):
        """Instaniate update window"""
        self._update_win = tk.Toplevel()
        self._update = UpdateWindow(self._update_win, self._close_update_popup, self._save_entry)

    def _close_update_popup(self):
        """Close add popup"""
        self._update_win.destroy()

    def _save_entry(self):
        """Calls the add_callback and _close_update_popup methods"""
        self.update_callback()
        self._close_update_popup()

    def update_callback(self):
        form_data = self._update.get_form_data()

        data = {'title': form_data[0],
                'artist': form_data[1],
                'rating': form_data[4],
                'album': form_data[2],
                'genre': form_data[3]}

        response = requests.put("http://localhost:5000/song/" + form_data[0], json=data)

    def list_songs(self):
        """Gets list of songs and display in listbox"""
        response = requests.get('http://localhost:5000/song/all')
        song_names = []
        for s in response.json():
            song_names.append(s['title'])
        self._player.list_songs(song_names)

    def play_callback(self):
        """plays selected song"""
        selected_song, index = self._player.selected_song()
        response = requests.get('http://localhost:5000/song/' + selected_song)
        song_object = response.json()
        media_file = song_object['pathname']
        media_file = media_file.replace('/', '\\')
        media = self._vlc_instance.media_new_path(media_file)
        self._vlc_player.set_media(media)
        self._vlc_player.play()
        self._player.set_current_song_text(song_object['title'])
        print(f"Playing {song_object['title']} from file {media_file}")

    def stop_callback(self):
        """stops player"""
        self._vlc_player.stop()

    def pause_callback(self):
        """pauses current song"""
        self._vlc_player.pause()

    def skip_callback(self):
        """skips current song, plays next song in queue"""
        self._vlc_player.stop()
        media = self._vlc_instance.media_new_path(self.queue_path[0])
        self._vlc_player.set_media(media)
        self._vlc_player.play()
        self._player.set_current_song_text(self.queue_name[0])
        self.queue_path.pop(0)
        self.queue_name.pop(0)
        self._player.list_songs_queue(self.queue_name)



    def queue_callback(self):
        """Adds selected song from list to queue"""
        selected_song, index = self._player.selected_song()
        response = requests.get('http://localhost:5000/song/' + selected_song)
        song_object = response.json()
        media_file = song_object['pathname']
        media_file = media_file.replace('/', '\\')
        song_name = song_object['title']
        self.queue_path.append(media_file)
        self.queue_name.append(song_name)
        self._player.list_songs_queue(self.queue_name)

if __name__ == "__main__":
    """ Create Tk window manager and a main window. Start the main loop """
    root = tk.Tk()
    MainAppController(root).pack()
    tk.mainloop()
