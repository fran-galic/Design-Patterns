import tkinter as tk
import signal
import sys
from model import TextEditorModel
from editor_view import TextEditor
from undo import UndoManager

def sigint_handler(sig, frame):
    print("Zatvaram editor.")
    sys.exit(0)

def on_close(window):
    print("Zatvaram aplikaciju.")
    window.destroy()
    sys.exit(0)

def main():
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Greška pri učitavanju datoteke: {e}")
            exit(1)
    else:
        text = "Ovo je moj prvi teskt!\nOvo je jako cool!\nVolimo OOUP!"

    signal.signal(signal.SIGINT, sigint_handler)

    model = TextEditorModel(text)
    undo_manager = UndoManager.getInstance()

    main_window = tk.Tk()
    main_window.title("My Text Editor")
    editor = TextEditor(main_window, model, width=800, height=800)
    main_window.protocol("WM_DELETE_WINDOW", lambda: on_close(main_window))

    main_window.mainloop()

if __name__ == "__main__":
    main()