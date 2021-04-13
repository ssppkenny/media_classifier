import tkinter as tk
from tkinter import ttk
import getpass
import os
import classify

def move_files():
    for k,v in elements:
        subfolder = k.cget("text")
        file = v.get()
        print(f"moving {file} to {subfolder}")


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
lables = []
comboboxes = []
for k,v in prediction.items():
    n = tk.StringVar()
    string_vars.append(n)
    label = ttk.Label(window, text=k)
    label.grid(column = 2, row = i)
    lables.append(label)
    filechosen = ttk.Combobox(window, width=30, textvariable=n)
    filechosen['values'] = tuple(classify.media_type.values())
    filechosen.grid(column = 1, row = i)
    ind = inv_media_type[v]
    filechosen.current(ind)
    comboboxes.append(filechosen)
    i += 1


elements = []
i = 1
for k, v in prediction.items():
    n = string_vars[i-1] 
    label = lables[i-1]
    combobox = comboboxes[i-1]
    i += 1
    elements.append((label, n))


button = ttk.Button(window, text="Move Files", command=move_files)
button.grid(column=1, row=i+5)



window.mainloop()






