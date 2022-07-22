*** Settings ***
Library     RequestsLibrary
Library     SeleniumLibrary
Library     OperatingSystem

Suite Teardown      Delete All Sessions


*** Variables ***
${Base_URL}     https://poc-python-template-dev.azurewebsites.net
${Login_URL}    ${Base_URL}/loginpage
${EXECDIR}      ${CURDIR}


*** Test Cases ***
Get_Login_Request
    create_session      Login_Page      ${Base_URL}
    ${response}=    GET On Session     Login_Page      /loginpage
    Should Contain      ${response.text}        Sign in to start your session
    Should Contain      ${response.text}        Sign in using Google
    Should Contain      ${response.text}        Sign in using Azure AD
    Should Contain      ${response.text}        Register a new membership

Wrong_Username_Login_Failed
    Create Webdriver    Chrome      executable_path=${EXECDIR}/chromedriver
    Go to        ${Login_URL}
    Input text      name=email      wrongusername@gmail.com
    Input text      name=password       helloworld
    Click Button        Sign In
    Wait Until Page Contains        Login Failed
 
Wrong_Email_Login_Failed
    Input text      name=email      talaykd@gmail.com
    Input text      name=password      wrongpassword
    Click Button        Sign In
    Wait Until Page Contains        Login Failed

Login_Success
    Input text      name=email      talaykd@gmail.com
    Input text      name=password      helloworld
    Click Button        Sign In
    Wait Until Page Contains        Student Records Table

Insert_Record
    Handle Alert
    Click Link        Insert New Record
    Input text      name=name       RobotFramework
    Input text      name=nationality        Selenium
    Input text      name=age        18
    select from list by label       name=gender     Male
    Input text      name=grade      93
    select from list by label       name=education_id       Masters
    Click Button        Submit
    Wait Until Page Contains        RobotFramework

Update_Record
    Click Link      Edit Record
    Input text      name=name       iRobot
    Input text      name=age        29
    Click Button        Submit
    Wait Until Page Contains        iRobot

Clear_and_Logout
    Click Link        Delete Record
    Click Link      Logout
    Wait Until Page Contains        Sign in to start your session
    Close Browser
    
