class C1{
    public int x = 5;
    protected int y=8;
    int z=0;
    private int w=1;
    public void meth1(){
        System.out.println(x);
        System.out.println(y);
        System.out.println(z);
        System.out.println(w);
    }
}

public class Video66_Access_Modifier {
    public static void main(String[] args) {
        C1 c= new C1();
        c.meth1();
    }
}
