from flask import Flask, render_template, request, json, redirect
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
from flask import session
app.secret_key = 'why would I tell you my secret key?'

mysql = MySQL() #Create my MySQL Object named mysql

#MySQL configurations (Todo move to config.file)

app.config['MYSQL_DATABASE_USER'] = 'gn570lv2dz55'
app.config['MYSQL_DATABASE_PASSWORD'] = 'VQ35HR@tt'
app.config['MYSQL_DATABASE_DB'] = 'what'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

#Server start my sql -> login -> make cursor object 

mysql.init_app(app) #Start MySQL Application inside Flask

# Function endpoints
#@app.route('/')
#@app.route('/index')
#def index():
#    return render_template('/index.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

#@app.route('/signIn')
#def signIn():
#    return render_template('/signin.html')

#@app.route('/showSignUp')#          <------ same as main, this will turn into showSignUp.js
#def showSignUp():
#    return render_template('/signUp.html')


#Register User function
@app.route('/signUp', methods=['POST'])#      
def signUp():

    # read the posted values from the UI

    #Grab data from html page
    p_firstName = request.form['inputFirstName']
    p_lastName = request.form['inputLastName']
    p_userName = request.form['inputUserName']
    p_email = request.form['inputEmail']
    p_Password = request.form['inputPassword']
 
    # validate the received values (prevents program from continuing if a field is blank)
    if p_firstName and p_lastName and p_userName and p_email and p_Password:
       
        p_hashedPassword = generate_password_hash(p_Password)
        #Check db for user existence
        dbConnection = mysql.connect() #Connect (object) to db with Admin settings
        dbCursor = dbConnection.cursor() #Create a cursor object
        dbCursor.execute("SELECT * FROM `tbl_user` WHERE `user_username` = \'"+p_userName+"\'"),   
        #Grab results (if none data = {})
        data = dbCursor.fetchall()
        
        #if data is {} ADD USER
        
        if len(data) is 0:
            dbCursor.execute("INSERT INTO `tbl_user` (`ID`, `user_firstname`, `user_lastname`, `user_username`, `user_email`, `user_password`) "
            "VALUES (NULL, \'"+p_firstName+"\',\'"+p_lastName+"\',\'"+p_userName+"\',\'"+p_email+"\',\'"+p_hashedPassword+"\');")
            #Commit db changes
            dbConnection.commit()
            #bring to signin
            dbCursor.close()
            dbConnection.close()
            return redirect("http://keepkeet.com/signIn.html")
            return 'user created succ'
        else:
            dbCursor.close()
            dbConnection.close()
            print("error Username exist boiis")
            return 'error Username exist boiis'
    else:
        print("error 446")
        json.dumps({'<span>Enter the required fields</span>'})
        return render_template('Enter the required fields')


@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['Username']
        _password = request.form['inputPassword']

        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM tbl_user WHERE user_username = %s ;',(_username))
      
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][5]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
    except Exception as e:
        print('error 555')
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()
@app.route('/userHome.html')
@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

#       #       #       #       #       #       #       #       #       #
#@app.route('/proof')
#def proof():
#    dbConnection = mysql.connect() #Connect (object) to db with Admin settings
#    dbCursor = dbConnection.cursor() #Create a cursor object
#    query = """SELECT * FROM Users"""
#    dbCursor.execute(query)
#    s = "<table style='border:1px solid red'>"  
#    for row in dbCursor:
#        s = s + "<tr>"    
#    for x in row:    
#        s = s + "<td>" + str(x) + "</td>"    
#        s = s + "</tr>" 
#    
#    return "<html><body>" + s + "</body></html>"
#    return "<html><body>" +dbCursor.execute(query)+ "</body></html>"
#       #       #       #       #       #       #       #       #       #

if __name__ == "__main__":
    app.run(debug=True)
