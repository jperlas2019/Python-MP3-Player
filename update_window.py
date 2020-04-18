import tkinter as tk


class UpdateWindow(tk.Frame):

    def __init__(self, parent, close_callback, save_callback):
        """ Initialize the popup window """
        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self._save_cb = save_callback

        parent.title('Update Song')

        self.top_frame = tk.Frame(self.master)
        self.mid_frame = tk.Frame(self.master)
        self.bot_frame = tk.Frame(self.master)
        self.midleft_frame = tk.Frame(self.master)
        self.top_frame.grid(row=0, padx=30, pady=10)
        self.midleft_frame.grid(row=1, column=0, padx=30, pady=10)
        self.mid_frame.grid(row=1, column=1, padx=30, pady=10)
        self.bot_frame.grid(row=2, padx=30, pady=10)

        tk.Label(self.top_frame, text="Update Song").pack()

        # Labels and Entries
        self.title = tk.Entry(self.mid_frame, width=20)
        self.artist = tk.Entry(self.mid_frame, width=20)
        self.album = tk.Entry(self.mid_frame, width=20)
        self.genre = tk.Entry(self.mid_frame, width=20)
        self.rating = tk.Entry(self.mid_frame, width=20)

        tk.Label(self.midleft_frame, text="title").pack()
        self.title.pack()
        tk.Label(self.midleft_frame, text="artist").pack()
        self.artist.pack()
        tk.Label(self.midleft_frame, text="album").pack()
        self.album.pack()
        tk.Label(self.midleft_frame, text="genre").pack()
        self.genre.pack()
        tk.Label(self.midleft_frame, text="rating").pack()
        self.rating.pack()

        # Buttons
        self.save_button = tk.Button(self.bot_frame, text='Save', width=10, command=self._save_cb)
        self.close_button = tk.Button(self.bot_frame, text='Cancel', width=10, command=self._close_cb)

        self.save_button.pack()
        self.close_button.pack()

    def get_form_data(self):
        """returns song info to be added separated by commas"""
        form_data = []
        form_data.append(self.title.get())
        form_data.append(self.artist.get())
        form_data.append(self.album.get())
        form_data.append(self.genre.get())
        form_data.append(self.rating.get())
        return form_data

    def clear_form_fields(self):
        """ Clear the entry boxes """
        self.title.delete(0, tk.END)
        self.artist.delete(0, tk.END)
        self.album.delete(0, tk.END)
        self.genre.delete(0, tk.END)
        self.rating.delete(0, tk.END)
