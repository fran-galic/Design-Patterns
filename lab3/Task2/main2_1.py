import tkinter as tk

class CustomComponent(tk.Canvas):
    def __init__(self, parent, text1="Prvi red", text2="Drugi red", **kwargs):
        super().__init__(parent, bg="white", **kwargs)
        self.pack(fill=tk.BOTH, expand=True)

        self.bind("<Key>", self.on_key)
        self.focus_set()

        width = int(self['width'])
        height = int(self['height'])

        self.create_line(0, height//2, width, height//2, fill="red", width=1)
        self.create_line(width//2, 0, width//2, height, fill="red", width=1)

        self.create_text(width//2, height//2 - 30, text=text1)
        self.create_text(width//2, height//2 + 30, text=text2)

    def on_key(self, event):
        if event.keysym == "Return":
            self.master.destroy()

def main():
    root = tk.Tk()
    root.title("Moja prva CustomKomponenta")
    root.geometry("400x300")

    component = CustomComponent(
        root,
        text1="Hello wolrd",
        text2="Ovo je drugi red.",
        width=400,
        height=300
    )

    root.mainloop()

if __name__ == "__main__":
    main()

# 1. obrazac koji nam omogucava da nasljedimo nasu Defoltnu komponentu i da nadajcamo i napsiemo svoje metode i da se one mogu koristiti bi bio 
#    Okvirna metoda

# 2. obrazac koji nam omogucje da registiramo neki keybind i onda tek kada se neki dodagajd dodi da reagiramo je Observer