import shutil
import gi
import classify
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ComboBoxWindow(Gtk.ApplicationWindow):
    def __init__(self):
        Gtk.Window.__init__(self, title="Downloaded Files Classifier")
        self.dir_name = os.path.expanduser("~/" + "Downloads")
        filenames, Y,  bag = classify.read_dir(self.dir_name)
        cls, bag = classify.prepare_data(filenames, Y, bag, from_files=False)
        prediction = classify.classify(self.dir_name, cls, bag)

        prediction = dict([(x, prediction[x]) for x in sorted(prediction.keys())])

        self.set_border_width(10)
        self.set_size_request(800,300)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.elements = []
        hboxes = []
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
            hboxes.append(hbox)
            self.elements.append((label, type_combo))


        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1, homogeneous=True)
        button = Gtk.Button("Move Files")
        button.set_size_request(200, 40)
        button.connect("clicked", self.on_button_clicked)
        hbox.pack_start(button, False, False, 0)
        vbox.pack_start(hbox, True, True, 0)
        scrolled_window = Gtk.ScrolledWindow.new (None, None)
        scrolled_window.set_policy(Gtk.PolicyType.NEVER,
                                Gtk.PolicyType.ALWAYS)
        #vbox.add(scrolled_window)
        scrolled_window.add(vbox)
        self.add(scrolled_window)
        #height = self.get_screen().get_height()
        #width = self.get_screen().get_width()
        #for hbox in hboxes:
        #    print(dir(hbox.get_visual()))
        #    for ch in hbox.get_children():
        #        a = ch.get_allocation()
        #        total_height += a.height*20
        #        total_width += a.width*25
        #self.set_size_request(-1,-1)

    def on_button_clicked(self, button):
        inv_media_type = {v: k for k, v in classify.media_type.items()}
        for name, folder in self.elements:
            target_folder = classify.media_type[folder.get_active()]
            shutil.move(os.path.join(self.dir_name, name.get_text()), os.path.join(self.dir_name, target_folder))


win = ComboBoxWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
