import time
import npyscreen
import shutil
import classify
import os
import warnings
warnings.filterwarnings('ignore')

class MyForm(npyscreen.FormMultiPageAction):
    def __init__(self, name, *args, **kw):
        super().__init__(name, *args,  **kw)
        self.dir_name = os.path.expanduser("~/" + "Downloads")
        filenames, Y,  bag = classify.read_dir(self.dir_name)
        cls, bag = classify.prepare_data(filenames, Y, bag, from_files=False)
        prediction = classify.classify(self.dir_name, cls, bag)
        self.prediction = dict([(x, prediction[x]) for x in sorted(prediction.keys())])
        
    def items(self):
        return self.prediction

    def set_widgets(self, widgets):
        self.widget_list = widgets

    def on_ok(self):
        inv_media_type = {v: k for k, v in classify.media_type.items()}
        for widget in self.widget_list:
            target_folder = classify.media_type[widget.value]
            shutil.move(os.path.join(self.dir_name, widget.name), os.path.join(self.dir_name, target_folder))

class TestApp(npyscreen.NPSAppManaged):
    def main(self):
        F = MyForm("MyForm")
        inv_media_type = {v: k for k, v in classify.media_type.items()}
        values = list(inv_media_type.keys())
        i = 0
        widgets = []
        for k,v in F.items().items():
            cb = F.add(npyscreen.TitleCombo, name=k, values=values)
            cb.value = values.index(v)
            widgets.append(cb)
            if i % 40 == 0 and i > 0:
                F.add_page()
            i+=1
        F.set_widgets(widgets)

        F.edit()

if __name__ == '__main__':
    app = TestApp()
    app.run()
