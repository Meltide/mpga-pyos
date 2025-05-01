import java.util.Scanner;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.io.Console;

import src.*;

public class Main {
    public static void clear() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }
    
    public static void sleepFor(double time) {
        try {
            Thread.sleep((int) (time * 1000));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static String getHiddenPassword() {
        Console console = System.console();
        if (console == null) {
            System.err.println("\033[31mWarning: The current environment does not support hidden password input. Passwords will be displayed in plain text!\033[0m");
            return new Scanner(System.in).nextLine();
        }
        return new String(console.readPassword());
    }

    public static void printStartupInfo() {
        String[] printList = {
            "\033[33mMake PyOS Great Again!\n",
            "\033[35mContributors: MeltIce\nVisit this project in github: github.com/Meltide/mpga-pyos\nMPGA Team Telegram Group: @MPGATeam\nMPGA Team Matrix Group: #MPGATeam:mozilla.org\n",
            "\033[36mAlso try PyOS's improved version by minqwq and bibimingming!\033[0m\n"
        };
        
        for (String i: printList) {
            System.out.println(i);
            sleepFor(0.1);
        }
    }
    
    public static void helpList() {
        System.out.println("\033[44m Tools \033[0m");
        System.out.println("calc       Simple Calcuator");
        System.out.println("time       Show the now time");
        System.out.println("\033[44m Games \033[0m");
        System.out.println("numguess   Number guessing game");
        System.out.println("\033[44m System \033[0m");
        System.out.println("ls         List directory contents");
        System.out.println("clear      Clear the screen");
        System.out.println("version    Show system version");
        System.out.println("shutdown   Shut down the system");
        System.out.println("help       Show this help message");
    }
    
    public static void main(String[] args) {
        String version = "1.0";
        String username = "root";
        String defPasswd = "114514";
        SimpleDateFormat formatDate = new SimpleDateFormat();

        clear();

        System.out.println("\n\033[2mMPGA PyOS in Java V" + version + "\033[0m");
        System.out.println("\033[34m  __  __ ___  ___   _   ");
        System.out.println(" |  \\/  | _ \\/ __| /_\\  ");
        System.out.println(" | |\\/| |  _/ (_ |/ _ \\ ");
        System.out.println(" |_|  |_|_|  \\___/_/ \\_\\\033[0m\n");
        
        printStartupInfo();

        Scanner input = new Scanner(System.in);

        while (true) {
            System.out.print("localhost login: ");
            String user = input.nextLine();
            if (user.equals(username)) break;
            System.out.println("Username not exist.");
        }

        while (true) {
            System.out.print("Password: ");
            String passwd = getHiddenPassword();

            if (passwd.equals(defPasswd)) {
                Date date = new Date();
                formatDate.applyPattern("yy/MM/dd HH:mm:ss");
                System.out.println("\nLast login: \033[36m" + formatDate.format(date) + "\033[0m\n");
                break;
            } else {
                System.out.println("Incorrect password.");
            }
        }

        formatDate.applyPattern("MM/dd HH:mm:ss");
        while (true) {
            Date date = new Date();
            System.out.print("\033[47m\033[30m " + formatDate.format(date) + " \033[43m " + username + "@localhost \033[37m\033[44m ~ \033[0m> ");
            String cmd = input.nextLine().trim();

            switch (cmd) {
                case "calc": Calc.calc(); break;
                case "time": Time.time(); break;
                
                case "numguess": NumGuess.numguess(); break;
                
                case "ls": System.out.println("bin  etc  home  lib  tmp  usr"); break;
                case "version": System.out.println("PyOS in Java V" + version); break;
                case "shutdown": System.out.println("\033[34mShutting down\033[0m..."); System.exit(0); break;
                case "clear": clear(); break;
                case "help": helpList(); break;
                
                default:
                    if (!cmd.isEmpty()) {
                        System.out.println("Unknown command: " + cmd);
                        System.out.println("Type 'help' for available commands");
                    }
            }
        }
    }
}