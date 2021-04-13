import tkinter as tk
from tkinter import ttk
import getpass
import os
import classify


window = tk.Tk()
window.title('Classify')
window.geometry('700x550')


dir_name = os.path.expanduser("~/" + "Downloads")


filenames, Y,  bag = classify.read_dir(dir_name)
cls, bag = classify.prepare_data(filenames, Y, bag, from_files=False)

prediction = classify.classify(dir_name, cls, bag)
#for k, v in prediction.items():
#    print(k,v)

i = 1
inv_media_type = {v: k for k, v in classify.media_type.items()}


string_vars = []
for k,v in prediction.items():
    string_vars.append(tk.StringVar())


for k, v in prediction.items():
    n = string_vars[i-1] 
    label = ttk.Label(window, text=k)
    filechosen = ttk.Combobox(window, width=30, textvariable=n)
    filechosen['values'] = tuple(classify.media_type.values())
    label.grid(column = 2, row = i)
    filechosen.grid(column = 1, row = i)
    ind = inv_media_type[v]
    print(v)
    print(ind)
    filechosen.current(ind)
    i += 1



window.mainloop()






