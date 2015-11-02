import Tkinter as tk
from Tkinter import *
import Tkinter

class SettingsGUI(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.title = ("Heriot-Watt University Pi Spectrometer")
        logo = Tkinter.PhotoImage(file = "img/logo/favicon32.png")
        #call('wm', 'iconphoto', self._w, logo)

        self.settings = Settings()
        self.settings.description = "Settings for spectrometer."
        lay_label = tk.Frame()
        lay_label.pack(side = LEFT)
        lay_value = tk.Frame()
        lay_value.pack(side = RIGHT)
        lay_bottom = tk.Frame()
        lay_bottom.pack(side = BOTTOM)
        lbl_first_name = tk.Label(lay_label, text = "First Name: ")
        lbl_first_name.grid(row = 1)
        txt_first_name = tk.Text(lay_value, width = 10, height = 1)
        txt_first_name.grid(row = 1)
        lbl_last_name = tk.Label(lay_label, text = "Last Name: ")
        lbl_last_name.grid()
        txt_last_name = tk.Text(lay_value,width = 10, height = 1, command = self.save_settings)
        txt_last_name.grid()
        lbl_scale = tk.Label(lay_label, text = "Enable graph scaling: ")
        lbl_scale.grid()
        rad_scaling = tk.Radiobutton(lay_value)
        rad_scaling.grid()

        save_button = tk.Button(lay_bottom, text = "Save"''', command = controller.save_settings(self.settings)''')
        save_button.grid()
        self.pack()

    def save_settings(self):
        self.settings.first_name = self.txt_first_name.text
        self.settings.last_name = self.txt_last_name.text


class Settings:
    pass


class TestController(tk.Tk):
    def __init__(self, *args, **kargs):
        tk.Tk.__init__(self, *args, **kargs)
        self.settings = Settings()

if __name__ == "__main__":
    c = TestController()
    s = SettingsGUI(None, c)
    s.mainloop()
