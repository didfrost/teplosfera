from flask import Flask, render_template, request, json
import MySQLdb
import quickstart
import sqlite3

app = Flask(__name__)
dbName = "teplosfera.db"

class DB:
    conn = None

    def connect(self):
        #self.conn = MySQLdb.connect("teplosfera.mysql.pythonanywhere-services.com", "teplosfera", "Step1993", "teplosfera$myDB",charset='utf8')
        self.conn = MySQLdb.connect("sql11.freemysqlhosting.net", "sql11206944", "McQ4scpNVX", "sql11206944",charset='utf8')

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
        return cursor

def myInsert(conn, args):
	with conn.cursor() as c:
		c.execute()
	conn.commit()

def myFetchAll(sql):
	con = sqlite3.connect(dbName)
	with con:
		cur = con.cursor()
		cur.execute(sql)
		res = cur.fetchall()
	if con:
		con.close()
	return res
	
def init_tables_mysql():
	table_event = "CREATE TABLE IF NOT EXISTS ts_events (\
	id int(11) NOT NULL AUTO_INCREMENT,\
	idDoc varchar(25),\
	dateDoc date,\
	idClient varchar(25),\
	nameClient varchar(150),\
	adressClient varchar(150),\
	telClient varchar(50),\
	idTopic varchar(25),\
	nameTopic varchar(150),\
	description varchar (500),\
	start datetime,\
	finish datetime,\
	idUser varchar(25),\
	nameUser varchar(50),\
	idCalendar varchar(500),\
	PRIMARY KEY (id)\
	)\
	ENGINE=InnoDB DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci;"
	
	# MySQL
	#cursor = db.cursor()
	#cursor.execute(table_event)

def init_tables_sqlite():
	table_event = "CREATE TABLE IF NOT EXISTS ts_events (\
	id INTEGER PRIMARY KEY AUTOINCREMENT,\
	idDoc TEXT,\
	dateDoc DATETIME,\
	idClient TEXT,\
	nameClient TEXT,\
	adressClient TEXT,\
	telClient TEXT,\
	idTopic TEXT,\
	nameTopic TEXT,\
	description TEXT,\
	start datetime,\
	finish datetime,\
	idUser TEXT,\
	nameUser TEXT,\
	idCalendar TEXT\
	idEvent TEXT\
	)"
	
	myFetchAll(table_event)

@app.route('/')
def index():
	init_tables_sqlite();
	sql = "SELECT id,idDoc,dateDoc,start,finish,nameTopic,description,nameClient,adressClient,telClient from ts_events"
	events = myFetchAll(sql)
	#db = DB()
	#cursor = db.query(sql)
	#cursor.execute(query)
	#db.commit()
	#events = cursor.fetchall();
	#print(events)
	
	return render_template("index.html",events=events)

@app.route('/addEvents',methods=['POST'])
def addEvents():
	queryKey = ""
	queryVal = ""
	idDoc = ""
	nameClient = "No client"
	adressClient = "No adress"
	description = "No description"
	idCalendar = ""
	idEvent = ""
	sqlInsert = "INSERT INTO ts_events "
	sqlUpdate = "UPDATE ts_events SET "
	myDict = dict(request.form)
	for key, val in myDict.items():
		if (key == 'idDoc'):
			idDoc = val[0]
		elif (key == 'idCalendar'):
			idCalendar = val[0]
		else:
			queryKey += key+","
			queryVal += "'"+val[0]+"',"
			sqlUpdate += key+"='"+val[0] +"'," #Update table set key1=value1, key2=value2

		if(key == 'nameClient'):
			nameClient = val[0]
		elif(key == 'adressClient'):
			adressClient = val[0]
		elif(key == 'description'):
			description = val[0]
		elif(key == 'start'):
			start = val[0]
		elif(key == 'finish'):
			finish = val[0]
		elif(key == 'idEvent'):
			idEvent = val[0]
			
	print("idCalendar = " + idCalendar)
	print("idEvent = " + idEvent)
	#db = DB()

	# First retrieve the event from the API.
	if (idEvent == ""):
		# first try to find idEvent in Database
		# if empty or isn't exist in Google calendar then add new one
		# finish this algorith later
	
		event = {
			'summary': nameClient,
			'location': adressClient,
			'description': description,
			'start': {
			'dateTime': start,
			'timeZone': 'Europe/Kiev',
		},
			'end': {
			'dateTime': finish,
			'timeZone': 'Europe/Kiev',
		},
			'recurrence': [
			'RRULE:FREQ=DAILY;COUNT=1'
		],
			'reminders': {
			'useDefault': False,
			'overrides': [
				{'method': 'popup', 'minutes': 60},
		],
		},
		}
		
		eventId = quickstart.add_event(event,idCalendar,idEvent)
	else:	
		event = quickstart.get_event(idEvent,idCalendar)
		eventId = event.get('id')
		print(event)
	
	
	if (eventId != "Something wrong"):
		sql = "select idDoc from ts_events where idDoc="+idDoc
		#cur = db.query(sql)
		#res = cur.fetchall();
		res = myFetchAll(sql)
		if len(res)==0:
			sqlInsert += "("+queryKey[:-1] + ",idEvent "+") values ("+ queryVal[:-1]+","+eventId+")"
			myFetchAll(sqlInsert)
		else:
			sqlUpdate = sqlUpdate[:-1]+", idEvent="+idEvent+" where idDoc = "+idDoc
			myFetchAll(sqlUpdate)
	
	return eventId

@app.route('/test')
def test():
	#quickstart.main()
	nameClient = "No client"
	adressClient = "No adress"
	description = "No description"
	idCalendar = "7lc9qlkhavhid2d3o7ughcpu7k@group.calendar.google.com"
	event = {
        'summary': nameClient,
        'location': adressClient,
        'description': description,
        'start': {
        'dateTime': '2018-01-15T20:00:00',
        'timeZone': 'Europe/Kiev',
    },
        'end': {
        'dateTime': '2018-01-15T21:00:00',
        'timeZone': 'Europe/Kiev',
    },
        'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=1'
    ],
        'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'popup', 'minutes': 60},
    ],
    },
    }
	quickstart.add_event(event,idCalendar)

	return "test OK"


if __name__ == "__main__":
	app.run(debug=True)
