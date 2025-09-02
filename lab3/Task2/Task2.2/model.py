from undo import InsertAction, DeleteAction, UndoManager

class Location:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return f"({self.row}, {self.col})"
    
class LocationRange:
    def __init__(self, begin, end):
        self.begin = begin  
        self.end = end      

    def __str__(self):
        return f"Range: {self.start}-{self.end}"
    
class TextEditorModel:
    def __init__(self, text):
        self.lines = text.split('\n')
        self.cursorLocation = Location(0, 0)
        self.selectionRange = None
        self.cursor_observers = []
        self.text_observers = []

    def getSelectionRange(self):
        return self.selectionRange

    def setSelectionRange(self, new_range):
        if self.selectionRange != new_range:
            self.selectionRange = new_range
            self.notify_cursor_observers()
    
    def deleteRange(self, r, from_undo=False):
        if not r or r.begin == r.end:
            return False
        location_before = Location(r.begin.row, r.begin.col)
        deleted_text = self.getTextFromRange(r)
        start_loc = r.begin 
        end_loc = r.end
        text_changed = False
        if start_loc.row == end_loc.row:
            line_content = self.lines[start_loc.row]
            self.lines[start_loc.row] = line_content[:start_loc.col] + line_content[end_loc.col:]
            text_changed = True
        else:
            first_line_part = self.lines[start_loc.row][:start_loc.col]
            last_line_part = self.lines[end_loc.row][end_loc.col:]
            self.lines[start_loc.row] = first_line_part + last_line_part
            del self.lines[start_loc.row + 1 : end_loc.row + 1]
            text_changed = True
        if text_changed:
            self.cursorLocation = Location(start_loc.row, start_loc.col)
            self.selectionRange = None
            action = DeleteAction(self, deleted_text, location_before, self.cursorLocation)
            UndoManager.getInstance().push(action= action)
            if not from_undo:
                action = DeleteAction(self, deleted_text, location_before, self.cursorLocation)
                UndoManager.getInstance().push(action)
            self.notify_cursor_observers()
            self.notify_text_observers()
        return text_changed
    
    def getTextFromRange(self, row):
        if not row or row.begin == row.end:
            return ""
        start_loc = row.begin
        end_loc = row.end
        if (start_loc.row > end_loc.row) or (start_loc.row == end_loc.row and start_loc.col > end_loc.col):
            start_loc, end_loc = end_loc, start_loc
        selected_parts = []
        if start_loc.row == end_loc.row:
            selected_parts.append(self.lines[start_loc.row][start_loc.col:end_loc.col])
        else:
            selected_parts.append(self.lines[start_loc.row][start_loc.col:])
            for i in range(start_loc.row + 1, end_loc.row):
                selected_parts.append(self.lines[i])
            selected_parts.append(self.lines[end_loc.row][:end_loc.col])
        return "\n".join(selected_parts)

    def lines_iterator(self):
        for line in self.lines:
            yield line
    
    def range_lines_iterator(self, start, end):
        start = max(0, start)
        end = min(len(self.lines), end)

        if start < end:
            for line in self.lines[start:end]:
                yield line

    def register_cursor_observer(self, observer):
        self.cursor_observers.append(observer)
    def remove_cursor_observer(self, observer):
        self.cursor_observers.remove(observer)
    def notify_cursor_observers(self):
        for o in self.cursor_observers:
            o.updateCursorLocation(self.cursorLocation)
    
    def register_text_observer(self, observer):
        self.text_observers.append(observer)
    def remove_text_observer(self, observer):
        self.text_observers.remove(observer)
    def notify_text_observers(self):
        for o in self.text_observers:
            o.updateText()

    def moveCursorLeft(self):
        row, col = self.cursorLocation.row, self.cursorLocation.col
        if col > 0:
            self.cursorLocation.col -= 1
        elif row > 0:
            self.cursorLocation.row -= 1
            self.cursorLocation.col = len(self.lines[row - 1])
        self.notify_cursor_observers()
    def moveCursorRight(self):
        row, col = self.cursorLocation.row, self.cursorLocation.col
        line_length = len(self.lines[row])
        
        if col < line_length:
            self.cursorLocation.col += 1
        elif row < len(self.lines) - 1:
            self.cursorLocation.row += 1
            self.cursorLocation.col = 0
        self.notify_cursor_observers()
    def moveCursorUp(self):
        if self.cursorLocation.row > 0:
            self.cursorLocation.row -= 1
            new_row_len = len(self.lines[self.cursorLocation.row])
            self.cursorLocation.col = min(self.cursorLocation.col, new_row_len)
            self.notify_cursor_observers()
    def moveCursorDown(self):
        if self.cursorLocation.row < len(self.lines) - 1:
            self.cursorLocation.row += 1
            new_row_len = len(self.lines[self.cursorLocation.row])
            self.cursorLocation.col = min(self.cursorLocation.col, new_row_len)
            self.notify_cursor_observers()
    def deleteBefore(self, from_undo=False):
        location_before = Location(self.cursorLocation.row, self.cursorLocation.col)
        deleted_text = ""
        text_changed = False
        if self.selectionRange and self.selectionRange.begin != self.selectionRange.end:
            deleted_text = self.getTextFromRange(self.selectionRange)
            text_changed = self.deleteRange(self.selectionRange)
            location_after = Location(self.cursorLocation.row, self.cursorLocation.col)
        else:
            row, col = self.cursorLocation.row, self.cursorLocation.col
            if col > 0:
                deleted_text = self.lines[row][col-1]
                self.lines[row] = self.lines[row][:col-1] + self.lines[row][col:]
                self.cursorLocation.col -= 1
                text_changed = True
            elif col == 0 and row > 0:
                deleted_text = "\n"
                current_line = self.lines.pop(row)
                prev_line_len = len(self.lines[row-1])
                self.lines[row-1] += current_line
                self.cursorLocation.row -= 1
                self.cursorLocation.col = prev_line_len
                text_changed = True
            location_after = Location(self.cursorLocation.row, self.cursorLocation.col)
        if text_changed and not from_undo:
            location_after = Location(self.cursorLocation.row, self.cursorLocation.col)
            action = DeleteAction(self, deleted_text, location_before, location_after)
            UndoManager.getInstance().push(action)
        if text_changed:
            action = DeleteAction(self, deleted_text, location_before, location_after)
            UndoManager.getInstance().push(action)
            self.notify_cursor_observers()
            self.notify_text_observers()
        return text_changed
    def deleteAfter(self, from_undo=False):
        location_before = Location(self.cursorLocation.row, self.cursorLocation.col)
        deleted_text = ""
        text_changed = False
        if self.selectionRange and self.selectionRange.begin != self.selectionRange.end:
            deleted_text = self.getTextFromRange(self.selectionRange)
            text_changed = self.deleteRange(self.selectionRange)
            location_after = Location(self.cursorLocation.row, self.cursorLocation.col)
        else:
            row, col = self.cursorLocation.row, self.cursorLocation.col
            if row < len(self.lines):
                line_content = self.lines[row]
                if col < len(line_content):
                    deleted_text = line_content[col]
                    self.lines[row] = line_content[:col] + line_content[col+1:]
                    text_changed = True
                elif row < len(self.lines) - 1:
                    deleted_text = "\n"
                    next_line = self.lines[row+1]
                    self.lines[row] += self.lines.pop(row + 1)
                    text_changed = True
                location_after = Location(self.cursorLocation.row, self.cursorLocation.col)
        if text_changed and not from_undo:
            location_after = Location(self.cursorLocation.row, self.cursorLocation.col)
            action = DeleteAction(self, deleted_text, location_before, location_after)
            UndoManager.getInstance().push(action)
        if text_changed:
            action = DeleteAction(self, deleted_text, location_before, location_after)
            UndoManager.getInstance().push(action)
            self.notify_cursor_observers()
            self.notify_text_observers()
        return text_changed
    def handleReturn(self, from_undo=False):
        location_before = Location(self.cursorLocation.row, self.cursorLocation.col)
        if self.selectionRange and self.selectionRange.begin != self.selectionRange.end:
            self.deleteRange(self.selectionRange)
        row, col = self.cursorLocation.row, self.cursorLocation.col
        line = self.lines[row]
        new_old_line = line[:col]
        new_new_line = line[col:]
        self.lines.insert(row + 1, new_new_line)
        self.lines[row] = new_old_line
        self.cursorLocation.row += 1
        self.cursorLocation.col = 0
        location_after = Location(self.cursorLocation.row, self.cursorLocation.col)
        action = InsertAction(self, "\n", location_before, location_after)
        UndoManager.getInstance().push(action)
        if not from_undo:
            location_after = Location(self.cursorLocation.row, self.cursorLocation.col)
            action = InsertAction(self, "\n", location_before, location_after)
            UndoManager.getInstance().push(action)
        self.notify_cursor_observers()
        self.notify_text_observers()
    def insert(self, text_to_insert: str, from_undo=False):
        if self.selectionRange and self.selectionRange.begin != self.selectionRange.end:
            self.deleteRange(self.selectionRange)

        location_before = Location(self.cursorLocation.row, self.cursorLocation.col)
        row, col = self.cursorLocation.row, self.cursorLocation.col
        lines_to_insert = text_to_insert.split('\n')

        if len(lines_to_insert) == 1: 
            single_line_text = lines_to_insert[0]
            if row >= len(self.lines): self.lines.append("")
            current_line = self.lines[row]
            self.lines[row] = current_line[:col] + single_line_text + current_line[col:]
            self.cursorLocation.col += len(single_line_text)
        else: 
            if row >= len(self.lines): self.lines.append("")
            first_part = lines_to_insert[0]
            text_after_cursor_in_original_line = self.lines[row][col:]
            self.lines[row] = self.lines[row][:col] + first_part
            self.cursorLocation.col = len(self.lines[row]) 
            for i in range(1, len(lines_to_insert)):
                self.cursorLocation.row += 1 
                middle_part = lines_to_insert[i]
                if i == len(lines_to_insert) - 1: 
                    self.lines.insert(self.cursorLocation.row, middle_part + text_after_cursor_in_original_line)
                    self.cursorLocation.col = len(middle_part) 
                else: 
                    self.lines.insert(self.cursorLocation.row, middle_part)
                    self.cursorLocation.col = len(middle_part) 
        
        location_after = Location(self.cursorLocation.row, self.cursorLocation.col)
        action = InsertAction(self, text_to_insert, location_before, location_after)
        UndoManager.getInstance().push(action)
        if not from_undo:
            location_after = Location(self.cursorLocation.row, self.cursorLocation.col)
            action = InsertAction(self, text_to_insert, location_before, location_after)
            UndoManager.getInstance().push(action)
        self.notify_cursor_observers()
        self.notify_text_observers()

    def handlePrintable(self, char):
        self.insert(char)