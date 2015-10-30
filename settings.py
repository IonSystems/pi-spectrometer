import Tkinter as tk
from Tkinter import *
from Tkinter import Tk

class SettingsGUI(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        tk.Frame.wm_title("Heriot-Watt University Pi Spectrometer")
        logo = Tkinter.PhotoImage(file = "img/logo/favicon32.png")
        tk.call('wm', 'iconphoto', self._w, logo)
        
        label = tk.Label(self, text = "Settings Menu")
        label.pack(pady = 10, padx = 10)

        save_button = tk.Button(self, text = "Save"''', command = controller.save_settings(self.settings)''')
        save_button.pack()

class TestController(tk.Tk):
    def __init__(self, *args, **kargs):
        tk.Tk.__init__(self, *args, **kargs)
        
if __name__ == "__main__":
    c = TestController()
    s = SettingsGUI(None, c)
    s.mainloop()
