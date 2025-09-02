from observers import ClipboardObserver

class ClipboardStack:
    def __init__(self):
        self.texts = [] 
        self.observers = []
    def register_observer(self, observer: ClipboardObserver):
        if observer not in self.observers:
            self.observers.append(observer)
    def remove_observer(self, observer : ClipboardObserver):
        if observer in self.observers:
            self.observers.remove(observer)
    def notify_observers(self):
        for observer in self.observers:
            observer.updateClipboard()
    def push(self, text_data):
        self.texts.append(text_data)
        self.notify_observers()
    def pop(self):
        if not len(self.texts) == 0:
            text_data = self.texts.pop()
            self.notify_observers()
            return text_data
        return None
    def peek(self):
        if not len(self.texts) == 0:
            return self.texts[-1]
        return None
    def clear_stack(self):
        if not len(self.texts) == 0: 
            self.texts.clear()
            self.notify_observers()