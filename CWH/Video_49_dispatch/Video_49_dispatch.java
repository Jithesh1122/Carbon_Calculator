package Video_49_dispatch;
class One{
    public void name(){
        System.out.println("My name is Java");
    }

    public void greet(){
        System.out.println("Good morning");
    }
}

class Two extends One{
    public void name(){
        System.out.println("My name is java in class two");
    }

    public void welcome(){
        System.out.println("Welcome");
    }
}

public class Video_49_dispatch {
    public static void main(String[] args) {
        // One obj = new One();//Allowed
        // Two tobj = new Two();//Allowed
        One obj = new Two();//Allowed
        //Two obj2 = new One()   Not Allowed
        obj.greet();
        obj.name();
        // obj.welcome();  not possible
    }
}
