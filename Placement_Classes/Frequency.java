import java.util.Scanner;

public class Frequency {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String str1 = sc.next();
        for(int i=0;i<str1.length();i++){
            int count=0;
            for(int j=0;j<str1.length();j++){
                if(str1.charAt(i)==str1.charAt(j)){
                    count++;
                }
            }
            System.out.println(str1.charAt(i)+" "+count);
        }
        sc.close();
    }
}
