from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model import TextEditorModel, LocationRange, Location

class EditAction:
    def execute_do(self):
        raise NotImplementedError("Metoda execute_do mora biti implementirana")
    def execute_undo(self):
        raise NotImplementedError("Metoda execute_undo mora biti implementirana")

class InsertAction(EditAction):
    def __init__(self, model, text, location_before, location_after):
        self.model = model
        self.text = text
        self.location_before = location_before
        self.location_after = location_after
    def execute_do(self):
        self.model.cursorLocation = self.location_before
        self.model.insert(self.text, from_undo=True)
        self.model.cursorLocation = self.location_after
    def execute_undo(self):
        self.model.cursorLocation = self.location_after
        start_row = self.location_before.row
        start_col = self.location_before.col
        end_row = self.location_after.row
        end_col = self.location_after.col
        self.model.cursorLocation = Location(start_row, start_col)
        self.model.selectionRange = LocationRange(
            Location(start_row, start_col),
            Location(end_row, end_col)
        )
        self.model.deleteRange(self.model.selectionRange, from_undo=True)
        self.model.selectionRange = None
        self.model.cursorLocation = self.location_before
class DeleteAction(EditAction):
    def __init__(self, model, deleted_text, location_before, location_after):
        self.model = model
        self.deleted_text = deleted_text
        self.location_before = location_before
        self.location_after = location_after
    def execute_do(self):
        self.model.cursorLocation = self.location_before
        self.model.selectionRange = LocationRange(self.location_before, self.location_after)
        self.model.deleteRange(self.model.selectionRange, from_undo=True)
        self.model.cursorLocation = self.location_before
    def execute_undo(self):
        self.model.cursorLocation = self.location_before
        self.model.insert(self.deleted_text, from_undo=True)
        self.model.cursorLocation = self.location_after

class UndoManager:
    _instance = None

    @staticmethod
    def getInstance():
        if UndoManager._instance is None:
            UndoManager._instance = UndoManager()
        return UndoManager._instance

    def __init__(self):
        if UndoManager._instance is not None:
            raise Exception("Potrebno je korisitti geInstance metodu")
        self.undo_stack = []
        self.redo_stack = []
        self.observers = []
        UndoManager._instance = self

    def push(self, action: EditAction):
        self.redo_stack.clear()
        self.undo_stack.append(action)
        self.notify_observers()
    def undo(self):
        if not self.undo_stack:
            return
        action = self.undo_stack.pop()
        action.execute_undo()
        self.redo_stack.append(action)
        self.notify_observers()
    def redo(self):
        if not self.redo_stack:
            return
        action = self.redo_stack.pop()
        action.execute_do()
        self.undo_stack.append(action)
        self.notify_observers()
    def register_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
    def notify_observers(self):
        for observer in self.observers:
            observer.update_undo_redo_status(
                can_undo=bool(self.undo_stack),
                can_redo=bool(self.redo_stack)
            )