from flask import Flask,redirect,url_for,render_template,request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("Form.db",check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Registration (Name TEXT,Address TEXT,Phone INTEGER,Per_Brick_Cost INTEGER,Bricks_Per_Day INTEGER, Bricks_Made_Date DATE ,Revised_By TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS Adv_Pay (Name TEXT,Advance INTEGER)')




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

		c.execute("INSERT INTO Registration (Name,Phone,Address,Per_Brick_Cost,Bricks_Per_Day,Bricks_Made_Date,Revised_By) values (?,?,?,?,?,?,?)",(Name,phone,Address,value,value,value,value))
		conn.commit()

		return redirect(url_for("user",usr=Name))
	else:
		return render_template('Registration.html')









@app.route("/AdvancePay",methods=['POST','GET'])	
def Advance():
	if request.method=='POST':
		Name = request.form['brickmaker']
		Adv_Pay = request.form['AdvancePay']
		c.execute("INSERT INTO Adv_Pay (Name,Advance) values (?,?)",(Name,Adv_Pay))
		conn.commit()

		return render_template('Home.html')
	else:
		result = c.execute("Select Name from Registration")
		result = result.fetchall()
		return render_template('AdvancePay.html',result=result)










@app.route('/WeeklyWork',methods=['GET','POST'])
def WeeklyWork():

	if request.method=='POST':
		FromDate = request.form['FromDate']
		ToDate   = request.form['ToDate']
		brickmaker = request.form['brickmaker']

		result1=c.execute("Select Name,Phone,Per_Brick_Cost,Bricks_Per_Day,Bricks_Made_Date,Revised_By from Registration where Name=? and Bricks_Made_Date>=? and Bricks_Made_Date<=?",(brickmaker,FromDate,ToDate))
		result1=result1.fetchall()		

		result2 = c.execute("Select * from Adv_Pay where Name=?",(brickmaker,))
		result2 = result2.fetchall()

		result3 = c.execute("Select sum(Bricks_Per_Day) from Registration where Name=? and Bricks_Made_Date>=? and Bricks_Made_Date<=?",(brickmaker,FromDate,ToDate))
		result3 = result3.fetchall()
		
		result4 = c.execute("Select Per_Brick_Cost from Registration where Name=?",(brickmaker,))
		result4 = result4.fetchall()

		Total_Price = result4[0][0]*result3[0][0]

		return render_template('WeeklyWorkShow.html',result1=result1,result2=result2,result3=result3[0][0],Total_Price=Total_Price,result4=result4[0][0])

	else:
		result=c.execute('Select DISTINCT Name from Registration')
		result=result.fetchall()
		return render_template('WeeklyWork.html',result=result)













@app.route("/<usr>",methods=['GET'])
def user(usr):
	return render_template('Show.html')










@app.route("/Table")
def table():
		result = c.execute("Select * from Registration")
		result = result.fetchall()
		table2 = c.execute("Select * from Adv_Pay") 
		table2 = table2.fetchall()
		return render_template('Table.html',result=result,table2=table2)









@app.route("/Rate",methods=['POST','GET'])
def Rate():
	if request.method=='POST':
		brick = request.form["Brick Rate"]
		name  = request.form["brickmaker"]	

		c.execute("UPDATE Registration SET Per_Brick_Cost=? where Name=?",(brick,name))
		conn.commit()

		return render_template('Home.html')
	else:
		result = c.execute("Select DISTINCT Name from Registration")
		result = result.fetchall()
		#print(result)
		return render_template('Rate.html',result=result)








@app.route("/DailyWork",methods=['POST','GET'])
def DailyWork():
	if request.method == 'POST':
		brick_per_day = request.form["BrickPerDay"]
		BrickDate     = request.form["BrickDate"]
		Revisor       = request.form["Revisor"]
		#Adv_Pay       = request.form["Advance"]
		name          = request.form["brickmaker"]
		print(brick_per_day)

		result = c.execute("Select count(*) from Registration where Name=? and Bricks_Made_Date=?",(name,BrickDate))
		result = result.fetchall()
		print(result)
		if result[0][0]==1:
			return "The value already exists in the database"

			
		else:
			value=''
			result = c.execute("Select count(*) from Registration where Name=? and Bricks_Made_Date=?",(name,value))
			result = result.fetchall()
			if result[0][0]==1:
				c.execute("UPDATE Registration SET Bricks_Per_Day=?,Bricks_Made_Date=?,Revised_By=? where Name=?",(brick_per_day,BrickDate,Revisor,name))
				conn.commit()
				return render_template('Home.html')

				
			result = c.execute("Select Name,Address,Phone,Per_Brick_Cost from Registration where Name=?",(name,))
			result = result.fetchall()
			Address = result[0][1]
			Phone   = result[0][2]
			Per_Brick_Cost = result[0][3]
			c.execute("INSERT INTO Registration (Name,Address,Phone,Per_Brick_Cost,Bricks_Per_Day,Bricks_Made_Date,Revised_By) values (?,?,?,?,?,?,?)",(name,Address,Phone,Per_Brick_Cost,brick_per_day,BrickDate,Revisor))
			conn.commit()
				
		#return render_template('Home.html')
		return render_template('Home.html')
	else:
		result = c.execute("Select DISTINCT Name from Registration")
		result = result.fetchall()
		return render_template('DailyWork.html',result=result)





if __name__ == "__main__":
	app.run()
