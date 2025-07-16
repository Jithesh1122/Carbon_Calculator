import java.util.*;
public class Anagram1 {
    public static void main(String[] args) {
        /*Length of two words not equal return 0
         * choose any one word as template word
         * access each char from template word:tch
         * take the count of tch in word 1 and store as word1count
         * take the count of tch in word2 and store as word2count
         * compare word1count and word2count if not equal return 0
         * return 1 if no count mismatch
         */
        Scanner sc=new Scanner(System.in);
        String str1 = sc.next();
        String str2= sc.next();
        int sum1=0,sum2=0;
        if(str1.length()==str2.length()){
            for(int i=0;i<str1.length();i++){
                sum1=sum2=0;
                for(int j=0;j<str2.length();j++){
                    if(str1.charAt(i)==str2.charAt(j)){
                        sum1++;
                    }
                    if(str2.charAt(i)==str1.charAt(j)){
                        sum2++;
                    }
                    if (sum1!=sum2){
                        System.out.println("Not anagram");
                        System.exit(0);;
                    }
                }
        }
    }
    System.out.println("Anagram");
}
}
