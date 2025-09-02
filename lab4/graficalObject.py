from __future__ import annotations
from abc import ABC, abstractmethod
from functools import reduce
from math import sqrt
from typing import List
import math
from collections.abc import Sequence
import tkinter as tk
from tkinter import Canvas, ttk
    
class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    def getX(self):
        return self._x
    def getY(self):
        return self._y
    def translate(self, transition: Point):
        self._x += transition.getX()
        self._y += transition.getY()
    def difference(self, point: Point):
        return Point(self.getX() - point.getX(), self.getY() - point.getY())
    
class HotPoint(Point):
    def __init__(self, x, y, selected = False):
        super().__init__(x, y)
        self._selected = selected
    def setSelected(self, selected : bool):
        self._selected = selected
    def getSelected(self):
        return self._selected

class Rectangle:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
    def getX(self):
        return self._x
    def getY(self):
        return self._y
    def getWidth(self):
        return self._width
    def getHeight(self):
        return self._height
    
class AbstractGraphicalObject(ABC):
    def __init__(self, hotPoints: List[HotPoint] = None, selected = False):
        self._hotpoints = hotPoints if hotPoints is not None else []
        self._is_selected = selected
        self._go_listeners = []

    # uređivanje objekta
    def isSelected(self):
        return self._is_selected
    def setSelected(self, selected: bool):
        if self._is_selected != selected:
            self._is_selected = selected
            self.notifySelectionObservers()
    def getNumberOfHotPoints(self):
        return len(self._hotpoints)
    def getHotPoint(self, index: int):
        return self._hotpoints[index]
    # mozd abi ovja hot point mozda trebao dodavit stvair istu u polje hot pointova
    def setHotPoint(self, index: int, point: HotPoint):
        if index < len(self._hotpoints):
            self._hotpoints[index]._x = point.getX()
            self._hotpoints[index]._y = point.getY()
            self.notifyObservers()
    def isHotPointSelected(self, index: int):
        return self._hotpoints[index].getSelected()
    def setHotPointSelected(self, index: int, selected: bool):
        if index < len(self._hotpoints):
            self._hotpoints[index].setSelected(selected)
            self.notifyObservers()
    def getHotPointDistance(self, index: int, mousePoint: Point):
        return GeometryUtil.distanceFromPoint(self.getHotPoint(index), mousePoint)

    # gemottrijkse operacije:
    def translate(self, delta: Point):
        for hp in self._hotpoints:
            hp.translate(delta)
        self.notifyObservers()
    def getBoundingBox(self):
        if not self._hotpoints:
            return Rectangle(0, 0, 0, 0)
        max_x = max(hp.getX() for hp in self._hotpoints)
        max_y = max(hp.getY() for hp in self._hotpoints)
        min_x = min(hp.getX() for hp in self._hotpoints)
        min_y = min(hp.getY() for hp in self._hotpoints)
        return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

    def addGraphicalObjectListener(self, go_listener: GraphicalObjectListener):
        self._go_listeners.append(go_listener)
    def removeGraphicalObjectListener(self, go_listener: GraphicalObjectListener):
        self._go_listeners.remove(go_listener)
    def notifyObservers(self):
        for o in self._go_listeners:
            o.graphicalObjectChanged(self)
    def notifySelectionObservers(self):
        for o in self._go_listeners:
            o.graphicalObjectSelectionChanged(self)
    
    @abstractmethod
    def selectionDistance(self, mousePoint: Point):
        pass
    @abstractmethod
    def getShapeName(self):
        pass
    @abstractmethod
    def duplicate(self):
        pass
    # @abstractmethod
    # def getShapeId(self):
    #     pass
    # @abstractmethod
    # def load(self, stack: List["AbstractGraphicalObject"], row: str):
    #     pass
    # @abstractmethod
    # def save(self):
    #     pass
    @abstractmethod
    def render(self, r: Renderer):
        pass

class GeometryUtil:
    @staticmethod
    def distanceFromPoint(p1: Point, p2: Point):
        return sqrt((p1.getX() - p2.getX())**2 + (p1.getY() - p2.getY())**2)
    @staticmethod
    def distanceFromLineSegment(s: Point, e: Point, p: Point):
        len_sq = (e.getX() - s.getX())**2 + (e.getY() - s.getY())**2
        if len_sq == 0:
            return GeometryUtil.distanceFromPoint(p, s)
        dot = (p.getX() - s.getX()) * (e.getX() - s.getX()) + (p.getY() - s.getY()) * (e.getY() - s.getY())
        t = dot / len_sq
        if t < 0:
            return GeometryUtil.distanceFromPoint(p, s)
        elif t > 1:
            return GeometryUtil.distanceFromPoint(p, e)
        else:
            numerator = abs((e.getX() - s.getX()) * (s.getY() - p.getY()) - (s.getX() - p.getX()) * (e.getY() - s.getY()))
            denominator = sqrt(len_sq)
            return numerator / denominator

class GraphicalObjectListener(ABC):
    # Poziva se kad se nad objektom promjeni bio što...
    @abstractmethod
    def graphicalObjectChanged(self, go: AbstractGraphicalObject):
        pass

    # Poziva se isključivo ako je nad objektom promjenjen status selektiranosti
	# (baš objekta, ne njegovih hot-point-a).
    @abstractmethod
    def graphicalObjectSelectionChanged(self, go: AbstractGraphicalObject):
        pass


class LineSegment(AbstractGraphicalObject):
    def __init__(self, s: HotPoint = None, e: HotPoint = None):
        if s is None and e is None:
            super().__init__([HotPoint(0, 0), HotPoint(10, 0)])
        elif s is not None and e is not None:
            super().__init__([s, e])
        else:
            raise AttributeError("Potrebno je unijeti obje točke ili nijednu")
    def selectionDistance(self, mousePoint: Point):
        return GeometryUtil.distanceFromLineSegment(self.getHotPoint(0), self.getHotPoint(1), mousePoint)
    def duplicate(self):
        hp0 = self.getHotPoint(0)
        hp1 = self.getHotPoint(1)
        return LineSegment(
            HotPoint(hp0.getX(), hp0.getY()),
            HotPoint(hp1.getX(), hp1.getY())
        )
    def getShapeName(self):
        return "Linija"
    def render(self, r: Renderer): r.drawLine(self.getHotPoint(0), self.getHotPoint(1))

class Oval(AbstractGraphicalObject):
    def __init__(self, right: HotPoint = None, bottom: HotPoint = None):
        if right is None and bottom is None:
            super().__init__([HotPoint(10, 0), HotPoint(0, 10)])
        elif right is not None and bottom is not None:
            super().__init__([right, bottom])
        else:
            raise AttributeError("Potrebno je unijeti oba hot-pointa ili nijedan")
        self._update_center()
    def _update_center(self):
        bbox = self.getBoundingBox()
        radius_x = bbox.getWidth() / 2.0
        radius_y = bbox.getHeight() / 2.0
        self.center = Point(bbox.getX() + radius_x, bbox.getY() + radius_y)
    def selectionDistance(self, mousePoint: Point):

        bbox = self.getBoundingBox()
        a = bbox.getWidth() / 2.0
        b = bbox.getHeight() / 2.0
        if a == 0 or b == 0:
            return float('inf')
        cx = self.center.getX()
        cy = self.center.getY()
        dx = mousePoint.getX() - cx
        dy = mousePoint.getY() - cy
        p = ((dx / a)**2) + ((dy / b)**2)
        return abs(math.sqrt(p) - 1.0)
    def duplicate(self):
        hp0 = self.getHotPoint(0)
        hp1 = self.getHotPoint(1)
        return Oval(
            HotPoint(hp0.getX(), hp0.getY()),
            HotPoint(hp1.getX(), hp1.getY())
        )
    def getShapeName(self):
        return "Oval"
    def translate(self, delta: Point):
        super().translate(delta)
        self._update_center()
    def setHotPoint(self, index: int, point: Point):
        super().setHotPoint(index, point)
        self._update_center()
    def render(self, r : Renderer): 
        r.drawOval(self.getBoundingBox())

class CompositeShape(AbstractGraphicalObject):
    def __init__(self, children):
        super().__init__([])
        self.children = list(children)
    def get_children(self):
        return self.children
    def translate(self, delta):
        for child in self.children:
            child.translate(delta)
    def render(self, r):
        for child in self.children:
            child.render(r)
    def selectionDistance(self, p):
        if not self.children:
            return float('inf')
        all_distances = map(lambda child: child.selectionDistance(p), self.children)
        return min(all_distances)

    def _union_of_two_bboxes(self, box1, box2):
        if not box1: return box2
        if not box2: return box1
        x1 = min(box1.getX(), box2.getX())
        y1 = min(box1.getY(), box2.getY())
        x2 = max(box1.getX() + box1.getWidth(), box2.getX() + box2.getWidth())
        y2 = max(box1.getY() + box1.getHeight(), box2.getY() + box2.getHeight())
        return Rectangle(x1, y1, x2 - x1, y2 - y1)
    def getBoundingBox(self):
        if not self.children:
            return Rectangle(0, 0, 0, 0)
        child_bboxes = map(lambda child: child.getBoundingBox(), self.children)
        union_box = reduce(self._union_of_two_bboxes, child_bboxes)
        return union_box
    def duplicate(self):
        duplicated_children = list(map(lambda child: child.duplicate(), self.children))
        return CompositeShape(duplicated_children)

    def getShapeName(self):
        return "Grupa"

class Renderer(ABC):
    @abstractmethod
    def drawLine(self, s : Point, e : Point):
        pass

    @abstractmethod
    def fillPolygon(self, points : List[Point]):
        pass

    # dodo sam svoje jer je stvarno puno lakse
    @abstractmethod
    def drawOval(self, bbox: Rectangle):
        pass


### Document model
class DocumentModelListener(ABC):
    @abstractmethod
    def documentChange(self):
        pass

class ReadOnlyGraphicalObject:
    def __init__(self, obj: AbstractGraphicalObject):
        object.__setattr__(self, '_obj', obj)

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def __setattr__(self, name, value):
        raise AttributeError("Read-only objekt")

    def __delattr__(self, name):
        raise AttributeError("Read-only objekt")

    def __repr__(self):
        return f"ReadOnly{repr(self._obj)}"

class ReadOnlyList(Sequence):
    def __init__(self, original_list):
        self._original = original_list
        self._cache = {}
    def __getitem__(self, index):
        item = self._original[index]
        cached = self._cache.get(id(item))
        if cached is None or cached._obj is not item:
            cached = ReadOnlyGraphicalObject(item)
            self._cache[id(item)] = cached
        return cached
    def __len__(self):
        return len(self._original)
    def __repr__(self):
        return f"ReadOnlyList({self._original!r})"


class DocumentModel(GraphicalObjectListener):
    SELECTION_PROXIMITY = 10
    def __init__(self, objects=None):
        self._objects = objects if objects is not None else []
        self._ro_objects = ReadOnlyList(self._objects)
        self._listeners = []
        self._selected_objects = [o for o in self._objects if o.isSelected()]
        self._ro_selected_objects = ReadOnlyList(self._selected_objects)
        self._register_on_all_objects()
    def clear(self):
        for o in self._objects: o.removeGraphicalObjectListener(self)
        self._objects.clear(); self._selected_objects.clear()
        self._notify_listeners()
    def graphicalObjectChanged(self, go): self._notify_listeners()
    def graphicalObjectSelectionChanged(self, go):
        is_sel, is_in_list = go.isSelected(), go in self._selected_objects
        if is_sel and not is_in_list: self._selected_objects.append(go)
        elif not is_sel and is_in_list: self._selected_objects.remove(go)
        self._notify_listeners()
    def _register_on_all_objects(self):
        for o in self._objects: o.addGraphicalObjectListener(self)
    def addGraphicalObject(self, obj):
        self._objects.append(obj); obj.addGraphicalObjectListener(self)
        if obj.isSelected(): self._selected_objects.append(obj)
        self._notify_listeners()
    def removeGraphicalObject(self, obj):
        if obj in self._selected_objects: self._selected_objects.remove(obj)
        if obj in self._objects:
            self._objects.remove(obj); obj.removeGraphicalObjectListener(self)
            self._notify_listeners()
    def list(self): return self._ro_objects
    def addDocumentModelListener(self, l): self._listeners.append(l)
    def removeDocumentModelListener(self, l):
        if l in self._listeners: self._listeners.remove(l)
    def getSelectedObjects(self): return self._ro_selected_objects
    def increaseZ(self, go):
        try:
            idx = self._objects.index(go)
            if idx < len(self._objects) - 1:
                self._objects[idx], self._objects[idx+1] = self._objects[idx+1], self._objects[idx]
                self._notify_listeners()
        except ValueError: pass # Ignoriraj ako objekt nije u listi
    def decreaseZ(self, go):
        try:
            idx = self._objects.index(go)
            if idx > 0:
                self._objects[idx], self._objects[idx-1] = self._objects[idx-1], self._objects[idx]
                self._notify_listeners()
        except ValueError: pass # Ignoriraj ako objekt nije u listi
    def findSelectedGraphicalObject(self, p):
        closest, min_dist = None, self.SELECTION_PROXIMITY
        for o in reversed(self._objects):
            dist = o.selectionDistance(p)
            if dist < min_dist:
                min_dist, closest = dist, o
        return closest
    def findSelectedHotPoint(self, obj, p):
        closest_i, min_dist = -1, self.SELECTION_PROXIMITY
        for i in range(obj.getNumberOfHotPoints()):
            dist = obj.getHotPointDistance(i, p)
            if dist < min_dist:
                min_dist, closest_i = dist, i
        return closest_i
    def _notify_listeners(self):
        for l in self._listeners:
            l.documentChange()
    def groupObjects(self, objects_to_group):
        # Kopiraj listu da se može sigurno iterirati i brisati
        for obj in list(objects_to_group):
            self.removeGraphicalObject(obj)
        group = CompositeShape(objects_to_group)
        group.setSelected(True)
        self.addGraphicalObject(group)
    def ungroupObject(self, group):
        children = list(group.get_children())
        self.removeGraphicalObject(group)
        for child in children:
            self.addGraphicalObject(child)
            child.setSelected(True)

# main klasa i 3. dio zadatka
class TkRenderer(Renderer):
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.color = "#FF9999"  
    def drawLine(self, s: Point, e: Point):
        self.canvas.create_line(s.getX(), s.getY(), e.getX(), e.getY(), fill=self.color, width=2)
    def drawOval(self, bbox: Rectangle):
        self.canvas.create_oval(bbox.getX(), bbox.getY(), bbox.getX() + bbox.getWidth(), bbox.getY() + bbox.getHeight(), width=2, outline=self.color)
    def fillPolygon(self, points: List[Point]):
        tk_points = [ [p.getX(), p.getY()] for p in points]
        self.canvas.create_polygon(tk_points, fill=self.color, outline="blue", width=2)

class GUI(tk.Tk):
    def __init__(self, name = "Grafičko sučelje", objects : List[AbstractGraphicalObject] = None):
        super().__init__()
        self.objects = objects if objects is not None else []
        self.title(name)
        self.model = DocumentModel()
        self.current_state = IdleState()
        toolbar = tk.Frame(self, bd=2, relief=tk.SOLID)
        for obj in self.objects:
            btn = tk.Button(toolbar, text=obj.getShapeName(), command=lambda shape=obj: self.set_state(AddShapeState(self.model, shape.duplicate())))
            btn.pack(side=tk.LEFT, padx=3, pady=3)
        select_btn = tk.Button(toolbar, text="Selektiraj", command=lambda: self.set_state(SelectShapeState(self.model)))
        select_btn.pack(side=tk.LEFT, padx=3, pady=3)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.canvas = Canvas(self, self.model, bg="white")
        self.init_bindings()
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.geometry("500x500")

    def init_bindings(self):
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Motion>", self.on_mouse_dragged)
        self.bind_all("<Escape>", self.on_escape_key) 
        self.canvas.focus_set() 
        self.canvas.bind("<KeyPress>", self.on_key_press)
    def on_mouse_down(self, event):
        shift = (event.state & 0x0001) != 0
        ctrl = (event.state & 0x0004) != 0
        self.current_state.mouseDown(Point(event.x, event.y), shift, ctrl)
    def on_mouse_up(self, event):
        shift = (event.state & 0x0001) != 0
        ctrl = (event.state & 0x0004) != 0
        self.current_state.mouseUp(Point(event.x, event.y), shift, ctrl)
    def on_mouse_dragged(self, event):
        self.current_state.mouseDragged(Point(event.x, event.y))
    def on_key_press(self, event):
        self.current_state.keyPressed(event.keysym)
    def on_escape_key(self, event):
        self.set_state(IdleState())
    def set_state(self, new_state: IdleState):
        self.current_state.onLeaving()
        self.current_state = new_state
    def get_current_state(self):
        return self.current_state

class IdleState:
    # poziva se kad progam registrira da je pritisnuta lijeva tipka miša
    def mouseDown(self, mousePoint : Point, shiftDown : bool, ctrlDown : bool):
        return
    # poziva se kad progam registrira da je otpuštena lijeva tipka miša
    def mouseUp(self, mousePoint : Point, shiftDown : bool, ctrlDown : bool):
        return
    # poziva se kad progam registrira da korisnik pomiče miš dok je tipka pritisnuta
    def mouseDragged(self, mousePoint : Point):
        return
    # poziva se kad progam registrira da je korisnik pritisnuo tipku na tipkovnici
    def keyPressed(self, keyCode : int):
        return
    # Poziva se nakon što je platno nacrtalo grafički objekt predan kao argument
    def afterDraw(self, r : Renderer, go : AbstractGraphicalObject):
        return
    def afterDrawAll(self, r : Renderer):
        return
    # Poziva se kada program napušta ovo stanje kako bi prešlo u neko drugo
    def onLeaving(self):
        return

class AddShapeState(IdleState):
    def __init__(self, model: DocumentModel, prototype: AbstractGraphicalObject):
        self.model = model
        self.prototype = prototype
    def mouseDown(self, mousePoint, shiftDown, ctrlDown):
        new_obj = self.prototype.duplicate()
        new_obj.translate(mousePoint)
        self.model.addGraphicalObject(new_obj)

class SelectShapeState(IdleState):
    def __init__(self, model):
        self.model = model
        self.dragged_object = None
        self.dragged_hot_point_index = -1
        self.last_point = None
    def mouseDown(self, mousePoint, shiftDown, ctrlDown):
        obj = self.model.findSelectedGraphicalObject(mousePoint)
        if obj is None:
            if not ctrlDown:
                for o in list(self.model.getSelectedObjects()):
                    o.setSelected(False)
            return
        selected_list = list(self.model.getSelectedObjects())
        if obj.isSelected() and len(selected_list) == 1 and not isinstance(obj, CompositeShape):
            hp_index = self.model.findSelectedHotPoint(obj, mousePoint)
            if hp_index != -1:
                self.dragged_object = obj
                self.dragged_hot_point_index = hp_index
                self.last_point = mousePoint
                return
        if not ctrlDown:
            for o in selected_list:
                if o is not obj:
                    o.setSelected(False)
        obj.setSelected(not obj.isSelected())
        self.dragged_object = obj if obj.isSelected() else None
        self.last_point = mousePoint
    def mouseUp(self, mousePoint, shiftDown, ctrlDown):
        self.dragged_object = None
        self.dragged_hot_point_index = -1
        self.last_point = None
    def mouseDragged(self, mousePoint):
        if self.dragged_object is None or self.last_point is None:
            return
        delta = mousePoint.difference(self.last_point)
        if self.dragged_hot_point_index != -1:
            hp = self.dragged_object.getHotPoint(self.dragged_hot_point_index)
            new_pos = Point(hp.getX() + delta.getX(), hp.getY() + delta.getY())
            self.dragged_object.setHotPoint(self.dragged_hot_point_index, new_pos)
        else:
            self.dragged_object.translate(delta)
        self.last_point = mousePoint
    def keyPressed(self, keyCode):
        selected_objects = list(self.model.getSelectedObjects())
        keyCode_lower = keyCode.lower()

        if keyCode_lower == 'escape':
            for obj in selected_objects:
                obj.setSelected(False)
            return
        
        if not selected_objects: return

        if keyCode_lower == 'delete':
            for obj in selected_objects:
                self.model.removeGraphicalObject(obj)
            return
        if keyCode_lower == 'g':
            if len(selected_objects) > 1:
                self.model.groupObjects(selected_objects)
            return
        elif keyCode_lower == 'u':
            if len(selected_objects) == 1 and isinstance(selected_objects[0], CompositeShape):
                self.model.ungroupObject(selected_objects[0])
            return

        key_map = {'up': Point(0, -1), 'down': Point(0, 1), 'left': Point(-1, 0), 'right': Point(1, 0)}
        if keyCode_lower in key_map:
            for obj in selected_objects:
                obj.translate(key_map[keyCode_lower])
            return

        if keyCode_lower == 'plus' or keyCode_lower == 'kp_add':
            for obj in selected_objects:
                self.model.increaseZ(obj)
        elif keyCode_lower == 'minus' or keyCode_lower == 'kp_subtract':
            for obj in selected_objects:
                self.model.decreaseZ(obj)
    def afterDrawAll(self, r):
        selected = list(self.model.getSelectedObjects())
        for obj in selected:
            bbox = obj.getBoundingBox()
            x1, y1 = bbox.getX(), bbox.getY()
            x2, y2 = x1 + bbox.getWidth(), y1 + bbox.getHeight()
            r.canvas.create_rectangle(x1, y1, x2, y2, outline='red', dash=(2, 4))
        if len(selected) == 1 and not isinstance(selected[0], CompositeShape):
            obj = selected[0]
            handle_size = 3
            for i in range(obj.getNumberOfHotPoints()):
                hp = obj.getHotPoint(i)
                r.canvas.create_rectangle(
                    hp.getX() - handle_size, hp.getY() - handle_size,
                    hp.getX() + handle_size, hp.getY() + handle_size,
                    fill='red', outline='red'
                )
    def onLeaving(self):
        for obj in list(self.model.getSelectedObjects()):
            obj.setSelected(False)
            
class Canvas(tk.Canvas, DocumentModelListener):
    def __init__(self, master, document_model : DocumentModel, **kwr):
        tk.Canvas.__init__(self, master, **kwr)
        self.document_model = document_model
        self.document_model.addDocumentModelListener(self)
        self.renderer = TkRenderer(self)
        self.master = master
    def documentChange(self):
        self.redraw()
    def redraw(self):
        self.delete("all")
        for obj in self.document_model.list():
            obj.render(self.renderer)
            self.master.get_current_state().afterDraw(self.renderer, obj)
        self.master.get_current_state().afterDrawAll(self.renderer)


def main():
    objects = [
        LineSegment(),
        Oval()
    ]
    gui = GUI(objects=objects)
    gui.mainloop()

if __name__ == "__main__":
    main()
