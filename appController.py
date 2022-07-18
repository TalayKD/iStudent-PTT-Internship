from service import *
from flask import session, redirect, render_template, request

def initController():
    createClientTable()
    createEducationTable()
    createStudentTable()

########################
### Page Controllers ###
########################

### Display Pages ###

def displayController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')

        data = getStudentAll()
        ed = getEducationAll()
        data.append(ed)
        data.append(getClientName(session))
        return render_template('displayAdmin.html', data=data)

    except Exception as e:
        print("display student ERROR : " , str(e))
        return "display student ERROR : " + str(e)

def displayEducationController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')

        data = getEducationAll()
        data.append(getClientName(session))
        return render_template('displayEd.html', data=data)

    except Exception as e:
        print("display education ERROR : " , str(e))
        return "display education ERROR : " + str(e)

### Insert Form Pages ###

def insertpageController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')

        data = getEducationAll()
        data.append(getClientName(session))
        return render_template('formAdmin.html', data=data)

    except Exception as e:
        print("student form ERROR : " , str(e)) 
        return "student form ERROR : " + str(e)

def insertpageEducationController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')

        data = []
        data.append(getClientName(session))
        return render_template('formEd.html', data=data)

    except Exception as e:
        print("education form ERROR : " , str(e))
        return "education form ERROR : " + str(e)

### Update Form Pages ###

def updatepageController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')    

        # Connect to database
        data = getEducationAll()
        student = getStudentRow("student_id", request.args.get("student_id"))
        data.append(student[0])
        data.append(getClientName(session))
        return render_template('updateformAdmin.html', data=data)

    except Exception as e:
        print("student update page ERROR : " , str(e)) 
        return "student update page ERROR : " + str(e)

def updatepageEducationController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')

        education = getEducationRow("education_id", request.args.get("education_id"))
        data = []
        data.append(education[0])
        data.append(getClientName(session))
        return render_template('updateformEd.html', data=data)

    except Exception as e:
        print("education update page ERROR : " , str(e)) 
        return "education update page ERROR : " + str(e)

##########################
### Action Controllers ###
##########################

### Insert Data ###

def insertdataController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')

        data = request.form
        insertStudentRow(list(data.keys()), list(data.values()))
        return redirect("/")

    except Exception as e:
        print("insert student ERROR : " , str(e))
        return "insert student ERROR : " + str(e)

def insertdataEducationController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')

        data = request.form
        insertEducationRow(list(data.keys()), list(data.values()))
        return redirect("/displayEducation")

    except Exception as e:
        print("insert education ERROR : " , str(e))
        return "insert education ERROR : " + str(e)

### Update Data ###

def updatedataController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')

        data = request.form
        arguments = request.args
        if ('student_id' in arguments):
            updateStudent(data, "student_id", arguments.get('student_id'))
        else:
            updateStudent(data)
        return redirect("/")

    except Exception as e:
        print("update student ERROR : " , str(e))
        return "update student ERROR : " + str(e)


def updatedataEducationController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')

        data = request.form
        arguments = request.args
        if ('education_id' in arguments):
            updateEducation(data, "education_id", arguments.get('education_id'))
        else:
            updateEducation(data)
        return redirect("/displayEducation")

    except Exception as e:
        print("update education ERROR : " , str(e))
        return "update education ERROR : " + str(e)
    
    
### Delete Data ###

def deleterecordController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')

        argument = request.args
        if ('student_id' not in argument):
            deleteStudent()
        else:
            deleteStudent("student_id", argument.get('student_id'))
        return redirect("/")

    except Exception as e:
        print("delete student ERROR : " , str(e))
        return "delete student ERROR : " + str(e)

def deleterecordEducationController():
    try:
        # Logs user out if not logged in
        if not session.get('name'):
            return redirect('/loginpage')

        #for use with postman
        #data = request.get_json(force=True)
        argument = request.args
        if ('education_id' not in argument):
            deleteEducation()
        else:
            deleteEducation("education_id", argument.get('education_id'))
        return redirect("/displayEducation")

    except Exception as e:
        data = []
        data.append(str(e))
        data.append(getClientName(session))
        return render_template("errorpage.html", data=data)
