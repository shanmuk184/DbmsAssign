from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config.update(MYSQL_DATABASE_USER='root',MYSQL_DATABASE_PASSWORD='password123', MYSQL_DATABASE_DB='PUBLIC_LIBRARY')
mysql.init_app(app)
@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/readerlogin', methods=['GET', 'POST'])
def reader_login():
	if request.method == 'GET':
		return render_template('readerlogin.html')
	else:
		readerId = request.form['readerId']
		cursor = mysql.get_db().cursor()
		try:
			cursor.execute("SELECT * FROM `Reader` WHERE ReaderID = {};".format(readerId))
			x = cursor.fetchone()
			print(x)
			return render_template('readerhome.html', name=x[2])
			
		except Exception as e:
			print(str(e))
			return render_template('readerlogin.html')
			
	return 'came'


@app.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
	if request.method == 'GET':

		return render_template('adminlogin.html')
	else:
		userId = request.form['Id']
		password = request.form['Password']
		cursor = mysql.get_db().cursor()
		try:
			print(password)
			cursor.execute("SELECT * FROM `Administrator` WHERE AdminID = {} AND LoginPassword = {};".format(userId, password))
			x = cursor.fetchone()
			
			print(x)
			return render_template('adminhome.html', name= userId)
		except Exception as e:
			print(str(e))
			return render_template('adminlogin.html')
	return 'came'

@app.route('/branch')
def getBranch():
	cursor = mysql.connect().cursor()
	try:
		operation = "SELECT `LName`, `LLocation` FROM `Branch`"

		cursor.execute(operation)
		y = cursor.fetchall()
		return render_template('branch.html', branches=y, rows =['Name', 'Location'])
	except Exception as e:
		print(str(e))


@app.route('/borrowers')
def getBorrowers():
	cursor = mysql.connect().cursor()
	try:
		operation = "SELECT `ReaderID`, count(`DocID`) FROM `Borrows` GROUP BY ReaderID LIMIT 10;"

		cursor.execute(operation)
		y = cursor.fetchall()
		print(y)
		return render_template('branch.html', branches=y, rows=['Borrower Id', 'Number of Books Borrowed'])
	except Exception as e:
		print(str(e))

@app.route('/borrowedbook')
def getMostBorrowed():
	cursor = mysql.connect().cursor()
	try:
		operation = "SELECT `DocID`, count(`ReaderID`) FROM `Borrows` GROUP BY DocID LIMIT 10;"

		cursor.execute(operation)
		y = cursor.fetchall()
		print(y)
		return render_template('branch.html', branches=y, rows=['Book Id', 'Number of Readers'])
	except Exception as e:
		print(str(e))

@app.route('/reader', methods=['GET', 'POST'])
def reader():
	if request.method == 'GET':
		return render_template('reader.html')
	elif request.method == 'POST':
		conn = mysql.connect()
		cursor = conn.cursor()
		# typ = request.form['type']
		print(request.form)
		name = request.form['Name']
		address = request.form['Address']
		phone = request.form['Phone']
		cursor.execute("INSERT INTO Reader (RType, RName, ReadAddress, PhoneNumber, Fine) VALUES {};".format(('Regular', name, address, phone, 0.0)))
		conn.commit()
		return render_template('adminhome.html')

@app.route('/quit')
def quit():
	return redirect('/')

