class CursorObserver:
    def updateCursorLocation(self, location):
        raise NotImplementedError("Observer mora imati implementiranu metodu updateCursorLocation")

class TextObserver:
    def updateText(self):
        raise NotImplementedError("Observer mora imati implementiranu metodu updateText")

class ClipboardObserver:
    def updateClipboard(self):
        raise NotImplementedError("Observer mora imati implementiranu metodu updateClipboard")

class UndoRedoObserver:
    def update_undo_redo_status(self, can_undo, can_redo):
        raise NotImplementedError("Metoda update_undo_redo_status mora biti implementirana")