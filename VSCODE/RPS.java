import java.util.*;

public class RPS {
      public static void main(String[] args) {
        Random rand = new Random();
        Scanner sc = new Scanner(System.in);
        int comp=rand.nextInt(3);
        System.out.println("Enter 0 for Rock, 1 for Paper, 2 for Scissors");
        int user = sc.nextInt();
        if(user==comp){
            System.out.println("Tie");
        }
        else if(user==0 &&comp==2 ||user==1 && comp==0 ||user==2 && comp==1){
            System.out.println("Your choice "+user+" Compuer Choice "+comp);
            System.out.println("You win");
        }
        else{
            System.out.println("Your choice "+user+" Compuer Choice "+comp);
            System.out.println("Computer wins");
        }
        sc.close();
      }
}
