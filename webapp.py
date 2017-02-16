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
	print("hereeee")
	print(login_session)
	if 'email' in login_session:
		coach=session.query(Coach).filter_by(email=login_session['email']).first()
		players=coach.players
		if request.method=='GET':
			return render_template("build_starting_5.html", players=players)
		'''
		else:
			position_1=request.form['position_1']
			position_2=request.form['position_2']
			position_3=request.form['position_3']
			position_4=request.form['position_4']
			position_5=request.form['position_5']
			player_1=session.query(Player).filter_by(name=position_1)
			player_2=session.query(Player).filter_by(name=position_2)
			player_3=session.query(Player).filter_by(name=position_3)
			player_4=session.query(Player).filter_by(name=position_4)
			player_5=session.query(Player).filter_by(name=position_5)
			players=[palyer_1,player_2,player_3,player_4,player_5]
			details=startind_5_details(players)
			return redirect('build_starting_5', details=details)
		'''
	return redirect(url_for('login'))

@app.route('/starting_5_details', methods = ['GET','POST'])
def starting_5_details():
	print("amos")
	print(request.method)
	if 'email' in login_session:
		coach=session.query(Coach).filter_by(email=login_session['email']).first()
		coach_players=coach.players
		print(coach_players)
		print("email")
		if request.method=='GET':
			return render_template('build_starting_5.html',players=coach_players)

		else:
			players=[]
			print(startind_5_details(players))
			print("before")
			if request.form['position_1']=="" or request.form['position_2']=="" or request.form['position_3']=="" or request.form['position_4']=="" or request.form['position_5']=="":
				flash("missing players")
				return redirect(url_for('build_starting_5'))
			position_1=request.form['position_1']
			print("after")
			position_2=request.form['position_2']
			position_3=request.form['position_3']
			position_4=request.form['position_4']
			position_5=request.form['position_5']

			player_1=session.query(Player).filter_by(unique_name=position_1).first()
			player_2=session.query(Player).filter_by(unique_name=position_2).first()
			player_3=session.query(Player).filter_by(unique_name=position_3).first()
			player_4=session.query(Player).filter_by(unique_name=position_4).first()
			player_5=session.query(Player).filter_by(unique_name=position_5).first()

			login_session['position_1']=player_1.unique_name
			login_session['position_2']=player_2.unique_name
			login_session['position_3']=player_3.unique_name
			login_session['position_4']=player_4.unique_name
			login_session['position_5']=player_5.unique_name
			players=[player_1,player_2,player_3,player_4,player_5]
			details=startind_5_details(players)
			login_session['details']=details
			print(login_session)
			return render_template('build_starting_5.html', players=coach_players,details=details)
	return redirect(url_for('login'))

@app.route('/save_starting_5', methods = ['GET','POST'])
def save_starting_5():
	if 'email' in login_session:
		coach=session.query(Coach).filter_by(email=login_session['email']).first()
		coach_players=coach.players
		print(coach_players)
		print("email")
		if request.method=='GET':
			return render_template('build_starting_5.html',players=coach_players)
		else:
			player_1=login_session['position_1']
			player_2=login_session['position_2']
			player_3=login_session['position_3']
			player_4=login_session['position_4']
			player_5=login_session['position_5']
			print(player_1)
			details=login_session['details']

			player_1=session.query(Player).filter_by(unique_name=player_1).first()
			player_2=session.query(Player).filter_by(unique_name=player_2).first()
			player_3=session.query(Player).filter_by(unique_name=player_3).first()
			player_4=session.query(Player).filter_by(unique_name=player_4).first()
			player_5=session.query(Player).filter_by(unique_name=player_5).first()
			print(player_1)
			team_name=request.form['team_name']

			new_team=Starting_5(coach=coach,
								name=team_name,
								players=[player_1,player_2,player_3,player_4,player_5]
								)

			session.add(new_team)
			coach.starting_5s.append(new_team)
			print(new_team.players)
			session.commit()
			return render_template('build_starting_5.html', players=coach_players,details=details)




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
			unique_name=request.form['unique_name']
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
									unique_name=unique_name,
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
		print(starting_5s[0].players)
		return render_template('starting_5s.html',starting_5s=starting_5s)

	return redirect(url_for('login'))


@app.route('/my_players', methods=['GET','POST'])
def my_players():
	if 'email' in login_session:
		coach=session.query(Coach).filter_by(email=login_session['email']).first()
		players=coach.players
		return render_template('my_players.html', players=players)



@app.route("/player/<int:player_id>")
def player(player_id):
	if 'email' in login_session:
		coach=session.query(Coach).filter_by(email=login_session['email']).first()
		player=session.query(Player).filter_by(id=player_id).first()
		coach_players=coach.players
		if player in coach_players:
			return render_template('player.html', player=player)
		else:
			redirect('my_players')

@app.route("/edit_player/<int:player_id>", methods=['GET','POST'])
def edit_player(player_id):
	if 'email' in login_session:
		coach=session.query(Coach).filter_by(email=login_session['email']).first()
		player=session.query(Player).filter_by(id=player_id).first()
		if request.method=='GET':
			return render_template('edit_player.html', player=player)
		else:
			new_name=request.form['name']
			new_unique_name=request.form['unique_name']
			new_player_position=request.form['position']
			new_two_points=request.form['two_points']
			new_three_points=request.form['three_points']
			new_one_on_one=request.form['one_on_one']
			new_defense=request.form['defense']
			player.name=new_name
			player.player_position=new_player_position
			player.two_points=new_two_points
			player.three_points=tnew_hree_points
			player.one_on_one=new_one_on_one
			player.defense=new_defense
			session.commit()
			return redirect('player', player_id=player.id)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    login_session.pop('username', None)
    return redirect(url_for('login'))

		

def startind_5_details(players):
	three_points_abilities=""
	two_points_abilities=""
	defense_abilities=""
	three_points_abilities=""
	one_on_one_abilities=""

	three_points_average=0
	two_points_average=0
	defense_average=0
	one_on_one_average=0

	startind_5_details=[]
	print(players)
	for player in players:
		three_points_average=three_points_average+int(player.three_points)
		two_points_average=two_points_average+int(player.two_points)
		defense_average=defense_average+int(player.defense)
		one_on_one_average=one_on_one_average+int(player.one_on_one)


	three_points_average=three_points_average/5.0
	two_points_average=two_points_average/5.0
	defense_average=defense_average/5.0
	one_on_one_average=one_on_one_average/5.0

	

	if three_points_average>=40:
		three_points_abilities="High chance for three points."
	
	elif three_points_average>30 and three_points_average<40:
		print("three points is here")
		three_points_abilities="Mediume chance for three points."
	
	else:
		three_points_abilities="Low chance for three points."
	


	if two_points_average>=60:
		two_points_abilities="high chance for two points."
	
	elif two_points_average>45 and two_points_average<60:
		two_points_abilities="mediume chance for two points."
	
	else:
		two_points_abilities="low chance for two points."
	

	if defense_average>=8:
		defense_abilities="very good defense."
	
	elif defense_average>4 and defense_average<8:
		defense_abilities="good defense."
	
	else:
		defense_abilities="bad defense."
	

	if one_on_one_average>=8:
		one_on_one_abilities="very good one on one abilities."
	
	elif one_on_one_average>4 and one_on_one_average<8:
		one_on_one_abilities="good one on one abilities."
	
	else:
		one_on_one_abilities="bad one on one abilities."
	


	startind_5_details.append(three_points_abilities)
	startind_5_details.append(two_points_abilities)
	startind_5_details.append(one_on_one_abilities)
	startind_5_details.append(defense_abilities)
	
	
	

	return startind_5_details



def verify_password(email, password):
	coach = session.query(Coach).filter_by (email=email).first()
	if not coach or not coach.verify_password(password):
		return False
	return True



if __name__ == '__main__':
    app.run(debug=True)