public class Vararg {
    static int sum(int ...arr){
        //available as int [] arr
        int res=0;
        for(int a: arr){
             res+=a;
        }
        return res;
    }
    // static int sum(int x,int ...arr){           Atleast one integer required
    //     //available as int [] arr
    //     int res=0;
    //     for(int a: arr){
    //          res+=a;
    //     }
    //     return res;
    // }
    public static void main(String[] args) {
        System.out.println("Sum of 4 and 5 is "+ sum(4,5));
        System.out.println("Sum of 4,3 and 5 is "+ sum(4,3,5));
        System.out.println("Sum of 4,3,6 and 5 is "+ sum(4,3,6,5));
        System.out.println("Sum of 4,6,7,8,9, and 5 is "+ sum(4,6,7,8,9,5));
    }
}
