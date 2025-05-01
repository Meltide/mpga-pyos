package src;

import java.util.Scanner;

public class Calc {
    public static void calc() {
        Scanner scanner = new Scanner(System.in);
        
        try {
            while (true) {
                System.out.print("Input first number: ");
                double num1 = scanner.nextDouble();
                
                System.out.print("Input operator (+, -, *, /): ");
                char operator = scanner.next().charAt(0);
                
                System.out.print("Input second number: ");
                double num2 = scanner.nextDouble();
                
                double result;
                
                switch(operator) {
                    case '+':
                        result = num1 + num2;
                        break;
                    case '-':
                        result = num1 - num2;
                        break;
                    case '*':
                        result = num1 * num2;
                        break;
                    case '/':
                        if(num2 != 0) {
                            result = num1 / num2;
                        } else {
                            System.out.println("Error: The divisor cannot be zero!");
                            return;
                        }
                        break;
                    default:
                        System.out.println("Error: Invalid operator!");
                        return;
                }
                
                System.out.println("Result: \033[34m" + result + "\033[0m");
                System.out.print("\033[33mContiune the calculation? \033[0m(y/n): ");
                if (!scanner.next().equalsIgnoreCase("y")) {
                    break;
                }
            }
        } catch (Exception e) {
            System.err.println("\033[31mInput error: " + e + "\033[0m");
        }
    }
}