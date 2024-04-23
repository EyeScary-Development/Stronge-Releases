#Single file ezlog
#Not officially a library yet
import datetime
import os

def appendn(name, data):
    str(data)
    dataw = "\n" + data
    with open(name, "a+") as f:
        f.write(dataw)

def log(data, printLog=True):
        timenstr = datetime.datetime.now()
        datenstr = datetime.date.today()
        date = str(datenstr)
        if os.name=='nt':
            datewlog = os.getcwd()+ "\\logs\\" + date + ".log"
        else:
            datewlog = os.getcwd()+ "/logs/" + date + ".log"
        if printLog:
            print(data)
        time = str(timenstr)
        timewlog = time + ": " + data
        try:
            appendn(datewlog, timewlog)
        except:
             os.mkdir(os.path.join(os.getcwd(), "logs"))
             appendn(datewlog, timewlog)