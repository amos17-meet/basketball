from flask import Flask, url_for, flash, redirect, request, render_template, session as login_session

from database_setup import *

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

engine = create_engine('sqlite:///fizzBuzz.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

@app.route('/')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method=='GET':
		return render_template('login.html')
	elif request.method=='POST':
		email=request.form['email']
		password=request.form['password']

		if email=="" or password == "":
			flash("missing arguments")
			return redirect(url_for('login'))
		coach=session.query(Coach).filter_by(email=email).first()
		if coach!=None:
			if coach.password==password:
				flash('Login successfuly, welcme, %s' % coach.name)
				login_session['email']=coach.email
				login_session['name']=coach.name
				login_session['id']=coach.id
				print ("hereee")
				return redirect('build_starting_5')
			else:
				flash('incorrect user/password')
				return redirect(url_for('login.html'))
		else:
			flash("Could not found such a coach")
			return redirect(url_for('login'))
			


@app.route('/build_starting_5', methods = ['GET','POST'])
def build_starting_5():
	if 'email' in login_session:
		coach=session.query(Coach).filter_by(email=login_session['email']).first()
		if request.method=='GET':
			return render_template("build_starting_5.html")

	return redirect(url_for('login'))




@app.route('/singup', methods=['GET','POST'])
def signup():
	if request.method=='GET':
		return render_template('signup.html')
	else:

		email=request.form['email']
		name=request.form['name']
		password=request.form['password']
		nickname=request.form['nickname']
		if email=="" or name=="" or password=="" or nickname=="":
			flash("missing arguments")
			return redirect(url_for('singup'))
		else:
			new_coach=Coach(name=name,
							email=email,
							password=password,
							nickname=nickname)

			session.add(new_coach)
			session.commit()
			return redirect('build_starting_5')



@app.route('/create_player', methods=['GET','POST'])
def create_player():
	if 'email' in login_session:
		coach=session.query(Coach).filter_by(email=login_session['email']).first()
		if request.method=='GET':
			return render_template('create_player.html')
		else:
			print("name")
			name=request.form['name']
			print("position")
			player_position=request.form['position']
			print("two")
			two_points=request.form['two_points']
			print("three")
			three_points=request.form['three_points']
			print("one")
			one_on_one=request.form['one_on_one']
			print("def")
			defense=request.form['defense']

			if name=="" or player_position=="" or two_points=="" or three_points=="" or one_on_one=="" or defense=="":
				flash("missing arguments")
				return redirect(url_for('create_player'))
			else:
				new_player= Player(name=name,
									player_position=player_position,
									two_points=two_points,
									three_points=three_points,
									one_on_one=one_on_one,
									defense=defense)
				session.add(new_player)
				coach.players.append(new_player)
				session.commit()
				return redirect('build_starting_5')
	return redirect(url_for('login'))


@app.route('/starting_5s', methods=['GET','POST'])
def starting_5s():
	
	print('email' in login_session)
	if 'email' in login_session:
		print("hereeee")
		coach=session.query(Coach).filter_by(email=login_session['email']).first()
		starting_5s = coach.starting_5s
		print(starting_5s)
		return render_template('starting_5s.html',starting_5s=starting_5s)

	return redirect(url_for('login'))


@app.route('/my_players', methods=['GET','POST'])
def my_players():
	if 'email' in login_session:
		coach=session.query(Coach).filter_by(email=login_session['email']).first()
		players=coach.players
		return render_template('my_players.html', players=players)



def verify_password(email, password):
	coach = session.query(Coach).filter_by (email=email).first()
	if not coach or not coach.verify_password(password):
		return False
	return True



if __name__ == '__main__':
    app.run(debug=True)