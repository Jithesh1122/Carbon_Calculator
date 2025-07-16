
interface Bicycle{
    int a=99;
    void applyBrake(int decrement);
    void speedup(int increment);
}

interface HornBicycle{
    void blowHorn(int decrement);
    void onLight(int increment);
}

class AvonCycle implements Bicycle,HornBicycle{
    void blowHorn(){
        System.out.println("Hooooorrrrrrrnnnnn");

    }

    public void applyBrake(int decrement){
        System.out.println("Applying Brake");
    }

    public void speedup(int increment){
        System.out.println("Applying speed");
    }

    public void blowHorn(int decrement){
        System.out.println("Peeeeeee");
    }

    public void onLight(int increment){
        System.out.println("Headlight");
    }
}

public class Interfaces {
    public static void main(String[] args) {
        AvonCycle c1 = new AvonCycle();
        // c1.applyBrake(8);
        // //You can create properties in interfaces
        // System.out.println(c1.a);
        // //You cannot change the properties of interfaces as they are final
        // //c1.a=108;  not allowed
        c1.blowHorn(7);
        c1.onLight(0);
        
    }
}
