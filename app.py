from __init__ import *
from appController import *
from authentication import *

### DISPLAY PAGE ###

# Student Table
@app.route('/')
def display():
    return displayController()

# Education Table
@app.route('/displayEducation')
def displayEducation():
    return displayEducationController()


### INSERT FORM PAGE ###

# Student
@app.route('/insertpage')
def insertpage():
    return insertpageController()

# Education
@app.route('/insertpageEducation')
def insertpageEducation():
    return insertpageEducationController()


### UPDATE FORM PAGE ###

# Student
@app.route('/updatepage')
def updatepage():
    return updatepageController()

# Education
@app.route('/updatepageEducation')
def updatepageEducation():
    return updatepageEducationController()


# ACTIONS #

### INSERT DATA ###

# Student
@app.route('/insertdata', methods=['GET', 'POST'])
def insertdata():
    return insertdataController()

# Education
@app.route('/insertdataEducation', methods=['GET', 'POST'])
def insertdataEducation():
    return insertdataEducationController()


### UPDATE DATA ###

# Student
@app.route('/updatedata', methods=['GET', 'POST', 'PUT'])
def updatedata():
    return updatedataController()

# Education
@app.route('/updatedataEducation', methods=['GET', 'POST', 'PUT'])
def updatedataEducation():
    return updatedataEducationController()


### DELETE RECORD ###

# Student
@app.route('/deleterecord', methods = ['GET','POST','DELETE'])
def deleterecord():
    return deleterecordController()

# Education
@app.route('/deleterecordEducation', methods = ['GET','POST','DELETE'])
def deleterecordEducation():
    return deleterecordEducationController()


if __name__ == "__main__":
    app.run(debug=True)