import repository

from wtforms import Form, StringField, EmailField, PasswordField, validators
from wtforms.validators import ValidationError

########################################
### Database Initialization Services ###
########################################

edCols = ["education_id", "degree", "credits", "duration", "earnings"]
studentCols = ["student_id", "name", "nationality", "age", "gender", "grade", "education_id"]
clientCols = ["client_id", "name", "email", "password"]

# creates client table in database for user login and registration
def createClientTable():
    return repository.create_client_table()

# initializes the client table with one user
def initClientTable():
    return repository.init_client_table()

# creates education table in database for education data
def createEducationTable():
    return repository.create_education_table()

# initializes the education table with basic education degrees
def initEducationTable():
    return repository.init_education_table()

# creates student table in database for student data
def createStudentTable():
    return repository.create_student_table()

###############################
### Database Fetch Services ###
###############################

# All

def getEducationAll():
    return repository.get_table("education")

def getStudentAll():
    return repository.get_table("student")

def getClientAll():
    return repository.get_table("client")

# Column

def getEducationCol(col):
    col = str(col)
    if (col not in edCols):
        return "Column does not exist in Education Table"
    return repository.get_table_col("education", col)

def getStudentCol(col):
    col = str(col)
    if (col not in studentCols):
        return "Column does not exist in Student Table"
    return repository.get_table_col("student", col)

def getClientCol(col):
    col = str(col)
    if (col not in clientCols):
        return "Column does not exist in Client Table"
    return repository.get_table_col("client", col)

# Row

def getEducationRow(col, val):
    col = str(col)
    if (col not in edCols):
        return "Column does not exist in Education Table"
    return repository.get_table_row("education", col, val)

def getStudentRow(col, val):
    col = str(col)
    if (col not in studentCols):
        return "Column does not exist in Student Table"
    return repository.get_table_row("student", col, val)

def getClientRow(col, val):
    col = str(col)
    if (col not in clientCols):
        return "Column does not exist in Client Table"
    return repository.get_table_row("client", col, val)

################################
### Database Insert Services ###
################################

# columns is an array of columns to be inserted into
# values is an array of the corresponding values in each column
def insertEducationRow(columns, values):
    for col in columns:
        if (col not in edCols):
            return "One or more columns does not exist in Education Table"
    if (len(columns) != len(values)):
        return "Columns and values don't match"
    return repository.insert_row("education", columns, values)

def insertStudentRow(columns, values):
    for col in columns:
        if (col not in studentCols):
            return "One or more columns does not exist in Student Table"
    if (len(columns) != len(values)):
        return "Columns and values don't match"
    return repository.insert_row("student", columns, values)

def insertClientRow(columns, values):
    for col in columns:
        if (col not in clientCols):
            return "One or more columns does not exist in Client Table"
    if (len(columns) != len(values)):
        return "Columns and values don't match"
    return repository.insert_row("client", columns, values)


################################
### Database Update Services ###
################################


# data is a dictionary that stores column : value pairs
# update only at col with row (value in the col) if the arguments are given
def updateEducation(data, col=None, row=None):
    for d in data:
        if (d not in edCols):
            return "One or more columns does not exist in Education Table"
    if (col != None):
        if (col not in edCols):
            return "Specified col is not a field in the table"
        if (row == None):
            return "Col given but row is not specified"
    else:
        if (row != None):
            return "Row given but col is not specified"
    return repository.update_table("education", data, col, row)


def updateStudent(data, col=None, row=None):
    for d in data:
        if (d not in studentCols):
            return "One or more columns does not exist in Student Table"
    if (col != None):
        if (col not in studentCols):
            return "Specified col is not a field in the table"
        if (row == None):
            return "Col given but row is not specified"
    else:
        if (row != None):
            return "Row given but col is not specified"
    return repository.update_table("student", data, col, row)


def updateClient(data, col=None, row=None):
    for d in data:
        if (d not in clientCols):
            return "One or more columns does not exist in Client Table"
    if (col != None):
        if (col not in clientCols):
            return "Specified col is not a field in the table"
        if (row == None):
            return "Col given but row is not specified"
    else:
        if (row != None):
            return "Row given but col is not specified"
    return repository.update_table("client", data, col, row)


################################
### Database Delete Services ###
################################

# delete only at col with row (value in col) only if arguments are given
# otherwise, delete all rows in the table
def deleteEducation(col=None, row=None):
    if (col != None):
        if (col not in edCols):
            return "Specified col is not a field in the table"
        if (row == None):
            return "Col given but row is not specified"
    else:
        if (row != None):
            return "Row given but col is not specified"
    return repository.delete_row("education", col, row)

def deleteStudent(col=None, row=None):
    if (col != None):
        if (col not in studentCols):
            return "Specified col is not a field in the table"
        if (row == None):
            return "Col given but row is not specified"
    else:
        if (row != None):
            return "Row given but col is not specified"
    return repository.delete_row("student", col, row)

def deleteClient(col=None, row=None):
    if (col != None):
        if (col not in clientCols):
            return "Specified col is not a field in the table"
        if (row == None):
            return "Col given but row is not specified"
    else:
        if (row != None):
            return "Row given but col is not specified"
    return repository.delete_row("client", col, row)



##############################
### Miscellaneous Services ###
##############################

def getClientName(session):
    if not session.get('user'):
        email = session['name']
        data = getClientRow("email", email)
        return data[0][1]
    return session['name']


# Registration Authentication Service
class RegistrationForm(Form):
    name = StringField('Name', [validators.InputRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "Name", "class": "form-control"})
    email = EmailField('Email', [validators.DataRequired(), validators.Email(message="Invalid email address")], render_kw={"placeholder": "Email", "class": "form-control"})
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6),
        validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={"placeholder": "Password", "class": "form-control"})
    confirm = PasswordField('Retype password', [validators.InputRequired()], render_kw={"placeholder": "Retype Password", "class": "form-control"})

    #Check that this email does not already exist in the database
    def validate_email(self, email):
        client = getClientAll()
        for user in client:
            if user[2] == self.email.data:
                raise ValidationError("Email already taken")

