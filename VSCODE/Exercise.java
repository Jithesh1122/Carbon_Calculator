import java.util.*;

class Game{
    private int num;
    int noOfGuess;
    Random rand = new Random();
    public Game(){
      num=rand.nextInt(10);
      noOfGuess=5;
    }
    public int getNum(){
        return num;
    }
    
}

public class Exercise {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Game guess=new Game();
        for(int i=1;i<=guess.noOfGuess;i++){
            System.out.println("Guess a number");
        int n=sc.nextInt();
        if(n==guess.getNum()){
            System.out.println("You guessed the correct number");break;
        }
        else if(n>guess.getNum())
            System.out.println("Your guess is larger than the number\nYou have "+ (guess.noOfGuess-i) +" chances");
        else 
        System.out.println("Your guess is smaller than the number\nYou have "+ (guess.noOfGuess-i) +" chances");
        }
        System.out.println("The num is "+ guess.getNum());
        sc.close();
    }
}
