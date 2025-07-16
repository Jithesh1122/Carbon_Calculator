
interface sampleInterface{
    void meth1();
    void meth2();
}

//you can extend an interface with a parent interface but cannot use extends with class and interface
interface childSampleInterface extends sampleInterface{
    void meth3();
    void meth4();
}

class MySampleClass implements childSampleInterface{
    public void meth3(){
        System.out.println("Meth3");
    }
    public void meth4(){
        System.out.println("Meth4");
    }

    //methods of sampleInterface
    public void meth1(){
        System.out.println("Meth1");
    }
    public void meth2(){
        System.out.println("Meth2");
    }
}

public class Inheritence_in_Interfaces {
    public static void main(String[] args) {
        MySampleClass obj=new MySampleClass();
        obj.meth1();
        obj.meth2();
        obj.meth3();
        obj.meth4();
    }
}
