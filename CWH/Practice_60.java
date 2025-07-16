
abstract class Pen{
    abstract void write();
    abstract void refill();
}

class FountainPen extends Pen{
    void write(){
        System.out.println("Writing...");
    }

    void refill(){
        System.out.println("Refilling...");
    }

    void changeNib(){
        System.out.println("Changing...");
    }
}


class Monkey{
    void jump(){
        System.out.println("Jumping...");
    }
    void bite(){
        System.out.println("Bite...");
    }
}

interface BasicAnimal{
    void eat();
    void sleep();
}

class Human extends Monkey implements BasicAnimal{
    void speak(){
        System.out.println("Helloooooo");
    }

    public void eat(){
        System.out.println("Eating");
    }
    public void sleep(){
        System.out.println("Sleeping");
    }

}

public class Practice_60 {
    public static void main(String[] args) {
        FountainPen pen = new FountainPen();
        pen.write();
        pen.refill();
        pen.changeNib();


        Human h = new Human();
        h.sleep();

        Monkey m = new Human();
        m.bite();
        m.jump();
        //m.speak()   not allowed

        BasicAnimal l = new Human();
            l.eat();
            l.sleep();
    }
}
