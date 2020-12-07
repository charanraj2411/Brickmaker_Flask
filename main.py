from flask import Flask,redirect,url_for,render_template,request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("Form.db",check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Registration (Name TEXT,Address TEXT,Phone INTEGER PRIMARY KEY,Per_Brick_Cost INTEGER,Bricks_Per_Day INTEGER, Bricks_Made_Date DATE,Revised_By TEXT,Adv_Pay INTEGER)')

#@app.route("/<name>")
#def home(name):
#	return render_template('index2.html')


@app.route("/Home")
def Home():
	return render_template('Home.html')



@app.route("/Registration",methods=['POST','GET'])
def register():
	if request.method=='POST':
		Name=request.form["Name"]
		Address=request.form["Address"]
		phone=request.form["phone"]
		value=''

		c.execute("INSERT INTO Registration (Name,Phone,Address,Per_Brick_Cost,Bricks_Per_Day,Bricks_Made_Date,Revised_By,Adv_Pay) values (?,?,?,?,?,?,?,?)",(Name,phone,Address,value,value,value,value,value))
		conn.commit()

		return redirect(url_for("user",usr=Name))
	else:
		return render_template('Registration.html')

@app.route("/<usr>",methods=['GET'])
def user(usr):
	return render_template('Show.html')


@app.route("/Table")
def table():
		result = c.execute("Select * from Registration")
		result = result.fetchall()
		return render_template('Table.html',result=result)

@app.route("/Rate",methods=['POST','GET'])
def Rate():
	if request.method=='POST':
		brick = request.form["Brick Rate"]
		name  = request.form["brickmaker"]	
		c.execute("UPDATE Registration SET Per_Brick_Cost=? where Name=?",(brick,name))
		conn.commit()

		return render_template('Home.html')
	else:
		result = c.execute("Select * from Registration")
		result = result.fetchall()
		return render_template('Rate.html',result=result)

@app.route("/DailyWork",methods=['POST','GET'])
def DailyWork():
	if request.method == 'POST':
		brick_per_day = request.form["BrickPerDay"]
		BrickDate     = request.form["BrickDate"]
		Revisor       = request.form["Revisor"]
		Adv_Pay       = request.form["Advance"]
		name          = request.form["brickmaker"]
		c.execute("UPDATE Registration SET Bricks_Per_Day=?,Bricks_Made_Date=?,Revised_By=?,Adv_Pay=? where Name=?",(brick_per_day,BrickDate,Revisor,Adv_Pay,name))
		conn.commit()
		return render_template('Home.html')
	else:
		result = c.execute("Select * from Registration")
		result = result.fetchall()
		return render_template('DailyWork.html',result=result)

if __name__ == "__main__":
	app.run()
