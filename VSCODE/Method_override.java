class A{
    public int a;
    public int me(){
        return 4;
    }
    public void me2(){
        System.out.println("I am 2 of class A");
    }
}

class B extends A{
    @Override
    public void me2(){
        System.out.println("I am 2 of class B");
    }

    public void meth3(){
        System.out.println("I am a method 3 of class B");
    }
}

public class Method_override {
    public static void main(String[] args) {
        A a=new A();
        a.me2();

        B b=new B();
        b.me2();
    }
}
