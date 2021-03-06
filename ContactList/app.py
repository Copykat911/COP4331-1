from flask import Flask, render_template, request, json, redirect, session, flash
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
@app.route('/test')
def test():
    return render_template('test.html')
    
@app.route('/')
def index():
    return render_template('test.html')

@app.route('/signUp', methods=['POST'])#      
def signUp():

    # read the posted values from the UI

    #Grab data from html page
    p_firstName = "NULL"
    p_lastName = "NULL"
    p_userName = request.form['inputUsername']
    p_email = request.form['inputEmail']
    p_Password = request.form['inputPassword']
 
    # validate the received values (prevents program from continuing if a field is blank)
    if p_userName and p_email and p_Password:
       
        p_hashedPassword = generate_password_hash(p_Password)
        #Check db for user existence
        dbConnection = mysql.connect() #Connect (object) to db with Admin settings
        dbCursor = dbConnection.cursor() #Create a cursor object
        dbCursor.execute("SELECT * FROM `tbl_user` WHERE `user_username` = \'"+p_userName+"\'"),   

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
            return redirect("/")
            return 'user created succ'
        else:
            dbCursor.close()
            dbConnection.close()
            print("error Username exist boiis")
            return 'error Username exist boiis'
    else:
        print("error 446")
        json.dumps({'<span>Enter the required fields</span>': 'hi'})
        return render_template('Enter the required fields')

#When user attempts to log in DO:
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['Username']
        _password = request.form['inputPassword']

        # connect cursor to mysql

        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM tbl_user WHERE user_username = %s ;',(_username))
      
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][5]),_password):
                session['user'] = data[0][0]
                session['username'] = data[0][3]
                session['password'] = data[0][5]
                return redirect('/userHome')
                #return render_template('/userHome.html', title = session.get('username'))
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Unauthorized Access')
 
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    
    finally:
        cursor.close()
        con.close()

#Successful login redirect
@app.route('/userHome')
def userHome():
    if session.get('user'):
        data = readContact()

        return render_template('/userHome.html', title = session.get('username'), data = data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

#When user hits logout DO:
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

#       #       #       #       Function endpoints Contacts      #       #       #       #      #       #       #       #
@app.route('/CreateContact', methods=['POST'])
def CreateContact():

    #Grab data from html page

        contact_firstName = request.form['inputFirstName']
        contact_lastName = request.form['inputLastName']
        contact_email = request.form['inputEmail']
        contact_phone = request.form['inputPhone']
        contact_userID = session.get('user')

        if contact_firstName and contact_lastName:
            dbConnection = mysql.connect() #Connect (object) to db with Admin settings
            dbCursor = dbConnection.cursor() #Create a cursor object
            
            print('''(
            "INSERT INTO `tbl_contacts` (`ID`, `contact_firstName`, `contact_lastName`, `contact_email`, `contact_phone`, `contact_dateCreated) "
            "VALUES (NULL, %s, %s, %s, %s, NULL, %s)",(contact_firstName, contact_lastName, contact_email, contact_phone)
            )"''')
        
            dbCursor.execute(
                "INSERT INTO `tbl_contacts` (`contact_firstName`, `contact_lastName`, `contact_email`, `contact_phone`,`contact_userID`) "
                "VALUES (%s, %s, %s, %s, %s)",(contact_firstName, contact_lastName, contact_email, contact_phone, contact_userID)
                )

       
            dbConnection.commit()
        if session.get('user'):
            dbCursor.close()
            dbConnection.close()
            return redirect('/userHome')

        else:
            dbCursor.close()
            dbConnection.close()
            return render_template('error.html',error = ' Database Error Try again')
        dbCursor.close()
        dbConnection.close()
        return 'oof'

@app.route('/editContact', methods=['POST'])
def editContact():
   
    contact_firstName = request.form['inputFirstName']
    contact_lastName = request.form['inputLastName']
    contact_email = request.form['inputEmail']
    contact_phone = request.form['inputPhone']
    ID = request.form['contactId']
    
    dbConnection = mysql.connect() #Connect (object) to db with Admin settings
    dbCursor = dbConnection.cursor() #Create a cursor object
    dbCursor.execute(
    '''UPDATE `tbl_contacts` SET 
    `contact_firstName` = %s, 
    `contact_lastName` = %s, 
    `contact_email` = %s, 
    `contact_phone` = %s 
    WHERE `tbl_contacts`.`ID`= %s;''',(contact_firstName, contact_lastName, contact_email, contact_phone, ID)

    )
    dbConnection.commit()
    dbCursor.close()
    dbConnection.close()
    
    return redirect('/userHome')

@app.route('/readContact')
def readContact():
    contact_userID = session.get('user')
    dbConnection = mysql.connect() #Connect (object) to db with Admin settings
    dbCursor = dbConnection.cursor()
    dbCursor.execute('SELECT * FROM `tbl_contacts` WHERE `contact_userID` = %s',(contact_userID))
    
    returndata=dbCursor.fetchall()
    dataa = []
    for returndata in returndata:
        data = {
        'Id': returndata[0],
        'Firstname': returndata[1],
        'Lastname': returndata[2],
        'Email': returndata[3],
        'Phone': returndata[4]
        }
        dataa.append(data)
    dbCursor.close()
    dbConnection.close()
    
    return dataa

@app.route('/deleteContact', methods=['POST'])
def deleteContact():
    contact_userID = request.form['id']
    dbConnection = mysql.connect()
    dbCursor = dbConnection.cursor()
    
    dbCursor.execute("DELETE FROM tbl_contacts WHERE `ID` = %s", (contact_userID))
    
    dbConnection.commit()
    dbCursor.close()
    dbConnection.close()
    
    return redirect('/userHome')

if __name__ == "__main__":
    app.run(debug=True)

