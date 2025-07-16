class Solution {
    public int reverse(int x) {
        int rem,rev=0;
        while(x!=0){
           if(rev<=Math.pow(2,31)-1  && rev>= Math.pow(-2,31)){
            rem=x%10;
            rev=rev*10+rem;
            x=x/10;
            System.out.println(rev);
           }
           else{
            return 0;
           }
        }
        return rev;
    }
}

public class Home {
    public static void main(String[] args) {
        Solution s=new Solution();
        System.out.println(s.reverse(1534236469)); 
    }
}
