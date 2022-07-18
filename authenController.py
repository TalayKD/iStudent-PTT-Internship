from service import *
from __init__ import *
from app_config import *
from functions import *
from flask import session, render_template

import json

###############################
### Basic Login Controllers ###
###############################

def loginpageController():
    try:
        # Technically we could use empty list [] as scopes to do just sign in,
        # here we choose to also collect end user consent upfront
        session["flow"] = build_auth_code_flow(scopes=app_config.SCOPE)
        return render_template('login.html', auth_url=session["flow"]["auth_uri"])

    except Exception as e:
        print("load login page ERROR : " , str(e))
        return "load login page ERROR : " + str(e)

def loginfailedController():
    try:
        # Technically we could use empty list [] as scopes to do just sign in,
        # here we choose to also collect end user consent upfront
        session["flow"] = build_auth_code_flow(scopes=app_config.SCOPE)
        return render_template('loginfailed.html', auth_url=session["flow"]["auth_uri"])

    except Exception as e:
        print("load loginfailed page ERROR : " , str(e))
        return "load loginfailed page ERROR : " + str(e)

def loginController():
    try:
        client = getClientAll()
        # Take data from form
        data = request.form
        for user in client:
            if(user[2] == data['email'] and user[3] == data['password']):
                session['name'] = data['email']
                return redirect("/")
        return redirect("/loginfailed")

    except Exception as e:
        print("login ERROR : " , str(e))
        return "login ERROR : " + str(e)

################################
### Google Login Controllers ###
################################

def logingoogleController():
    try:
        # Find out what URL to hit for Google login
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = clientGoogle.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"]
        )
        return redirect(request_uri)

    except Exception as e:
        print("login google ERROR : " , str(e))
        return "login google ERROR : " + str(e)

def googlecallbackController():
    try:
        # Get authorization code Google sent back to you
        code = request.args.get("code")

        # Find out what URL to hit to get tokens that allow you to ask for
        # things on behalf of a user
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        #Prepare and send a request to get tokens!
        token_url, headers, body = clientGoogle.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
        )

        # Parse the tokens!
        clientGoogle.parse_request_body_response(json.dumps(token_response.json()))

        # Now that you have tokens, let's find and hit the URL
        # from Google that gives you the user's profile information,
        # including their Google profile and email
        userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
        uri, headers, body = clientGoogle.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        # You want to make sure their email is verified.
        # The user authenticated with Google, authorized your app, and now
        # you've verified their email through Google!
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()['sub']
            users_email = userinfo_response.json()['email']
            users_name = userinfo_response.json()['given_name']
        else:
            return "User email not available or not verified by Google.", 400

        # Create user in database, if not exists already
        # Log the user in and send them to the homepage

        data = getClientCol("email")
        emails = []
        for d in data:
            emails.append(d[0])
        if users_email not in emails:
            insertClientRow(["name", "email"], [users_name, users_email])

        # Start session and redirect to home page
        session['name'] = users_email
        return redirect("/")

    except Exception as e:
        print("login google callback ERROR : " , str(e))
        return "login google callback ERROR : " + str(e)

##################################
### Azure AD Login Controllers ###
##################################

def authorizedController():
    try:
        cache = load_cache()
        result = build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        session["name"] = session["user"].get("name")
        save_cache(cache)

    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them

    return redirect(url_for("display"))

#########################
### Logout Controller ###
#########################

def logoutController():
    try:
        if not session.get('user'):
            session['name'] = None
            return redirect('/loginpage')
        session.clear()  # Wipe out user and its token cache from session
        return redirect(  # Also logout from your tenant's web session
            app_config.AUTHORITY + "/oauth2/v2.0/logout" +
            "?post_logout_redirect_uri=" + url_for("loginpage", _external=True))

    except Exception as e:
        print("logout ERROR : " , str(e))
        return "logout ERROR : " + str(e)

###############################
### Registration Controller ###
###############################

def registerController():
    try:
        form = RegistrationForm(request.form)
        if (request.method == 'POST' and form.validate()):
            insertClientRow(["name", "email", "password"], [form.name.data, form.email.data, form.password.data])
            return redirect('/loginpage')
        return render_template('register.html', form=form)

    except Exception as e:
        print("register info ERROR : " , str(e))
        return "register info ERROR : " + str(e)