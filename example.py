from flask import Flask, render_template, request, json, redirect, session
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.secret_key = 'why would I tell you my secret key?'
mysql = MySQL()                                                  #       #       #       #       #       #       #       #
app.config['MYSQL_DATABASE_USER'] = 'gn570lv2dz55'               #   Create my MySQL Object named mysql                  #
app.config['MYSQL_DATABASE_PASSWORD'] = 'VQ35HR@tt'              #                                                       #
app.config['MYSQL_DATABASE_DB'] = 'what'                         #   MySQL configurations (Todo move to config.file)     #
app.config['MYSQL_DATABASE_HOST'] = 'localhost'                  #                                                       #
mysql.init_app(app)                                              #           Start MySQL Application inside Flask        #
                                                                 #       #       #       #       #       #       #       #

#       #       #       #       Function endpoints Frontpage      #       #       #       #      #       #       #       #

#When user hits signup DO::
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
        else:
            dbCursor.close()
            dbConnection.close()
            return 'error Username exist boiis'
    else:
        print("error 446")
        json.dumps({'<span>Enter the required fields</span>'})
        return render_template('Enter the required fields')

#When user attempts to log in DO:
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        user_username = request.form['Username']
        user_password = request.form['inputPassword']

        # connect cursor to mysql

        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM tbl_user WHERE user_username = %s ;',(user_username))
      
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][5]),user_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    
    finally:
        cursor.close()
        con.close()

#Successful login redirect
@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('/userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

#When user hits logout DO:
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

#       #       #       #       Function endpoints Contacts      #       #       #       #      #       #       #       #

@app.route('/userHome#createContact')
def createContact(methods=['POST']):
    try:
    #Grab data from html page

        contact_firstName = request.form['inputFirstName']
        contact_lastName = request.form['inputLastName']
        contact_email = request.form['inputEmail']
        contact_phone = request.form['inputPhone']
        contact_userID = session.get('user')
        if contact_firstName and contact_lastName:
            dbConnection = mysql.connect() #Connect (object) to db with Admin settings
            dbCursor = dbConnection.cursor() #Create a cursor object
            dbCursor.execute(
                "INSERT INTO `tbl_contacts` (`contact_ID`, `contact_firstName`, `contact_lastName`, `contact_email`, `contact_phone`, `contact_dateCreated`, `contact_userID`)" 
                "VALUES (NULL, \'"+contact_firstName+"\', \'"+contact_lastName+"\', \'"+contact_email+"\', \'"+contact_phone+"\', CURRENT_TIMESTAMP, \'"+contact_userID+"\);"
                )
            dbConnection.commit()
        if session.get('user'):
            return render_template('/userHome.html')
        else:
            return render_template('error.html',error = 'Unauthorized Access')

        return 'oof'
    
    finally: 
        dbCursor.close()
        dbConnection.close()


@app.route('/userHome#editContact')
def editContact(methods=['POST']):
    return 'oof'

    #UPDATE `tbl_contacts` SET 
    # `contact_firstName` = 'contact_firstName5', 
    # `contact_lastName` = 'contact_lastName5', 
    # `contact_email` = 'contact_email5', 
    # `contact_phone` = 'contact_phone5' 
    #WHERE `tbl_contacts`.`contact_ID` = 2;

@app.route('/userHome#readContact')
def readContact(methods=['POST']):
    return 'oof'

@app.route('/userHome#deleteContact')
def deleteContact(methods=['POST']):
    return 'oof'
if __name__ == "__main__":
    app.run()
