from __init__ import *
from service import *
from authenController import *


### LOGIN ###

@app.route('/loginpage')
def loginpage():
    return loginpageController()

@app.route('/loginfailed')
def loginfailed():
    return loginfailedController()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return loginController()

@app.route('/logingoogle')
def logingoogle():
    return logingoogleController()

@app.route('/logingoogle/callback')
def googlecallback():
    return googlecallbackController()

# AZURE AD LOGIN

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    return authorizedController()

app.jinja_env.globals.update(build_auth_code_flow=build_auth_code_flow)  # Used in template

### LOGOUT ###
@app.route('/logout')
def logout():
    return logoutController()


### REGISTER ###

@app.route('/register', methods=['GET','POST'])
def register():
    return registerController()

