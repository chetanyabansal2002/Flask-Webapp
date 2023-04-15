# Importing the Flask Framework

from modules import *
from flask import *
import database
import configparser


page = {}
session = {}

# Initialise the FLASK application
app = Flask(__name__)
app.secret_key = 'SoMeSeCrEtKeYhErE'


# Debug = true if you want debug output on error ; change to false if you dont
app.debug = True


# Read my unikey to show me a personalised app
config = configparser.ConfigParser()
config.read('config.ini')
unikey = config['DATABASE']['user']
portchoice = config['FLASK']['port']

#####################################################
##  INDEX
#####################################################

# What happens when we go to our website
@app.route('/')
def index():
    # If the user is not logged in, then make them go to the login page
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['unikey'] = unikey
    page['title'] = 'Welcome'
    return render_template('welcome.html', session=session, page=page)

################################################################################
# Login Page
################################################################################

# This is for the login
# Look at the methods [post, get] that corresponds with form actions etc.
@app.route('/login', methods=['POST', 'GET'])
def login():
    page = {'title' : 'Login', 'unikey' : unikey}
    # If it's a post method handle it nicely
    if(request.method == 'POST'):
        # Get our login value
        val = database.check_login(request.form['sid'], request.form['password'])

        # If our database connection gave back an error
        if(val == None):
            flash("""Error with the database connection. Please check your terminal
            and make sure you updated your INI files.""")
            return redirect(url_for('login'))

        # If it's null, or nothing came up, flash a message saying error
        # And make them go back to the login screen
        if(val is None or len(val) < 1):
            flash('There was an error logging you in')
            return redirect(url_for('login'))
        # If it was successful, then we can log them in :)
        session['name'] = val[1]
        session['sid'] = request.form['sid']
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        # Else, they're just looking at the page :)
        if('logged_in' in session and session['logged_in'] == True):
            return redirect(url_for('index'))
        return render_template('index.html', page=page)


################################################################################
# Logout Endpoint
################################################################################

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You have been logged out')
    return redirect(url_for('index'))


################################################################################
# Transcript Page
################################################################################

@app.route('/transcript')
def transcript():
    # TODO
    # Now it's your turn to add to this ;)
    # Good luck!
    #   Look at the function below
    #   Look at database.py
    #   Look at units.html and transcript.html
    return render_template('transcript.html', page=page, session=session)


################################################################################
# List Units page
################################################################################


@app.route('/list-units')
def list_units():
    # Go into the database file and get the list_units() function
    units = database.list_units()

    # What happens if units are null?
    if (units is None):
        # Set it to an empty list and show error message
        units = []
        flash('Error, there are no units of study')
    page['title'] = 'Units of Study'
    return render_template('units.html', page=page, session=session, units=units)




################################################################################
# List classrooms page
################################################################################


@app.route('/get-classrooms-type')
def get_classrooms_type():
    classrooms = database.classroom_type()
    if (classrooms is None):
        classrooms= []
        flash('Error, there are no classrooms')

        
    page['title'] = 'Classrooms by type'
    return render_template('classroom_type.html', page=page, session=session, classrooms=classrooms)    



################################################################################
# List classrooms by type
################################################################################

@app.route('/get-classrooms')
def get_classrooms():   
    classrooms = database.get_classrooms()  
    if (classrooms is None):
        classrooms= []
        flash('Error, there are no classrooms')
    page['title'] = 'Classrooms'
    return render_template('classrooms.html', page=page, session=session, classrooms=classrooms)  





################################################################################
# List classrooms by seats
################################################################################

# List all the classrooms by seats
@app.route('/get-classroom-seats', methods=['POST','GET'])
def get_classroom_seats():
    page = {'title' : 'Search Prerequisites'}    
    classrooms= []
    if(request.method == 'POST'):
        classrooms = database.classroom_by_seat(request.form['Seats'])
        if classrooms == None:
            classrooms = []
            flash('Error, there are no units of study')
            return render_template('classroom_seats.html', page=page, session=session,  classrooms=classrooms)
        return render_template('classroom_seats.html', page=page, session=session,  classrooms=classrooms)
    else:
        return render_template('classroom_seats.html', page=page, session=session, classrooms=classrooms)


        
 ##############################################################################
#Insert Value
###############################################################################
@app.route('/insert-classroom', methods=['POST','GET'])
def insert_classroom():
    page = {'title' : 'Insert Classroom'}
    if(request.method == 'POST'):
        saved=database.insert_value(request.form['classroomID'],request.form['Seats'],request.form['Type'])  
        if(saved):
            pass
        else:
            flash('Error, It is impossible to add this relation')
        return render_template('insert_classroom.html', page=page, session=session )
    else:
        return render_template('insert_classroom.html', page=page, session=session)
    
    
################################################################################
# Order by seats
################################################################################


@app.route('/order-seats')
def order_seats(): 
    classrooms = database.get_classrooms_seats()  
    if (classrooms is None):
        classrooms= []
        flash('Error, there are no classrooms')
    page['title'] = 'Classrooms'
    return render_template('classrooms.html', page=page, session=session, classrooms=classrooms) 



################################################################################
# Order by type
################################################################################


@app.route('/order-type')
def order_type():   
    classrooms = database.get_classrooms_type()  
    if (classrooms is None):
        classrooms= []
        flash('Error, there are no classrooms')
    page['title'] = 'Classrooms'
    return render_template('classrooms.html', page=page, session=session, classrooms=classrooms) 


@app.route('/piechart')
def piechart():
    classrooms = database.classroom_type()
    if (classrooms is None):
        classrooms= []
        flash('Error, there are no classrooms')
    class_type = []
  
    
    class_count = []
    
    if classrooms != None:
     for classroom in classrooms:
        class_type.append(classroom[0])
        class_count.append(int(classroom[1]))
        
    page['title'] = 'Classrooms by type'
    return render_template('piechart.html', page=page, session=session, classrooms=classrooms,class_type = class_type,class_count = class_count)   