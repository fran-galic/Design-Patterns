  #include <iostream>
  #include <assert.h>
  #include <stdlib.h>

  struct Point{
    int x; int y;
  };

  class Shape{
    public:
        enum EType {circle, square, rhomb}; 
        EType type_;
        virtual void draw()=0;
        virtual bool hasCenter() const { return false; }
  };
  class ShapeWithCenter: public Shape {
    public:
        Point center_;
        bool hasCenter() const override { return true; }
  };

  class Circle : public ShapeWithCenter{
    public: 
     double radius_;
     void draw() {
        std::cerr << "in drawCircle\n";
        std::cerr << "Center: (" << this->center_.x << ", " << this->center_.y << ")\n";
    }
  };
  class Square : public ShapeWithCenter{
    public:
     double side_;
     void draw() {
        std::cerr << "in drawSquare\n";
        std::cerr << "Center: (" << this->center_.x << ", " << this->center_.y << ")\n";
     }
  };
  class Rhomb : public ShapeWithCenter{
    public:
        double side_;
        double alpha;
        void draw() {
            std::cerr << "in drawRhomb\n";
            std::cerr << "Center: (" << this->center_.x << ", " << this->center_.y << ")\n";
        }
  };

// KOMENTAR: bolja verzija jer tu koristimo inverziju ovinsoti i omogucava nam Nadogradnju bez promjene i puno vise fleksibilnosti
void drawShapes(Shape** shapes, int n){
    for (int i=0; i<n; ++i){
      struct Shape* s = shapes[i];
      s->draw();
    }
  }
// Također vrjedi kao i gore
void moveShapes(Shape** shapes, int n, int x, int y){
    for (int i = 0; i < n; i++){
        Shape* s = shapes[i];
        if (s->hasCenter()) {
                ((ShapeWithCenter*)s)->center_.x = ((ShapeWithCenter*)s)->center_.x + x;
                ((ShapeWithCenter*)s)->center_.y = ((ShapeWithCenter*)s)->center_.y + y;
        }
    }
}

  // moglo se još napraviti da se automatski postave type pri stvaranju specifcine klase ali to se ne trazi u zadataku pa sam za sada ovako ostavio
  int main(){
    Shape* shapes[5];
    shapes[0]=(Shape*)new Circle;
    shapes[0]->type_=Shape::circle;
    shapes[1]=(Shape*)new Square;
    shapes[1]->type_=Shape::square;
    shapes[2]=(Shape*)new Square;
    shapes[2]->type_=Shape::square;
    shapes[3]=(Shape*)new Circle;
    shapes[3]->type_=Shape::circle;;
    shapes[4]=(Shape*)new Rhomb;
    shapes[4]->type_=Shape::rhomb;


    moveShapes(shapes, 5, 2, 1);
    drawShapes(shapes, 5);
  }