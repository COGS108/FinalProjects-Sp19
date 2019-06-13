import java.util.Scanner;
import java.io.File;
import java.lang.StringBuilder;

public class DataToCSV
{
    public static void main(String[] args)
    {
        if(args.length != 2)
        {
            System.err.println("Usage:\n");
            System.err.println("java DataToCSV [filename] [class number]\n");
        }

        Scanner myScanner;

        try
        {
            myScanner = new Scanner(new File(args[0]));
        }

        catch(Exception e)
        {
            System.err.print("FileNotFoundException: Please");
            System.err.println(" enter a valid file name.");
            return;
        }

        StringBuilder mySB = new StringBuilder();

        while(myScanner.hasNextLine())
        {
            mySB.append(myScanner.nextLine());
            mySB.append("\n");
        }

        myScanner.close();

        String htmlText = mySB.toString();

        ExtractData capeData = new ExtractData(htmlText);
        capeData.fillLinesAsStrings();
        capeData.fillLinesAsObjects();
        System.out.println(capeData.makeCSV(args[1]));
    }
}
