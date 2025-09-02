import tkinter as tk
import tkinter.font as tkFont
from observers import CursorObserver, TextObserver, ClipboardObserver
from model import TextEditorModel, Location, LocationRange
from clipboard import ClipboardStack
from undo import UndoManager

class TextEditor(tk.Canvas, CursorObserver, TextObserver, ClipboardObserver):
    def __init__(self, parent, model, line_height = 30, x_transition = 5, font_family_name="Courier", **kwargs):
        super().__init__(parent, bg="white", **kwargs)
        self.pack(fill=tk.BOTH, expand=True)
        self.model = model
        self.model.register_cursor_observer(self)
        self.model.register_text_observer(self)
        self.selection_anchor = None
        self.highlight_ids = []
        self.cursor_location = self.model.cursorLocation
        self.clipboard = ClipboardStack()
        self.clipboard.register_observer(self)

        self.line_height = line_height
        self.char_width = self._get_font_for_line_height(line_height, font_family_name).get("char_width")
        self.x_transition = x_transition
        
        font_info = self._get_font_for_line_height(self.line_height, font_family_name)
        self.char_width = font_info.get("char_width")
        self.font = tkFont.Font(family=font_family_name, size=font_info.get("font_size"))

        self.text_ids = []
        self.cursor_id = None
        
        self.focus_set()
        self.bind("<Key>", self.on_key)
        self.bind("<Configure>", lambda e: self.redraw())

        self.redraw()

    def updateCursorLocation(self, location):
        self.cursor_location = location  
        self.redraw()

    def updateText(self):
        self.redraw()

    def updateClipboard(self):
        print("Ovo cudno radi!")


    def redraw(self):
        self.delete("all")
        self.cursor_id = None 
        self.highlight_ids.clear()
        self.text_ids.clear()
        
        selection = self.model.getSelectionRange()
        if selection:
            sel_begin = selection.begin
            sel_end = selection.end

            if (sel_begin.row > sel_end.row) or (sel_begin.row == sel_end.row and sel_begin.col > sel_end.col):
                sel_begin, sel_end = sel_end, sel_begin

            for r in range(sel_begin.row, sel_end.row + 1):
                y0 = r * self.line_height + self.x_transition
                y1 = (r + 1) * self.line_height + self.x_transition

                current_line_text = ""
                if r < len(self.model.lines):
                    current_line_text = self.model.lines[r]
                x0_begin, x1_end = 0, 0

                if r == sel_begin.row == sel_end.row:
                    x0_begin = sel_begin.col * self.char_width + self.x_transition
                    x1_end = sel_end.col * self.char_width + self.x_transition

                elif r == sel_begin.row: 
                    x0_begin = sel_begin.col * self.char_width + self.x_transition
                    x1_end = len(current_line_text) * self.char_width + self.x_transition
                elif r == sel_end.row:
                    x0_begin = self.x_transition
                    x1_end = sel_end.col * self.char_width + self.x_transition
                else:
                    x0_begin = self.x_transition
                    x1_end = len(current_line_text) * self.char_width + self.x_transition
                
                if x1_end > x0_begin: 
                    rect_id = self.create_rectangle(
                        x0_begin, y0, x1_end, y1, 
                        fill="#FF9999", outline=""
                    )
                    self.highlight_ids.append(rect_id)
        
        for i, line_text in enumerate(self.model.lines_iterator()):
            text_y = i * self.line_height + self.x_transition 
            text_id = self.create_text(
                self.x_transition, 
                text_y, 
                anchor="nw", 
                text=line_text, 
                font=self.font,
                fill="black" 
            )
            self.text_ids.append(text_id)

        self.draw_cursor()

    def draw_cursor(self):
        loc = self.model.cursorLocation
        x = loc.col * self.char_width + self.x_transition
        y = loc.row * self.line_height
        self.cursor_id = self.create_line(x, y, x, y + self.line_height, fill="black", width=2)

    def on_key(self, event):
        shift_is_pressed = (event.state & 0x0001) != 0
        control_is_pressed = (event.state & 0x0004) != 0
        old_cursor_loc = Location(self.model.cursorLocation.row, self.model.cursorLocation.col)
        current_selection = self.model.getSelectionRange()
        action_taken_by_model = False

        if control_is_pressed and event.keysym.lower() == 'a':
            start_location = Location(0, 0)
            end_row = len(self.model.lines) - 1
            end_col = len(self.model.lines[end_row])
            end_location = Location(end_row, end_col)
            self.model.setSelectionRange(LocationRange(start_location, end_location))
            self.model.cursorLocation = end_location
            self.redraw()
            return "break"
        if control_is_pressed and not shift_is_pressed and event.keysym.lower() == 'z':
            UndoManager.getInstance().undo()
            return "break"
        elif control_is_pressed and not shift_is_pressed and event.keysym.lower() == 'y':
            UndoManager.getInstance().redo()
            return "break"
        if control_is_pressed and not shift_is_pressed and event.keysym.lower() == 'c':
            selection = self.model.getSelectionRange()
            if selection and selection.begin != selection.end:
                selected_text = self.model.getTextFromRange(selection)
                if selected_text:
                    self.clipboard.push(selected_text)
            return 
        elif control_is_pressed and not shift_is_pressed and event.keysym.lower() == 'x': 
            selection = self.model.getSelectionRange()
            if selection and selection.begin != selection.end:
                selected_text = self.model.getTextFromRange(selection)
                if selected_text:
                    self.clipboard.push(selected_text)
                    self.model.deleteRange(selection) 
            return 
        elif control_is_pressed and not shift_is_pressed and event.keysym.lower() == 'v': 
            text_to_paste = self.clipboard.peek()
            if text_to_paste is not None:
                self.model.insert(text_to_paste)
            return
        elif control_is_pressed and shift_is_pressed and event.keysym.lower() == 'v': 
            text_to_paste = self.clipboard.pop()
            if text_to_paste is not None:
                self.model.insert(text_to_paste)
            return

        if event.char and event.char.isprintable():
            self.model.handlePrintable(event.char)
            action_taken_by_model = True
        elif event.keysym == "Left":
            self.model.moveCursorLeft()
        elif event.keysym == "Right":
            self.model.moveCursorRight()
        elif event.keysym == "Up":
            self.model.moveCursorUp()
        elif event.keysym == "Down":
            self.model.moveCursorDown()
        elif event.keysym == "BackSpace":
            if current_selection and current_selection.begin != current_selection.end:
                self.model.deleteRange(current_selection)
            else:
                self.model.deleteBefore()
            self.model.setSelectionRange(None) 
            action_taken_by_model = True
        elif event.keysym == "Delete":
            current_selection = self.model.getSelectionRange()
            if current_selection and current_selection.begin != current_selection.end:
                self.model.deleteRange(current_selection)
            else:
                self.model.deleteAfter()
            self.model.setSelectionRange(None) 
            action_taken_by_model = True
        elif event.keysym == "Return":
            self.model.handleReturn()
            action_taken_by_model = True

        is_move_key = event.keysym in ["Left", "Right", "Up", "Down"]
        if is_move_key:
            new_cursor_loc = self.model.cursorLocation
            if shift_is_pressed:
                if self.selection_anchor is None:
                    self.selection_anchor = old_cursor_loc
                self.model.setSelectionRange(LocationRange(self.selection_anchor, new_cursor_loc))
            else:
                self.model.setSelectionRange(None)
                self.selection_anchor = None
        elif action_taken_by_model: 
            self.selection_anchor = None 

    def _get_font_for_line_height(self, target_height, font_family="Courier"):
        root = tk.Tk()
        root.withdraw()

        for size in range(1, 100):
            f = tkFont.Font(family=font_family, size=size)
            real_height = f.metrics("linespace")
            if real_height >= target_height:
                char_widths = [f.measure(c) for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"]
                avg_char_width = sum(char_widths) / len(char_widths)

                return {
                    "font_family": font_family,
                    "font_size": size,
                    "line_height": real_height,
                    "char_width": avg_char_width
                }
        return None