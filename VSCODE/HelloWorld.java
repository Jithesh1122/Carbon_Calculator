
public class HelloWorld {
    public static void main(String[] args) {
       String name = "Jithesh";
       String value = name.toUpperCase();
       System.out.println("Hello, World! " + value);

       String n= "    Jithesh   ";
       System.out.println(n.trim());

       System.out.println(name.substring(3,5));

       System.out.println(name.replace('J','K'));

       System.out.println(name.startsWith("Jit"));

       System.out.println(name.charAt(4));

       System.out.println(name.indexOf("h"));

       System.out.println(name.indexOf("h", 4));

       System.out.println(name.equals("Jithesh"));

       System.out.println(name.equalsIgnoreCase("jithesh"));
    }
}