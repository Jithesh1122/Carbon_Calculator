import java.util.*;

class Employee{
    int salary;
    String name;
    public void Print(){
        System.out.println("Name : "+name);
    }
    public int getsalary(){
            return salary;
    }
    public String getName(){
        return name;
    }
    public String setName(){
        Scanner sc= new Scanner(System.in);
        name=sc.nextLine();
        sc.close();
        return name;

    }
}

public class OOB {
    public static void main(String[] args) {
        System.out.println("This is our custom class");
        Employee jithesh = new Employee();
        jithesh.name=jithesh.setName();
        jithesh.salary=25;
        jithesh.Print();
        System.out.println(jithesh.salary
        );
    }
}
