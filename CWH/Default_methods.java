
interface Camera{
    void takeSnap();
    void recordVideo();

    private void greet(){                   // you can use private methods if the logic in default method is too long as you cant use private methods in other classes
        System.out.println("Good Morning");
    }

    default void record4k(){
        greet();
        System.out.println("Recording in 4k...");       //You can override default method sin the classes
    }
}

interface Wifi{
    String[] getNetworks();
    void connectToNetwork(String network);
}

class MyCellPhone{
    void callNumber(int pno){
        System.out.println("Calling..."+ pno);
    }

    void pickCall(){
        System.out.println("connecting...");
    }
}

class Smartphone extends MyCellPhone implements Wifi,Camera{
    public void takeSnap(){
        System.out.println("Taking Snap...");
    }

    public void recordVideo(){
        System.out.println("Recording...");
    }
    public String[] getNetworks(){
        System.out.println("Getting network list..");
        String[] nlist= {"Jithesh","Kirthesh","Rishik"};
        return nlist;
    }
    public void connectToNetwork(String network){
        System.out.println("Connecting to "+network);
    }
}

public class Default_methods {
    public static void main(String[] args) {
        Smartphone ms = new Smartphone();
        String[] ar= ms.getNetworks();
        for(String item:ar){
            System.out.println(item);
        }

        ms.record4k();
    }
}
