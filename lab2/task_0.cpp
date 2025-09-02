  #include <iostream>
  #include <assert.h>
  #include <stdlib.h>

  struct Point{
    int x; int y;
  };
  struct Shape{
    enum EType {circle, square, rhomb};
    EType type_;
  };
  struct Circle{
     Shape::EType type_;
     double radius_;
     Point center_;
  };
  struct Square{
     Shape::EType type_;
     double side_;
     Point center_;
  };
  struct Rhomb{
    Shape::EType type_;
    double side_;
    double alpha;
    Point center_;

  };
void drawSquare(struct Square* sq){
    std::cerr << "in drawSquare\n";
    std::cerr << "Center: (" << sq->center_.x << ", " << sq->center_.y << ")\n";
}

void drawRhomb(struct Rhomb* rh){
    std::cerr << "in drawRhomb\n";
    std::cerr << "Center: (" << rh->center_.x << ", " << rh->center_.y << ")\n";
}

void drawCircle(struct Circle* c){
    std::cerr << "in drawCircle\n";
    std::cerr << "Center: (" << c->center_.x << ", " << c->center_.y << ")\n";
}
  void drawShapes(Shape** shapes, int n){
    for (int i=0; i<n; ++i){
      struct Shape* s = shapes[i];
      switch (s->type_){
      case Shape::square:
        drawSquare((struct Square*)s);
        break;
      case Shape::circle:
        drawCircle((struct Circle*)s);
        break;
      case Shape::rhomb:
        drawRhomb((struct Rhomb*)s);
        break;
      default:
        assert(0); 
        exit(0);
      }
    }
  }
// naravno d anije dobra organzaicja ali mislim da je to i poanta
void moveShapes(Shape** shapes, int n, int x, int y){
    for (int i = 0; i < n; i++){
        Shape* s = shapes[i];
        switch (s->type_){
            case Shape::square:
                ((Square*)s)->center_.x = ((Square*)s)->center_.x + x;
                ((Square*)s)->center_.y = ((Square*)s)->center_.y + y;
                break;
            case Shape::circle:
                ((Circle*)s)->center_.x = ((Circle*)s)->center_.x + x;
                ((Circle*)s)->center_.y = ((Circle*)s)->center_.y + y;
                break;
            // na ovaj naicn se javlja krutost; ako u ovom slucaju adekvatno ne dodmao novu funkcionalnsot
            // svkai puta kada nesto promjenio program ce se srusititi, tj jvalja se lanac ovisnosti a to nam je NEPOŽELJNO
            case Shape::rhomb:
                ((Rhomb*)s)->center_.x = ((Rhomb*)s)->center_.x + x;
                ((Rhomb*)s)->center_.y = ((Rhomb*)s)->center_.y + y;
                break;
            default:
                assert(0); 
                exit(0);
        }
    }
}




  int main(){
    Shape* shapes[5];
    shapes[0]=(Shape*)new Circle;
    shapes[0]->type_=Shape::circle;
    shapes[1]=(Shape*)new Square;
    shapes[1]->type_=Shape::square;
    shapes[2]=(Shape*)new Square;
    shapes[2]->type_=Shape::square;
    shapes[3]=(Shape*)new Circle;
    shapes[3]->type_=Shape::circle;
    shapes[4]=(Shape*)new Rhomb;
    shapes[4]->type_=Shape::rhomb;


    moveShapes(shapes, 5, 2, 1);
    drawShapes(shapes, 5);
  }