package video_52;

abstract class Parent{
    public Parent(){
        System.out.println("I am a constructor of Parent");
    }
    public void sayHello(){
        System.out.println("Hello");
    }
    abstract public void greet();
}

class Child extends Parent{
    @Override
    public void greet(){
        System.out.println("Good Morning");
    }
}

abstract class Child2 extends Parent{
    public void th(){
        System.out.println("Iam good");
    }
}


public class Video_52 {
    public static void main(String[] args) {
        Child c = new Child();
        // Parent p = new Parent(); not allowed cause Parent is an abstract class
        c.greet();
    }
}
