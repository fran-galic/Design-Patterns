import tkinter as tk


main_window = tk.Tk()

canvas = tk.Canvas(main_window, width=300, height=300)
canvas.pack()

canvas.create_line(100,200,200,35, fill="green", width=5)
canvas.create_polygon(50, 50, 180, 50, 100, 150, fill="blue")
canvas.create_text(100, 100, text="Pozdrav!")

def on_key(event):
    print(f"Na Canvasu pritisnuto: {event.keysym}")
    if event.keysym == "f":
        print("Zatvaram prozor.")
        main_window.destroy()

canvas.focus_set()
canvas.bind("<Key>", on_key)

main_window.mainloop()
