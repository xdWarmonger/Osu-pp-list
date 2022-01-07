import numpy as np
import requests
import tkinter
import json
from tempfile import TemporaryFile
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

outfile = TemporaryFile()
finished_entry = False
create_table = True


def player_submit():
    global players
    global zeile
    global plistcount
    global playerlist
    players.append(player.get())
    player.delete(0, 'end')
    playerlist = "plist{}".format(zeile)
    playerlist = Label(window)
    plistcount.append(playerlist)
    playerlist.grid(row=zeile+2, column=0)
    for y in players:
        playerlist.config(text=y[25:])
    zeile = zeile+1


def clear_entry_text():
    player.bind("<FocusIn>", lambda args: player.delete('0', 'end'))


def save():
    global players
    filename_save = filedialog.asksaveasfilename()
    if filename_save:
        try:
            np.save(filename_save + ".npy", np.array(players))
        except FileExistsError:
            pass


def load():
    global finished_entry
    global labelloaded
    global players
    filename_load = filedialog.askopenfilename()
    if filename_load:
        players = np.load(filename_load)
        button_load.destroy()
        labelloaded = Label(window, text="Loaded!")
        labelloaded.grid(column=1, row=2)


def load1():
    global finished_entry
    global labelloaded
    global players
    global button_reload
    global create_table
    filename_load = filedialog.askopenfilename()
    if filename_load:
        players = np.load(filename_load)
        button_load.destroy()
        finished_entry = True
        labelloaded = Label(window, text="Loaded!")
        labelloaded.pack(padx=20, side=LEFT)
        button_reload = Button(window, text="Reload Highscorelist", command=entries)
        button_reload.pack(padx=20, side=LEFT)
        create_table = False


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    try:
        l.sort(key=lambda t: int(t[0]), reverse=reverse)

    except ValueError:
        l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def entries():
    global finished_entry
    global button_load
    global button_save
    global treeview

    try:
        button_reload.destroy()
    except NameError:
        pass

    try:
        button_save.destroy()
    except NameError:
        pass

    try:
        button_load.destroy()
    except NameError:
        pass

    try:
        labelloaded.destroy()
    except NameError:
        pass

    try:
        for i in plistcount:
            i.destroy()
    except NameError:
        pass

    try:
        treeview.delete(*treeview.get_children())
    except NameError:
        pass

    try:
        player.destroy()
        button_playersubmit.destroy()
        button_finished_entries_button.destroy()
    except NameError:
        pass

    finished_entry = True

    if finished_entry:
        finished_entry = False
        columns = ('player', 'pp', 'global rank', 'hit accuracy', 'play time (hours)')

        if create_table:
            treeview = ttk.Treeview(window, columns=columns, show='headings')

        for x in players:

            pageContent = requests.get(str(x), verify=True)

            HTMLstring = ""
            for chara in pageContent.content:
                try:
                    schar = chr(chara)
                    HTMLstring = HTMLstring + schar
                except:
                    HTMLstring = HTMLstring + 'UKN'

            expr = re.compile(r'(<script id=\"json-user\" type=\"application\/json\">)([\s\S]*?)(<\/script>)',
                              re.MULTILINE)
            res = re.search(expr, HTMLstring)
            stats = json.loads(res.group(2))

            treeview.insert('', END, values=(stats["username"],
                                             str(round(int(stats["statistics"]["pp"]), 0)),
                                             str(round(int(stats["statistics"]["pp_rank"]), 0)),
                                             str(round(float(stats["statistics"]["hit_accuracy"]), 2)),
                                             str(round(int(stats["statistics"]["play_time"]) / 86400*24))))
            treeview.pack()
            for col in columns:
                treeview.heading(col, text=col, command=lambda c=col: treeview_sort_column(treeview, c, False))

        button_save = Button(window, text="save", command=save)
        button_save.pack(padx=20, side=LEFT)

        button_load = Button(window, text="load", command=load1)
        button_load.pack(padx=20, side=LEFT)


window = tkinter.Tk()
window.title("PP-Highscorelist")

players = []
plistcount = []
zeile = 0

player = Entry(window)
player.grid(row=0, column=0)
player.insert(0, "Insert profile link here")
player.bind('<Button-1>', clear_entry_text())

button_load = Button(window, text="Load", command=load)
button_load.grid(column=1, row=2)

button_playersubmit = Button(window, text="Submit", command=player_submit)
button_playersubmit.grid(column=1, row=0)

button_finished_entries_button = Button(window, text="Go to Highscorelist", command=entries)
button_finished_entries_button.grid(column=1, row=1)

window.mainloop()
