from flask import Flask, render_template,request,redirect,url_for,flash,session
from datetime import datetime



#IMPORTING FLASK
app=Flask(__name__, template_folder='templates')
app.secret_key="lol"



@app.route('/')
def homepage():
    if 'user' in session:
        return render_template('index.html', username=session['user'], logged_in=True)
    else:
        return render_template('index.html', logged_in=False)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.methods=='POST':
        username=request.form['username']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        if confirm_password!=password:
            flash('Passwords do not match', catagory='error')
        
            
        


@app.route('/calendar')
def calendar():
    return render_template('calendar.html')
        
@app.route('/logout')
def logout():
    session.pop('user',None)
    return render_template('logout.html')
        
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        #BASE AUTENTICATION FOR TESTING PURPOSE
        if username=='username' and password=='password':
            session['user']=username
            return redirect(url_for('homepage'))
        else:
            flash("Wrong username/password","danger")
    return render_template('login.html')




# @app.route('/addEvent', methods=['GET','POST'])
# def addEvent():
#     if request.method=='POST':






if __name__ == "__main__":
    app.run(debug=True)

            






    
