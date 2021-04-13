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
window.geometry('800x550')

frame_main = tk.Frame(window, bg="gray")
frame_main.grid(sticky='news')

dir_name = os.path.expanduser("~/" + "Downloads")


filenames, Y,  bag = classify.read_dir(dir_name)
cls, bag = classify.prepare_data(filenames, Y, bag, from_files=False)

prediction = classify.classify(dir_name, cls, bag)
#for k, v in prediction.items():
#    print(k,v)

i = 0
inv_media_type = {v: k for k, v in classify.media_type.items()}

frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=1, column=0, pady=(0, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas, bg="grey")
canvas.grid(row=0, column=0, sticky="news")

vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Create a frame to contain the buttons
frame_buttons = tk.Frame(canvas, bg="grey")
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

string_vars = []
lables = []
comboboxes = []
for k,v in prediction.items():
    n = tk.StringVar()
    string_vars.append(n)
    label = ttk.Label(frame_buttons, text=k)
    label.grid(column = 0, row = i)
    lables.append(label)
    filechosen = ttk.Combobox(frame_buttons, width=30, textvariable=n)
    filechosen['values'] = tuple(classify.media_type.values())
    filechosen.grid(column = 1, row = i)
    ind = inv_media_type[v]
    filechosen.current(ind)
    comboboxes.append(filechosen)
    i += 1

frame_canvas.config(width=800 + vsb.winfo_width(),
                    height=400)

elements = []
i = 1
for k, v in prediction.items():
    n = string_vars[i-1] 
    label = lables[i-1]
    combobox = comboboxes[i-1]
    i += 1
    elements.append((label, n))

# Set the canvas scrolling region


button = ttk.Button(frame_main, text="Move Files", command=move_files)
button.grid(column=0, row=i)

# Link a scrollbar to the canvas
vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)
canvas.config(scrollregion=canvas.bbox("all"))


window.mainloop()






