*** Settings ***
Library  Collections
Library  String
Library  RequestsLibrary
Library  OperatingSystem

Suite Teardown  Delete All Sessions

*** Variables ***
${url}    ${APPLICATION}
${data}		{  "function_id": "demo_nodb",  "app_user": "demo",  "app_password": "tq9jGm8tUr",  "req_transaction_id": "111111",  "state_name": "",  "req_parameters": [    {      "k": "wait_command",      "v": "1"    },     {      "k": "user_id",      "v": "JuM+"    }  ],   "extra_xml": "test no extra xml"}	
 
*** Test Cases ***
Get Requests ${APPLICATION}
    [Tags]	get
	Create Session    app         ${url}  
    ${resp}=          GET On Session    app    /      data=${data}   
	Log   ${data}
	Log   ${resp.text}	
	# Request Should Be Successful     ${resp} 
	Should Contain  ${resp.text}  iStudent
