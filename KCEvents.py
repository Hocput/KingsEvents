import sqlite3
from datetime import date
from flask import Flask, render_template, request, jsonify

DB_NAME = "Events450.db"

def eventTable():
    dbConnection = sqlite3.connect(DB_NAME)
    dbCursor = dbConnection.cursor()

    dbCmnd = "select eventnames.name, " +\
                "events.StartDate, " +\
                "eventNames.Individual, " +\
                "eventNames.Alliance, " +\
                "eventNames.CrossServer, " +\
                "eventNames.ServerAwards " +\
            "from EventNames inner join Events on Events.EventID = EventNames.EventID " +\
            "order by Events.StartDate"
    res = dbCursor.execute(dbCmnd)
    
    print ("Name\t\t\tStart\t\tInd\tAll\tXS\tSA")
    for record in res:
        RowTxt = record[0] +"\t"
        if len(record[0]) < 16:
            RowTxt +=  "\t"
        if len(record[0]) < 8:
            RowTxt +="\t"
        Date = date.fromordinal(record[1])
        RowTxt += Date.isoformat() + "\t"
        RowTxt += str(record[2]) + "\t"
        RowTxt += str(record[3]) + "\t"
        RowTxt += str(record[4]) + "\t"
        RowTxt += str(record[5])
        print (RowTxt)

app = Flask(__name__)

@app.route("/")
def eventTableHTML():
    dbConnection = sqlite3.connect(DB_NAME)
    dbCursor = dbConnection.cursor()

    dbCmnd = "select eventnames.name, " +\
                "events.StartDate, " +\
                "eventNames.Individual, " +\
                "eventNames.Alliance, " +\
                "eventNames.CrossServer, " +\
                "eventNames.ServerAwards " +\
            "from EventNames, Events where Events.EventID = EventNames.EventID " +\
            "order by Events.StartDate"
    res = dbCursor.execute(dbCmnd)
    
    tableHTML = []
    for record in res:
        RowTxt = []
        RowTxt.append( record[0] )
        
        Date = date.fromordinal(record[1])
        RowTxt.append( Date.isoformat() )
        Date = date.fromordinal(record[1]+13)
        RowTxt.append( Date.isoformat() )
        OtherTxt=""
        if record[2] > 0:
            OtherTxt += "Individual"
        if record[3] > 0:
            if len(OtherTxt)>0:
                OtherTxt += ", "
            OtherTxt += "Alliance"
        if record[4] > 0:
            if len(OtherTxt)>0:
                OtherTxt += ", "
            OtherTxt += "Cross Server" 
        RowTxt.append( OtherTxt )
        
        tableHTML.append(RowTxt)

        print (tableHTML)

    return render_template("events.html", rows=tableHTML)
    

if __name__ == "__main__":
   # app.run()
    eventTable()
    