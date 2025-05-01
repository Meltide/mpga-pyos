package src;

import java.text.SimpleDateFormat;
import java.util.Date;

public class Time {
    public static void time() {
        SimpleDateFormat formatDate = new SimpleDateFormat();
        Date date = new Date();
        formatDate.applyPattern("yyyy/MM/dd HH:mm:ss a");
        System.out.println(formatDate.format(date));
    }
}