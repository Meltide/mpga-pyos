package src;

import java.util.Scanner;
import java.util.Random;

public class NumGuess {
    public static int randInt(int min, int max) {
        Random rand = new Random();
        return rand.nextInt(max - min + 1) + min;
    }
    
    static Scanner in = new Scanner(System.in);
    static int guessNum = randInt(100, 1000);
    
    public static void mainMenu() {
        System.out.println("\033[35mNUMBER GUESSING GAME\033[0m");
        System.out.println("Numerical Range: \033[34m100-1000\033[0m");
        System.out.println("Difficulty: \033[34mNormal\033[0m");
        System.out.println("The answer is an integer.\n");
        
        menuLoop:
        while (true) {
            System.out.print("Press 'start' to start, 'exit' to exit.\n> ");
            String cmd = in.nextLine();
            
            switch (cmd) {
                case "start":
                    game();
                    break;
                case "exit":
                    break menuLoop;
                default:
                    System.err.println("\033[31mUnknown command.\033[0m");
            }
        }
    }
    
    public static void game() {
        System.out.println("\033[34mGAME START\033[0m");
        
        while (true) {
            System.out.print("Enter the number of guesses \033[2m(Press 'exit' to exit)\n\033[0m> ");
            String guess = in.nextLine();
            
            if (guess.equalsIgnoreCase("exit")) {
                break;
            }
            
            try {
                if (Integer.parseInt(guess) == guessNum) {
                    System.out.println("\033[32mYou win!\033[0m\nThe anwser is: \033[34m" + guessNum + "\033[0m");
                    break;
                } else if (Integer.parseInt(guess) < guessNum) {
                    System.out.println("\033[31mLess.\033[0m");
                } else if (Integer.parseInt(guess) > guessNum) {
                    System.out.println("\033[31mLarge.\033[0m");
                }
            } catch (NumberFormatException e) {
                System.err.println("\033[31mError: No integer inputed.\033[0m");
            } catch (Exception e) {
                System.err.println("\033[31mError: " + e + "\033[0m");
            }
        }
    }
    
    public static void numguess() {
        mainMenu();
    }
}