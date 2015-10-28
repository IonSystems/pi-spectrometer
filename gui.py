import Tkinter

class App(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.label = Tkinter.Label(text="Image", compound="top")
        self.label.pack(side="top", padx=8, pady=8)
        self.iteration=0
        self.UpdateImage(1000)

    def UpdateImage(self, delay, event=None):
        self.iteration += 1

        self.image = self.get_image()
        self.label.configure(image=self.image, text="Iteration %s" % self.iteration)
        self.after(delay, self.UpdateImage, 1000)

    def get_image(self):
        data = '''
            R0lGODlhIAAgALMAAAAAAAAAgHCAkC6LV76+vvXeswD/ANzc3DLNMubm+v/6zS9PT6Ai8P8A////
            /////yH5BAEAAAkALAAAAAAgACAAAAS00MlJq7046803AF3ofAYYfh8GIEvpoUZcmtOKAO5rLMva
            0rYVKqX5IEq3XDAZo1GGiOhw5rtJc09cVGo7orYwYtYo3d4+DBxJWuSCAQ30+vNTGcxnOIARj3eT
            YhJDQ3woDGl7foNiKBV7aYeEkHEignKFkk4ciYaImJqbkZ+PjZUjaJOElKanqJyRrJyZgSKkokOs
            NYa2q7mcirC5I5FofsK6hcHHgsSgx4a9yzXK0rrV19gRADs=
        '''
        image = Tkinter.PhotoImage(data=data)
        return image

if __name__ == "__main__":
    app=App()
    app.mainloop()
