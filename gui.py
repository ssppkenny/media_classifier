import shutil
import gi
import classify
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ComboBoxWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Downloaded Files Classifier")
        self.dir_name = os.path.expanduser("~/" + "Downloads")
        filenames, Y,  bag = classify.read_dir(self.dir_name)
        cls, bag = classify.prepare_data(filenames, Y, bag, from_files=False)
        prediction = classify.classify(self.dir_name, cls, bag)


        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.elements = []
        inv_media_type = {v: k for k, v in classify.media_type.items()}
        for k, v in prediction.items():
            combobox_values = Gtk.ListStore(int, str)

            for i, val in enumerate(classify.media_type.values()):
                combobox_values.append([i, val])

            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1, homogeneous=True)

            type_combo = Gtk.ComboBox.new_with_model_and_entry(combobox_values)
            type_combo.set_entry_text_column(1)
            classify.media_type.values()
            type_combo.set_active(inv_media_type[v])


            label = Gtk.Label.new(k)
            label.set_selectable(True)
            hbox.pack_start(label, False, False, True)
            hbox.pack_start(type_combo, False, False, 0)
            vbox.pack_start(hbox, False, False, 0)
            self.elements.append((label, type_combo))


        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1, homogeneous=True)
        button = Gtk.Button("Move Files")
        button.set_size_request(200, 40)
        button.connect("clicked", self.on_button_clicked)
        hbox.pack_start(button, False, False, 0)
        vbox.pack_start(hbox, True, True, 0)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(vbox)
        self.add(scrolled_window)
        self.set_size_request(500,500)

    def on_button_clicked(self, button):
        inv_media_type = {v: k for k, v in classify.media_type.items()}
        for name, folder in self.elements:
            target_folder = classify.media_type[folder.get_active()]
            shutil.move(os.path.join(self.dir_name, name.get_text()), os.path.join(self.dir_name, target_folder))


win = ComboBoxWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
