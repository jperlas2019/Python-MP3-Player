import tkinter as tk


class SonglistWindow(tk.Frame):

    def __init__(self, parent, close_callback, delete_callback, add_popup, update_popup):
        """ Initialize the popup listbox window """
        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self._delete_cb = delete_callback
        self._add_popup = add_popup
        self._update_popup = update_popup

        parent.title('Song List')

        self.top_frame = tk.Frame(self.master)
        self.mid_frame = tk.Frame(self.master)
        self.bot_frame = tk.Frame(self.master)
        self.top_frame.grid(row=0, padx=30, pady=10)
        self.mid_frame.grid(row=1, padx=30, pady=10)
        self.bot_frame.grid(row=2, padx=30, pady=10)

        self.song_listbox = tk.Listbox(self.top_frame, width=20,
                                       selectmode=tk.BROWSE)
        self.song_scrollbar = tk.Scrollbar(self.top_frame, orient='vertical')
        self.song_scrollbar.config(command=self.song_listbox.yview)
        self.song_listbox.config(yscrollcommand=self.song_scrollbar.set)

        self.add_button = tk.Button(self.mid_frame, text='Add', width=10,
                                    command=self._add_popup)
        self.add_button = tk.Button(self.bot_frame, text='Add', width=10,
                                    command=self._add_popup)
        self.delete_button = tk.Button(self.bot_frame, text='Delete', width=10,
                                   command=self._delete_cb)
        self.close_button = tk.Button(self.bot_frame, text='Close', width=10,
                                      command=self._close_cb)

        self.song_listbox.grid(row=0, column=2, side=tk.LEFT, fill=tk.BOTH)
        self.song_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_button.pack()
        self.delete_button.pack()
        self.close_button.pack()

    def set_songs(self, songs):
        """ Update the listbox to display all names """
        self.song_listbox.delete(0, tk.END)
        for song in songs:
            self.song_listbox.insert(tk.END, name)

    def selected_student(self):
        return self.song_listbox.get(self.song_listbox.curselection())

