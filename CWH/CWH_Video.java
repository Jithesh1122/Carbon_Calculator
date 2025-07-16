
import java.util.*;

class Library {
    public String [] availableBook = new String[100];
    public String [] issuedBook = new String[100];
    private int k=4;
    Scanner sc = new Scanner(System.in);

    public Library() {
        availableBook[0] = "Java";
        availableBook[1] = "C++";
        availableBook[2] = "Python";
        availableBook[3] = "JavaScript";
    }

    public void addBook(){
        System.out.println("Enter book name:");
        availableBook[k++] = sc.next();
    }

    public void issueBook(){
        System.out.println("Enter the name of book you want:");
        String name = sc.next();
        boolean found = false;

        for(int i = 0; i < k; i++){
            if(availableBook[i] != null && availableBook[i].equals(name)) {
                issuedBook[i] = name;
                availableBook[i] = null;  // Remove book from available list
                System.out.println("Your book has been issued.");
                found = true;
                break;
            }
        }
        if (!found) { System.out.println("Book not available"); }
    }

    public void returnBook(String name){
        boolean found = false;
        for(int i = 0; i < k; i++){
            if(issuedBook[i] != null && issuedBook[i].equals(name)){
                issuedBook[i] = null;  // Remove from issued books
                availableBook[k++] = name;  // Add back to available books
                System.out.println("Book returned successfully");
                found = true;
                break;
            }
        }
        if (!found) {
            System.out.println("This book was not issued.");
        }
    }

    public void showAvailableBook(){
        System.out.print("Available books: ");
        for(int i=0; i < k; i++){
            if (availableBook[i] != null)
                System.out.print(availableBook[i] + " , ");
        }
        System.out.println();
    }
}

public class CWH_Video {
    public static void main(String[] args) {
        Library L1 = new Library();
        Scanner sc = new Scanner(System.in);
        int choice;
        
        do {
            System.out.println("\nEnter 1 to add book to library");
            System.out.println("Enter 2 to view available books");
            System.out.println("Enter 3 to issue book");
            System.out.println("Enter 4 to return book");
            System.out.println("Enter 5 to exit");
            System.out.print("Your choice: ");
            choice = sc.nextInt();

            switch(choice) {
                case 1: L1.addBook(); break;
                case 2: L1.showAvailableBook(); break;
                case 3: L1.issueBook(); break;
                case 4: 
                    System.out.println("Enter the book name to be returned:"); 
                    L1.returnBook(sc.next());
                    break;
                case 5: System.out.println("Exiting..."); break;
                default: System.out.println("Invalid choice. Try again.");
            }
        } while(choice != 5);

        sc.close();
    }
}
