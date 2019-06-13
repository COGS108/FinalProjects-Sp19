import java.util.ArrayList;
import java.lang.Double;
import java.lang.StringBuilder;

public class ExtractData
{
    public ArrayList<String> dataLinesAsStrings;
    public ArrayList<OneLine> data;
    public String html;

    public ExtractData(String html)
    {
        int startIndex = html.indexOf("<tbody>");
        int endIndex = html.indexOf("</tbody>") + 8;
        this.html = html.substring(startIndex, endIndex);

        this.data = new ArrayList<OneLine>();
        this.dataLinesAsStrings = new ArrayList<String>();
    }

    public void fillLinesAsStrings()
    {
        int begOfLine = 0;

        while(this.html.indexOf("<tr class=\"odd\">", begOfLine) != -1
              || this.html.indexOf("<tr class=\"even\">", begOfLine) != -1)
        {
            int endOfLine = this.html.indexOf("</tr>", begOfLine);
            endOfLine = endOfLine + 5;
            String currLine = html.substring(begOfLine, endOfLine);
            this.dataLinesAsStrings.add(currLine);
            begOfLine = endOfLine;
        }
    }

    public void fillLinesAsObjects()
    {
        for(int i = 0; i < this.dataLinesAsStrings.size(); i++)
        {
            String currLineString = this.dataLinesAsStrings.get(i);

            int startIndex;
            int endIndex;

            //get study hours
            startIndex = currLineString.indexOf("StudyHours\">") + 12;
            endIndex = currLineString.indexOf("</span>", startIndex);
            String hoursString = currLineString.substring(startIndex, endIndex);
            double hours = Double.parseDouble(hoursString);

            //get average grade
            startIndex = currLineString.indexOf("GradeReceived\">") + 15;
            endIndex = currLineString.indexOf("</span>", startIndex);
            String grades = currLineString.substring(startIndex, endIndex);

            if(grades.indexOf("(") != -1)
            {
                startIndex = grades.indexOf("(") + 1;
                endIndex = grades.indexOf(")");
                grades = grades.substring(startIndex, endIndex);
            }

            this.data.add(new OneLine(hours, grades));
        }
    }

    public String makeCSV(String classNum)
    {
        StringBuilder mySB = new StringBuilder();
        mySB.append("Class,Avg Hours Studied,Avg Grade\n");

        for(int i = 0; i < this.data.size(); i++)
        {
            OneLine currOneLine = this.data.get(i);
            String csvLineString = classNum + "," + currOneLine.getHours();
            csvLineString = csvLineString + "," + currOneLine.getAvgGrade();

            mySB.append(csvLineString);
            mySB.append("\n");
        }

        return mySB.toString();
    }
}
