import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from chooser import Chooser
import os


class PlayerWindow(tk.Frame):
    """ Main Application Window """

    def __init__(self, parent, my_controller):
        """ Initialize Main Application """
        tk.Frame.__init__(self, parent)

        # 1: create any instances of other support classes that are needed
        self.song_names = Chooser('')

        # 2: set main window attributes such as title, geometry etc
        parent.title('Music Player')
        parent.geometry("800x600")

        # 3: set up menus if there are any
        main_menu = tk.Menu(master=parent)
        parent.config(menu=main_menu)
        file_menu = tk.Menu(main_menu)
        main_menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open', command=my_controller.openfile)
        file_menu.add_command(label='Clear', command=my_controller.clear_callback)
        file_menu.add_command(label='Quit', command=my_controller.quit_callback)

        # 4: define frames and place them in the window
        top_frame = tk.Frame(master=parent)
        top_frame.grid(row=0, padx=30, pady=10)
        mid_frame = tk.Frame(master=parent)
        mid_frame.grid(row=1, padx=30, pady=10)
        bot_frame = tk.Frame(master=parent)
        bot_frame.grid(row=2, padx=30, pady=10)

        # 5: define/create widgets, bind to events, place them in frames
        tk.Label(top_frame, text='Current Song:').grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self._current_song = tk.Label(mid_frame, text='')
        self._current_song.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Label(mid_frame, text='Collection:').grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        tk.Label(mid_frame, text='Song Queue:').grid(row=1, column=2, sticky=tk.E, padx=5, pady=5)

        # Song Listbox
        self.song_listbox = tk.Listbox(mid_frame, width=20,
                                       selectmode=tk.BROWSE)
        self.song_scrollbar = tk.Scrollbar(mid_frame, orient='vertical')
        self.song_scrollbar.config(command=self.song_listbox.yview)
        self.song_listbox.config(yscrollcommand=self.song_scrollbar.set)
        self.song_listbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W + tk.E)
        self.song_scrollbar.grid(sticky=tk.N + tk.E + tk.S, row=0, column=4, padx=5, pady=5, columnspan=3, rowspan=3)

        #Queue Listbox
        self.queue_listbox = tk.Listbox(mid_frame, width=20,
                                       selectmode=tk.BROWSE)
        self.queue_scrollbar = tk.Scrollbar(mid_frame, orient='vertical')
        self.queue_scrollbar.config(command=self.queue_listbox.yview)
        self.queue_listbox.config(yscrollcommand=self.queue_scrollbar.set)
        self.queue_listbox.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W + tk.E)
        self.queue_scrollbar.grid(sticky=tk.N + tk.E + tk.S, row=0, column=6, padx=5, pady=5, columnspan=3, rowspan=3)

        # Buttons
        tk.Button(bot_frame, text='Play', width=10, command=my_controller.play_callback)\
            .grid(row=0, column=0, sticky=tk.E, padx=20, pady=5)
        tk.Button(bot_frame, text='Stop', width=10, command=my_controller.stop_callback) \
            .grid(row=0, column=1, sticky=tk.E, padx=20, pady=5)
        tk.Button(bot_frame, text='Pause', width=10, command=my_controller.pause_callback) \
            .grid(row=0, column=2, sticky=tk.E, padx=20, pady=5)
        tk.Button(bot_frame, text='Skip', width=10, command=my_controller.skip_callback) \
            .grid(row=0, column=3, sticky=tk.E, padx=20, pady=5)

        self.add_button = tk.Button(bot_frame, text='Add Song', width=10, command=my_controller.openfile)
        self.add_button.grid(row=0, column=4, sticky=tk.E, padx=20, pady=5)
        self.add_button = tk.Button(bot_frame, text='Queue Song', width=10, command=my_controller.queue_callback)
        self.add_button.grid(row=1, column=4, sticky=tk.E, padx=20, pady=5)
        self.delete_button = tk.Button(bot_frame, text='Delete', width=10, command=my_controller.delete_callback)
        self.delete_button.grid(row=2, column=4, sticky=tk.E, padx=20, pady=5)
        self.update_button = tk.Button(bot_frame, text='Update', width=10, command=my_controller.update_popup)
        self.update_button.grid(row=3, column=4, sticky=tk.E, padx=20, pady=5)

    def display_current_song(self, song):
        """ Put the song in the song label """
        self._current_song['text'] = song

    def display_db_name(self, name):
        """ Put the db name in the top label """
        self._file_value['text'] = name

    def list_songs(self, song_names):
        """ Update the listbox to display all names """
        self.song_listbox.delete(0, tk.END)
        for song in song_names:
            self.song_listbox.insert(tk.END, song)

    def list_songs_queue(self, song_names):
        """Update the queue listbox to display all names in queue"""
        self.queue_listbox.delete(0, tk.END)
        for song in song_names:
            self.queue_listbox.insert(tk.END, song)

    def selected_song(self):
        """Return selected song from collection listbox"""
        index = self.song_listbox.curselection()
        return self.song_listbox.get(index), str(index[0])

    def selected_song_queue(self):
        """Return selected song from queue listbox"""
        index = self.queue_listbox.curselection()
        return self.queue_listbox.get(index), str(index[0])

    def set_current_song_text(self, text):
        """Set self._current_song text"""
        self._current_song['text'] = text



