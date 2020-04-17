import tkinter as tk
import csv
from tkinter.filedialog import askopenfilename
import requests
from tkinter import messagebox
from player_window import PlayerWindow
from update_window import UpdateWindow


class MainAppController(tk.Frame):
    """Contains callback functions"""

    def __init__(self, parent):
        """Create the views"""
        tk.Frame.__init__(self, parent)
        self._root_win = tk.Toplevel()
        self._player = PlayerWindow(self._root_win, self)

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

    def add_callback(self):
        """ Add a new song name to the file. """
        form_data = self._add.get_form_data()
        form_data = form_data.split(',')
        self._add.clear_form_fields()

        if len(form_data) != 3:
            messagebox.showerror(title='Invalid name data',
                                 message='Enter "id,first,last"')
            return

        data = {'song_id': form_data[0],
                'first_name': form_data[1],
                'last_name': form_data[2]}

        response = requests.post("http://localhost:5000/song", json=data)
        if response.status_code == 200:
            msg_str = f'{" ".join(form_data)} added to the database'
            messagebox.showinfo(title='Add Student', message=msg_str)

    def openfile(self):
        """Load all the names from the file"""
        selected_file = askopenfilename(initialdir='.')
        if selected_file:
            self.file_name = selected_file
            num_added = 0
            not_added = []
            with open(self.file_name, 'r') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',')
                for row in csv_reader:
                    data = {'song_id': row[0],
                            'first_name': row[1],
                            'last_name': row[2]}
                    response = requests.post("http://localhost:5000/song",json=data)
                    if response.status_code == 200:
                        num_added += 1
                    else:
                        not_added.append(' '.join(row))
            msg = f'{num_added} names added to DB.'
            if len(not_added) > 0:
                not_added = '\n'.join(not_added)
                msg += '\n' + f'The following names were not added:'
                msg += '\n' + not_added
            messagebox.showinfo(title='Load Names', message=msg)

    # def classlist_popup(self):
    #     """ Show Classlist Popup Window """
    #     self._class_win = tk.Toplevel()
    #     self._class = ClasslistWindow(self._class_win, self._close_classlist_popup, self.classlist_delete)
    #     response = requests.get("http://localhost:5000/song/names")
    #     name_list = [f'{s["first_name"]} {s["last_name"]}' for s in response.json()]
    #     self._class.set_names(name_list)

    def delete_callback(self):
        """Deletes highlighted song in listbox"""
        title = self._class.selected_song()

        response = requests.get("http://localhost:5000/song/all")
        song_id = ""
        for song in response.json():
            if title == song["title"]:
                song_id = song["song_id"]

        requests.delete("http://localhost:5000/song/" + song_id)

        response = requests.get("http://localhost:5000/song/all")
        name_list = [f'{s["title"]}' for s in response.json()]
        self._player.set_names(name_list)

    def update_popup(self):
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

    def play_callback(self):
        """plays selected song"""
        pass

    def stop_callback(self):
        """stops player"""
        pass

    def pause_callback(self):
        """pauses current song"""
        pass

    def skip_callback(self):
        """skips current song, plays next song in queue"""
        pass

    def queue_callback(self):
        """Adds selected song from list to queue"""
        pass


if __name__ == "__main__":
    """ Create Tk window manager and a main window. Start the main loop """
    root = tk.Tk()
    MainAppController(root).pack()
    tk.mainloop()
